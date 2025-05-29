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
import { Switch } from "@/components/ui/switch";
import { MenuCafe } from "@/types";
import { mockMenuCafe } from "@/lib/data";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { Clock, Coffee, Utensils, Cookie, IceCream } from "lucide-react";

const categoryIcons = {
  Food: Utensils,
  Beverage: Coffee,
  Snack: Cookie,
  Dessert: IceCream,
};

const categoryColors = {
  Food: "bg-orange-600",
  Beverage: "bg-blue-600",
  Snack: "bg-yellow-600",
  Dessert: "bg-pink-600",
};

export default function MenuManagement() {
  const [menuItems, setMenuItems] = useLocalStorage<MenuCafe[]>(
    "menuItems",
    mockMenuCafe,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<MenuCafe | null>(null);
  const [formData, setFormData] = useState<Partial<MenuCafe>>({
    name: "",
    category: "Food",
    price: 0,
    description: "",
    ingredients: [],
    availability: true,
    preparationTime: 0,
    imageUrl: "",
  });

  const columns: Column<MenuCafe>[] = [
    {
      key: "name",
      label: "Name",
      sortable: true,
    },
    {
      key: "category",
      label: "Category",
      sortable: true,
      render: (value: string) => {
        const Icon = categoryIcons[value as keyof typeof categoryIcons];
        const colorClass = categoryColors[value as keyof typeof categoryColors];
        return (
          <Badge className={`${colorClass} text-white`}>
            <Icon className="w-3 h-3 mr-1" />
            {value}
          </Badge>
        );
      },
    },
    {
      key: "price",
      label: "Price",
      sortable: true,
      render: (value: number) => `$${value.toFixed(2)}`,
    },
    {
      key: "preparationTime",
      label: "Prep Time",
      sortable: true,
      render: (value: number) => (
        <div className="flex items-center">
          <Clock className="w-3 h-3 mr-1 text-slate-400" />
          {value} min
        </div>
      ),
    },
    {
      key: "availability",
      label: "Available",
      sortable: true,
      render: (value: boolean) => (
        <Badge
          variant={value ? "default" : "secondary"}
          className={value ? "bg-green-600" : "bg-red-600"}
        >
          {value ? "Available" : "Unavailable"}
        </Badge>
      ),
    },
    {
      key: "ingredients",
      label: "Ingredients",
      render: (value: string[]) => (
        <div className="max-w-xs">
          <p className="text-sm text-slate-300 truncate">{value.join(", ")}</p>
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

    if (editingItem) {
      setMenuItems(
        menuItems.map((item) =>
          item.id === editingItem.id ? { ...item, ...formData } : item,
        ),
      );
    } else {
      const newItem: MenuCafe = {
        id: Date.now().toString(),
        name: formData.name || "",
        category: formData.category || "Food",
        price: formData.price || 0,
        description: formData.description || "",
        ingredients: formData.ingredients || [],
        availability: formData.availability ?? true,
        preparationTime: formData.preparationTime || 0,
        imageUrl: formData.imageUrl,
      };
      setMenuItems([...menuItems, newItem]);
    }

    handleCloseDialog();
  };

  const handleEdit = (item: MenuCafe) => {
    setEditingItem(item);
    setFormData(item);
    setIsDialogOpen(true);
  };

  const handleDelete = (item: MenuCafe) => {
    if (confirm(`Are you sure you want to delete ${item.name}?`)) {
      setMenuItems(menuItems.filter((i) => i.id !== item.id));
    }
  };

  const handleCloseDialog = () => {
    setIsDialogOpen(false);
    setEditingItem(null);
    setFormData({
      name: "",
      category: "Food",
      price: 0,
      description: "",
      ingredients: [],
      availability: true,
      preparationTime: 0,
      imageUrl: "",
    });
  };

  const handleIngredientsChange = (value: string) => {
    const ingredients = value
      .split(",")
      .map((ingredient) => ingredient.trim())
      .filter(Boolean);
    setFormData({ ...formData, ingredients });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">Menu Management</h1>
          <p className="text-slate-400">
            Manage your cafe menu items and pricing
          </p>
        </div>
      </div>

      <DataTable
        title="Menu Items"
        data={menuItems}
        columns={columns}
        searchPlaceholder="Search menu items..."
        searchKey="name"
        onAdd={() => setIsDialogOpen(true)}
        onEdit={handleEdit}
        onDelete={handleDelete}
        addButtonText="Add Menu Item"
      />

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-slate-800 border-slate-700 text-white max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingItem ? "Edit Menu Item" : "Add New Menu Item"}
            </DialogTitle>
          </DialogHeader>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="name">Item Name</Label>
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
                <Label htmlFor="category">Category</Label>
                <Select
                  value={formData.category}
                  onValueChange={(value) =>
                    setFormData({ ...formData, category: value as any })
                  }
                >
                  <SelectTrigger className="bg-slate-700 border-slate-600 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-slate-700 border-slate-600">
                    <SelectItem value="Food">Food</SelectItem>
                    <SelectItem value="Beverage">Beverage</SelectItem>
                    <SelectItem value="Snack">Snack</SelectItem>
                    <SelectItem value="Dessert">Dessert</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="price">Price ($)</Label>
                <Input
                  id="price"
                  type="number"
                  min="0"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      price: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="preparationTime">
                  Preparation Time (minutes)
                </Label>
                <Input
                  id="preparationTime"
                  type="number"
                  min="0"
                  value={formData.preparationTime}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      preparationTime: parseInt(e.target.value) || 0,
                    })
                  }
                  className="bg-slate-700 border-slate-600 text-white"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                className="bg-slate-700 border-slate-600 text-white"
                rows={3}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="ingredients">Ingredients (comma-separated)</Label>
              <Textarea
                id="ingredients"
                value={formData.ingredients?.join(", ") || ""}
                onChange={(e) => handleIngredientsChange(e.target.value)}
                className="bg-slate-700 border-slate-600 text-white"
                rows={2}
                placeholder="e.g., Tomato, Lettuce, Cheese, Bread"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="imageUrl">Image URL (optional)</Label>
              <Input
                id="imageUrl"
                type="url"
                value={formData.imageUrl}
                onChange={(e) =>
                  setFormData({ ...formData, imageUrl: e.target.value })
                }
                className="bg-slate-700 border-slate-600 text-white"
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div className="flex items-center space-x-2">
              <Switch
                id="availability"
                checked={formData.availability}
                onCheckedChange={(checked) =>
                  setFormData({ ...formData, availability: checked })
                }
              />
              <Label htmlFor="availability">Available for order</Label>
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
                {editingItem ? "Update" : "Add"} Menu Item
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
