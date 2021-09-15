#!/bin/bash
password=ITsC0mpl1cat3d

echo Setting up MSSQL Server Databases...

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $password -i ./docker/init_databases.sql
