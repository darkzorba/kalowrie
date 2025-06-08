import json
from PIL import Image
from .ai import AI
from ..base.decorator import Response


class CalorieTracker(AI):
    def __init__(self):
        super().__init__()
        self.get_chat('calorie-tracker')

    @Response(desc_error="Error Tracking Macros.", return_list=['macros_dict'])
    def track_macros(self, list_ingredients, name, amount, food_img):
        if food_img:
            img = Image.open(food_img)
            response = self.chat.send_message(img)
        else:
            str_ingredients = ""
            for ingredient in list_ingredients:
                str_ingredients += f"""
                Ingredient Name: {ingredient['name']}
                Ingredient Quantity: {ingredient['quantity']}
                Quantity Unit: {ingredient['default_unit']}
                """
            response = self.chat.send_message(f"""
            Meal Name: {name}
            Total Meal Amount: {amount}
            
            Ingredients:
            {str_ingredients}
            """)
        macros_dict = json.loads(response.text.replace('```','').replace('json',''))

        return macros_dict

