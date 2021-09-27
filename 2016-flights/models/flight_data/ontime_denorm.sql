{{ config(materialized='table') }}

select
  od.year,
  od.month,
  od.day_of_month,
  od.carrier as carrier_code,
  coalesce(cc.description, 'UNKNOWN') as carrier_desc,
  od.fl_num as flight_number,
  od.origin,
  od.dest as destination,
  CASE
    WHEN od.cancelled != 0 OR od.diverted != 0
      THEN 'N'
    WHEN od.arr_delay is not null THEN 'Y'
    ELSE NULL
  END as arrived_flag
from {{ var("db_name") }}.[{{ var("schema_name") }}].ontime_data od
left join {{ var("db_name") }}.[{{ var("schema_name") }}].carrier_code cc
  on od.carrier = cc.code
