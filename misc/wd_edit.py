from aiogram.fsm.state import StatesGroup, State


class WdEditState(StatesGroup):
    """
    * State for editing 
    """

    main = State()
    name = State()
    message = State()
    words_add = State()
    words_remove = State()