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
  Activity,
  Target,
  Zap,
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

      {/* Optimized Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Customers - Ocean Blue Theme */}
        <Card className="relative overflow-hidden bg-gradient-to-br from-cyan-500/10 via-blue-600/10 to-indigo-700/10 border-cyan-400/20 hover:border-cyan-400/40 transition-all duration-300 group">
          <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-blue-600/5 to-indigo-700/5"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
            <CardTitle className="text-sm font-medium text-white">
              Total Customers
            </CardTitle>
            <div className="p-2 bg-cyan-500/20 rounded-lg group-hover:bg-cyan-500/30 transition-colors">
              <Users className="h-4 w-4 text-cyan-400" />
            </div>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-3xl font-bold text-white">
              {stats.totalCustomers}
            </div>
            <p className="text-xs text-white/80 flex items-center mt-1">
              <TrendingUp className="w-3 h-3 mr-1" />
              Registered members
            </p>
          </CardContent>
        </Card>

        {/* Today's Revenue - Emerald Green Theme */}
        <Card className="relative overflow-hidden bg-gradient-to-br from-emerald-500/10 via-green-600/10 to-teal-700/10 border-emerald-400/20 hover:border-emerald-400/40 transition-all duration-300 group">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 via-green-600/5 to-teal-700/5"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
            <CardTitle className="text-sm font-medium text-white">
              Today's Revenue
            </CardTitle>
            <div className="p-2 bg-emerald-500/20 rounded-lg group-hover:bg-emerald-500/30 transition-colors">
              <DollarSign className="h-4 w-4 text-emerald-400" />
            </div>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-3xl font-bold text-white">
              ${stats.todayRevenue.toFixed(2)}
            </div>
            <p className="text-xs text-white/80 flex items-center mt-1">
              <Activity className="w-3 h-3 mr-1" />
              From {stats.todayOrders} orders
            </p>
          </CardContent>
        </Card>

        {/* Available Tables - Violet Purple Theme */}
        <Card className="relative overflow-hidden bg-gradient-to-br from-violet-500/10 via-purple-600/10 to-fuchsia-700/10 border-violet-400/20 hover:border-violet-400/40 transition-all duration-300 group">
          <div className="absolute inset-0 bg-gradient-to-br from-violet-500/5 via-purple-600/5 to-fuchsia-700/5"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
            <CardTitle className="text-sm font-medium text-white">
              Available Tables
            </CardTitle>
            <div className="p-2 bg-violet-500/20 rounded-lg group-hover:bg-violet-500/30 transition-colors">
              <CircleDot className="h-4 w-4 text-violet-400" />
            </div>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-3xl font-bold text-white">
              {stats.availableTables}/{stats.totalTables}
            </div>
            <p className="text-xs text-white/80 flex items-center mt-1">
              <Target className="w-3 h-3 mr-1" />
              Ready for use
            </p>
          </CardContent>
        </Card>

        {/* Active Rentals - Amber Orange Theme */}
        <Card className="relative overflow-hidden bg-gradient-to-br from-amber-500/10 via-orange-600/10 to-red-700/10 border-amber-400/20 hover:border-amber-400/40 transition-all duration-300 group">
          <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 via-orange-600/5 to-red-700/5"></div>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
            <CardTitle className="text-sm font-medium text-white">
              Active Rentals
            </CardTitle>
            <div className="p-2 bg-amber-500/20 rounded-lg group-hover:bg-amber-500/30 transition-colors">
              <Zap className="h-4 w-4 text-amber-400" />
            </div>
          </CardHeader>
          <CardContent className="relative z-10">
            <div className="text-3xl font-bold text-white">
              {stats.activeRentals}
            </div>
            <p className="text-xs text-white/80 flex items-center mt-1">
              <Clock className="w-3 h-3 mr-1" />
              Tables in use
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Secondary Management Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-slate-800/40 border-slate-700/50 hover:bg-slate-800/60 transition-colors backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">
              Staff Members
            </CardTitle>
            <UserCheck className="h-4 w-4 text-slate-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {stats.totalEmployees}
            </div>
            <p className="text-xs text-slate-400">Active workforce</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/40 border-slate-700/50 hover:bg-slate-800/60 transition-colors backdrop-blur-sm">
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

        <Card className="bg-slate-800/40 border-slate-700/50 hover:bg-slate-800/60 transition-colors backdrop-blur-sm">
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
            <p className="text-xs text-slate-400">Completed today</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-800/40 border-slate-700/50 hover:bg-slate-800/60 transition-colors backdrop-blur-sm">
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
            <button className="p-4 bg-cyan-600/20 border border-cyan-500/30 rounded-lg hover:bg-cyan-600/30 transition-colors">
              <Users className="h-6 w-6 text-cyan-400 mx-auto mb-2" />
              <p className="text-sm text-white">Add Customer</p>
            </button>
            <button className="p-4 bg-emerald-600/20 border border-emerald-500/30 rounded-lg hover:bg-emerald-600/30 transition-colors">
              <ShoppingCart className="h-6 w-6 text-emerald-400 mx-auto mb-2" />
              <p className="text-sm text-white">New Order</p>
            </button>
            <button className="p-4 bg-violet-600/20 border border-violet-500/30 rounded-lg hover:bg-violet-600/30 transition-colors">
              <Calendar className="h-6 w-6 text-violet-400 mx-auto mb-2" />
              <p className="text-sm text-white">Make Reservation</p>
            </button>
            <button className="p-4 bg-amber-600/20 border border-amber-500/30 rounded-lg hover:bg-amber-600/30 transition-colors">
              <CircleDot className="h-6 w-6 text-amber-400 mx-auto mb-2" />
              <p className="text-sm text-white">Start Rental</p>
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
