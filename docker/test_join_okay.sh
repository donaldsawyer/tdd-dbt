# dbt parameters
db_name=dev
sqlcmd_base="sqlcmd -S 127.0.0.1,1433 -U sa -P ITsC0mpl1cat3d "

# create the source tables
# run_sqlcmd "-v db_name=$db_name -i docker/ontime_data.sql"
# run_sqlcmd "-v db_name=$db_name -i docker/carrier_code.sql"
eval "$sqlcmd_base -v db_name=$db_name -i docker/ontime_data.sql"
eval "$sqlcmd_base -v db_name=$db_name -i docker/carrier_code.sql"

cd 2016-flights

# seed with the test data
dbt seed --select carrier_code_01_joinok --target dev
dbt seed --select ontime_data01_01_joinok --target dev

# execute the model to get the destination table
dbt run --target dev --vars "{db_name: $db_name}"

# execute the tests
dbt test --target dev --vars "{db_name: $db_name}"

# cleanup
eval "$sqlcmd_base -Q \"truncate table demo.dbo.ontime_data\""
eval "$sqlcmd_base -Q \"truncate table demo.dbo.carrier_code\""
eval "$sqlcmd_base -Q \"truncate table demo.dbo.ontime_denorm\""
