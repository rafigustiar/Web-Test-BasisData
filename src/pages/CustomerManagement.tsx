import { useState } from "react";
import { DataTable, Column } from "@/components/DataTable";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
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
import { Customer } from "@/types";
import { mockCustomers } from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { Plus, Star, Award, Users } from "lucide-react";

const membershipIcons = {
  Regular: Users,
  VIP: Star,
  Premium: Award,
};

const membershipColors = {
  Regular: "bg-slate-600",
  VIP: "bg-yellow-600",
  Premium: "bg-purple-600",
};

export default function CustomerManagement() {
  const [customers, setCustomers] = useLocalStorage<Customer[]>(
    "customers",
    mockCustomers,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState<Customer | null>(null);
  const [formData, setFormData] = useState<Partial<Customer>>({
    name: "",
    email: "",
    phone: "",
    address: "",
    membershipType: "Regular",
    joinDate: new Date().toISOString().split("T")[0],
    totalSpent: 0,
    loyaltyPoints: 0,
  });

  const columns: Column<Customer>[] = [
    {
      key: "name",
      label: "Name",
      sortable: true,
    },
    {
      key: "email",
      label: "Email",
      sortable: true,
    },
    {
      key: "phone",
      label: "Phone",
      sortable: true,
    },
    {
      key: "membershipType",
      label: "Membership",
      sortable: true,
      render: (value: string) => {
        const Icon = membershipIcons[value as keyof typeof membershipIcons];
        const colorClass =
          membershipColors[value as keyof typeof membershipColors];
        return (
          <Badge className={`${colorClass} text-white`}>
            <Icon className="w-3 h-3 mr-1" />
            {value}
          </Badge>
        );
      },
    },
    {
      key: "totalSpent",
      label: "Total Spent",
      sortable: true,
      render: (value: number) => `$${value.toLocaleString()}`,
    },
    {
      key: "loyaltyPoints",
      label: "Loyalty Points",
      sortable: true,
      render: (value: number) => (
        <Badge variant="outline" className="text-blue-400 border-blue-400">
          {value} pts
        </Badge>
      ),
    },
    {
      key: "joinDate",
      label: "Join Date",
      sortable: true,
      render: (value: string) => new Date(value).toLocaleDateString(),
    },
    {
      key: "actions",
      label: "Actions",
    },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (editingCustomer) {
      // Update existing customer
      setCustomers(
        customers.map((customer) =>
          customer.id === editingCustomer.id
            ? { ...customer, ...formData }
            : customer,
        ),
      );
    } else {
      // Add new customer
      const newCustomer: Customer = {
        id: Date.now().toString(),
        name: formData.name || "",
        email: formData.email || "",
        phone: formData.phone || "",
        address: formData.address || "",
        membershipType: formData.membershipType || "Regular",
        joinDate: formData.joinDate || new Date().toISOString().split("T")[0],
        totalSpent: formData.totalSpent || 0,
        loyaltyPoints: formData.loyaltyPoints || 0,
      };
      setCustomers([...customers, newCustomer]);
    }

    handleCloseDialog();
  };

  const handleEdit = (customer: Customer) => {
    setEditingCustomer(customer);
    setFormData(customer);
    setIsDialogOpen(true);
  };

  const handleDelete = (customer: Customer) => {
    if (confirm(`Are you sure you want to delete ${customer.name}?`)) {
      setCustomers(customers.filter((c) => c.id !== customer.id));
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingCustomer(null);
    setFormData({
      name: "",
      email: "",
      phone: "",
      address: "",
      membershipType: "Regular",
      joinDate: new Date().toISOString().split("T")[0],
      totalSpent: 0,
      loyaltyPoints: 0,
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Customer Management</h1>
          <p className="text-slate-400">
            Manage your customer database and memberships
          </p>
        </div>
      </div>

      <DataTable
        title="Customers"
        data={customers}
        columns={columns}
        searchPlaceholder="Search customers..."
        searchKey="name"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="Add Customer"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingCustomer ? "Edit Customer" : "Add New Customer"}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">Phone</Label>
                <Input
                  id="phone"
                  value={formData.phone}
                  onChange={(e) =>
                    setFormData({ ...formData, phone: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="membershipType">Membership Type</Label>
                <Select
                  value={formData.membershipType}
                  onValueChange={(value) =>
                    setFormData({ ...formData, membershipType: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Regular">Regular</SelectItem>
                    <SelectItem value="VIP">VIP</SelectItem>
                    <SelectItem value="Premium">Premium</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="joinDate">Join Date</Label>
                <Input
                  id="joinDate"
                  type="date"
                  value={formData.joinDate}
                  onChange={(e) =>
                    setFormData({ ...formData, joinDate: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="totalSpent">Total Spent ($)</Label>
                <Input
                  id="totalSpent"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.totalSpent}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      totalSpent: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="address">Address</Label>
              <Textarea
                id="address"
                value={formData.address}
                onChange={(e) =>
                  setFormData({ ...formData, address: e.target.value })
                }
                className="bg-slate-700 border-slate-600 text-white"
                rows={3}
              />
            </div>

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
              >
                {editingCustomer ? "Update" : "Add"} Customer
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
