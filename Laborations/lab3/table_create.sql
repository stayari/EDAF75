PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS theaters;

DROP TABLE IF EXISTS movies;

DROP TABLE IF EXISTS shows;

DROP TABLE IF EXISTS customers;

DROP TABLE IF EXISTS tickets;

DROP TABLE IF EXISTS performances;

PRAGMA foreign_keys = OFF;

CREATE TABLE theaters(
	th_name TEXT,
	capacity INT,
	PRIMARY KEY (th_name)
);

CREATE TABLE movies(
	IMDB_key TEXT,
	title TEXT,
	year INT,
	duration INT DEFAULT 120,
	PRIMARY KEY (IMDB_key)
);

CREATE TABLE performances(
    show_id INT DEFAULT(lower(hex(randomblob(16)))), --för att få en id
	IMDB_key TEXT,
	th_name TEXT,
	start_date DATE,
	start_time TIME,
	remaining_seats INT DEFAULT(999),
	PRIMARY KEY(show_id)
--PRIMARY KEY(IMDB_key, start_time, start_date, th_name)
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
	user_name TEXT,
	show_id INT,
	PRIMARY KEY (ticket_id) 
	FOREIGN KEY (show_id)
	REFERENCES performances(show_id)
	FOREIGN KEY	(user_name) 
	REFERENCES customers(user_name)
	);