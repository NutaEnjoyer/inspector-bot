from aiogram import Router

# * Import all handlers
from . import control, wd, wd_create, wd_edit, inspector

routers = Router(name="all handlers")

routers.include_routers(
    control.router,
    wd.router,
    wd_create.router,
    wd_edit.router,
    inspector.router
)