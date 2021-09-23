# dbt parameters
db_name=dev
sqlcmd_base="sqlcmd -S 0.0.0.0,1433 -U sa -P ITsC0mpl1cat3d "

# create the source tables
# run_sqlcmd "-v db_name=$db_name -i docker/ontime_data.sql"
# run_sqlcmd "-v db_name=$db_name -i docker/carrier_code.sql"
# eval "$sqlcmd_base -v db_name=$db_name -i docker/ontime_data.sql"
# eval "$sqlcmd_base -v db_name=$db_name -i docker/carrier_code.sql"

cd 2016-flights

################################################################################
# Scenario 01
#  - Join results in value of "A1 Airlines" for carrier_desc
#  - 2 lookup values, but only one row should be result
################################################################################

# seed with the test data
dbt seed --select tag:01_joinok --target dev
# dbt seed --select 01_ontime_data_joinok --target dev
# dbt seed --select 01_ontime_denorm_joinok_expected --target dev

# execute the model to get the destination table
dbt run --target dev --vars "{db_name: $db_name, schema_name: dbo_01_joinok}"

# execute the tests
# dbt test --target dev --vars "{db_name: $db_name}"
# dbt test --target dev --vars "{db_name: $db_name}" tag:01_joinok
dbt test --target dev --vars "{db_name: $db_name, schema_name: dbo_01_joinok}" --models ontime_denorm --exclude tag:02_joinunknown tag:03_joincombined tag:04_arrived_flag

eval "$sqlcmd_base -Q \"drop table dev.dbo_01_joinok.ontime_data\""
eval "$sqlcmd_base -Q \"drop table dev.dbo_01_joinok.carrier_code\""
eval "$sqlcmd_base -Q \"drop table dev.dbo_01_joinok.[01_ontime_denorm_joinok_expected]\""
eval "$sqlcmd_base -Q \"drop table dev.dbo.ontime_denorm\""
