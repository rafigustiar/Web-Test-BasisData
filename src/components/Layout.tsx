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
  Bell,
  Settings,
} from "lucide-react";
import { useState } from "react";

interface LayoutProps {
  children: ReactNode;
}

const navigationItems = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard, group: "main" },
  { href: "/customers", label: "Customers", icon: Users, group: "management" },
  { href: "/employees", label: "Staff", icon: UserCheck, group: "management" },
  { href: "/menu", label: "Menu", icon: Coffee, group: "operations" },
  { href: "/orders", label: "Orders", icon: ShoppingCart, group: "operations" },
  {
    href: "/payments",
    label: "Payments",
    icon: CreditCard,
    group: "operations",
  },
  {
    href: "/reservations",
    label: "Reservations",
    icon: Calendar,
    group: "billiard",
  },
  { href: "/rentals", label: "Rentals", icon: Receipt, group: "billiard" },
  { href: "/tables", label: "Tables", icon: CircleDot, group: "billiard" },
];

export function Layout({ children }: LayoutProps) {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-black/30 backdrop-blur-lg border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo Section - Enhanced */}
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div
                  className="w-10 h-10 rounded-xl shadow-lg bg-no-repeat bg-center bg-cover"
                  style={{
                    backgroundImage:
                      "url(https://cdn.builder.io/api/v1/image/assets%2F420a2dccf542446cabbce903b3e093cd%2F595bdb5ec74c409aba04ec2433147a93)",
                  }}
                />
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-slate-900"></div>
              </div>
              <div className="flex flex-col">
                <h1 className="text-xl font-bold text-white tracking-tight">
                  Amorty
                </h1>
                <p className="text-xs text-slate-400 font-medium tracking-wider">
                  BILLIARDS & CAFE
                </p>
              </div>
            </div>

            {/* Desktop Navigation - Improved */}
            <nav className="hidden lg:flex items-center space-x-1">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    to={item.href}
                    className={cn(
                      "relative flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 group",
                      isActive
                        ? "bg-blue-600/90 text-white shadow-lg shadow-blue-600/25"
                        : "text-slate-300 hover:text-white hover:bg-slate-700/60",
                    )}
                  >
                    <Icon
                      className={cn(
                        "w-4 h-4 transition-transform duration-200",
                        isActive ? "scale-110" : "group-hover:scale-105",
                      )}
                    />
                    <span className="hidden xl:inline">{item.label}</span>
                    {isActive && (
                      <div className="absolute inset-0 bg-blue-600/20 rounded-lg blur-sm -z-10"></div>
                    )}
                  </Link>
                );
              })}
            </nav>

            {/* Right Side Actions - Enhanced */}
            <div className="hidden lg:flex items-center space-x-3">
              <Button
                variant="ghost"
                size="sm"
                className="text-slate-400 hover:text-white hover:bg-slate-700/50 relative"
              >
                <Bell className="w-4 h-4" />
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </Button>

              <Button
                variant="ghost"
                size="sm"
                className="text-slate-400 hover:text-white hover:bg-slate-700/50"
              >
                <Settings className="w-4 h-4" />
              </Button>

              <div className="w-px h-6 bg-slate-600"></div>

              <div className="flex items-center space-x-2 text-xs text-slate-400">
                <span>Tel:</span>
                <span className="text-slate-300">(0341) 487789</span>
              </div>

              <Button
                size="sm"
                className="bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-700 hover:to-pink-800 text-white shadow-lg hover:shadow-pink-600/25 transition-all duration-200"
              >
                Staff Area
              </Button>
            </div>

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden text-white hover:bg-slate-700/50"
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

      {/* Mobile Navigation - Improved */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-black/40 backdrop-blur-lg border-b border-slate-700/50">
          <nav className="max-w-7xl mx-auto px-4 py-4">
            <div className="grid grid-cols-2 gap-2 mb-4">
              {navigationItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    to={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={cn(
                      "flex items-center space-x-3 px-3 py-3 rounded-lg text-sm font-medium transition-all duration-200",
                      isActive
                        ? "bg-blue-600/90 text-white shadow-lg"
                        : "text-slate-300 hover:text-white hover:bg-slate-700/60",
                    )}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </div>

            {/* Mobile Actions */}
            <div className="pt-4 border-t border-slate-700/50 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  Tel: (0341) 487789
                </span>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-slate-400 hover:text-white"
                  >
                    <Bell className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-slate-400 hover:text-white"
                  >
                    <Settings className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              <Button
                size="sm"
                className="w-full bg-gradient-to-r from-pink-600 to-pink-700 hover:from-pink-700 hover:to-pink-800 text-white"
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

      {/* Enhanced Background Elements */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/3 rounded-full blur-3xl animate-pulse" />
        <div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/3 rounded-full blur-3xl animate-pulse"
          style={{ animationDelay: "1s" }}
        />
        <div
          className="absolute top-1/2 left-1/2 w-96 h-96 bg-green-500/2 rounded-full blur-3xl transform -translate-x-1/2 -translate-y-1/2 animate-pulse"
          style={{ animationDelay: "2s" }}
        />
      </div>
    </div>
  );
}
