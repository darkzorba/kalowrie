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
