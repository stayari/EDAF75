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