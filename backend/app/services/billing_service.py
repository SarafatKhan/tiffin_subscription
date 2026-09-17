from calendar import monthrange
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pause import Pause
from app.models.subscription import Subscription


SERVICE_DAYS = {
	0,  # Monday
	1,  # Tuesday
	2,  # Wednesday
	3,  # Thursday
	4,  # Friday
}


def get_month_boundaries(
	year: int,
	month: int
) -> tuple[date, date]:

	first_day = date(year, month, 1)

	last_day = date(
		year,
		month,
		monthrange(year, month)[1]
	)

	return first_day, last_day


def get_service_days(
	start_date: date,
	end_date: date
) -> list[date]:

	service_days = []

	current_date = start_date

	while current_date <= end_date:

		if current_date.weekday() in SERVICE_DAYS:
			service_days.append(current_date)

		current_date += timedelta(days=1)

	return service_days


def get_eligible_service_days(
	subscription: Subscription,
	billing_start: date,
	billing_end: date
) -> list[date]:

	effective_start = max(
		subscription.start_date,
		billing_start
	)

	effective_end = billing_end

	if subscription.end_date:
		effective_end = min(
			subscription.end_date,
			billing_end
		)

	if effective_start > effective_end:
		return []

	return get_service_days(
		effective_start,
		effective_end
	)


def get_paused_service_days(
	db: Session,
	subscription: Subscription,
	service_days: list[date]
) -> list[date]:

	pauses = db.scalars(
		select(Pause)
		.where(
			Pause.subscription_id == subscription.id
		)
	).all()

	paused_days = []

	for service_day in service_days:

		for pause in pauses:

			if (
				pause.start_date
				<= service_day
				<= pause.end_date
			):
				paused_days.append(service_day)
				break

	return paused_days


def calculate_daily_rate(
	monthly_price: Decimal,
	eligible_days: int
) -> Decimal:

	if eligible_days <= 0:
		return Decimal("0.00")

	daily_rate = (
		monthly_price
		/ Decimal(eligible_days)
	)

	return daily_rate.quantize(
		Decimal("0.01"),
		rounding=ROUND_HALF_UP
	)


def calculate_bill_amount(
    monthly_price: Decimal,
    billable_days: int,
    eligible_days: int
) -> Decimal:

    if eligible_days <= 0:
        return Decimal("0.00")

    amount = (
        monthly_price
        * Decimal(billable_days)
        / Decimal(eligible_days)
    )

    return amount.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


def calculate_subscription_bill(
	db: Session,
	subscription: Subscription,
	year: int,
	month: int
) -> dict:

	billing_start, billing_end = get_month_boundaries(
		year,
		month
	)

	service_days = get_eligible_service_days(
		subscription,
		billing_start,
		billing_end
	)

	paused_days = get_paused_service_days(
		db,
		subscription,
		service_days
	)

	eligible_days_count = len(service_days)

	paused_days_count = len(paused_days)

	billable_days_count = (
		eligible_days_count
		- paused_days_count
	)

	monthly_price = Decimal(
		str(subscription.monthly_price)
	)

	daily_rate = calculate_daily_rate(
		monthly_price,
		eligible_days_count
	)

	amount = calculate_bill_amount(
		monthly_price,
		billable_days_count,
		eligible_days_count
	)

	return {
		"subscription_id": subscription.id,
		"billing_year": year,
		"billing_month": month,
		"billing_start": billing_start,
		"billing_end": billing_end,
		"eligible_days": eligible_days_count,
		"paused_days": paused_days_count,
		"billable_days": billable_days_count,
		"monthly_price": monthly_price,
		"daily_rate": daily_rate,
		"amount": amount,
	}


if __name__ == "__main__":

	monthly_price = Decimal("3000.00")
	eligible_days = 22
	billable_days = 17

	amount = calculate_bill_amount(
		monthly_price,
		billable_days,
		eligible_days
	)

	print("Monthly Price:", monthly_price)
	print("Eligible Days:", eligible_days)
	print("Billable Days:", billable_days)
	print("Final Bill:", amount)
