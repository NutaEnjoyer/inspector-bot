from aiogram.types import Message
from aiogram.filters import BaseFilter


class OnlyGroup(BaseFilter):

    def __init__(self) -> None:
        """
        * Default start for new user
        """
        super().__init__()


    async def __call__(self, ctx: Message) -> bool:
        return ctx.chat.type in ["group", "supergroup"]