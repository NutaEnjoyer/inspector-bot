from aiogram.types import Message


def get_name(ctx : Message):
    """Get name/fullname from Message"""

    if not ctx.from_user.last_name:
        return ctx.from_user.full_name
    return f"{ctx.from_user.first_name, ctx.from_user.last_name}"


def get_user(ctx : Message):
    """Get user from Message"""

    if username:=ctx.from_user.username:
        return f"@{username}"
    
    return f'<a href="tg://user?id={ctx.from_user.id}">{get_name(ctx)}</a>'
    
