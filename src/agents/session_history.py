from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory
)

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    get or create session history
    :param session_id:
    :return: BaseChatMessageHistory
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]