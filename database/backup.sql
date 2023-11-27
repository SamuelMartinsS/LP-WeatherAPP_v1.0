PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE sensor(
id_sensor INTEGER PRIMARY KEY,
unidade TEXT NOT NULL
);

INSERT INTO sensor VALUES(1,'ºC');
INSERT INTO sensor VALUES(2,'RH');
INSERT INTO sensor VALUES(3,'Kh');
INSERT INTO sensor VALUES(4,'º');
INSERT INTO sensor VALUES(5,'cm');

CREATE TABLE valores(
id_valor INTEGER PRIMARY KEY,
sensor INTEGER NOT NULL,
valor FLOAT, 
timestp TIMESTAMP,
FOREIGN KEY (sensor) REFERENCES sensor (id_sensor) 
);

COMMIT;