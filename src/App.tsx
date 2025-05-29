import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "@/components/Layout";
import Dashboard from "@/pages/Dashboard";
import CustomerManagement from "@/pages/CustomerManagement";
import EmployeeManagement from "@/pages/EmployeeManagement";
import MenuManagement from "@/pages/MenuManagement";
import BilliardTableManagement from "@/pages/BilliardTableManagement";
import OrderManagement from "@/pages/OrderManagement";
import PaymentManagement from "@/pages/PaymentManagement";
import ReservationManagement from "@/pages/ReservationManagement";
import RentalTransactionManagement from "@/pages/RentalTransactionManagement";
import NotFound from "@/pages/NotFound";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/customers" element={<CustomerManagement />} />
          <Route path="/employees" element={<EmployeeManagement />} />
          <Route path="/menu" element={<MenuManagement />} />
          <Route path="/tables" element={<BilliardTableManagement />} />
          <Route path="/orders" element={<OrderManagement />} />
          <Route path="/payments" element={<PaymentManagement />} />
          <Route path="/reservations" element={<ReservationManagement />} />
          <Route path="/rentals" element={<RentalTransactionManagement />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
