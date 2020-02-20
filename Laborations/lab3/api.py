from bottle import get, post, run, request, response
import sqlite3
import json


conn = sqlite3.connect("movies2.sqlite")

def create_sql(filename):
    text_commands = open(filename, 'r').read().split(";")

    # Run every command
    for command in text_commands:
        try:
            conn.execute(command)
        except:
            print("except in create_sql")
def format_response(d):
    return json.dumps(d, indent=4) + "\n"

@get('/ping')
def return_pong():
    return "pong"

@post('/reset')
def reset_db(): 


    c = conn.cursor()
    create_sql("table_create.sql")
    c.execute(
        """
        INSERT
        INTO    customers(user_name, full_name, password)
        VALUES  ("sepehr123", "Sepehr Tayari", "s123"),
                ("fabian", "Fabian Frankel", "f123"),
                ("albin", "Albin Andersson", "a123")
        """
    )
    conn.commit()


    c.execute(
        """
        INSERT
        INTO    movies(name, year, IMDB_key, duration)
        VALUES  ("The Shape of Water", 2017, "tt5580390", 120),
                ("Moonlight", 2016, "tt4975722", 120),
                ("Spotlight", 2015, "tt1895587", 120),
                ("Birdman", 2014, "tt2562232", 120)
        """
    )
    conn.commit()

    c.execute(
        """
        INSERT
        INTO    theaters(th_name, capacity)
        VALUES  ("Kino", 10),
                ("Södran", 16),
                ("Skandia", 100)
        """
    )
    conn.commit()
    return "OK"




@get('/movies')
def get_movies():
    response.content_type = 'application/json'
    query ="""
            SELECT *
            FROM   movies
            WHERE 1 = 1
            """
    params = []
    if request.query.name:
        query += "AND name = ?"
        params.append(request.query.name)
    if request.query.IMDB_key:
        query += "AND IMDB_key = ?"
        params.append(request.query.IMDB_key)
    if request.query.year: 
        query += "AND year = ?"
        params.append(request.query.year)

    c = conn.cursor()
    c.execute(
        query,
        params
        )

    s = [{"IMDB_key": IMDB_key, "name": name, "year": year, "duration": duration}
         for (IMDB_key, name , year,  duration) in c]
    response.status = 200
    return format_response({"data": s})
    #return json.dumps({"data": s}, indent=4)

@get('/movies/<IMDB_key>')
def get_movie_from_IMDB(IMDB_key):
    print("IMDB case")
    response.content_type = 'application/json'
    query = """
            SELECT * 
            FROM movies 
            WHERE IMDB_KEY = ?
            """
    c = conn.cursor()
    c.execute(query,
              [IMDB_key])
    s = [{"IMDB_key": IMDB_key, "name": name, "year": year, "duration": duration}
         for (IMDB_key, name, year, duration) in c]
    response.status = 200
    return format_response({"data": s})

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
