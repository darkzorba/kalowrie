import google.generativeai as genai
import json
from PIL import Image
from .ai import AI

class CalorieTracker(AI):
    def __init__(self):
        super().__init__()
        self.get_chat('calorie-tracker')

    def get_calories_by_img(self, img: str):
        """
        :param img: path of the picture of the dish, used to estimate the meal and its macro-nutrients
        :return: json with the macro-nutrients of the dish in the picture
        """
        img = Image.open(img)
        response = self.model.generate_content([img])
        json_macro = json.loads(response.text.replace('```', '').replace('json', ''))

        return json_macro
