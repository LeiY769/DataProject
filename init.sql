START TRANSACTION;

-- For TRAIN_SERV
CREATE TABLE SERVICE (
    id INT PRIMARY KEY, -- id of the service, autoincrement
    name VARCHAR(100) NOT NULL -- name of the service
) ;

CREATE TABLE REGION(
    id INT PRIMARY KEY, -- id of the region, autoincrement
    name VARCHAR(255) NOT NULL -- name of the region
) ;

-- For UNIQUE_STATION
CREATE TABLE STATIONS (
    id INT PRIMARY KEY, -- id of the station, autoincrement
    name VARCHAR(255) NOT NULL, -- name of the station
    region INT NOT NULL, -- region of the station
    latitude DOUBLE PRECISION NOT NULL, -- latitude of the station
    longitude DOUBLE PRECISION NOT NULL, -- longitude of the station

    FOREIGN KEY (region) REFERENCES REGION(id)
) ;

CREATE TABLE RELATION(
    id INT PRIMARY KEY, -- id of the relation, autoincrement
    name VARCHAR(255) NOT NULL, -- name of the relation
    type INT NOT NULL -- type of the relation
);


CREATE TABLE TRAIN_DATA(
    departure_date DATE,
    train_number INT,
    relation INT,
    train_service INT,
    ptcar_number INT,
    line_number_departure VARCHAR(255),
    real_time_arrival TIME,
    real_time_departure TIME,
    planned_time_arrival TIME,
    planned_time_departure TIME,
    delay_arrival REAL,
    delay_departure REAL,
    ptcar_name INT,
    line_number_arrival VARCHAR(255),
    station_departure INT,
    station_arrival INT,

    FOREIGN KEY (relation) REFERENCES RELATION(id),
    FOREIGN KEY (train_service) REFERENCES SERVICE(id),
    FOREIGN KEY (ptcar_name) REFERENCES STATIONS(id),
    FOREIGN KEY (station_departure) REFERENCES STATIONS(id),
    FOREIGN KEY (station_arrival) REFERENCES STATIONS(id)
) ;


CREATE TABLE WEATHER (
    temperature_2m REAL NOT NULL,
    apparent_temperature REAL NOT NULL,
    dewpoint_2m REAL NOT NULL,  
    relative_humidity_2m REAL NOT NULL,
    precipitation REAL NOT NULL,
    rain REAL NOT NULL,
    snowfall  REAL NULL,
    cloudcover INT NOT NULL,
    cloudcover_low INT NOT NULL,
    cloudcover_mid INT NOT NULL,
    cloudcover_high INT NOT NULL,
    windgusts_10m REAL NOT NULL,
    shortwave_radiation REAL NOT NULL,
    direct_radiation REAL NOT NULL,
    diffuse_radiation REAL NOT NULL,
    direct_normal_irradiance REAL NOT NULL,
    et0_fao_evapotranspiration REAL NOT NULL,
    REGION INT NOT NULL,
    date DATE NOT NULL,
    hour TIME NOT NULL,

    FOREIGN KEY (REGION) REFERENCES REGION(id)
) ;

CREATE TABLE type_day (
    date DATE NOT NULL,
    holiday int NOT NULL,
    weekend boolean NOT NULL,
    day_after_rest boolean NOT NULL
) ;

CREATE TABLE province(

    id INT PRIMARY KEY, -- id of the province, autoincrement
    province VARCHAR(255) NOT NULL, -- name of the province
    REGION INT NOT NULL, -- region of the province
    FOREIGN KEY (REGION) REFERENCES REGION(id)
) ;


COMMIT;
