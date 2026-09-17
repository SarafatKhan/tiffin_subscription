import api from "./api";


export const getBills = async () => {
  const response = await api.get("/billing/");
  return response.data;
};


export const getCustomerBills = async (
  customerId
) => {
  const response = await api.get(
    `/billing/customer/${customerId}`
  );

  return response.data;
};


export const generateBill = async (billData) => {
  const response = await api.post(
    "/billing/generate",
    billData
  );

  return response.data;
};
