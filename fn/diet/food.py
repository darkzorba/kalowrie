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


    @Response(desc_error="Error creating food.", return_list=['new_food'])
    def create_food(self, name, quantity, carbs_g, proteins_g, fats_g, calories, grams_per_unit):
        food_fields = f"""
        name,
        quantity,
        carbs_g,
        proteins_g,
        fats_g,
        calories,
        grams_per_unit
        """

        dict_food = {
            'name': name,
            'quantity': quantity,
            'carbs_g': carbs_g,
            'proteins_g': proteins_g,
            'fats_g': fats_g,
            'calories': calories,
            'grams_per_unit': grams_per_unit
        }

        new_food_dict = self.save('food_macro',dict_food, returning=food_fields)
        if not new_food_dict:
            return ValidationError('Error creating food.')
        return new_food_dict



    @Response(desc_error="Error fetching categories.", return_list=['categories_list'])
    def get_all_categories(self):
        return self.select(f"""
        select fc.name,
               fc.id
        from public.food_category fc
            where fc.status = true
        """)