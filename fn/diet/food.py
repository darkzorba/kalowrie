from fn.base.decorator import Response
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
               fc.name as category_name
        from public.food_macro f 
            left join public.food_category fc
                on fc.id = f.category_id
                and fc.status = true 
        where f.status = true
        """)