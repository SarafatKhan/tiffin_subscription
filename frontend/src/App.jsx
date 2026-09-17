import {
  Link,
  Route,
  Routes,
} from "react-router-dom";

import Customers from "./pages/Customers";


function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100 p-8">

      <div className="mx-auto max-w-6xl">

        <h1 className="text-3xl font-bold">
          Tiffin Management System
        </h1>

        <p className="mt-2 text-gray-600">
          Subscription and billing management
        </p>


        <div className="mt-8 grid gap-4 md:grid-cols-3">

          <Link
            to="/customers"
            className="rounded-xl bg-white p-6 shadow hover:shadow-md"
          >
            <h2 className="text-xl font-semibold">
              Customers
            </h2>

            <p className="mt-2 text-gray-500">
              Manage customers
            </p>
          </Link>


          <Link
            to="/subscriptions"
            className="rounded-xl bg-white p-6 shadow hover:shadow-md"
          >
            <h2 className="text-xl font-semibold">
              Subscriptions
            </h2>

            <p className="mt-2 text-gray-500">
              Manage subscriptions
            </p>
          </Link>


          <Link
            to="/billing"
            className="rounded-xl bg-white p-6 shadow hover:shadow-md"
          >
            <h2 className="text-xl font-semibold">
              Billing
            </h2>

            <p className="mt-2 text-gray-500">
              Manage bills and payments
            </p>
          </Link>

        </div>

      </div>

    </div>
  );
}


function Subscriptions() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-2xl font-bold">
        Subscriptions
      </h1>
    </div>
  );
}


function Billing() {
  return (
    <div className="min-h-screen p-8">
      <h1 className="text-2xl font-bold">
        Billing
      </h1>
    </div>
  );
}


function App() {
  return (
    <Routes>

      <Route
        path="/"
        element={<Dashboard />}
      />

      <Route
        path="/customers"
        element={<Customers />}
      />

      <Route
        path="/subscriptions"
        element={<Subscriptions />}
      />

      <Route
        path="/billing"
        element={<Billing />}
      />

    </Routes>
  );
}


export default App;