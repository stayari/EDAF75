

PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS shows;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys=OFF;


CREATE TABLE theaters(
	th_name 	TEXT,
	capacity	INT,
	PRIMARY KEY (th_name)
); 
-- Osäker

CREATE TABLE movies(
	IMDB_key	TEXT, 
	name		TEXT,
	year		INT,
	duration    INT, 
	--start_time	TEXT,
	PRIMARY KEY (IMDB_key)
); 

CREATE TABLE shows(
	IMDB_key	TEXT,
	th_name		TEXT,
	start_date  DATE,
	start_time	TIME,

	PRIMARY KEY(IMDB_key, start_time, start_date, th_name)
	);


CREATE TABLE customers(
	user_id		TEXT DEFAULT (lower(hex(randomblob(16)))),
	full_name	TEXT,
	password 	TEXT, -- hasha
	PRIMARY KEY (user_id)
); 

CREATE TABLE tickets(		
	ticket_id   INT DEFAULT (lower(hex(randomblob(16)))), 
	th_name		TEXT,
	IMDB_key	TEXT,
	start_time  TIME,
	start_date  DATE,

	PRIMARY KEY (ticket_id)
	--FOREIGN KEY (th_name) REFERENCES theaters(th_name)
	--FOREIGN KEY (IMDB_key, start_time) REFERENCES movies(IMDB_key, start_time)
	--FOREIGN KEY (start_time) REFERENCES movies(start_time)
); 
--INSERTING DATA INTO TABLES
INSERT
INTO theaters
VALUES ("SF LUND", 200
);

INSERT
INTO movies
VALUES ("tt0111161", "The Shawshank Redemption", 1994, 142
);

INSERT
INTO shows
VALUES ("tt0111161", "SF LUND", "2019–02-12", "20:00"
);

INSERT
INTO customers (full_name, password)
VALUES ("FABIAN FRANKEL", "hallojsan"
);

INSERT
INTO tickets (th_name, IMDB_key, start_time, start_date)
VALUES ("SF LUND", "tt0111161", "20:00", "2019–02-12"
);

