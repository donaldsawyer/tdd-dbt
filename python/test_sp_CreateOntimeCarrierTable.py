import pytest
import pyodbc
import pandas as pd

import DataManager as dm
import SQLTestManager as tm

base_query = 'SELECT * FROM dbo.ontime_denorm'


@pytest.fixture(autouse=True)
def reset_data(mssql_conn: pyodbc.Connection):
    data_manager = dm.DataManager(mssql_conn)
    yield
    data_manager.refresh_tables(['ontime_denorm', 'carrier_code', 'ontime_data'])


def test_flight_cancelled(mssql_conn: pyodbc.Connection):
    data_paths = {
        'ontime_data': '2016-flights/data/01_joinok/01_ontime_data_joinok.csv',
        'carrier_code': '2016-flights/data/01_joinok/01_carrier_code_joinok.csv'
    }
    data_manager = dm.DataManager(mssql_conn)
    data_manager.insert_csv_files(data_paths)

    test_manager = tm.SQLTestManager(mssql_conn, base_query)
    expected_df = pd.DataFrame.from_dict({
        'year': [2016],
        'month': [1],
        'day_of_month': [1],
        'carrier_code': ['A01'],
        'carrier_desc': ['A1 Airlines'],
        'flight_number': [11],
        'origin': ['A01'],
        'destination': ['A11'],
        'arrived_flag': ['Y']
    })

    test_manager.exec_stored_procedure('sp_CreateOntimeCarrierTable')
    actual_df = test_manager.exec_query()
    assert(test_manager.are_equal(expected_df, actual_df, 'carrier_code'))

def test_flight_unknown(mssql_conn: pyodbc.Connection):
    data_paths = {
        'ontime_data': '2016-flights/data/02_joinunknown/02_ontime_data_joinunknown.csv',
        'carrier_code': '2016-flights/data/02_joinunknown/02_carrier_code_joinunknown.csv'
    }
    data_manager = dm.DataManager(mssql_conn)
    data_manager.insert_csv_files(data_paths)

    test_manager = tm.SQLTestManager(mssql_conn, base_query)
    expected_df = pd.DataFrame.from_dict({
        'year': [2016],
        'month': [1],
        'day_of_month': [1],
        'carrier_code': ['A01'],
        'carrier_desc': ['UNKNOWN'],
        'flight_number': [11],
        'origin': ['A01'],
        'destination': ['A11'],
        'arrived_flag': ['Y']
    })

    test_manager.exec_stored_procedure('sp_CreateOntimeCarrierTable')
    actual_df = test_manager.exec_query()
    assert(test_manager.are_equal(expected_df, actual_df, 'carrier_code'))

def test_flight_combined(mssql_conn: pyodbc.Connection):
    data_paths = {
        'ontime_data': '2016-flights/data/03_joincombined/03_ontime_data_joincombined.csv',
        'carrier_code': '2016-flights/data/03_joincombined/03_carrier_code_joincombined.csv'
    }
    data_manager = dm.DataManager(mssql_conn)
    data_manager.insert_csv_files(data_paths)

    test_manager = tm.SQLTestManager(mssql_conn, base_query)
    expected_df = pd.DataFrame.from_dict({
        'year': [2016, 2016],
        'month': [1, 1],
        'day_of_month': [1, 1],
        'carrier_code': ['A01', 'A02'],
        'carrier_desc': ['A1 Airlines', 'UNKNOWN'],
        'flight_number': [11, 11],
        'origin': ['A01', 'A01'],
        'destination': ['A11', 'A11'],
        'arrived_flag': ['Y', 'Y']
    })

    test_manager.exec_stored_procedure('sp_CreateOntimeCarrierTable')
    actual_df = test_manager.exec_query()
    assert(test_manager.are_equal(expected_df, actual_df, 'carrier_code'))

def test_arrived_flag(mssql_conn: pyodbc.Connection):
    data_paths = {
        'ontime_data': '2016-flights/data/04_arrived_flag/04_ontime_data_arrived_flag.csv',
        'carrier_code': '2016-flights/data/04_arrived_flag/04_carrier_code_arrived_flag.csv'
    }
    data_manager = dm.DataManager(mssql_conn)
    data_manager.insert_csv_files(data_paths)

    test_manager = tm.SQLTestManager(mssql_conn, base_query)
    expected_df = pd.DataFrame.from_dict({
        'year': [2016, 2016, 2016, 2016, 2016, 2016, 2016, 2016],
        'month': [1, 1, 1, 1, 1, 1, 1, 1],
        'day_of_month': [1, 1, 1, 1, 1, 1, 1, 1],
        'carrier_code': ['A01', 'A02', 'A02', 'A02', 'A02', 'A02', 'A02', 'A03'],
        'carrier_desc': ['Arrived Airlines', "Didn't Arrive Airlines", "Didn't Arrive Airlines", "Didn't Arrive Airlines", "Didn't Arrive Airlines", "Didn't Arrive Airlines", "Didn't Arrive Airlines", "Arrival Unsure Airlines"],
        'flight_number': [11, 11, 11, 11, 11, 11, 11, 11],
        'origin': ['A01', 'A01', 'A01', 'A01', 'A01', 'A01', 'A01', 'A01'],
        'destination': ['A11', 'A11', 'A11', 'A11', 'A11', 'A11', 'A11', 'A11'],
        'arrived_flag': ['Y', 'N', 'N', 'N', 'N', 'N', 'N', None]
    })

    test_manager.exec_stored_procedure('sp_CreateOntimeCarrierTable')
    actual_df = test_manager.exec_query()
    assert(test_manager.are_equal(expected_df, actual_df, 'carrier_code'))