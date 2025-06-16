from fn.base.decorator import Response
from fn.base.exception import ValidationError
from fn.base.sql import SQLQuery



class Food(SQLQuery):
    def __init__(self):
        super().__init__()

    @Response(desc_error="Error searching foods.", return_list=['foods_list'])
    def get_all_foods(self):
        return self.select(f"""
        select f.name,
               f.quantity,
               f.carbs_g,
               f.proteins_g,
               f.fats_g,
               f.calories,
               f.grams_per_unit,
               fc.name as category_name
        from public.food_macro f 
            left join public.food_category fc
                on fc.id = f.category_id
                and fc.status = true 
        where f.status = true
        """)


    @Response(desc_error="Error creating food.", return_list=['foods_list'])
    def create_food(self, name, quantity, carbs_g, proteins_g, fats_g, calories, grams_per_unit):
        dict_food = {
            'name': name,
            'quantity': quantity,
            'carbs_g': carbs_g,
            'proteins_g': proteins_g,
            'fats_g': fats_g,
            'calories': calories,
            'grams_per_unit': grams_per_unit
        }

        food_id = self.save('food_macro',dict_food)
        if not food_id:
            return ValidationError('Error creating food.')
        return food_id