import { useState } from "react";
import { DataTable, Column } from "@/components/DataTable";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Payment, Order, Employee } from "@/types";
import { mockPayments, mockOrders, mockEmployees } from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { CreditCard, DollarSign } from "lucide-react";

const statusColors = {
  Pending: "bg-yellow-600",
  Completed: "bg-green-600",
  Failed: "bg-red-600",
  Refunded: "bg-blue-600",
};

const methodColors = {
  Cash: "bg-green-600",
  "Credit Card": "bg-blue-600",
  "Debit Card": "bg-purple-600",
  "Digital Wallet": "bg-orange-600",
  "Bank Transfer": "bg-slate-600",
};

export default function PaymentManagement() {
  const [payments, setPayments] = useLocalStorage<Payment[]>(
    "payments",
    mockPayments,
  );
  const [orders] = useLocalStorage<Order[]>("orders", mockOrders);
  const [employees] = useLocalStorage<Employee[]>("employees", mockEmployees);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingPayment, setEditingPayment] = useState<Payment | null>(null);
  const [formData, setFormData] = useState<Partial<Payment>>({
    orderId: "",
    amount: 0,
    paymentMethod: "Cash",
    paymentDate: new Date().toISOString(),
    status: "Pending",
    transactionId: "",
    cashierName: "",
    change: undefined,
  });

  const columns: Column<Payment>[] = [
    {
      key: "id",
      label: "Payment ID",
      sortable: true,
      render: (value: string) => `#${value.slice(-6).toUpperCase()}`,
    },
    {
      key: "orderId",
      label: "Order ID",
      sortable: true,
      render: (value: string) => {
        const order = orders.find((o) => o.id === value);
        return order ? `#${value.slice(-6).toUpperCase()}` : "N/A";
      },
    },
    {
      key: "amount",
      label: "Amount",
      sortable: true,
      render: (value: number) => (
        <div className="flex items-center">
          <DollarSign className="w-3 h-3 mr-1 text-green-400" />$
          {value.toFixed(2)}
        </div>
      ),
    },
    {
      key: "paymentMethod",
      label: "Method",
      sortable: true,
      render: (value: string) => {
        const colorClass = methodColors[value as keyof typeof methodColors];
        return (
          <Badge className={`${colorClass} text-white`}>
            <CreditCard className="w-3 h-3 mr-1" />
            {value}
          </Badge>
        );
      },
    },
    {
      key: "status",
      label: "Status",
      sortable: true,
      render: (value: string) => {
        const colorClass = statusColors[value as keyof typeof statusColors];
        return <Badge className={`${colorClass} text-white`}>{value}</Badge>;
      },
    },
    {
      key: "cashierName",
      label: "Cashier",
      sortable: true,
    },
    {
      key: "paymentDate",
      label: "Date",
      sortable: true,
      render: (value: string) => new Date(value).toLocaleString(),
    },
    {
      key: "transactionId",
      label: "Transaction ID",
      render: (value: string) => value || "N/A",
    },
    {
      key: "actions",
      label: "Actions",
    },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const selectedOrder = orders.find((o) => o.id === formData.orderId);
    if (!selectedOrder) return;

    if (editingPayment) {
      setPayments(
        payments.map((payment) =>
          payment.id === editingPayment.id
            ? { ...payment, ...formData }
            : payment,
        ),
      );
    } else {
      const newPayment: Payment = {
        id: Date.now().toString(),
        orderId: formData.orderId || "",
        amount: formData.amount || 0,
        paymentMethod: formData.paymentMethod || "Cash",
        paymentDate: formData.paymentDate || new Date().toISOString(),
        status: formData.status || "Pending",
        transactionId: formData.transactionId,
        cashierName: formData.cashierName || "",
        change: formData.change,
      };
      setPayments([...payments, newPayment]);
    }

    handleCloseDialog();
  };

  const handleEdit = (payment: Payment) => {
    setEditingPayment(payment);
    setFormData(payment);
    setIsDialogOpen(true);
  };

  const handleDelete = (payment: Payment) => {
    if (
      confirm(
        `Are you sure you want to delete payment #${payment.id.slice(-6).toUpperCase()}?`,
      )
    ) {
      setPayments(payments.filter((p) => p.id !== payment.id));
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingPayment(null);
    setFormData({
      orderId: "",
      amount: 0,
      paymentMethod: "Cash",
      paymentDate: new Date().toISOString(),
      status: "Pending",
      transactionId: "",
      cashierName: "",
      change: undefined,
    });
  };

  const selectedOrder = orders.find((o) => o.id === formData.orderId);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Payment Management</h1>
          <p className="text-slate-400">
            Process and track all payment transactions
          </p>
        </div>
      </div>

      <DataTable
        title="Payments"
        data={payments}
        columns={columns}
        searchPlaceholder="Search payments..."
        searchKey="cashierName"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="Record Payment"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingPayment ? "Edit Payment" : "Record New Payment"}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="orderId">Order</Label>
                <Select
                  value={formData.orderId}
                  onValueChange={(value) => {
                    const order = orders.find((o) => o.id === value);
                    setFormData({
                      ...formData,
                      orderId: value,
                      amount: order?.totalAmount || 0,
                    });
                  }}
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Select order" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    {orders
                      .filter((order) => order.status !== "Cancelled")
                      .map((order) => (
                        <SelectItem key={order.id} value={order.id}>
                          #{order.id.slice(-6).toUpperCase()} -{" "}
                          {order.customerName} (${order.totalAmount.toFixed(2)})
                        </SelectItem>
                      ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="amount">Amount ($)</Label>
                <Input
                  id="amount"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      amount: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="paymentMethod">Payment Method</Label>
                <Select
                  value={formData.paymentMethod}
                  onValueChange={(value) =>
                    setFormData({ ...formData, paymentMethod: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Cash">Cash</SelectItem>
                    <SelectItem value="Credit Card">Credit Card</SelectItem>
                    <SelectItem value="Debit Card">Debit Card</SelectItem>
                    <SelectItem value="Digital Wallet">
                      Digital Wallet
                    </SelectItem>
                    <SelectItem value="Bank Transfer">Bank Transfer</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="status">Status</Label>
                <Select
                  value={formData.status}
                  onValueChange={(value) =>
                    setFormData({ ...formData, status: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Pending">Pending</SelectItem>
                    <SelectItem value="Completed">Completed</SelectItem>
                    <SelectItem value="Failed">Failed</SelectItem>
                    <SelectItem value="Refunded">Refunded</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="cashierName">Cashier</Label>
                <Select
                  value={formData.cashierName}
                  onValueChange={(value) =>
                    setFormData({ ...formData, cashierName: value })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Select cashier" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    {employees
                      .filter((emp) => emp.status === "Active")
                      .map((employee) => (
                        <SelectItem key={employee.id} value={employee.name}>
                          {employee.name} - {employee.position}
                        </SelectItem>
                      ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="paymentDate">Payment Date</Label>
                <Input
                  id="paymentDate"
                  type="datetime-local"
                  value={formData.paymentDate?.slice(0, 16)}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      paymentDate: new Date(e.target.value).toISOString(),
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>
            </div>

            {formData.paymentMethod !== "Cash" && (
              <div className="space-y-2">
                <Label htmlFor="transactionId">Transaction ID</Label>
                <Input
                  id="transactionId"
                  value={formData.transactionId}
                  onChange={(e) =>
                    setFormData({ ...formData, transactionId: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  placeholder="Enter transaction reference"
                />
              </div>
            )}

            {formData.paymentMethod === "Cash" && (
              <div className="space-y-2">
                <Label htmlFor="change">Change Given ($)</Label>
                <Input
                  id="change"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.change || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      change: parseFloat(e.target.value) || undefined,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  placeholder="Amount of change given"
                />
              </div>
            )}

            {selectedOrder && (
              <div className="p-4 bg-slate-700/50 rounded-lg border border-slate-600">
                <h4 className="font-semibold text-white mb-2">Order Details</h4>
                <div className="text-sm text-slate-300 space-y-1">
                  <p>Customer: {selectedOrder.customerName}</p>
                  <p>Items: {selectedOrder.items.length} item(s)</p>
                  <p>Order Total: ${selectedOrder.totalAmount.toFixed(2)}</p>
                  <p>Status: {selectedOrder.status}</p>
                </div>
              </div>
            )}

            <div className="flex justify-end space-x-2 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={handleCloseDialog}
                className="border-slate-600 text-slate-300 hover:bg-slate-700"
              >
                Cancel
              </Button>
              <Button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white"
                disabled={!formData.orderId || !formData.cashierName}
              >
                {editingPayment ? "Update" : "Record"} Payment
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
