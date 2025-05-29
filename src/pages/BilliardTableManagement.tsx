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
import { BilliardTable } from "@/types";
import { mockBilliardTables } from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { CircleDot, MapPin } from "lucide-react";

const statusColors = {
  Available: "bg-green-600",
  Occupied: "bg-blue-600",
  Reserved: "bg-yellow-600",
  Maintenance: "bg-red-600",
};

const conditionColors = {
  Excellent: "bg-green-600",
  Good: "bg-blue-600",
  Fair: "bg-yellow-600",
  "Needs Repair": "bg-red-600",
};

const typeColors = {
  "8-Ball": "bg-purple-600",
  "9-Ball": "bg-blue-600",
  Snooker: "bg-green-600",
  Carom: "bg-orange-600",
};

export default function BilliardTableManagement() {
  const [tables, setTables] = useLocalStorage<BilliardTable[]>(
    "billiardTables",
    mockBilliardTables,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingTable, setEditingTable] = useState<BilliardTable | null>(null);
  const [formData, setFormData] = useState<Partial<BilliardTable>>({
    tableNumber: 0,
    type: "8-Ball",
    status: "Available",
    hourlyRate: 0,
    location: "",
    condition: "Good",
  });

  const columns: Column<BilliardTable>[] = [
    {
      key: "tableNumber",
      label: "Table #",
      sortable: true,
      render: (value: number) => (
        <div className="flex items-center">
          <CircleDot className="w-4 h-4 mr-2 text-blue-400" />
          <span className="font-semibold">#{value}</span>
        </div>
      ),
    },
    {
      key: "type",
      label: "Type",
      sortable: true,
      render: (value: string) => {
        const colorClass = typeColors[value as keyof typeof typeColors];
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
      key: "condition",
      label: "Condition",
      sortable: true,
      render: (value: string) => {
        const colorClass =
          conditionColors[value as keyof typeof conditionColors];
        return <Badge className={`${colorClass} text-white`}>{value}</Badge>;
      },
    },
    {
      key: "hourlyRate",
      label: "Hourly Rate",
      sortable: true,
      render: (value: number) => `$${value}/hr`,
    },
    {
      key: "location",
      label: "Location",
      sortable: true,
      render: (value: string) => (
        <div className="flex items-center">
          <MapPin className="w-3 h-3 mr-1 text-slate-400" />
          <span className="text-sm">{value}</span>
        </div>
      ),
    },
    {
      key: "actions",
      label: "Actions",
    },
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (editingTable) {
      setTables(
        tables.map((table) =>
          table.id === editingTable.id ? { ...table, ...formData } : table,
        ),
      );
    } else {
      const newTable: BilliardTable = {
        id: Date.now().toString(),
        tableNumber: formData.tableNumber || 0,
        type: formData.type || "8-Ball",
        status: formData.status || "Available",
        hourlyRate: formData.hourlyRate || 0,
        location: formData.location || "",
        condition: formData.condition || "Good",
      };
      setTables([...tables, newTable]);
    }

    handleCloseDialog();
  };

  const handleEdit = (table: BilliardTable) => {
    setEditingTable(table);
    setFormData(table);
    setIsDialogOpen(true);
  };

  const handleDelete = (table: BilliardTable) => {
    if (
      confirm(`Are you sure you want to delete Table #${table.tableNumber}?`)
    ) {
      setTables(tables.filter((t) => t.id !== table.id));
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingTable(null);
    setFormData({
      tableNumber: 0,
      type: "8-Ball",
      status: "Available",
      hourlyRate: 0,
      location: "",
      condition: "Good",
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">
            Billiard Table Management
          </h1>
          <p className="text-slate-400">
            Manage your billiard tables and their status
          </p>
        </div>
      </div>

      <DataTable
        title="Billiard Tables"
        data={tables}
        columns={columns}
        searchPlaceholder="Search tables..."
        searchKey="location"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="Add Table"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingTable ? "Edit Billiard Table" : "Add New Billiard Table"}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="tableNumber">Table Number</Label>
                <Input
                  id="tableNumber"
                  type="number"
                  min="1"
                  value={formData.tableNumber}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      tableNumber: parseInt(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="type">Table Type</Label>
                <Select
                  value={formData.type}
                  onValueChange={(value) =>
                    setFormData({ ...formData, type: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="8-Ball">8-Ball</SelectItem>
                    <SelectItem value="9-Ball">9-Ball</SelectItem>
                    <SelectItem value="Snooker">Snooker</SelectItem>
                    <SelectItem value="Carom">Carom</SelectItem>
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
                    <SelectItem value="Available">Available</SelectItem>
                    <SelectItem value="Occupied">Occupied</SelectItem>
                    <SelectItem value="Reserved">Reserved</SelectItem>
                    <SelectItem value="Maintenance">Maintenance</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="condition">Condition</Label>
                <Select
                  value={formData.condition}
                  onValueChange={(value) =>
                    setFormData({ ...formData, condition: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Excellent">Excellent</SelectItem>
                    <SelectItem value="Good">Good</SelectItem>
                    <SelectItem value="Fair">Fair</SelectItem>
                    <SelectItem value="Needs Repair">Needs Repair</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="hourlyRate">Hourly Rate ($)</Label>
                <Input
                  id="hourlyRate"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.hourlyRate}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      hourlyRate: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="location">Location</Label>
                <Input
                  id="location"
                  value={formData.location}
                  onChange={(e) =>
                    setFormData({ ...formData, location: e.target.value })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  placeholder="e.g., Main Floor - Section A"
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
                {editingTable ? "Update" : "Add"} Table
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
