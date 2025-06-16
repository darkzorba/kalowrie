from fn.base.decorator import Response
from fn.base.sql import SQLQuery


class Meal(SQLQuery):
    def __init__(self, user_id, diet_id):
        super().__init__()
        self.user_id = user_id
        self.diet_id = diet_id

    @Response(desc_error="Error saving meal.", return_list=[])
    def save_meal(self, name, meal_time, meal_date, total_kcals, total_proteins, total_carbs, total_fats,
                  list_ingredients):
        dict_meal = {
            'name': name,
            'time': meal_time,
            'date': meal_date,
            'calories': total_kcals,
            'proteins_gr': total_proteins,
            'fats_gr': total_fats,
            'carbs_gr': total_carbs,
            'user_id': self.user_id,
        }
        meal_id = self.save(table_name="public.user_meal",dict_save=dict_meal)

        list_insert_ingredients = []
        for ingredient in list_ingredients:
            list_insert_ingredients.append({
                'meal_id': meal_id,
                'quantity': ingredient['quantity'],
                'unit': ingredient['default_unit'],
                'name': ingredient['name'],

            })

        self.bulk_insert('public.user_mealingredient', list_insert_ingredients)

        dict_progress = self.select(f"""
        select udp.id,
               udp.total_kcals::float,
               udp.total_proteins::float,
               udp.total_carbs::float,
               udp.total_fats::float,
               udp.diet_id,
               ud.carbs_g as carbs_goal,
               ud.fats_g as fats_goal,
               ud.proteins_g as proteins_goal,
               ud.total_kcals as kcals_goal
        from public.user_dailyprogress udp
            join public.user_diet ud 
                on ud.id = udp.diet_id  
        where udp.date = :date
              and udp.user_id = :user_id
              and udp.status = true
              and udp.diet_id = :diet_id
        """,parameters=dict(date=meal_date, user_id=self.user_id, diet_id=self.diet_id), is_first=True)
        if not dict_progress:
            dict_progress = {
                'total_kcals': 0,
                'total_proteins': 0,
                'total_carbs': 0,
                'total_fats': 0,
            }
        dict_progress['total_kcals'] += total_kcals
        dict_progress['total_proteins'] += total_proteins
        dict_progress['total_carbs'] += total_carbs
        dict_progress['total_fats'] += total_fats
        dict_progress['date'] = meal_date
        dict_progress['user_id'] = self.user_id
        dict_progress['diet_id'] = self.diet_id

        self.save(table_name="public.user_dailyprogress",dict_save=dict_progress)