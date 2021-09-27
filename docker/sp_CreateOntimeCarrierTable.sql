USE $(db_name)
GO

CREATE PROCEDURE dbo.sp_CreateOntimeCarrierTable
AS
BEGIN
    IF EXISTS (SELECT * FROM sys.objects WHERE type = 'U' AND name = 'ontime_denorm')
        BEGIN
            DROP TABLE dbo.ontime_denorm
        END

    CREATE TABLE dbo.ontime_denorm(
        year int,
        month tinyint,
        day_of_month tinyint,
        carrier_code varchar(3),
        carrier_desc varchar(128),
        flight_number int,
        origin varchar(3),
        destination varchar(3),
        arrived_flag varchar(1)
    )

    INSERT INTO dbo.ontime_denorm(
        year,
        month,
        day_of_month,
        carrier_code,
        carrier_desc,
        flight_number,
        origin,
        destination,
        arrived_flag
    )
    SELECT
        OD.year,
        OD.month,
        OD.day_of_month,
        OD.carrier,
        COALESCE(CC.description, 'UNKNOWN'),
        OD.fl_num,
        OD.origin,
        OD.dest,
        CASE WHEN OD.cancelled != 0 OR OD.diverted != 0 THEN 'N'
            WHEN OD.arr_delay IS NOT NULL THEN 'Y'
            ELSE NULL
            END as arrived_flag
    FROM dbo.ontime_data OD
    LEFT JOIN dbo.carrier_code CC
        ON OD.carrier = CC.code
END
GO