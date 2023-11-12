from typing import List
from aiogram.types import Message
from aiogram.filters import BaseFilter

from ..pd import PandasDatabase
from ..table import UserStatus


class OnlyUser(BaseFilter):

    def __init__(self, pd : PandasDatabase) -> None:
        """
        * Default start for new user
        """
        super().__init__()

        self.table = pd.get_table("user")

    async def __call__(self, ctx: Message) -> bool:
        try:
            return self.table.at[ctx.from_user.id, "status"] == UserStatus.ADMIN.value
        
        except KeyError:
            return False