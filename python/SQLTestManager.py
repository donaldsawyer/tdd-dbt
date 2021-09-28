import pyodbc
import pandas as pd


class SQLTestManager:
    def __init__(self, connection: pyodbc.Connection, base_query=''):
        self.connection = connection
        self.base_query = base_query

    def exec_stored_procedure(self, name: str, params={}):
        cursor = self.connection.cursor()
        query = f"exec {name}"
        if not params:
            cursor.execute(query)
        else:
            for k, v in params.items():
                query = query + f" @{k} = '{v}',"

            query.rstrip(',')
            cursor.execute(query)

        cursor.commit()
        cursor.close()
        return

    def exec_query(self, filters={}):
        query = self.base_query
        if not filters:
            df = pd.read_sql(query, self.connection)
        else:
            query = query + " WHERE "
            for k, v in filters.items():
                key = k
                value = v
                operator = '='
                if type(v) is dict:
                    value = v['value']
                    operator = v['operator']
                else:
                    value = f"'{value}'"
                query = query + f" {key} {operator} {value} AND"
            query = query.rstrip(' AND')
            df = pd.read_sql(query, self.connection)
        return df

    @staticmethod
    def are_equal(df1: pd.DataFrame, df2: pd.DataFrame, sort_by, replace_blank_strings=False):
        if replace_blank_strings:
            df1 = df1.replace([''], [None])
            df2 = df2.replace([''], [None])

        if type(sort_by) is str:
            sort_by = [sort_by]
        df1 = df1.sort_values(by=sort_by)
        df2 = df2.sort_values(by=sort_by)

        df1 = df1.reindex(sorted(df1.columns), axis=1)
        df2 = df2.reindex(sorted(df2.columns), axis=1)
        df1.reset_index(drop=True, inplace=True)
        df2.reset_index(drop=True, inplace=True)

        if not df1.equals(df2):
            cols = []
            type_conflict = []
            for col in df1.columns:
                if df1[col].dtype != df2[col].dtype:
                    type_conflict.append(col)

                if not df1[col].equals(df2[col]):
                    cols.append(col)

            error = f'The following columns are not equal: {", ".join(cols)} \n'
            if type_conflict:
                error = error + f'The following columns do not share the same data type: {", ".join(type_conflict)}'

            raise AssertionError(error)

        return True