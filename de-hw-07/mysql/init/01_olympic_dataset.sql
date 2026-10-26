CREATE DATABASE IF NOT EXISTS olympic_dataset;

CREATE TABLE IF NOT EXISTS olympic_dataset.athlete_event_results (
    edition TEXT,
    edition_id INT,
    country_noc TEXT,
    sport TEXT,
    event TEXT,
    result_id BIGINT,
    athlete TEXT,
    athlete_id BIGINT,
    pos TEXT,
    medal TEXT,
    isTeamSport TEXT
);

LOAD DATA INFILE '/csv/athlete_event_results.csv'
INTO TABLE olympic_dataset.athlete_event_results
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
