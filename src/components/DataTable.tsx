import { ReactNode, useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Search, Plus, Edit, Trash2, Eye } from "lucide-react";
import { cn } from "@/lib/utils";

export interface Column<T> {
  key: keyof T | "actions";
  label: string;
  sortable?: boolean;
  render?: (value: any, item: T) => ReactNode;
}

interface DataTableProps<T> {
  title: string;
  data: T[];
  columns: Column<T>[];
  searchPlaceholder?: string;
  onAdd?: () => void;
  onEdit?: (item: T) => void;
  onDelete?: (item: T) => void;
  onView?: (item: T) => void;
  addButtonText?: string;
  searchKey?: keyof T;
  className?: string;
}

export function DataTable<T extends { id: string }>({
  title,
  data,
  columns,
  searchPlaceholder = "Search...",
  onAdd,
  onEdit,
  onDelete,
  onView,
  addButtonText = "Add New",
  searchKey,
  className,
}: DataTableProps<T>) {
  const [searchTerm, setSearchTerm] = useState("");
  const [sortColumn, setSortColumn] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");

  const filteredData = data.filter((item) => {
    if (!searchTerm) return true;

    if (searchKey && item[searchKey]) {
      return String(item[searchKey])
        .toLowerCase()
        .includes(searchTerm.toLowerCase());
    }

    return Object.values(item).some((value) =>
      String(value).toLowerCase().includes(searchTerm.toLowerCase()),
    );
  });

  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortColumn) return 0;

    const aValue = a[sortColumn];
    const bValue = b[sortColumn];

    if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
    if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
    return 0;
  });

  const handleSort = (column: keyof T) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortDirection("asc");
    }
  };

  const renderCellValue = (column: Column<T>, item: T) => {
    if (column.key === "actions") {
      return (
        <div className="flex items-center space-x-2">
          {onView && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onView(item)}
              className="h-8 w-8 p-0 text-slate-400 hover:text-blue-400"
            >
              <Eye className="h-4 w-4" />
            </Button>
          )}
          {onEdit && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit(item)}
              className="h-8 w-8 p-0 text-slate-400 hover:text-yellow-400"
            >
              <Edit className="h-4 w-4" />
            </Button>
          )}
          {onDelete && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(item)}
              className="h-8 w-8 p-0 text-slate-400 hover:text-red-400"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          )}
        </div>
      );
    }

    if (column.render) {
      return column.render(item[column.key], item);
    }

    const value = item[column.key];

    // Handle different value types
    if (typeof value === "boolean") {
      return (
        <Badge variant={value ? "default" : "secondary"}>
          {value ? "Yes" : "No"}
        </Badge>
      );
    }

    if (
      (typeof value === "number" && column.key.toString().includes("price")) ||
      column.key.toString().includes("amount") ||
      column.key.toString().includes("salary")
    ) {
      return `$${value.toLocaleString()}`;
    }

    return String(value || "-");
  };

  return (
    <Card className={cn("bg-slate-800/50 border-slate-700", className)}>
      <CardHeader>
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
          <CardTitle className="text-2xl font-bold text-white">
            {title}
          </CardTitle>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center space-y-2 sm:space-y-0 sm:space-x-4 w-full sm:w-auto">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-4 w-4" />
              <Input
                placeholder={searchPlaceholder}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-slate-700/50 border-slate-600 text-white placeholder-slate-400 w-full sm:w-64"
              />
            </div>
            {onAdd && (
              <Button
                onClick={onAdd}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                <Plus className="h-4 w-4 mr-2" />
                {addButtonText}
              </Button>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="rounded-md border border-slate-700 overflow-hidden">
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="bg-slate-700/30 border-slate-700 hover:bg-slate-700/30">
                  {columns.map((column) => (
                    <TableHead
                      key={String(column.key)}
                      className={cn(
                        "text-slate-300 font-semibold",
                        column.sortable &&
                          column.key !== "actions" &&
                          "cursor-pointer hover:text-white",
                      )}
                      onClick={() =>
                        column.sortable &&
                        column.key !== "actions" &&
                        handleSort(column.key as keyof T)
                      }
                    >
                      <div className="flex items-center space-x-1">
                        <span>{column.label}</span>
                        {column.sortable &&
                          column.key !== "actions" &&
                          sortColumn === column.key && (
                            <span className="text-xs">
                              {sortDirection === "asc" ? "↑" : "↓"}
                            </span>
                          )}
                      </div>
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {sortedData.length > 0 ? (
                  sortedData.map((item, index) => (
                    <TableRow
                      key={item.id}
                      className={cn(
                        "border-slate-700 hover:bg-slate-700/20 transition-colors",
                        index % 2 === 0 ? "bg-slate-800/20" : "bg-slate-800/10",
                      )}
                    >
                      {columns.map((column) => (
                        <TableCell
                          key={String(column.key)}
                          className="text-slate-200 py-4"
                        >
                          {renderCellValue(column, item)}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell
                      colSpan={columns.length}
                      className="text-center text-slate-400 py-8"
                    >
                      {searchTerm ? "No results found." : "No data available."}
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </div>

        {sortedData.length > 0 && (
          <div className="flex justify-between items-center mt-4 text-sm text-slate-400">
            <span>
              Showing {sortedData.length} of {data.length} entries
              {searchTerm && ` (filtered)`}
            </span>
            <span>Total: {data.length} records</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
