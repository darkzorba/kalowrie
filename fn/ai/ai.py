import os
from fn.base.sql import SQLQuery
import google.generativeai as genai
from kalowrie import settings
from core.ai.services import get_chat





class AI(SQLQuery):

    def __init__(self):
        super().__init__()
        self.model = None
        self.chat = None



    def get_chat(self, chat):
        self.chat = get_chat(chat)
        return self.chat

