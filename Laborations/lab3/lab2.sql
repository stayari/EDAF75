
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS theaters;

DROP TABLE IF EXISTS movies;

DROP TABLE IF EXISTS shows;

DROP TABLE IF EXISTS customers;

DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys = OFF;

CREATE TABLE theaters(
	th_name TEXT,
	capacity INT,
	PRIMARY KEY (th_name)
);

CREATE TABLE movies(
	IMDB_key TEXT,
	name TEXT,
	year INT,
	duration INT,
	PRIMARY KEY (IMDB_key)
);

CREATE TABLE shows(
	IMDB_key TEXT,
	th_name TEXT,
	start_date DATE,
	start_time TIME,
	PRIMARY KEY(IMDB_key, start_time, start_date, th_name) 
	FOREIGN KEY (th_name) REFERENCES theaters(th_name)
);

CREATE TABLE customers(
	user_name TEXT,
	full_name TEXT,
	password TEXT,
	PRIMARY KEY (user_name)
);

CREATE TABLE tickets(
	ticket_id INT DEFAULT (lower(hex(randomblob(16)))),
	th_name TEXT,
	IMDB_key TEXT,
	start_time TIME,
	start_date DATE,
	user_name TEXT,
	PRIMARY KEY (ticket_id) 
	FOREIGN KEY (th_name, IMDB_key, start_time, start_date)
	REFERENCES shows(th_name, IMDB_key, start_time, start_date)
	FOREIGN KEY	(user_name) 
	REFERENCES customers(user_name)
	);

--INSERTING DATA INTO TABLES
--INSERTING THEATERS
INSERT INTO
	theaters
VALUES
	("SF LUND", 200);

INSERT INTO
	theaters
VALUES
	("SF MALMO", 150);

INSERT INTO
	theaters
VALUES
	("SF STOCKHOLM", 300);

--INSERTING MOVIES
INSERT INTO
	movies
VALUES
	(
		"tt0111161",
		"The Shawshank Redemption",
		1994,
		142
	);

INSERT INTO
	movies
VALUES
	("tt0068646", "The Godfather", 1972, 275);

INSERT INTO
	movies
VALUES
	("tt0468569", "The Dark Knight", 2008, 152);

INSERT INTO
	movies
VALUES
	(
		"tt0167260",
		"The Lord of the Rings: The Return of the King",
		2003,
		301
	);

--INSERTING SHOWS
INSERT INTO
	shows
VALUES
	("tt0111161", "SF LUND", "2019–02-12", "20:00");

INSERT INTO
	shows
VALUES
	("tt0111161", "SF LUND", "2019–02-13", "20:00");

INSERT INTO
	shows
VALUES
	("tt0068646", "SF LUND", "2019–02-11", "20:00");

INSERT INTO
	shows
VALUES
	("tt0468569", "SF MALMO", "2019–02-13", "20:00");

INSERT INTO
	shows
VALUES
	("tt0068646", "SF MALMO", "2019–02-11", "20:00");

INSERT INTO
	shows
VALUES
	(
		"tt0068646",
		"SF STOCKHOLM",
		"2019–02-12",
		"20:00"
	);

INSERT INTO
	shows
VALUES
	(
		"tt0111161",
		"SF STOCKHOLM",
		"2019–02-13",
		"20:00"
	);

INSERT INTO
	shows
VALUES
	(
		"tt0068646",
		"SF STOCKHOLM",
		"2019–02-11",
		"20:00"
	);

--INSERT customers
INSERT INTO
	customers 
VALUES
	("Fabian","FABIAN FRANKEL", "hallojsan");

INSERT INTO
	customers 
VALUES
	("Sepehr","SEPEHR TAYARI", "jamboseli");

INSERT INTO
	customers
VALUES
	("Marcus","MARCUS INGEMANSSON", "DJINGSTRING");

--INSERT TICKETS
--DECLARE a INT;
--SET a = 0;
--WHILE a < 50
--	BEGIN
INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time,user_name)
VALUES
	("tt0111161", "SF LUND", "2019–02-12", "20:00", "Fabian");

INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time, user_name)
VALUES
	("tt0111161", "SF LUND", "2019–02-13", "20:00", "Sepehr");

INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time,user_name)
VALUES
	("tt0068646", "SF LUND", "2019–02-11", "20:00", "Marcus");

INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time, user_name)
VALUES
	(
		"tt0468569",
		"SF MALMO",
		"2019–02-13",
		"20:00",
		"Sepehr"
	);

INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time, user_name)
VALUES
	(
		"tt0068646",
		"SF MALMO",
		"2019–02-11",
		"20:00",
		"Fabian"
	);

INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time,  user_name)
VALUES
	(
		"tt0068646",
		"SF STOCKHOLM",
		"2019–02-12",
		"20:00",
		"Sepehr"
	);

INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time, user_name)
VALUES
	(
		"tt0111161",
		"SF STOCKHOLM",
		"2019–02-13",
		"20:00",
		"Marcus"
	);

INSERT INTO
	tickets (IMDB_key, th_name, start_date, start_time, user_name)
VALUES
	(
		"tt0068646",
		"SF STOCKHOLM",
		"2019–02-11",
		"20:00",
		"Fabian"
	);
