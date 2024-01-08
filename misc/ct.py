from aiogram.fsm.state import StatesGroup, State


class CtState(StatesGroup):
    """
    * State for control
    """

    main = State()
