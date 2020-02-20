from bottle import get, post, run, request, response
import sqlite3
import json
import uuid
import random
import uuid
from datetime import datetime


conn = sqlite3.connect('movies.db')
c = conn.cursor()

HOST = 'localhost'
PORT = 7007


    
def url(resource):
    return f"http://{HOST}:{PORT}{resource}"


def format_response(d):
    return json.dumps(d, indent=4) + "\n"


@get('/ping')
def ping():
    response.status = 200
    return "pong\n"



@post('/reset')
def reset():
    c.execute("DROP TABLE IF EXISTS theaters;")   
    c.execute("DROP TABLE IF EXISTS users;")
    c.execute("DROP TABLE IF EXISTS tickets;")
    c.execute("DROP TABLE IF EXISTS performances;")
    c.execute("DROP TABLE IF EXISTS movies;")
    c.execute("CREATE TABLE users(user_id  TEXT NOT NULL, name TEXT NOT NULL, password  TEXT NOT NULL, PRIMARY KEY (user_id))")
    c.execute("INSERT INTO users(user_id,name,password) VALUES ('alice', 'Alice','dobido'), ('bob', 'Bob', 'whatsinaname')")
    c.execute("CREATE TABLE movies (title TEXT NOT NULL, year INTEGER NOT NULL, imdb key TEXT NOT NULL, PRIMARY KEY (imdb))")
    c.execute("INSERT INTO movies ( title, year, imdb) VALUES ('The Shape of Water', 2017, 'tt5580390'), ('Moonlight', 2016, 'tt4975722'), ('Spotlight', 2015, 'tt1895587'), ('Birdman', 2014, 'tt2562232')")
    c.execute("CREATE TABLE theaters (name TEXT NOT NULL, capacity INTEGER NOT NULL)")
    c.execute("INSERT INTO theaters (name, capacity) VALUES ('Kino', 10),('Södran', 16),('Skandia', 100)")
    c.execute("CREATE TABLE performances (performance_id TEXT DEFAULT (lower(hex(randomblob(16)))), imdb TEXT NOT NULL, theater_name TEXT NOT NULL, date TEXT, time TEXT, remainingSeats INTEGER NOT NULL, PRIMARY KEY (performance_id), FOREIGN KEY (imdb) REFERENCES movies(imdb), FOREIGN KEY (theater_name) REFERENCES theaters(theater_name))")
    c.execute("CREATE TABLE tickets (ticket_id TEXT DEFAULT (lower(hex(randomblob(16)))), username TEXT NOT NULL, performance_id TEXT NOT NULL, PRIMARY KEY (ticket_id), FOREIGN KEY (username) REFERENCES customers(username), FOREIGN KEY (performance_id) REFERENCES performances(performance_id))")

   
    
    conn.commit()
    response.status = 200
    return "OK\n"

@get('/movies')
def get_movies():
    response.content_type = 'movies/json'
    query = """
        SELECT imdb, title, year
        FROM   movies
        WHERE  1 = 1
        """
    params = []
    if request.query.title:
        query += "AND title = ?"
        params.append(request.query.title)
    if request.query.year:
        query += "AND year = ?"
        params.append(request.query.year)
    if request.query.imdb:
        query += "AND imdb = ?"
        params.append(request.query.imdb)
    c = conn.cursor()
    c.execute(
        query,
        params
    )
    s = [{"imdbKey": imdb, "title": title, "year": year}
         for (imdb, title, year) in c]
    response.status = 200
    return format_response({"data": s})



@get('/movies/<imdb>')
def get_movie(imdb):
    response.content_type = 'movies/json'
    c.execute(
        """
        SELECT imdb, title, year
        FROM   movies
        WHERE  imdb = ?
        """,
        [imdb]
    )
    s = [{"imdbKey": imdb, "title": title, "year": year}
         for (imdb, title, year) in c]
    response.status = 200
    return format_response({"data": s})


@post('/performances')
def post_student():
    c = conn.cursor()
    response.content_type = 'performances/json'
    imdb = request.query.imdb
    theater_name = request.query.theater
    date = request.query.date
    time = request.query.time
    if not (imdb and theater_name):
        response.status = 400
        return format_response({"error": "Missing parameter"})
    
 
    
    c.execute(
        """
        SELECT   capacity
        FROM     theaters
        WHERE    name = ?
        """
        ,[theater_name] 
    )
    s = c.fetchall()
    capacity = int(([x[0] for x in s])[0])
    
    c.execute(
        """
        INSERT
        INTO   performances(imdb, theater_name, date, time, remainingSeats)
        VALUES (?, ?, ?, ?, ?)
        """,
        [imdb, theater_name, date, time, capacity]
    )
    conn.commit()
    c.execute(
        """
        SELECT   performance_id, imdb, theater_name, date, time, remainingSeats
        FROM     performances
        WHERE    rowid = last_insert_rowid()
        """
    )
    rows = c.fetchall()
    per_id = [x[0] for x in rows]
    
    response.status = 200
    return '\nperformances/'+per_id[0]+'\n'

@get('/performances')
def get_movies():
    response.content_type = 'performances/json'
    c.execute("""
        SELECT *
        FROM   performances
        """
    )
    s = [{"performance_id": performance_id, "imdb": imdb, "theater_name": theater_name, "date": date, "time": time, "remainingSeats": remainingSeats}
         for (performance_id, imdb, theater_name, date, time, remainingSeats) in c]
    response.status = 200
    return format_response({"data": s})

@post('/tickets')
def post_tickets():
    c = conn.cursor()
    response.content_type = 'tickets/json'
    username = request.query.username
    performance_id = request.query.performance_id
    password = request.query.password
 
    c.execute(
        """
        SELECT   password
        FROM     users
        WHERE    user_id = ?
        """
        ,[username] 
    )
    s = [password
         for (password) in c]
    real_password = s[0][0]
    
    if(password == real_password):
        
        c.execute(
            """
            SELECT   remainingSeats
            FROM     performances
            WHERE    performance_id = ?
            """
            ,[performance_id] 
            )
        s = [password
             for (password) in c]
        remainingSeats = s[0][0]
    
        if(remainingSeats > 0):

            c.execute(
                """
                INSERT
                INTO   tickets(username, performance_id)
                VALUES (?, ?)
                """,
                [username, performance_id]
            )
          

            
            c.execute(
                """
                UPDATE performances 
                SET remainingSeats = ? 
                WHERE performance_id = ?
                """, 
                [remainingSeats-1, performance_id]
            )
        else: return '\nNo tickets left\n\n'
            
            
        
    else: return '\nWrong password\n\n'
    c.execute(
        """
        SELECT   ticket_id
        FROM     tickets
        WHERE    rowid= last_insert_rowid()
        """
    )
    s = [ticket_id
         for (ticket_id) in c]
    ticket_id = s[0][0]
    
    response.status = 200
    conn.commit()
    return '\ntickets/'+ticket_id+'\n'

    
    
@get('/customers/<user_id>/tickets')
def get_movies(user_id):
    response.content_type = 'customers/json'
    c.execute(
        """
        SELECT date, time, theater_name, title, year, count() as nbrOfTickets
        FROM   tickets
        JOIN   performances
        USING (performance_id)
        JOIN   movies
        USING (imdb)
        WHERE  username = ?
        GROUP BY (performance_id)
        """,
        [user_id]
    )
    s = [{"date": date, "startTime": time, "theater_name": theater_name, "title": title, "year": year, "nbrOfTickets": nbrOfTickets}
         for (date, time, theater_name, title, year, nbrOfTickets) in c]
    response.status = 200
    return format_response({"data": s})

    
    
    
run(host=HOST, port=PORT, debug=True, reloader = True)