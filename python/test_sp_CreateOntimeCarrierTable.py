import pytest
import pyodbc
from pandas import DataFrame

import DataSetupManager
import SQLTestManager


@pytest.fixture(autouse=True)
def load_data(mssql_conn: pyodbc.Connection):
    data_paths = {
        'ontime_data': '../2016-flights/data/01_joinok/01_ontime_data_joinok.csv',
        'carrier_code': '../2016-flights/data/01_joinok/01_carrier_code_joinok.csv'
    }

    dataSetupManager = DataSetupManager(mssql_conn)
    dataSetupManager.insert_csv_files(data_paths)

    yield
    dataSetupManager.refresh_tables(data_paths.keys())


def test_flight_cancelled(mssql_conn: pyodbc.Connection):
    testManager = SQLTestManager(mssql_conn)

    expected_df = DataFrame.from_dict({
        'year': 2016,
        'month': 1,
        'day_of_month': 1,
        'carrier_code': 'A01',
        'carrier_desc': 'A1 Airlines',
        'flight_number': 11,
        'origin': 'A01',
        'destination': 'A11',
        'arrived_fla': 'Y'
    })

    actual_df = testManager.exec_stored_procedure('sp_CreateOntimeCarrierTable')
    assert(testManager.are_equal(expected_df, actual_df))
