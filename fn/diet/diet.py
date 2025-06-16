from ..base.decorator import Response
from ..base.exception import ValidationError
from ..base.sql import SQLQuery
import json




class Diet(SQLQuery):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @Response(desc_error="Error saving diet.", return_list=['diet_id'])
    def save_diet(self, diet_dict):
        dict_object = {
            "user_id": self.user_id,
            "diet_json":json.dumps(diet_dict),
            'total_kcals':diet_dict['total_kcal'],
            'proteins_g':diet_dict['total_protein'],
            'carbs_g':diet_dict['total_carb'],
            'fats_g':diet_dict['total_fat'],
            'status':True
        }
        diet_id = self.save('user_diet', dict_object)
        if not diet_id:
            return ValidationError("Error saving diet.")
        self.update('public.user',{'is_first_access':False},{'id':self.user_id})
        return diet_id


    @Response(desc_error="Error fetching cards.", return_list=['cards_dict'])
    def get_progress_cards(self, date):
        query = f"""
        select udp.total_proteins,
               udp.total_kcals,
               udp.total_carbs,
               udp.total_fats,
               ud.total_kcals as kcals_goal,
               ud.fats_g as fats_goal,
               ud.proteins_g as proteins_goal,
               ud.carbs_g as carbs_goal
        from public.user_diet ud 
        left join public.user_dailyprogress udp 
            on udp.diet_id = ud.id 
            and udp.status = true
            and udp.date = :date 
        where ud.status = true
              and ud.user_id = :user_id 
        """

        return self.select(query,parameters=dict(user_id=self.user_id, date=date),is_first=True)

    @Response(desc_error="Error fetching diet.", return_list=['diet_dict'])
    def get_user_diet(self):
        return self.select("""
        select ud.diet_json 
        from public.user_diet ud 
            where ud.user_id = :user_id
            and ud.status = true
        """, parameters=dict(user_id=self.user_id), is_first=True, is_values_list=True)


    @Response(desc_error="Error fetching graphics.", return_list=['graphics_list'])
    def get_progress_graphics(self, date):
        query = f"""
        select udp.date,
               round(udp.total_proteins / udp.proteins_goal * 100,2) as proteins_perc,
               round(udp.total_carbs / udp.carbs_goal * 100,2) as carbs_perc,
               round(udp.total_fats / udp.fats_goal * 100,2) as fats_perc,
               round(udp.total_kcals / udp.kcals_goal * 100,2) as kcal_perc
        from public.user_dailyprogress udp
            where udp.user_id = :user_id
                  and udp.status = true
                  and udp.date >= (to_date(:date,'yyyy-mm-dd') - interval '7 days')
        """
        return self.select(query,parameters=dict(user_id=self.user_id,date=date))

    @Response(desc_error="Error saving diet.", return_list=['diet_id'])
    def create_diet(self, meals_list, total_carbs, total_proteins, total_fats, total_calories):
        dict_diet = {
            'user_id': self.user_id,
            'total_kcals': total_calories,
            'carbs_g': total_carbs,
            'proteins_g': total_proteins,
            'fats_g': total_fats,
            'diet_json':self.build_json(meals_list=meals_list,total_carbs=total_carbs,total_proteins=total_proteins,
                                        total_fats=total_fats,total_kcals=total_calories)
        }
        diet_id = self.save('user_diet', dict_diet)
        if not diet_id:
            return ValidationError("Error saving diet.")

        self.save_meals(meals_list, diet_id)

        self.update('public.user',{'is_first_access':False},{'id':self.user_id})

        return diet_id

    def save_meals(self, meals_list, diet_id):
        if not meals_list:
            return

        meals_to_insert = [{
            'name': meal['name'],
            'time': meal['time'],
            'total_proteins': meal['total_proteins'],
            'total_carbs': meal['total_carbs'],
            'total_fats': meal['total_fats'],
            'total_calories': meal['total_calories'],
            'diet_id': diet_id,
        } for meal in meals_list]

        inserted_meal_ids = self.bulk_insert('user_dietmeal', meals_to_insert)


        all_components_to_insert = []


        temp_relations_map = []
        current_component_index = 0

        for meal, meal_id in zip(meals_list, inserted_meal_ids):
            for ingredient in meal['ingredients']:
                all_components_to_insert.append({
                    'diet_meal_id': meal_id,
                    'name': ingredient['name'],
                    'total_proteins': ingredient['total_proteins'],
                    'total_fats': ingredient['total_fats'],
                    'total_carbs': ingredient['total_carbs'],
                    'quantity': ingredient['quantity'],
                    'unit': ingredient['unit']
                })
                ingredient_temp_index = current_component_index
                current_component_index += 1

                for substitute in ingredient['substitutes']:
                    all_components_to_insert.append({
                        'diet_meal_id': meal_id,
                        'name': substitute['name'],
                        'total_proteins': substitute['total_proteins'],
                        'total_fats': substitute['total_fats'],
                        'total_carbs': substitute['total_carbs'],
                        'quantity': substitute['quantity'],
                        'unit': substitute['unit']
                    })
                    substitute_temp_index = current_component_index

                    temp_relations_map.append({
                        'original_index': ingredient_temp_index,
                        'substitute_index': substitute_temp_index
                    })
                    current_component_index += 1

        if not all_components_to_insert:
            return

        inserted_component_ids = self.bulk_insert('user_diet_mealcomponent', all_components_to_insert)

        relations_to_insert = [{
            'meal_component_id': inserted_component_ids[rel['original_index']],
            'substitution_id': inserted_component_ids[rel['substitute_index']]
        } for rel in temp_relations_map]

        if relations_to_insert:
            self.bulk_insert('meal_component_substitution', relations_to_insert)


    def build_json(self, meals_list, total_carbs, total_kcals, total_fats, total_proteins):
        return json.dumps({
            'carbs_g': total_carbs,
            'total_kcals': total_kcals,
            'fats_g': total_fats,
            'proteins_g': total_proteins,
            'meals': meals_list,
        })