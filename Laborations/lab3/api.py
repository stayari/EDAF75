from bottle import get
from bottle import run
import sqlite3
import json

conn = sqlite3.connect("movies.sqlite")

@get('/ping')
def return_pong():
    return "pong"



@get('/movies')
def return_movies():
    c = conn.cursor()  
    c.execute(
        """
        SELECT *
        FROM   movies
        """
    )
    s = [{"IMDB_KEY": IMDB_KEY, "name": name, "year": year, "duration": duration}
         for (IMDB_KEY, name, year, duration) in c]
    return json.dumps({"data": s}, indent=4)


@get('/customers')
def return_customers():
    c = conn.cursor()  
    c.execute(
        """
        SELECT *
        FROM customers   
        """
    )
    d = [{"user_name": user_name, "full_name": full_name, "password": password}
         for (user_name, full_name, password) in c]
    return json.dumps({"data": d}, indent=4)



run(host='localhost', port=7007)