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
import { Reservation, Customer, BilliardTable } from "@/types";
import {
  mockReservations,
  mockCustomers,
  mockBilliardTables,
} from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { Calendar, Clock, Users, MapPin } from "lucide-react";

const statusColors = {
  Confirmed: "bg-green-600",
  Pending: "bg-yellow-600",
  Cancelled: "bg-red-600",
  Completed: "bg-blue-600",
  "No Show": "bg-slate-600",
};

export default function ReservationManagement() {
  const [reservations, setReservations] = useLocalStorage<Reservation[]>(
    "reservations",
    mockReservations,
  );
  const [customers] = useLocalStorage<Customer[]>("customers", mockCustomers);
  const [tables] = useLocalStorage<BilliardTable[]>(
    "billiardTables",
    mockBilliardTables,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingReservation, setEditingReservation] =
    useState<Reservation | null>(null);
  const [formData, setFormData] = useState<Partial<Reservation>>({
    customerId: "",
    customerName: "",
    customerPhone: "",
    tableId: "",
    tableNumber: 0,
    reservationDate: "",
    startTime: "",
    endTime: "",
    duration: 2,
    status: "Pending",
    partySize: 1,
    specialRequests: "",
    deposit: 0,
  });

  const columns: Column<Reservation>[] = [
    {
      key: "id",
      label: "Reservation ID",
      sortable: true,
      render: (value: string) => `#${value.slice(-6).toUpperCase()}`,
    },
    {
      key: "customerName",
      label: "Customer",
      sortable: true,
    },
    {
      key: "customerPhone",
      label: "Phone",
      sortable: true,
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
      key: "reservationDate",
      label: "Date",
      sortable: true,
      render: (value: string) => (
        <div className="flex items-center">
          <Calendar className="w-3 h-3 mr-1 text-slate-400" />
          {new Date(value).toLocaleDateString()}
        </div>
      ),
    },
    {
      key: "startTime",
      label: "Time",
      sortable: true,
      render: (value: string, item: Reservation) => (
        <div className="flex items-center">
          <Clock className="w-3 h-3 mr-1 text-slate-400" />
          {value} - {item.endTime}
        </div>
      ),
    },
    {
      key: "partySize",
      label: "Party Size",
      sortable: true,
      render: (value: number) => (
        <div className="flex items-center">
          <Users className="w-3 h-3 mr-1 text-slate-400" />
          {value} {value === 1 ? "person" : "people"}
        </div>
      ),
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
      key: "deposit",
      label: "Deposit",
      sortable: true,
      render: (value: number) => `$${value.toFixed(2)}`,
    },
    {
      key: "actions",
      label: "Actions",
    },
  ];

  const calculateEndTime = (startTime: string, duration: number) => {
    const [hours, minutes] = startTime.split(":").map(Number);
    const startMinutes = hours * 60 + minutes;
    const endMinutes = startMinutes + duration * 60;
    const endHours = Math.floor(endMinutes / 60) % 24;
    const endMins = endMinutes % 60;
    return `${endHours.toString().padStart(2, "0")}:${endMins.toString().padStart(2, "0")}`;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const selectedCustomer = customers.find(
      (c) => c.id === formData.customerId,
    );
    const selectedTable = tables.find((t) => t.id === formData.tableId);
    if (!selectedCustomer || !selectedTable) return;

    const endTime = calculateEndTime(
      formData.startTime || "",
      formData.duration || 2,
    );
    const deposit = selectedTable.hourlyRate * (formData.duration || 2) * 0.2; // 20% deposit

    if (editingReservation) {
      setReservations(
        reservations.map((reservation) =>
          reservation.id === editingReservation.id
            ? {
                ...reservation,
                ...formData,
                customerName: selectedCustomer.name,
                customerPhone: selectedCustomer.phone,
                tableNumber: selectedTable.tableNumber,
                endTime,
                deposit: formData.deposit || deposit,
              }
            : reservation,
        ),
      );
    } else {
      const newReservation: Reservation = {
        id: Date.now().toString(),
        customerId: formData.customerId || "",
        customerName: selectedCustomer.name,
        customerPhone: selectedCustomer.phone,
        tableId: formData.tableId || "",
        tableNumber: selectedTable.tableNumber,
        reservationDate: formData.reservationDate || "",
        startTime: formData.startTime || "",
        endTime,
        duration: formData.duration || 2,
        status: formData.status || "Pending",
        partySize: formData.partySize || 1,
        specialRequests: formData.specialRequests,
        deposit: formData.deposit || deposit,
      };
      setReservations([...reservations, newReservation]);
    }

    handleCloseDialog();
  };

  const handleEdit = (reservation: Reservation) => {
    setEditingReservation(reservation);
    setFormData(reservation);
    setIsDialogOpen(true);
  };

  const handleDelete = (reservation: Reservation) => {
    if (
      confirm(
        `Are you sure you want to delete reservation #${reservation.id.slice(-6).toUpperCase()}?`,
      )
    ) {
      setReservations(reservations.filter((r) => r.id !== reservation.id));
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingReservation(null);
    setFormData({
      customerId: "",
      customerName: "",
      customerPhone: "",
      tableId: "",
      tableNumber: 0,
      reservationDate: "",
      startTime: "",
      endTime: "",
      duration: 2,
      status: "Pending",
      partySize: 1,
      specialRequests: "",
      deposit: 0,
    });
  };

  const selectedTable = tables.find((t) => t.id === formData.tableId);
  const calculatedDeposit = selectedTable
    ? selectedTable.hourlyRate * (formData.duration || 2) * 0.2
    : 0;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">
            Reservation Management
          </h1>
          <p className="text-slate-400">
            Manage table reservations and bookings
          </p>
        </div>
      </div>

      <DataTable
        title="Reservations"
        data={reservations}
        columns={columns}
        searchPlaceholder="Search reservations..."
        searchKey="customerName"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="New Reservation"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingReservation
                ? "Edit Reservation"
                : "Create New Reservation"}
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
                        {customer.name} - {customer.phone}
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
                      .filter((table) => table.status === "Available")
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
                <Label htmlFor="reservationDate">Reservation Date</Label>
                <Input
                  id="reservationDate"
                  type="date"
                  value={formData.reservationDate}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      reservationDate: e.target.value,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  min={new Date().toISOString().split("T")[0]}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="startTime">Start Time</Label>
                <Input
                  id="startTime"
                  type="time"
                  value={formData.startTime}
                  onChange={(e) =>
                    setFormData({ ...formData, startTime: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="duration">Duration (hours)</Label>
                <Select
                  value={formData.duration?.toString()}
                  onValueChange={(value) =>
                    setFormData({ ...formData, duration: parseFloat(value) })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="1">1 hour</SelectItem>
                    <SelectItem value="1.5">1.5 hours</SelectItem>
                    <SelectItem value="2">2 hours</SelectItem>
                    <SelectItem value="2.5">2.5 hours</SelectItem>
                    <SelectItem value="3">3 hours</SelectItem>
                    <SelectItem value="4">4 hours</SelectItem>
                    <SelectItem value="5">5 hours</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="partySize">Party Size</Label>
                <Input
                  id="partySize"
                  type="number"
                  min="1"
                  max="8"
                  value={formData.partySize}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      partySize: parseInt(e.target.value) || 1,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
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
                    <SelectItem value="Confirmed">Confirmed</SelectItem>
                    <SelectItem value="Cancelled">Cancelled</SelectItem>
                    <SelectItem value="Completed">Completed</SelectItem>
                    <SelectItem value="No Show">No Show</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="deposit">Deposit ($)</Label>
                <Input
                  id="deposit"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.deposit || calculatedDeposit}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      deposit: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                />
                {selectedTable && (
                  <p className="text-xs text-slate-400">
                    Suggested: ${calculatedDeposit.toFixed(2)} (20% of total
                    cost)
                  </p>
                )}
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="specialRequests">Special Requests</Label>
              <Textarea
                id="specialRequests"
                value={formData.specialRequests}
                onChange={(e) =>
                  setFormData({ ...formData, specialRequests: e.target.value })
                }
                className="bg-slate-700 border-slate-600 text-white"
                rows={3}
                placeholder="Any special requirements or notes..."
              />
            </div>

            {formData.startTime && formData.duration && (
              <div className="p-4 bg-slate-700/50 rounded-lg border border-slate-600">
                <h4 className="font-semibold text-white mb-2">
                  Reservation Summary
                </h4>
                <div className="text-sm text-slate-300 space-y-1">
                  <p>
                    End Time:{" "}
                    {calculateEndTime(formData.startTime, formData.duration)}
                  </p>
                  {selectedTable && (
                    <>
                      <p>Table Type: {selectedTable.type}</p>
                      <p>Hourly Rate: ${selectedTable.hourlyRate}</p>
                      <p>
                        Total Cost: $
                        {(selectedTable.hourlyRate * formData.duration).toFixed(
                          2,
                        )}
                      </p>
                    </>
                  )}
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
                  !formData.reservationDate ||
                  !formData.startTime
                }
              >
                {editingReservation ? "Update" : "Create"} Reservation
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
