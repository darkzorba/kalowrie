from .ai import AI
import json

from ..base.decorator import Response


class Nutrition(AI):
    GENDER_MAP = {
        'male':'+ 5',
        'female':'- 161',
    }
    ACTIVITY_MAP = {
        'light':1.375,
        'moderate':1.55,
        'high':1.725
    }
    DIET_TYPE_MAP = {
    'mass_gain':0.15,
    'fat_loss':-0.20,
    'maintenance':0
    }
    def __init__(self):
        super().__init__()
        self.get_chat('nutrition-specialist')

    @Response(desc_error="Error generating diet.", return_list=['meals_list'])
    def generate_diet(self,
        activity_frequency: str,
        age: int,
        dietary_preferences: str,
        dietary_restrictions: str,
        eating_routine: str,
        gender: str,
        height: int,
        weight: int,
        diet_type: str) -> list:

        macros_dict = self.get_macros(int(age), gender, int(height), int(weight), activity_frequency, diet_type)

        response = self.chat.send_message(
            f"""
            Total Daily Kcal {macros_dict['total_kcal']}
            Total Daily Protein {macros_dict['protein_g']}
            Total Daily Carbohydrates {macros_dict['carb_g']}
            Total Daily Fat {macros_dict['fat_g']}
    
            Eating Routine: {eating_routine}
            Dietary Preferences: {dietary_preferences}
            Dietary Restrictions: {dietary_restrictions}           
        """
        )
        meals_list = json.loads(response.text.replace('```','').replace('json',''))
        return meals_list

    def get_macros(self, age: int, gender: str, height: int, weight:int, activity_frequency: str, diet_type: str) -> dict:
        tmb = eval(f" (10 * {weight}) + (6.25 * {height}) - (5 * {age}) {self.GENDER_MAP.get(gender, '+ 5')}")
        tmb = tmb * self.ACTIVITY_MAP.get(activity_frequency, 1.2) * (1 + self.DIET_TYPE_MAP.get(diet_type, 0))
        protein_g = 2.2 * weight
        fat_g = tmb * 0.2 / 9
        carb_g = (tmb - (fat_g * 9 + protein_g * 4)) / 4
        return {
            'total_kcal':tmb,
            'protein_g':protein_g,
            'carb_g':carb_g,
            'fat_g':fat_g
        }