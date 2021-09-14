use $(db_name)

IF EXISTS(select * from sys.tables where name = 'carrier_code')
BEGIN
  DROP TABLE $(db_name).dbo.carrier_code
END

create table $(db_name).dbo.carrier_code (
  code varchar(3) not null,
  description varchar(128)
)
go
