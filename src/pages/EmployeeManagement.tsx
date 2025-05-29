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
import { Employee } from "@/types";
import { mockEmployees } from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";

const statusColors = {
  Active: "bg-green-600",
  Inactive: "bg-red-600",
  "On Leave": "bg-yellow-600",
};

const departmentColors = {
  Cafe: "bg-blue-600",
  Billiard: "bg-purple-600",
  Management: "bg-orange-600",
  Maintenance: "bg-gray-600",
};

export default function EmployeeManagement() {
  const [employees, setEmployees] = useLocalStorage<Employee[]>(
    "employees",
    mockEmployees,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
  const [formData, setFormData] = useState<Partial<Employee>>({
    name: "",
    email: "",
    phone: "",
    position: "",
    department: "Cafe",
    salary: 0,
    hireDate: new Date().toISOString().split("T")[0],
    status: "Active",
    shift: "Morning",
  });

  const columns: Column<Employee>[] = [
    {
      key: "name",
      label: "Name",
      sortable: true,
    },
    {
      key: "position",
      label: "Position",
      sortable: true,
    },
    {
      key: "department",
      label: "Department",
      sortable: true,
      render: (value: string) => {
        const colorClass =
          departmentColors[value as keyof typeof departmentColors];
        return <Badge className={`${colorClass} text-white`}>{value}</Badge>;
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
      key: "shift",
      label: "Shift",
      sortable: true,
      render: (value: string) => (
        <Badge variant="outline" className="text-slate-300 border-slate-500">
          {value}
        </Badge>
      ),
    },
    {
      key: "salary",
      label: "Salary",
      sortable: true,
      render: (value: number) => `$${value.toLocaleString()}`,
    },
    {
      key: "hireDate",
      label: "Hire Date",
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

    if (editingEmployee) {
      setEmployees(
        employees.map((employee) =>
          employee.id === editingEmployee.id
            ? { ...employee, ...formData }
            : employee,
        ),
      );
    } else {
      const newEmployee: Employee = {
        id: Date.now().toString(),
        name: formData.name || "",
        email: formData.email || "",
        phone: formData.phone || "",
        position: formData.position || "",
        department: formData.department || "Cafe",
        salary: formData.salary || 0,
        hireDate: formData.hireDate || new Date().toISOString().split("T")[0],
        status: formData.status || "Active",
        shift: formData.shift || "Morning",
      };
      setEmployees([...employees, newEmployee]);
    }

    handleCloseDialog();
  };

  const handleEdit = (employee: Employee) => {
    setEditingEmployee(employee);
    setFormData(employee);
    setIsDialogOpen(true);
  };

  const handleDelete = (employee: Employee) => {
    if (confirm(`Are you sure you want to delete ${employee.name}?`)) {
      setEmployees(employees.filter((e) => e.id !== employee.id));
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingEmployee(null);
    setFormData({
      name: "",
      email: "",
      phone: "",
      position: "",
      department: "Cafe",
      salary: 0,
      hireDate: new Date().toISOString().split("T")[0],
      status: "Active",
      shift: "Morning",
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Employee Management</h1>
          <p className="text-slate-400">Manage your staff and workforce</p>
        </div>
      </div>

      <DataTable
        title="Employees"
        data={employees}
        columns={columns}
        searchPlaceholder="Search employees..."
        searchKey="name"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="Add Employee"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingEmployee ? "Edit Employee" : "Add New Employee"}
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
                <Label htmlFor="position">Position</Label>
                <Input
                  id="position"
                  value={formData.position}
                  onChange={(e) =>
                    setFormData({ ...formData, position: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="department">Department</Label>
                <Select
                  value={formData.department}
                  onValueChange={(value) =>
                    setFormData({ ...formData, department: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Cafe">Cafe</SelectItem>
                    <SelectItem value="Billiard">Billiard</SelectItem>
                    <SelectItem value="Management">Management</SelectItem>
                    <SelectItem value="Maintenance">Maintenance</SelectItem>
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
                    <SelectItem value="Inactive">Inactive</SelectItem>
                    <SelectItem value="On Leave">On Leave</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="shift">Shift</Label>
                <Select
                  value={formData.shift}
                  onValueChange={(value) =>
                    setFormData({ ...formData, shift: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Morning">Morning</SelectItem>
                    <SelectItem value="Afternoon">Afternoon</SelectItem>
                    <SelectItem value="Night">Night</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="salary">Salary ($)</Label>
                <Input
                  id="salary"
                  type="number"
                  min="0"
                  value={formData.salary}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      salary: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="hireDate">Hire Date</Label>
                <Input
                  id="hireDate"
                  type="date"
                  value={formData.hireDate}
                  onChange={(e) =>
                    setFormData({ ...formData, hireDate: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>
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
                {editingEmployee ? "Update" : "Add"} Employee
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
