# dbt parameters
db_name=dev
sqlcmd_base="sqlcmd -S 0.0.0.0,1433 -U sa -P ITsC0mpl1cat3d "

cd 2016-flights

################################################################################
# Scenario 03
#  - Join results in two rows, one with A1 Airlines, one with "UNKNOWN" for carrier_desc
#  - 2 lookup values, but only one row should be result
################################################################################

# seed with the test data
dbt seed --select tag:03_joincombined --target dev
# dbt seed --select 01_ontime_data_joinok --target dev
# dbt seed --select 01_ontime_denorm_joinok_expected --target dev

# execute the model to get the destination table
dbt run --target dev --vars "{db_name: $db_name, schema_name: dbo_03_joincombined}"

# execute the tests
# dbt test --target dev --vars "{db_name: $db_name}"
# dbt test --target dev --vars "{db_name: $db_name}" tag:01_joinok
dbt test --target dev --vars "{db_name: $db_name, schema_name: dbo_03_joincombined}" --models ontime_denorm --exclude tag:01_joinok tag:02_joinunknown tag:04_arrived_flag

# cleanup
eval "$sqlcmd_base -Q \"drop table dev.dbo_03_joincombined.ontime_data\""
eval "$sqlcmd_base -Q \"drop table dev.dbo_03_joincombined.carrier_code\""
eval "$sqlcmd_base -Q \"drop table dev.dbo_03_joincombined.[03_ontime_denorm_joincombined_expected]\""
eval "$sqlcmd_base -Q \"drop table dev.dbo.ontime_denorm\""
