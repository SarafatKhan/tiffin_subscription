import { useEffect, useState } from "react";
import {
  createCustomer,
  deleteCustomer,
  getCustomers,
  updateCustomer,
} from "../services/customerService";


const emptyForm = {
  name: "",
  phone: "",
  email: "",
  address: "",
};


function Customers() {
  const [customers, setCustomers] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");


  const loadCustomers = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getCustomers();

      setCustomers(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Failed to load customers"
      );
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    loadCustomers();
  }, []);


  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };


  const resetForm = () => {
    setForm(emptyForm);
    setEditingId(null);
  };


  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setError("");
      setMessage("");

      const customerData = {
        name: form.name,
        phone: form.phone,
        email: form.email || null,
        address: form.address || null,
      };


      if (editingId) {
        await updateCustomer(
          editingId,
          customerData
        );

        setMessage(
          "Customer updated successfully"
        );
      } else {
        await createCustomer(customerData);

        setMessage(
          "Customer created successfully"
        );
      }

      resetForm();
      await loadCustomers();

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Operation failed"
      );
    }
  };


  const handleEdit = (customer) => {
    setEditingId(customer.id);

    setForm({
      name: customer.name || "",
      phone: customer.phone || "",
      email: customer.email || "",
      address: customer.address || "",
    });

    setMessage("");
    setError("");
  };


  const handleDelete = async (customerId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this customer?"
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setMessage("");

      await deleteCustomer(customerId);

      setMessage(
        "Customer deleted successfully"
      );

      await loadCustomers();

    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Failed to delete customer"
      );
    }
  };


  return (
    <div className="min-h-screen bg-gray-100 p-6">

      <div className="mx-auto max-w-7xl">

        <h1 className="mb-2 text-3xl font-bold">
          Customers
        </h1>

        <p className="mb-6 text-gray-600">
          Add and manage tiffin customers
        </p>


        {message && (
          <div className="mb-4 rounded-lg bg-green-100 p-3 text-green-700">
            {message}
          </div>
        )}


        {error && (
          <div className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
            {typeof error === "string"
              ? error
              : JSON.stringify(error)}
          </div>
        )}


        <div className="grid gap-6 lg:grid-cols-3">

          <div className="rounded-xl bg-white p-6 shadow">

            <h2 className="mb-5 text-xl font-semibold">
              {editingId
                ? "Edit Customer"
                : "Add Customer"}
            </h2>


            <form
              onSubmit={handleSubmit}
              className="space-y-4"
            >

              <div>
                <label className="mb-1 block text-sm font-medium">
                  Name
                </label>

                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  placeholder="Customer name"
                  required
                  minLength={2}
                  className="w-full rounded-lg border p-2.5 outline-none focus:ring-2"
                />
              </div>


              <div>
                <label className="mb-1 block text-sm font-medium">
                  Phone
                </label>

                <input
                  type="tel"
                  name="phone"
                  value={form.phone}
                  onChange={handleChange}
                  placeholder="9876543210"
                  required
                  minLength={10}
                  maxLength={15}
                  className="w-full rounded-lg border p-2.5 outline-none focus:ring-2"
                />
              </div>


              <div>
                <label className="mb-1 block text-sm font-medium">
                  Email
                </label>

                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="customer@email.com"
                  className="w-full rounded-lg border p-2.5 outline-none focus:ring-2"
                />
              </div>


              <div>
                <label className="mb-1 block text-sm font-medium">
                  Address
                </label>

                <textarea
                  name="address"
                  value={form.address}
                  onChange={handleChange}
                  placeholder="Delivery address"
                  rows={3}
                  className="w-full rounded-lg border p-2.5 outline-none focus:ring-2"
                />
              </div>


              <div className="flex gap-2">

                <button
                  type="submit"
                  className="rounded-lg bg-black px-5 py-2.5 font-medium text-white hover:bg-gray-800"
                >
                  {editingId
                    ? "Update Customer"
                    : "Add Customer"}
                </button>


                {editingId && (
                  <button
                    type="button"
                    onClick={resetForm}
                    className="rounded-lg border px-5 py-2.5 font-medium hover:bg-gray-100"
                  >
                    Cancel
                  </button>
                )}

              </div>

            </form>

          </div>


          <div className="overflow-hidden rounded-xl bg-white shadow lg:col-span-2">

            <div className="border-b p-6">

              <h2 className="text-xl font-semibold">
                Customer List
              </h2>

              <p className="text-sm text-gray-500">
                Total customers: {customers.length}
              </p>

            </div>


            {loading ? (

              <div className="p-6 text-center text-gray-500">
                Loading customers...
              </div>

            ) : customers.length === 0 ? (

              <div className="p-6 text-center text-gray-500">
                No customers found
              </div>

            ) : (

              <div className="overflow-x-auto">

                <table className="w-full text-left">

                  <thead className="bg-gray-50">

                    <tr>

                      <th className="px-6 py-3 text-sm font-semibold">
                        Name
                      </th>

                      <th className="px-6 py-3 text-sm font-semibold">
                        Phone
                      </th>

                      <th className="px-6 py-3 text-sm font-semibold">
                        Email
                      </th>

                      <th className="px-6 py-3 text-sm font-semibold">
                        Address
                      </th>

                      <th className="px-6 py-3 text-sm font-semibold">
                        Actions
                      </th>

                    </tr>

                  </thead>


                  <tbody className="divide-y">

                    {customers.map((customer) => (

                      <tr
                        key={customer.id}
                        className="hover:bg-gray-50"
                      >

                        <td className="px-6 py-4 font-medium">
                          {customer.name}
                        </td>

                        <td className="px-6 py-4">
                          {customer.phone}
                        </td>

                        <td className="px-6 py-4">
                          {customer.email || "-"}
                        </td>

                        <td className="max-w-xs px-6 py-4">
                          {customer.address || "-"}
                        </td>

                        <td className="px-6 py-4">

                          <div className="flex gap-2">

                            <button
                              onClick={() =>
                                handleEdit(customer)
                              }
                              className="rounded-md border px-3 py-1.5 text-sm hover:bg-gray-100"
                            >
                              Edit
                            </button>

                            <button
                              onClick={() =>
                                handleDelete(customer.id)
                              }
                              className="rounded-md bg-red-600 px-3 py-1.5 text-sm text-white hover:bg-red-700"
                            >
                              Delete
                            </button>

                          </div>

                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            )}

          </div>

        </div>

      </div>

    </div>
  );
}


export default Customers;