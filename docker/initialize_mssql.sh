#!/bin/bash
password=ITsC0mpl1cat3d

echo Setting up MSSQL Server Databases...

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $password -i ./docker/init_databases.sql
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $password -i ./docker/carrier_code.sql -v db_name=dev
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $password -i ./docker/ontime_data.sql -v db_name=dev
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $password -i ./docker/carrier_code.sql -v db_name=prod
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $password -i ./docker/ontime_data.sql -v db_name=prod
