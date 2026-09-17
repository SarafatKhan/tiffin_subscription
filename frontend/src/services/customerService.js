import api from "./api";


export const getCustomers = async () => {
  const response = await api.get("/customers/");
  return response.data;
};


export const getCustomerByPhone = async (phone) => {
  const response = await api.get(
    `/customers/phone/${phone}`
  );

  return response.data;
};


export const createCustomer = async (customer) => {
  const response = await api.post(
    "/customers/",
    customer
  );

  return response.data;
};


export const updateCustomer = async (
  customerId,
  customer
) => {
  const response = await api.put(
    `/customers/${customerId}`,
    customer
  );

  return response.data;
};


export const deleteCustomer = async (customerId) => {
  const response = await api.delete(
    `/customers/${customerId}`
  );

  return response.data;
};
