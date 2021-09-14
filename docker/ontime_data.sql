use $(db_name)

IF EXISTS(select * from sys.tables where name = 'ontime_data')
BEGIN
  DROP TABLE $(db_name).dbo.ontime_data
END

create table $(db_name).dbo.ontime_data (
  year int,
  month tinyint,
  day_of_month tinyint,
  fl_date varchar(8),
  unique_carrier varchar(3),
  airline_id int,
  carrier varchar(3),
  tail_num varchar(10),
  fl_num int,
  origin_airport_id int,
  origin_airport_sequence_id int,
  origin varchar(3),
  dest_airport_id int,
  dest_airport_seq_id int,
  dest varchar(3),
  dep_delay float,
  arr_delay float,
  cancelled float,
  diverted float,
  distance float
)
go
