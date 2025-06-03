import os
from kalowrie.fn.base.sql import SQLQuery
import google.generativeai as genai
from kalowrie.kalowrie import settings





class AI(SQLQuery):

    def __init__(self):
        super().__init__()
        self.model = None
        self.chat = None


    def get_all_chats(self):
        model = settings.MODEL
        chat_list = self.select("""
        select p.chat_name,
               p.prompt_content
        from public.prompts p 
        where status = true 
        """)
        dict_chats = {}
        for base_chat in chat_list:
            chat = model.start_chat()
            chat.send_message(base_chat['prompt_content'])
            dict_chats[base_chat['chat_name']] = chat
        return dict_chats


    def get_chat(self, chat):
        self.chat = settings.CHATS.get(chat)
        return self.chat

