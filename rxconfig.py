import reflex as rx
import os

config = rx.Config(
    app_name="amorty_cafe",
    db_url="sqlite:///reflex.db",  # Will be replaced with Oracle in production
    env=rx.Env.DEV,
    port=3000,
    backend_port=8000,
    frontend_packages=[
        "lucide-react",
        "@radix-ui/themes",
    ],
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "slate": {
                        "50": "#f8fafc",
                        "100": "#f1f5f9",
                        "200": "#e2e8f0",
                        "300": "#cbd5e1",
                        "400": "#94a3b8",
                        "500": "#64748b",
                        "600": "#475569",
                        "700": "#334155",
                        "800": "#1e293b",
                        "900": "#0f172a",
                        "950": "#020617"
                    }
                }
            }
        }
    }
)
