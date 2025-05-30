import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Users,
  UserCheck,
  Coffee,
  ShoppingCart,
  DollarSign,
  Calendar,
  CircleDot,
  TrendingUp,
  Clock,
  AlertCircle,
} from "lucide-react";
import {
  mockCustomers,
  mockEmployees,
  mockMenuCafe,
  mockBilliardTables,
  mockOrders,
  mockReservations,
  mockRentalTransactions,
} from "@/lib/data";
import { DashboardStats } from "@/types";

export default function Dashboard() {
  // Calculate dashboard statistics
  const stats: DashboardStats = {
    totalCustomers: mockCustomers.length,
    totalEmployees: mockEmployees.length,
    totalMenuItems: mockMenuCafe.length,
    totalTables: mockBilliardTables.length,
    todayOrders: mockOrders.filter(
      (order) =>
        new Date(order.orderDate).toDateString() === new Date().toDateString(),
    ).length,
    todayRevenue: mockOrders
      .filter(
        (order) =>
          new Date(order.orderDate).toDateString() ===
          new Date().toDateString(),
      )
      .reduce((sum, order) => sum + order.totalAmount, 0),
    activeRentals: mockRentalTransactions.filter(
      (rental) => rental.status === "Active",
    ).length,
    pendingReservations: mockReservations.filter(
      (res) => res.status === "Pending",
    ).length,
    availableTables: mockBilliardTables.filter(
      (table) => table.status === "Available",
    ).length,
  };

  const recentOrders = mockOrders.slice(0, 5);
  const upcomingReservations = mockReservations.slice(0, 3);
  const activeRentals = mockRentalTransactions.filter(
    (rental) => rental.status === "Active",
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-2">Amorty & Cafe</h1>
        <p className="text-xl text-slate-400">Management Dashboard</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-blue-200">
              Total Customers
            </CardTitle>
            <Users className="h-4 w-4 text-blue-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.totalCustomers}
            </div>
            <p className="text-xs text-blue-300">Registered members</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-green-200">
              Today's Revenue
            </CardTitle>
            <DollarSign className="h-4 w-4 text-green-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              ${stats.todayRevenue.toFixed(2)}
            </div>
            <p className="text-xs text-green-300">
              From {stats.todayOrders} orders
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-purple-200">
              Available Tables
            </CardTitle>
            <CircleDot className="h-4 w-4 text-purple-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.availableTables}/{stats.totalTables}
            </div>
            <p className="text-xs text-purple-300">Ready for use</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-orange-600/20 to-orange-800/20 border-orange-500/30">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-orange-200">
              Active Rentals
            </CardTitle>
            <Clock className="h-4 w-4 text-orange-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.activeRentals}
            </div>
            <p className="text-xs text-orange-300">Tables in use</p>
          </CardContent>
        </Card>
      </div>

      {/* Management Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">
              Employees
            </CardTitle>
            <UserCheck className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.totalEmployees}
            </div>
            <p className="text-xs text-slate-400">Staff members</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">
              Menu Items
            </CardTitle>
            <Coffee className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.totalMenuItems}
            </div>
            <p className="text-xs text-slate-400">Available items</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">
              Today's Orders
            </CardTitle>
            <ShoppingCart className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.todayOrders}
            </div>
            <p className="text-xs text-slate-400">Completed orders</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/50 border-slate-700 hover:bg-slate-800/70 transition-colors">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">
              Pending Reservations
            </CardTitle>
            <Calendar className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.pendingReservations}
            </div>
            <p className="text-xs text-slate-400">Awaiting confirmation</p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Orders */}
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <ShoppingCart className="h-5 w-5 mr-2" />
              Recent Orders
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentOrders.map((order) => (
              <div
                key={order.id}
                className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg"
              >
                <div>
                  <p className="font-medium text-white">{order.customerName}</p>
                  <p className="text-sm text-slate-400">
                    {order.items.length} items • ${order.totalAmount.toFixed(2)}
                  </p>
                </div>
                <Badge
                  variant={
                    order.status === "Served"
                      ? "default"
                      : order.status === "Preparing"
                        ? "secondary"
                        : "outline"
                  }
                >
                  {order.status}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Upcoming Reservations */}
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Calendar className="h-5 w-5 mr-2" />
              Upcoming Reservations
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {upcomingReservations.map((reservation) => (
              <div
                key={reservation.id}
                className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg"
              >
                <div>
                  <p className="font-medium text-white">
                    {reservation.customerName}
                  </p>
                  <p className="text-sm text-slate-400">
                    Table {reservation.tableNumber} • {reservation.startTime} -{" "}
                    {reservation.endTime}
                  </p>
                </div>
                <Badge
                  variant={
                    reservation.status === "Confirmed"
                      ? "default"
                      : reservation.status === "Pending"
                        ? "secondary"
                        : "outline"
                  }
                >
                  {reservation.status}
                </Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      {/* Active Rentals */}
      {activeRentals.length > 0 && (
        <Card className="bg-slate-800/50 border-slate-700">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <CircleDot className="h-5 w-5 mr-2" />
              Active Table Rentals
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {activeRentals.map((rental) => (
                <div key={rental.id} className="p-4 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-white">
                      Table {rental.tableNumber}
                    </h4>
                    <Badge className="bg-green-600">Active</Badge>
                  </div>
                  <p className="text-sm text-slate-400">
                    {rental.customerName}
                  </p>
                  <p className="text-sm text-slate-400">
                    Duration: {rental.duration}h • ${rental.totalAmount}
                  </p>
                  <p className="text-xs text-slate-500 mt-1">
                    Started: {new Date(rental.startTime).toLocaleTimeString()}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quick Actions */}
      <Card className="bg-gradient-to-r from-slate-800/50 to-slate-700/50 border-slate-600">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <TrendingUp className="h-5 w-5 mr-2" />
            Quick Actions
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="p-4 bg-blue-600/20 border border-blue-500/30 rounded-lg hover:bg-blue-600/30 transition-colors">
              <Users className="h-6 w-6 text-blue-400 mx-auto mb-2" />
              <p className="text-sm text-blue-200">Add Customer</p>
            </button>
            <button className="p-4 bg-green-600/20 border border-green-500/30 rounded-lg hover:bg-green-600/30 transition-colors">
              <ShoppingCart className="h-6 w-6 text-green-400 mx-auto mb-2" />
              <p className="text-sm text-green-200">New Order</p>
            </button>
            <button className="p-4 bg-purple-600/20 border border-purple-500/30 rounded-lg hover:bg-purple-600/30 transition-colors">
              <Calendar className="h-6 w-6 text-purple-400 mx-auto mb-2" />
              <p className="text-sm text-purple-200">Make Reservation</p>
            </button>
            <button className="p-4 bg-orange-600/20 border border-orange-500/30 rounded-lg hover:bg-orange-600/30 transition-colors">
              <CircleDot className="h-6 w-6 text-orange-400 mx-auto mb-2" />
              <p className="text-sm text-orange-200">Start Rental</p>
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
