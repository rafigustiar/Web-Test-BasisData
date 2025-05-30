import { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Users,
  UserCheck,
  Coffee,
  ShoppingCart,
  CreditCard,
  Calendar,
  Receipt,
  CircleDot,
  LayoutDashboard,
  Menu,
  X,
} from "lucide-react";
import { useState } from "react";

interface LayoutProps {
  children: ReactNode;
}

const navigationItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/customers", label: "Customers", icon: Users },
  { href: "/employees", label: "Employees", icon: UserCheck },
  { href: "/menu", label: "Menu Cafe", icon: Coffee },
  { href: "/orders", label: "Orders", icon: ShoppingCart },
  { href: "/payments", label: "Payments", icon: CreditCard },
  { href: "/reservations", label: "Reservations", icon: Calendar },
  { href: "/rentals", label: "Rentals", icon: Receipt },
  { href: "/tables", label: "Billiard Tables", icon: CircleDot },
];

export function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-sm border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <CircleDot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Amorty</h1>
                <p className="text-xs text-slate-400">& CAFE</p>
              </div>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden lg:flex space-x-1">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    to={item.href}
                    className={cn(
                      "flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200",
                      isActive
                        ? "bg-blue-600 text-white shadow-lg"
                        : "text-slate-300 hover:text-white hover:bg-slate-700/50",
                    )}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </nav>

            {/* Staff Area Button */}
            <div className="hidden lg:flex items-center space-x-4">
              <span className="text-sm text-slate-400">
                Tel: (0341) - 487789
              </span>
              <Button
                size="sm"
                className="bg-pink-600 hover:bg-pink-700 text-white"
              >
                Staff Area
              </Button>
            </div>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden text-white"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="w-5 h-5" />
              ) : (
                <Menu className="w-5 h-5" />
              )}
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-black/30 backdrop-blur-sm border-b border-slate-700/50">
          <nav className="max-w-7xl mx-auto px-4 py-4 space-y-2">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.href;

              return (
                <Link
                  key={item.href}
                  to={item.href}
                  onClick={() => setIsMobileMenuOpen(false)}
                  className={cn(
                    "flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200",
                    isActive
                      ? "bg-blue-600 text-white"
                      : "text-slate-300 hover:text-white hover:bg-slate-700/50",
                  )}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
            <div className="pt-4 border-t border-slate-700/50">
              <Button
                size="sm"
                className="w-full bg-pink-600 hover:bg-pink-700 text-white"
              >
                Staff Area
              </Button>
            </div>
          </nav>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Background Elements */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl" />
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-green-500/5 rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2" />
      </div>
    </div>
  );
}
