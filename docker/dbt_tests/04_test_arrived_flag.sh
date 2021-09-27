# dbt parameters
db_name=dev
sqlcmd_base="sqlcmd -S 0.0.0.0,1433 -U sa -P ITsC0mpl1cat3d "

cd 2016-flights

################################################################################
# Scenario 04
#  - Join results contain all possible data calculations for the arrived_flag results
################################################################################

# seed with the test data
dbt seed --select tag:04_arrived_flag --target dev
# dbt seed --select 01_ontime_data_joinok --target dev
# dbt seed --select 01_ontime_denorm_joinok_expected --target dev

# execute the model to get the destination table
dbt run --target dev --vars "{db_name: $db_name, schema_name: dbo_04_arrived_flag}"

# execute the tests
# dbt test --target dev --vars "{db_name: $db_name}"
# dbt test --target dev --vars "{db_name: $db_name}" tag:01_joinok
dbt test --target dev --vars "{db_name: $db_name, schema_name: dbo_04_arrived_flag}" --models ontime_denorm --exclude tag:01_joinok tag:02_joinunknown tag:03_joincombined

# cleanup
# eval "$sqlcmd_base -Q \"drop table dev.dbo_04_arrived_flag.ontime_data\""
# eval "$sqlcmd_base -Q \"drop table dev.dbo_04_arrived_flag.carrier_code\""
# eval "$sqlcmd_base -Q \"drop table dev.dbo_04_arrived_flag.[04_ontime_denorm_arrived_flag_expected]\""
# eval "$sqlcmd_base -Q \"drop table dev.dbo.ontime_denorm\""
