CREATE DATABASE event_app;
USE event_app;

CREATE TABLE events (
       id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
       name VARCHAR(100) NOT NULL,
       description VARCHAR(1000) NOT NULL,
       start TIMESTAMP NOT NULL,
       end TIMESTAMP NOT NULL,
       host VARCHAR(100) NOT NULL,
       location VARCHAR(200) NOT NULL,
       url VARCHAR(200) NOT NULL,
       study_program VARCHAR(200) NOT NULL,
       class_year INTEGER NOT NULL
);
