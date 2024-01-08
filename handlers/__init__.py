from aiogram import Router

# * Import all handlers
from . import control, wd, wd_create, wd_edit, inspector, ct, ct_create, ct_edit

routers = Router(name="all handlers")

routers.include_routers(
    control.router,
    wd.router,
    wd_create.router,
    wd_edit.router,
    ct.router,
    ct_create.router,
    ct_edit.router,
    inspector.router
)