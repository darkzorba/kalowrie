from kalowrie import settings
from fn.base.sql import SQLQuery

_cached_chats = None


def get_all_chats():
    global _cached_chats

    if _cached_chats:
        return _cached_chats
    model = settings.MODEL
    chat_list = SQLQuery().select("""
                            select p.chat_name,
                                   p.base_prompt
                            from public.ai_roles p
                            where status = true
                            """)
    dict_chats = {}
    for base_chat in chat_list:
        chat = model.start_chat()
        chat.send_message(base_chat['base_prompt'])
        dict_chats[base_chat['chat_name']] = chat
    _cached_chats = dict_chats
    return _cached_chats


def get_chat(chat_name):
    return _cached_chats.get(chat_name) if _cached_chats else None