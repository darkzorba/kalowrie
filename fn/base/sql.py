
import os
import sqlalchemy as db
from kalowrie.settings import SQL_CONFIG
from django.utils import timezone

class SQLQuery:
    def __init__(self):

        self.resultset = []

        self.engine = SQL_CONFIG['engine']




    def __query(self, query=None, parameters=None, is_serialized=True):
            if parameters is None:
                parameters = {}

            self.parse_list_to_tuple(parameters)

            # self.engine.dispose()
            with self.engine.begin() as conn:
                text = db.text(query)
                self.resultset = conn.execute(text, parameters)

            if self.resultset.returns_rows:
                return list(self.resultset) if not is_serialized else self.get_serialized_data()
            else:
                return None


    @staticmethod
    def parse_list_to_tuple(parameters):
        for p in parameters:
            if isinstance(parameters[p], (list, set)):
                if len(parameters[p]) > 0:
                    parameters[p] = tuple(parameters[p])
                else:
                    parameters[p] = tuple([None])

            elif isinstance(parameters[p], tuple):
                if len(parameters[p]) < 0:
                    parameters[p] = tuple([None])

    def get_serialized_data(self):
        return [row._asdict() for row in self.resultset]


    def update(self, table_name, dict_update, dict_filter, pk_name='id', is_disable=False, is_values_list=False,
               is_first=True):



        columns_list = dict_update.keys()

        update = ','.join([f'{column} = :{column}' for column in columns_list])

        where = ''
        for key, value in dict_filter.items():
            if isinstance(value, list):
                where += f" {key} in :{key} and"
            else:
                where += f" {key} = :{key} and"

        where = where[:-3]  # Removing the last 'and'

        query = f'update {table_name} set {update} where {where} returning {pk_name};'

        dict_update.update(dict_filter)

        result = self.__query(query=query, parameters=dict_update)

        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)


    @staticmethod
    def format_result(result=None, is_values_list=False, is_first=False):
        if not result:
            return {} if is_first else []

        if is_values_list:
            return_list = []
            for row in result:

                values = tuple(row.values())
                if len(values) == 1:
                    return_list.append(values[0])
                else:
                    return_list.append(values)

            result = return_list

        if is_first:
            return result[0]

        return result

    def select(self,query:str,parameters:dict={},is_values_list:bool=False,is_first:bool=False):

        result = self.__query(query=query,parameters=parameters,is_serialized=True)

        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)

    def save(self, table_name, dict_save, pk_name='id', is_values_list=True, is_first=True):

        dict_save = self.__build_log(dict_save, log_type='save')
        columns_list = dict_save.keys()

        columns = ','.join(columns_list)
        values_name = ','.join([f':{column}' for column in columns_list])
        update = ','.join([f'{column} = :{column}' for column in columns_list])

        query = f"""
            insert into {table_name}({columns}) values ({values_name}) 
            on conflict ({pk_name}) do update set {update} RETURNING {pk_name};
        """

        result = self.__query(query=query, parameters=dict_save)

        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)


    def __build_log(self, dict_object, log_type):
        mapper_dict = {
            'save':'datm_update',
            'insert':'datm_insert',
            'update':'datm_update',
            'delete':'datm_delete',
        }
        datm_col = mapper_dict[log_type]
        if datm_col == 'datm_update' and 'id' not in dict_object:
            datm_col = 'datm_insert'
        if 'status' not in dict_object:
            dict_object['status'] = True if log_type != 'delete' else False
        dict_object[datm_col] = timezone.now()
        return dict_object

    def bulk_insert(self, table_name, list_dict_insert, pk_name='id', is_values_list=True, is_first=False,returning=None):
        if not list_dict_insert:
            return None

        if not returning:
            returning = pk_name


        columns = ''
        values = ''
        parameters = {}
        for count, dict_insert in enumerate(list_dict_insert):
            dict_insert = self.__build_log(dict_object=dict_insert, log_type='insert')

            if not columns:
                columns = ','.join(dict_insert.keys())

            values_name = ''
            for chave, valor in dict_insert.items():
                parameters[f"{chave}_{count}"] = valor
                values_name += f" :{chave}_{count},"
            values_name = values_name[:-1]

            values += f"({values_name}),"
        values = values[:-1]

        query = f'insert into {table_name}({columns}) values {values} RETURNING {returning};'

        result = self.__query(query=query, parameters=parameters)

        return self.format_result(result=result, is_values_list=is_values_list, is_first=is_first)