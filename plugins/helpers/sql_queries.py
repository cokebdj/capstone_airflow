class SqlQueries:

    create_staging_weather = ("""  CREATE TABLE IF NOT EXISTS public.staging_weather (
                                        DATE                        varchar(256)        NOT NULL,
                                        HourlyPrecipitation         numeric(18,0),
                                        HourlyRelativeHumidity      numeric(18,0),
                                        HourlySeaLevelPressure      numeric(18,0),
                                        HourlyStationPressure       numeric(18,0),
                                        HourlyVisibility            numeric(18,0),
                                        HourlyWindDirection         numeric(18,0),
                                        HourlyWindSpeed             numeric(18,0)
                                );  """)

    create_staging_bikes = ("""  CREATE TABLE IF NOT EXISTS public.staging_bikes (
                                        Duration                    varchar(256),
                                        "Start date"                varchar(256),
                                        "End date"                  varchar(256),
                                        "Start station number"      varchar(256),
                                        "Start station"             varchar(256),
                                        "End station number"        varchar(256),
                                        "End station"               varchar(256),
                                        "Bike number"               varchar(256),
                                        "Member type"               varchar(256)
                                );  """)

    create_rides = ("""  CREATE TABLE IF NOT EXISTS public.rides (
                                        duration                    int4,
                                        start_date                  timestamp           NOT NULL,
                                        end_date                    timestamp           NOT NULL,
                                        start_station_number        int4                NOT NULL,   
                                        end_station_number          int4                NOT NULL,
                                        bike_number                 varchar(256)
    );  """)

    rides_table_insert = ("""SELECT 
                            trim('"' FROM "Duration")::int4 as duration, 
                            to_timestamp(trim('"' FROM "Start date"),'YYYY-MM-DD HH:MI:SS') as start_date,
                            to_timestamp(trim('"' FROM "End date"),'YYYY-MM-DD HH:MI:SS') as end_date,
                            trim('"' FROM "Start station number")::int4 as start_station_number,
                            trim('"' FROM "End station number")::int4 as end_station_number,
                            trim('"' FROM "Bike number") as bike_number
                            FROM staging_bikes
                            WHERE 
                            "Start date" IS NOT NULL AND
                            "End date" IS NOT NULL AND
                            "Start station number" IS NOT NULL AND
                            "End station number" IS NOT NULL """)

    create_stations = ("""  CREATE TABLE IF NOT EXISTS public.stations (
                                        station_number              int4                NOT NULL,   
                                        station_name                varchar(256)        NOT NULL
    );  """)

    stations_table_insert = ("""SELECT 
                                DISTINCT 
                                trim('"' FROM "Start station number")::int4 as station_number,
                                trim('"' FROM "Start station") AS station_name
                                FROM staging_bikes
                                WHERE
                                "Start station number" IS NOT NULL AND
                                "Start station" IS NOT NULL """)


    create_weather = ("""  CREATE TABLE IF NOT EXISTS public.weather (
                                            date                    timestamp           NOT NULL,
                                            precipitation           numeric(18,0),
                                            visibility              numeric(18,0),
                                            wind_speed              numeric(18,0)
    );  """)

    weather_table_insert = ("""SELECT 
                                to_timestamp(Date,'YYYY-MM-DD HH:MI:SS') AS date,
                                HourlyPrecipitation AS precipitation,
                                HourlyVisibility AS visibility,
                                HourlyWindSpeed AS wind_speed
                                FROM staging_weather
                                WHERE Date IS NOT NULL""")
