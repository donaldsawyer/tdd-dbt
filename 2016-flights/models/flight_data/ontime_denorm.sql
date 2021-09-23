{{ config(materialized='table') }}

select
  od.year,
  od.month,
  od.day_of_month,
  od.carrier as carrier_code,
  coalesce(cc.description, 'UNKNOWN') as carrier_desc,
  od.fl_num as flight_number,
  od.origin,
  od.dest as destination
from {{ var("db_name") }}.[{{ var("schema_name") }}].ontime_data od
left join {{ var("db_name") }}.[{{ var("schema_name") }}].carrier_code cc
  on od.carrier = cc.code
