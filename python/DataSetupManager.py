import os
import csv
import pyodbc


class DataSetupManager:
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


