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
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Order, OrderItem, Customer, MenuCafe } from "@/types";
import { mockOrders, mockCustomers, mockMenuCafe } from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { ShoppingCart, Plus, Minus, X } from "lucide-react";

const statusColors = {
  Pending: "bg-yellow-600",
  Preparing: "bg-blue-600",
  Ready: "bg-green-600",
  Served: "bg-slate-600",
  Cancelled: "bg-red-600",
};

export default function OrderManagement() {
  const [orders, setOrders] = useLocalStorage<Order[]>("orders", mockOrders);
  const [customers] = useLocalStorage<Customer[]>("customers", mockCustomers);
  const [menuItems] = useLocalStorage<MenuCafe[]>("menuItems", mockMenuCafe);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingOrder, setEditingOrder] = useState<Order | null>(null);
  const [formData, setFormData] = useState<Partial<Order>>({
    customerId: "",
    customerName: "",
    items: [],
    totalAmount: 0,
    orderDate: new Date().toISOString(),
    status: "Pending",
    tableNumber: undefined,
    notes: "",
    discount: 0,
    tax: 0,
  });
  const [orderItems, setOrderItems] = useState<OrderItem[]>([]);

  const columns: Column<Order>[] = [
    {
      key: "id",
      label: "Order ID",
      sortable: true,
      render: (value: string) => `#${value.slice(-6).toUpperCase()}`,
    },
    {
      key: "customerName",
      label: "Customer",
      sortable: true,
    },
    {
      key: "items",
      label: "Items",
      render: (value: OrderItem[]) => `${value.length} item(s)`,
    },
    {
      key: "totalAmount",
      label: "Total",
      sortable: true,
      render: (value: number) => `$${value.toFixed(2)}`,
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
      key: "orderDate",
      label: "Order Date",
      sortable: true,
      render: (value: string) => new Date(value).toLocaleString(),
    },
    {
      key: "tableNumber",
      label: "Table",
      render: (value: number | undefined) => (value ? `#${value}` : "Takeout"),
    },
    {
      key: "actions",
      label: "Actions",
    },
  ];

  const calculateTotal = (items: OrderItem[], discount: number = 0) => {
    const subtotal = items.reduce((sum, item) => sum + item.subtotal, 0);
    const discountAmount = subtotal * (discount / 100);
    const taxAmount = (subtotal - discountAmount) * 0.1; // 10% tax
    return {
      subtotal,
      discountAmount,
      taxAmount,
      total: subtotal - discountAmount + taxAmount,
    };
  };

  const addOrderItem = (menuItem: MenuCafe) => {
    const existingItem = orderItems.find((item) => item.menuId === menuItem.id);

    if (existingItem) {
      setOrderItems(
        orderItems.map((item) =>
          item.menuId === menuItem.id
            ? {
                ...item,
                quantity: item.quantity + 1,
                subtotal: (item.quantity + 1) * item.unitPrice,
              }
            : item,
        ),
      );
    } else {
      const newItem: OrderItem = {
        menuId: menuItem.id,
        menuName: menuItem.name,
        quantity: 1,
        unitPrice: menuItem.price,
        subtotal: menuItem.price,
      };
      setOrderItems([...orderItems, newItem]);
    }
  };

  const updateItemQuantity = (menuId: string, quantity: number) => {
    if (quantity <= 0) {
      setOrderItems(orderItems.filter((item) => item.menuId !== menuId));
    } else {
      setOrderItems(
        orderItems.map((item) =>
          item.menuId === menuId
            ? { ...item, quantity, subtotal: quantity * item.unitPrice }
            : item,
        ),
      );
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const selectedCustomer = customers.find(
      (c) => c.id === formData.customerId,
    );
    if (!selectedCustomer) return;

    const totals = calculateTotal(orderItems, formData.discount);

    if (editingOrder) {
      setOrders(
        orders.map((order) =>
          order.id === editingOrder.id
            ? {
                ...order,
                ...formData,
                customerName: selectedCustomer.name,
                items: orderItems,
                totalAmount: totals.total,
                tax: totals.taxAmount,
              }
            : order,
        ),
      );
    } else {
      const newOrder: Order = {
        id: Date.now().toString(),
        customerId: formData.customerId || "",
        customerName: selectedCustomer.name,
        items: orderItems,
        totalAmount: totals.total,
        orderDate: formData.orderDate || new Date().toISOString(),
        status: formData.status || "Pending",
        tableNumber: formData.tableNumber,
        notes: formData.notes,
        discount: formData.discount || 0,
        tax: totals.taxAmount,
      };
      setOrders([...orders, newOrder]);
    }

    handleCloseDialog();
  };

  const handleEdit = (order: Order) => {
    setEditingOrder(order);
    setFormData(order);
    setOrderItems(order.items);
    setIsDialogOpen(true);
  };

  const handleDelete = (order: Order) => {
    if (
      confirm(
        `Are you sure you want to delete order #${order.id.slice(-6).toUpperCase()}?`,
      )
    ) {
      setOrders(orders.filter((o) => o.id !== order.id));
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingOrder(null);
    setFormData({
      customerId: "",
      customerName: "",
      items: [],
      totalAmount: 0,
      orderDate: new Date().toISOString(),
      status: "Pending",
      tableNumber: undefined,
      notes: "",
      discount: 0,
      tax: 0,
    });
    setOrderItems([]);
  };

  const totals = calculateTotal(orderItems, formData.discount);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Order Management</h1>
          <p className="text-slate-400">
            Manage customer orders and track status
          </p>
        </div>
      </div>

      <DataTable
        title="Orders"
        data={orders}
        columns={columns}
        searchPlaceholder="Search orders..."
        searchKey="customerName"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="New Order"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-4xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {editingOrder ? "Edit Order" : "Create New Order"}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="customerId">Customer</Label>
                <Select
                  value={formData.customerId}
                  onValueChange={(value) =>
                    setFormData({ ...formData, customerId: value })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Select customer" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    {customers.map((customer) => (
                      <SelectItem key={customer.id} value={customer.id}>
                        {customer.name}
                      </SelectItem>
                    ))}
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
                    <SelectItem value="Preparing">Preparing</SelectItem>
                    <SelectItem value="Ready">Ready</SelectItem>
                    <SelectItem value="Served">Served</SelectItem>
                    <SelectItem value="Cancelled">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="tableNumber">Table Number (optional)</Label>
                <Input
                  id="tableNumber"
                  type="number"
                  min="1"
                  value={formData.tableNumber || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      tableNumber: e.target.value
                        ? parseInt(e.target.value)
                        : undefined,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  placeholder="For dine-in orders"
                />
              </div>
            </div>

            {/* Menu Items Selection */}
            <Card className="bg-slate-700/50 border-slate-600">
              <CardHeader>
                <CardTitle className="text-white">Add Menu Items</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-60 overflow-y-auto">
                  {menuItems
                    .filter((item) => item.availability)
                    .map((item) => (
                      <div
                        key={item.id}
                        className="p-3 bg-slate-600/50 rounded-lg border border-slate-500 hover:bg-slate-600/70 cursor-pointer transition-colors"
                        onClick={() => addOrderItem(item)}
                      >
                        <h4 className="font-medium text-white">{item.name}</h4>
                        <p className="text-sm text-slate-300">
                          ${item.price.toFixed(2)}
                        </p>
                        <p className="text-xs text-slate-400">
                          {item.category}
                        </p>
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>

            {/* Order Items */}
            {orderItems.length > 0 && (
              <Card className="bg-slate-700/50 border-slate-600">
                <CardHeader>
                  <CardTitle className="text-white">Order Items</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {orderItems.map((item) => (
                    <div
                      key={item.menuId}
                      className="flex items-center justify-between p-3 bg-slate-600/50 rounded-lg"
                    >
                      <div>
                        <h4 className="font-medium text-white">
                          {item.menuName}
                        </h4>
                        <p className="text-sm text-slate-300">
                          ${item.unitPrice.toFixed(2)} each
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() =>
                            updateItemQuantity(item.menuId, item.quantity - 1)
                          }
                          className="h-8 w-8 p-0 border-slate-500"
                        >
                          <Minus className="h-3 w-3" />
                        </Button>
                        <span className="text-white min-w-[2rem] text-center">
                          {item.quantity}
                        </span>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() =>
                            updateItemQuantity(item.menuId, item.quantity + 1)
                          }
                          className="h-8 w-8 p-0 border-slate-500"
                        >
                          <Plus className="h-3 w-3" />
                        </Button>
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => updateItemQuantity(item.menuId, 0)}
                          className="h-8 w-8 p-0 border-red-500 text-red-400 hover:bg-red-600"
                        >
                          <X className="h-3 w-3" />
                        </Button>
                        <span className="text-white font-semibold min-w-[4rem] text-right">
                          ${item.subtotal.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="discount">Discount (%)</Label>
                <Input
                  id="discount"
                  type="number"
                  min="0"
                  max="100"
                  step="0.1"
                  value={formData.discount}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      discount: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="notes">Notes</Label>
                <Textarea
                  id="notes"
                  value={formData.notes}
                  onChange={(e) =>
                    setFormData({ ...formData, notes: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  rows={2}
                />
              </div>
            </div>

            {/* Order Summary */}
            {orderItems.length > 0 && (
              <Card className="bg-slate-700/50 border-slate-600">
                <CardHeader>
                  <CardTitle className="text-white">Order Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex justify-between text-slate-300">
                    <span>Subtotal:</span>
                    <span>${totals.subtotal.toFixed(2)}</span>
                  </div>
                  {formData.discount > 0 && (
                    <div className="flex justify-between text-green-400">
                      <span>Discount ({formData.discount}%):</span>
                      <span>-${totals.discountAmount.toFixed(2)}</span>
                    </div>
                  )}
                  <div className="flex justify-between text-slate-300">
                    <span>Tax (10%):</span>
                    <span>${totals.taxAmount.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-white font-bold text-lg border-t border-slate-600 pt-2">
                    <span>Total:</span>
                    <span>${totals.total.toFixed(2)}</span>
                  </div>
                </CardContent>
              </Card>
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
                disabled={!formData.customerId || orderItems.length === 0}
              >
                {editingOrder ? "Update" : "Create"} Order
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
