from aiogram.fsm.state import StatesGroup, State



class WdCreateState(StatesGroup):
    """
    * State for creating 
    """

    name = State()
    message = State()
    words = State()


cancel_by_state = {
    WdCreateState.name.state : None,
    WdCreateState.message.state : WdCreateState.name,
    WdCreateState.words.state : WdCreateState.message  
}


state_by_state = {
    WdCreateState.name.state : WdCreateState.message,
    WdCreateState.message.state : WdCreateState.words,
    WdCreateState.words.state : None
}


args_by_state = {
    WdCreateState.name.state : "wd_create_name",
    WdCreateState.message.state : "wd_create_message",
    WdCreateState.words.state : "wd_create_words"
}