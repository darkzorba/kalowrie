from .ai import AI
import json




class Nutrition(AI):
    def __init__(self):
        super().__init__()
        self.get_chat('nutrition-specialist')


    def generate_diet(self, weight, weight_type, height, height_type, age, gender, questions ):
        response = self.chat.send_message(
            f"""
            Here's my infos:
            Weight {weight} {weight_type},
            Height {height} {height_type},
            Age {age},
            Gender {gender}
            
            {questions}
            """
        )
        list_meals = json.loads(response.text.replace('```','').replace('json',''))
        return list_meals
