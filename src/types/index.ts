export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  address: string;
  membershipType: "Regular" | "VIP" | "Premium";
  joinDate: string;
  totalSpent: number;
  loyaltyPoints: number;
}

export interface Employee {
  id: string;
  name: string;
  email: string;
  phone: string;
  position: string;
  department: "Cafe" | "Billiard" | "Management" | "Maintenance";
  salary: number;
  hireDate: string;
  status: "Active" | "Inactive" | "On Leave";
  shift: "Morning" | "Afternoon" | "Night";
}

export interface MenuCafe {
  id: string;
  name: string;
  category: "Food" | "Beverage" | "Snack" | "Dessert";
  price: number;
  description: string;
  ingredients: string[];
  availability: boolean;
  preparationTime: number; // in minutes
  imageUrl?: string;
}

export interface BilliardTable {
  id: string;
  tableNumber: number;
  type: "8-Ball" | "9-Ball" | "Snooker" | "Carom";
  status: "Available" | "Occupied" | "Reserved" | "Maintenance";
  hourlyRate: number;
  location: string;
  condition: "Excellent" | "Good" | "Fair" | "Needs Repair";
}

export interface Order {
  id: string;
  customerId: string;
  customerName: string;
  items: OrderItem[];
  totalAmount: number;
  orderDate: string;
  status: "Pending" | "Preparing" | "Ready" | "Served" | "Cancelled";
  tableNumber?: number;
  notes?: string;
  discount: number;
  tax: number;
}

export interface OrderItem {
  menuId: string;
  menuName: string;
  quantity: number;
  unitPrice: number;
  subtotal: number;
  specialInstructions?: string;
}

export interface Payment {
  id: string;
  orderId: string;
  amount: number;
  paymentMethod:
    | "Cash"
    | "Credit Card"
    | "Debit Card"
    | "Digital Wallet"
    | "Bank Transfer";
  paymentDate: string;
  status: "Pending" | "Completed" | "Failed" | "Refunded";
  transactionId?: string;
  cashierName: string;
  change?: number;
}

export interface Reservation {
  id: string;
  customerId: string;
  customerName: string;
  customerPhone: string;
  tableId: string;
  tableNumber: number;
  reservationDate: string;
  startTime: string;
  endTime: string;
  duration: number; // in hours
  status: "Confirmed" | "Pending" | "Cancelled" | "Completed" | "No Show";
  partySize: number;
  specialRequests?: string;
  deposit: number;
}

export interface RentalTransaction {
  id: string;
  customerId: string;
  customerName: string;
  tableId: string;
  tableNumber: number;
  startTime: string;
  endTime?: string;
  duration: number; // in hours
  hourlyRate: number;
  totalAmount: number;
  status: "Active" | "Completed" | "Paused" | "Cancelled";
  additionalServices: string[];
  employeeId: string;
  employeeName: string;
  paymentStatus: "Unpaid" | "Paid" | "Partial";
}

export interface DashboardStats {
  totalCustomers: number;
  totalEmployees: number;
  totalMenuItems: number;
  totalTables: number;
  todayOrders: number;
  todayRevenue: number;
  activeRentals: number;
  pendingReservations: number;
  availableTables: number;
}

export type EntityType =
  | "customers"
  | "employees"
  | "menu"
  | "tables"
  | "orders"
  | "payments"
  | "reservations"
  | "rentals";
