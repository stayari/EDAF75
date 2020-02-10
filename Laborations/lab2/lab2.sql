
DROP TABLE IF EXISTS theaters
CREATE TABLE theaters(
	th_name 	TEXT,
	capacity	INT,
	PRIMARY KEY (name)
) 
-- Osäker
DROP TABLE IF EXISTS movies
CREATE TABLE movies(
	IMDB_key	TEXT, --?? 
	name		TEXT,
	year		INT,
	duration    INT, 
	start_time	TEXT,
	PRIMARY KEY (name, start_time)
) 

DROP TABLE IF EXISTS customers
CREATE TABLE customers(
	user_id		TEXT,
	full_name	TEXT,
	password 	TEXT
	PRIMARY KEY (user_id)
) 

DROP TABLE IF EXISTS tickets
CREATE TABLE tickets(		
	ticket_id   INT, 
	th_name		TEXT,
	IMDB_key	TEXT,
	start_time  TEXT,

	PRIMARY KEY (ticket_id, th_name, IMDB_key, start_time),
	FOREIGN KEY (th_name) REFERENCES theaters(th_name)
	FOREIGN KEY (IMDB_key, start_time) REFERENCES movies(IMDB_key, start_time)
	--FOREIGN KEY (start_time) REFERENCES movies(start_time)


) 