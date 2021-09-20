import os
import csv
import pyodbc
from pandas import Dataframe


class DataManager:
    def __init__(self, connection: pyodbc.Connection):
        self.connection = connection

    def _create_query(cursor: pyodbc.Cursor, table_name: str, drop_identity_column):
        resp = cursor.execute(f"SELECT column_name, "
                              f"COLUMNPROPERTY(OBJECT_ID({os.environ['db']}.{table_name}), COLUMN_NAME, 'IsIdentity') "
                              f"from information_schema.Columns"
        )

        query = f"INSERT INTO {table_name} VALUES("
        for i in resp.fetchall():
            if drop_identity_column & i[1] == 1:
                continue
            query = query + '?, '
        return query.rstrip(', ') + ')'

    def _load_csv(self, path):
        with open(path, 'r') as file:
            row_iterator = csv.reader(file)
            next(row_iterator) #skipping the header
            rows = [row for row in row_iterator]
        return self._set_nulls_to_none(rows)

    @staticmethod
    def _set_nulls_to_none(rows):
        updated_rows = []
        for row in rows:
            for i in row:
                if type(i) is str and i.upper() == 'NULL':
                    updated_rows.append(None)
                else:
                    updated_rows.append(row)
        return updated_rows

    def insert_csv(self, table_name, path):
        cursor = self.connection.cursor()
        query = self._create_query(cursor, table_name)
        rows = self._load_csv(path)

        try:
            cursor.executemany(query, rows)
        except pyodbc.Error as err:
            print(f"Failed to insert values into the {table_name} table: \n" + str(err), file=sys.stderr)
        cursor.commit()
        cursor.close()
        return

    def insert_csv_files(self, connection: pyodbc.Connection, csv_paths: dict = {}):
        for table_name, csv_path in csv_paths.items():
            self.insert_csv(connection, table_name, csv_path)
        return

    def refresh_tables(self, tables: list):
        for table_name in tables:
            self.refresh_table(table_name)
        return

    def refresh_table(self, table_name: str):
        cursor = self.connection.cursor()
        query = f"DELETE FROM {os.environ['db']}.{table_name}"
        cursor.execute(query)
        reset_identity = f"DBCC CHECKIDENT ('{table_name}, RESEED, 0')"
        try:
            cursor.execute(reset_identity)
        except:
            pass
        cursor.commit()
        cursor.close()
        return

    @staticmethod
    def are_equal(df1: Dataframe, df2: Dataframe, sort_by, recast={}, replace_blank_strings=False):
        if replace_blank_strings:
            df1 = df1.replace([''], [None])
            df2 = df2.replace([''], [None])

        if sort_by:
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
                if df1[col].dtype != df2.dtype:
                    type_conflict.append(col)

                if not df1[col].equals(df2[col]):
                    cols.append(col)

            error = f'The following columns are not equal: {", ".join(cols)} \n'
            if type_conflict:
                error = error + f'The following columns do not share the same data type: {", ".join(type_conflict)}'

            raise AssertionError(error)

        return True
