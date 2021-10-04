#!/bin/bash
password=ITsC0mpl1cat3d

echo Setting up MSSQL Server Databases...

/usr/local/bin/sqlcmd -S 0.0.0.0,1433 -U sa -P $password -i ../docker/init_databases.sql
/usr/local/bin/sqlcmd -S 0.0.0.0,1433 -U sa -P $password -i ../docker/carrier_code.sql -v db_name=dev
/usr/local/bin/sqlcmd -S 0.0.0.0,1433 -U sa -P $password -i ../docker/ontime_data.sql -v db_name=dev
/usr/local/bin/sqlcmd -S 0.0.0.0,1433 -U sa -P $password -i ../docker/sp_CreateOntimeCarrierTable.sql -v db_name=dev
/usr/local/bin/sqlcmd -S 0.0.0.0,1433 -U sa -P $password -i ../docker/carrier_code.sql -v db_name=prod
/usr/local/bin/sqlcmd -S 0.0.0.0,1433 -U sa -P $password -i ../docker/ontime_data.sql -v db_name=prod
/usr/local/bin/sqlcmd -S 0.0.0.0,1433 -U sa -P $password -i ../docker/sp_CreateOntimeCarrierTable.sql -v db_name=prod

