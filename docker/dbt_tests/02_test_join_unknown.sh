# dbt parameters
db_name=dev
sqlcmd_base="sqlcmd -S 0.0.0.0,1433 -U sa -P ITsC0mpl1cat3d "

cd 2016-flights

################################################################################
# Scenario 02
#  - Join results in value of "unknown" for carrier_desc
#  - 2 lookup values, but only one row should be result
################################################################################

# seed with the test data
dbt seed --select tag:02_joinunknown --target dev
# dbt seed --select 01_ontime_data_joinok --target dev
# dbt seed --select 01_ontime_denorm_joinok_expected --target dev

# execute the model to get the destination table
dbt run --target dev --vars "{db_name: $db_name, schema_name: dbo_02_joinunknown}"

# execute the tests
# dbt test --target dev --vars "{db_name: $db_name}"
# dbt test --target dev --vars "{db_name: $db_name}" tag:01_joinok
dbt test --target dev --vars "{db_name: $db_name, schema_name: dbo_02_joinunknown}" --models ontime_denorm --exclude tag:01_joinok tag:03_joincombined tag:04_arrived_flag

eval "$sqlcmd_base -Q \"drop table dev.dbo_02_joinunknown.ontime_data\""
eval "$sqlcmd_base -Q \"drop table dev.dbo_02_joinunknown.carrier_code\""
eval "$sqlcmd_base -Q \"drop table dev.dbo_02_joinunknown.[02_ontime_denorm_joinunknown_expected]\""
eval "$sqlcmd_base -Q \"drop table dev.dbo.ontime_denorm\""
