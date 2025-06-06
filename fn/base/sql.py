
import os
import sqlalchemy as db
from kalowrie.settings import SQL_CONFIG

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
