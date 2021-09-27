use $(db_name)

CREATE PROCEDURE dbo.sp_CreateOntimeCarrierTable
AS
BEGIN
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
        CC.carrier_code,
        CC.carrier_desc,
        OD.flight_number,
        OD.origin,
        OD.destination,
        CASE WHEN OD.concelled != 0 OR OD.diverted != 0 THEN 'N'
            WHEN OD.arr_delay IS NOT NULL THEN 'Y'
            ELSE NULL
            END as arrived_flag
    FROM dbo.ontime_data OD
    JOIN dbo.carrier_code CC
        ON CC.carrier = OD.carrier
END