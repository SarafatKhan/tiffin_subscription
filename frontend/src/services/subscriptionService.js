import api from "./api";


export const getSubscriptions = async () => {
  const response = await api.get(
    "/subscriptions/"
  );

  return response.data;
};


export const getCustomerSubscriptions = async (
  customerId
) => {
  const response = await api.get(
    `/subscriptions/customer/${customerId}`
  );

  return response.data;
};


export const createSubscription = async (
  subscription
) => {
  const response = await api.post(
    "/subscriptions/",
    subscription
  );

  return response.data;
};


export const pauseSubscription = async (
  subscriptionId,
  pauseData
) => {
  const response = await api.post(
    `/subscriptions/${subscriptionId}/pause`,
    pauseData
  );

  return response.data;
};


export const resumeSubscription = async (
  subscriptionId
) => {
  const response = await api.post(
    `/subscriptions/${subscriptionId}/resume`
  );

  return response.data;
};
