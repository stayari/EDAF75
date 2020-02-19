from bottle import get
from bottle import run
import sqlite3
import json

conn = sqlite3.connect("movies.sqlite")

@get('/ping')
def return_pong():
    return "pong"

@get('/reset')
def reset_db(): 
    return ("OK")
    c = conn.cursor()
    c.execute(
        """
        DROP TABLE IF EXISTS theaters;
        DROP TABLE IF EXISTS movies;
        DROP TABLE IF EXISTS shows; ;
        DROP TABLE IF EXISTS customers;
        DROP TABLE IF EXISTS tickets;

        INSERT
        INTO    customers(user_name, full_name, password)
        VALUES  (sepehr, Sepehr Tayari, s123)
                (fabian, Fabian Frankel, f123)
                (albin, Albin Andersson, a123)
        INSERT
        INTO    movies(name, year, IMDB_key, duration)
        VAUES   ("The Shape of Water", 2017, "tt5580390", 120)
                ("Moonlight", 2016, "tt4975722", 120)
                ("Spotlight", 2015, "tt1895587", 120)
                ("Birdman", 2014, "tt2562232", 120)
        INSERT
        INTO    theaters(th_name, capacity)
        VALUES  (Kino, 10)
                (Södran, 16)
                (Skandia, 100)
        """)
#    s = [{"th_name": th_name, "capacity": capacity}
#         for (th_name, capacity) in c]
    return "OK"
    #return json.dumps({"data": s}, indent=4)

run(host='localhost', port=7007)