import api from "./api";


export const getPayments = async () => {
  const response = await api.get("/payments/");
  return response.data;
};


export const getBillPayments = async (billId) => {
  const response = await api.get(
    `/payments/bill/${billId}`
  );

  return response.data;
};


export const createPayment = async (payment) => {
  const response = await api.post(
    "/payments/",
    payment
  );

  return response.data;
};
