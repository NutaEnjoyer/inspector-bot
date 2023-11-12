from aiogram.filters import BaseFilter
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


class Button(BaseFilter):

    def __init__(self, button : KeyboardButton) -> None:
        """
        * Call when the button was pressed by user
        """
        super().__init__()

        self.button = button

    async def __call__(self, ctx: Message) -> bool:
        return ctx.text == self.button.text
    

class InlineButton(BaseFilter):

    def __init__(self, button : InlineKeyboardButton) -> None:
        """
        * Default start for new user
        """
        super().__init__()

        self.button = button

    async def __call__(self, callbac_data: CallbackQuery) -> bool:
        return callbac_data.data == self.button.callback_data
    

class OR_STATE(BaseFilter):

    def __init__(self, *args : State) -> None:
        """
        * Default start for new user
        """
        super().__init__()

        self.states = args

    async def __call__(self, ctx: Message, state: FSMContext) -> bool:

        user_state = await state.get_state()

        for _state in self.states:

            if _state.state != user_state:
                continue

            return True

        return False