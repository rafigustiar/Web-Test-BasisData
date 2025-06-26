import reflex as rx
import os

config = rx.Config(
    app_name="amorty_cafe",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
