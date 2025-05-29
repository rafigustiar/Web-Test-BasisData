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
import { Checkbox } from "@/components/ui/checkbox";
import { RentalTransaction, Customer, BilliardTable, Employee } from "@/types";
import {
  mockRentalTransactions,
  mockCustomers,
  mockBilliardTables,
  mockEmployees,
} from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { Clock, Play, Pause, Square, MapPin, User } from "lucide-react";

const statusColors = {
  Active: "bg-green-600",
  Completed: "bg-blue-600",
  Paused: "bg-yellow-600",
  Cancelled: "bg-red-600",
};

const paymentStatusColors = {
  Paid: "bg-green-600",
  Unpaid: "bg-red-600",
  Partial: "bg-yellow-600",
};

const additionalServices = [
  "Cue rental",
  "Chalk",
  "Table cover",
  "Premium balls",
  "Cleaning service",
  "Refreshments",
  "Tournament setup",
];

export default function RentalTransactionManagement() {
  const [rentals, setRentals] = useLocalStorage<RentalTransaction[]>(
    "rentalTransactions",
    mockRentalTransactions,
  );
  const [customers] = useLocalStorage<Customer[]>("customers", mockCustomers);
  const [tables] = useLocalStorage<BilliardTable[]>(
    "billiardTables",
    mockBilliardTables,
  );
  const [employees] = useLocalStorage<Employee[]>("employees", mockEmployees);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingRental, setEditingRental] = useState<RentalTransaction | null>(
    null,
  );
  const [formData, setFormData] = useState<Partial<RentalTransaction>>({
    customerId: "",
    customerName: "",
    tableId: "",
    tableNumber: 0,
    startTime: new Date().toISOString(),
    endTime: undefined,
    duration: 0,
    hourlyRate: 0,
    totalAmount: 0,
    status: "Active",
    additionalServices: [],
    employeeId: "",
    employeeName: "",
    paymentStatus: "Unpaid",
  });

  const columns: Column<RentalTransaction>[] = [
    {
      key: "id",
      label: "Transaction ID",
      sortable: true,
      render: (value: string) => `#${value.slice(-6).toUpperCase()}`,
    },
    {
      key: "customerName",
      label: "Customer",
      sortable: true,
      render: (value: string) => (
        <div className="flex items-center">
          <User className="w-3 h-3 mr-1 text-blue-400" />
          {value}
        </div>
      ),
    },
    {
      key: "tableNumber",
      label: "Table",
      sortable: true,
      render: (value: number) => (
        <div className="flex items-center">
          <MapPin className="w-3 h-3 mr-1 text-blue-400" />#{value}
        </div>
      ),
    },
    {
      key: "startTime",
      label: "Start Time",
      sortable: true,
      render: (value: string) => (
        <div className="flex items-center">
          <Clock className="w-3 h-3 mr-1 text-slate-400" />
          {new Date(value).toLocaleString()}
        </div>
      ),
    },
    {
      key: "duration",
      label: "Duration",
      sortable: true,
      render: (value: number) => `${value.toFixed(1)}h`,
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
      key: "paymentStatus",
      label: "Payment",
      sortable: true,
      render: (value: string) => {
        const colorClass =
          paymentStatusColors[value as keyof typeof paymentStatusColors];
        return <Badge className={`${colorClass} text-white`}>{value}</Badge>;
      },
    },
    {
      key: "employeeName",
      label: "Staff",
      sortable: true,
    },
    {
      key: "actions",
      label: "Actions",
    },
  ];

  const calculateDuration = (startTime: string, endTime?: string) => {
    const start = new Date(startTime);
    const end = endTime ? new Date(endTime) : new Date();
    return (end.getTime() - start.getTime()) / (1000 * 60 * 60); // hours
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const selectedCustomer = customers.find(
      (c) => c.id === formData.customerId,
    );
    const selectedTable = tables.find((t) => t.id === formData.tableId);
    const selectedEmployee = employees.find(
      (e) => e.id === formData.employeeId,
    );

    if (!selectedCustomer || !selectedTable || !selectedEmployee) return;

    const duration = formData.endTime
      ? calculateDuration(formData.startTime || "", formData.endTime)
      : formData.duration || 0;

    const totalAmount = duration * selectedTable.hourlyRate;

    if (editingRental) {
      setRentals(
        rentals.map((rental) =>
          rental.id === editingRental.id
            ? {
                ...rental,
                ...formData,
                customerName: selectedCustomer.name,
                tableNumber: selectedTable.tableNumber,
                employeeName: selectedEmployee.name,
                hourlyRate: selectedTable.hourlyRate,
                duration,
                totalAmount,
              }
            : rental,
        ),
      );
    } else {
      const newRental: RentalTransaction = {
        id: Date.now().toString(),
        customerId: formData.customerId || "",
        customerName: selectedCustomer.name,
        tableId: formData.tableId || "",
        tableNumber: selectedTable.tableNumber,
        startTime: formData.startTime || new Date().toISOString(),
        endTime: formData.endTime,
        duration,
        hourlyRate: selectedTable.hourlyRate,
        totalAmount,
        status: formData.status || "Active",
        additionalServices: formData.additionalServices || [],
        employeeId: formData.employeeId || "",
        employeeName: selectedEmployee.name,
        paymentStatus: formData.paymentStatus || "Unpaid",
      };
      setRentals([...rentals, newRental]);
    }

    handleCloseDialog();
  };

  const handleEdit = (rental: RentalTransaction) => {
    setEditingRental(rental);
    setFormData(rental);
    setIsDialogOpen(true);
  };

  const handleDelete = (rental: RentalTransaction) => {
    if (
      confirm(
        `Are you sure you want to delete rental #${rental.id.slice(-6).toUpperCase()}?`,
      )
    ) {
      setRentals(rentals.filter((r) => r.id !== rental.id));
    }
  };

  const handleCompleteRental = (rental: RentalTransaction) => {
    const endTime = new Date().toISOString();
    const duration = calculateDuration(rental.startTime, endTime);
    const totalAmount = duration * rental.hourlyRate;

    setRentals(
      rentals.map((r) =>
        r.id === rental.id
          ? {
              ...r,
              status: "Completed",
              endTime,
              duration,
              totalAmount,
            }
          : r,
      ),
    );
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingRental(null);
    setFormData({
      customerId: "",
      customerName: "",
      tableId: "",
      tableNumber: 0,
      startTime: new Date().toISOString(),
      endTime: undefined,
      duration: 0,
      hourlyRate: 0,
      totalAmount: 0,
      status: "Active",
      additionalServices: [],
      employeeId: "",
      employeeName: "",
      paymentStatus: "Unpaid",
    });
  };

  const selectedTable = tables.find((t) => t.id === formData.tableId);
  const estimatedCost =
    selectedTable && formData.duration
      ? (selectedTable.hourlyRate * formData.duration).toFixed(2)
      : "0.00";

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">
            Rental Transaction Management
          </h1>
          <p className="text-slate-400">
            Track active table rentals and manage transactions
          </p>
        </div>
      </div>

      {/* Quick Actions for Active Rentals */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {rentals
          .filter((r) => r.status === "Active")
          .map((rental) => (
            <div
              key={rental.id}
              className="p-4 bg-slate-700/50 rounded-lg border border-slate-600"
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-white">
                  Table #{rental.tableNumber}
                </h3>
                <Badge className="bg-green-600">Active</Badge>
              </div>
              <p className="text-sm text-slate-300 mb-1">
                {rental.customerName}
              </p>
              <p className="text-xs text-slate-400 mb-3">
                Started: {new Date(rental.startTime).toLocaleTimeString()}
              </p>
              <Button
                size="sm"
                onClick={() => handleCompleteRental(rental)}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                <Square className="w-3 h-3 mr-1" />
                Complete Rental
              </Button>
            </div>
          ))}
      </div>

      <DataTable
        title="Rental Transactions"
        data={rentals}
        columns={columns}
        searchPlaceholder="Search rentals..."
        searchKey="customerName"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="Start Rental"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingRental ? "Edit Rental Transaction" : "Start New Rental"}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                <Label htmlFor="tableId">Table</Label>
                <Select
                  value={formData.tableId}
                  onValueChange={(value) =>
                    setFormData({ ...formData, tableId: value })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Select table" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    {tables
                      .filter(
                        (table) =>
                          table.status === "Available" ||
                          table.id === formData.tableId,
                      )
                      .map((table) => (
                        <SelectItem key={table.id} value={table.id}>
                          Table #{table.tableNumber} - {table.type} ($
                          {table.hourlyRate}/hr)
                        </SelectItem>
                      ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="employeeId">Staff Member</Label>
                <Select
                  value={formData.employeeId}
                  onValueChange={(value) =>
                    setFormData({ ...formData, employeeId: value })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue placeholder="Select staff" />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    {employees
                      .filter((emp) => emp.status === "Active")
                      .map((employee) => (
                        <SelectItem key={employee.id} value={employee.id}>
                          {employee.name} - {employee.position}
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
                    <SelectItem value="Active">Active</SelectItem>
                    <SelectItem value="Paused">Paused</SelectItem>
                    <SelectItem value="Completed">Completed</SelectItem>
                    <SelectItem value="Cancelled">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="paymentStatus">Payment Status</Label>
                <Select
                  value={formData.paymentStatus}
                  onValueChange={(value) =>
                    setFormData({ ...formData, paymentStatus: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Unpaid">Unpaid</SelectItem>
                    <SelectItem value="Partial">Partial</SelectItem>
                    <SelectItem value="Paid">Paid</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="startTime">Start Time</Label>
                <Input
                  id="startTime"
                  type="datetime-local"
                  value={formData.startTime?.slice(0, 16)}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      startTime: new Date(e.target.value).toISOString(),
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>
            </div>

            {formData.status === "Completed" && (
              <div className="space-y-2">
                <Label htmlFor="endTime">End Time</Label>
                <Input
                  id="endTime"
                  type="datetime-local"
                  value={formData.endTime?.slice(0, 16) || ""}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      endTime: e.target.value
                        ? new Date(e.target.value).toISOString()
                        : undefined,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
            )}

            {formData.status !== "Completed" && (
              <div className="space-y-2">
                <Label htmlFor="duration">Estimated Duration (hours)</Label>
                <Input
                  id="duration"
                  type="number"
                  min="0.5"
                  step="0.5"
                  value={formData.duration}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      duration: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
            )}

            <div className="space-y-3">
              <Label>Additional Services</Label>
              <div className="grid grid-cols-2 gap-2">
                {additionalServices.map((service) => (
                  <div key={service} className="flex items-center space-x-2">
                    <Checkbox
                      id={service}
                      checked={formData.additionalServices?.includes(service)}
                      onCheckedChange={(checked) => {
                        const services = formData.additionalServices || [];
                        if (checked) {
                          setFormData({
                            ...formData,
                            additionalServices: [...services, service],
                          });
                        } else {
                          setFormData({
                            ...formData,
                            additionalServices: services.filter(
                              (s) => s !== service,
                            ),
                          });
                        }
                      }}
                    />
                    <Label htmlFor={service} className="text-sm">
                      {service}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {selectedTable && formData.duration > 0 && (
              <div className="p-4 bg-slate-700/50 rounded-lg border border-slate-600">
                <h4 className="font-semibold text-white mb-2">Cost Estimate</h4>
                <div className="text-sm text-slate-300 space-y-1">
                  <p>Table Type: {selectedTable.type}</p>
                  <p>Hourly Rate: ${selectedTable.hourlyRate}</p>
                  <p>Duration: {formData.duration} hours</p>
                  <p className="font-semibold text-white">
                    Total: ${estimatedCost}
                  </p>
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
                disabled={
                  !formData.customerId ||
                  !formData.tableId ||
                  !formData.employeeId
                }
              >
                {editingRental ? "Update" : "Start"} Rental
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
