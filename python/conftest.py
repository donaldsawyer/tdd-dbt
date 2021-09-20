import os
import pytest
import pyodbc
import subprocess


def pytest_sessionstart():
    print('Setting up databases')
    subprocess.run(f'../docker/initialize_mssql.sh', shell=True)
    return


@pytest.fixture(scope="session")
def mssql_conn(pytestconfig):
    '''
        Creates a connection to a local MSSQL instance available to all tests in a session.
        Requires the following environment variables:
            db - Name of database to connect to
            pwd - Password for the superadmin user
    '''
    if 'db' not in os.environ or 'pwd' not in os.environ:
        raise NameError('db and pwd environment variables required for local MSSQL connection')
    mssql_conn = pyodbc.connect(driver="ODBC Driver 17 for SQL Server",
                                server='0.0.0.0,1433',
                                database=f'{os.environ["db"]}',
                                UID='SA',
                                PWD=f'{os.environ["pwd"]}'
                                )
    yield mssql_conn
