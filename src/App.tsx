import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "@/components/Layout";
import Dashboard from "@/pages/Dashboard";
import CustomerManagement from "@/pages/CustomerManagement";
import EmployeeManagement from "@/pages/EmployeeManagement";
import MenuManagement from "@/pages/MenuManagement";
import BilliardTableManagement from "@/pages/BilliardTableManagement";
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
          <Route
            path="/orders"
            element={
              <div className="text-white text-center py-20">
                Orders Management - Coming Soon
              </div>
            }
          />
          <Route
            path="/payments"
            element={
              <div className="text-white text-center py-20">
                Payment Management - Coming Soon
              </div>
            }
          />
          <Route
            path="/reservations"
            element={
              <div className="text-white text-center py-20">
                Reservation Management - Coming Soon
              </div>
            }
          />
          <Route
            path="/rentals"
            element={
              <div className="text-white text-center py-20">
                Rental Management - Coming Soon
              </div>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
