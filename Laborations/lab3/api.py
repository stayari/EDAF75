from bottle import get, post, run, request, response
import sqlite3
import json
import hashlib

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
        INTO    movies(title, year, IMDB_key, duration)
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
    if request.query.title:
        query += "AND title = ?"
        params.append(request.query.title)
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

    s = [{"IMDB_key": IMDB_key, "title": title, "year": year, "duration": duration}
         for (IMDB_key, title , year,  duration) in c]
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
    s = [{"IMDB_key": IMDB_key, "title": title, "year": year, "duration": duration}
         for (IMDB_key, title, year, duration) in c]
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

@get('/performances')
def get_performances():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT * 
        FROM performances
        """
    )
    s = [{"show_id": show_id, "IMDB_key": IMDB_key, "th_name": th_name, "start_date": start_date, "start_time": start_time,
        "remaining_seats": remaining_seats}
       for (show_id, IMDB_key, th_name, start_date, start_time, remaining_seats) in c]
    response.status = 200
    return format_response({"data": s})

@post('/performances')
def put_performances():
    response.content_type = 'application/json'
    IMDB_key = request.query.imdb
    start_date = request.query.date
    start_time = request.query.time
    th_name = request.query.theater
    print(IMDB_key, start_time, start_date, th_name)

    if not (IMDB_key and start_date and start_time and th_name):            #Borde de inte vara or?
        response.status = 400
        return format_response({"error: Missing parameter"})

    c = conn.cursor()
    query = """
            SELECT  capacity
            FROM    theaters
            WHERE   th_name = ?
            """
    c.execute(
        query,
        [th_name]
    )
    remaining_seats = c.fetchall()[0][0] #-1
    print(remaining_seats)

    c.execute(
        """
        INSERT 
        INTO    performances(IMDB_key, th_name, start_date, start_time, remaining_seats)
        VALUES  (?, ?, ?, ?, ?)
        """,
        [IMDB_key, th_name, start_date, start_time, remaining_seats]
    )
    conn.commit()
    c.execute(
        """
        SELECT * 
        FROM performances
        WHERE rowid = last_insert_rowid()
        """
    )
    rows = c.fetchall()
    per_id = [x[0] for x in rows]

    response.status = 200
    return '\nperformances/' + per_id[0] + '\n'

"""
    response.status = 200
    #return format_response({"id": id})#"url": url(f"/performances/{id}")})

    s = [{"IMDB_key": IMDB_key, "th_name": th_name, "start_date": start_date, "start_time": start_time, "remaining_seats": remaining_seats}
         for (IMDB_key, th_name, start_date, start_time, remaining_seats) in c]
    response.status = 200
    return format_response({"data": s})
"""

@post('/tickets')
def post_ticket():
    #?user=<user-id>\&performance=<performance-id>\&pwd=<pwd>
    response.content_type = 'application/json'
    user_name = request.query.user
    show_id = request.query.performance
    password = request.query.pwd

    print(user_name, show_id, password)

    if not (user_name and show_id and password):      #Borde de inte vara or?
        response.status = 400
        return format_response({"error: Missing parameter"})


    c = conn.cursor()
    query = """
            SELECT  remaining_seats, th_name, IMDB_key, start_time, start_date
            FROM    performances
            WHERE   show_id = ?
            """
    c.execute(
        query,
        [show_id]
    )

   
    
    data = c.fetchall()[0]

    
    remaining_seats = data[0]
    th_name = data[1]
    IMDB_key = data[2]
    start_time = data[3]
    start_date = data[4]

    query = """
            SELECT password
            FROM customers
            WHERE user_name = user_name;
            """
    c.execute(query)

    pwd = str(c.fetchall()[0][0])



    print(th_name, IMDB_key, start_time, start_date, user_name, show_id)
    if remaining_seats > 0 and pwd == hash(password):
        query = """
                UPDATE performances
                SET remaining_seats = ?
                WHERE show_id = show_id;
                """
        c.execute(
            query,
            [remaining_seats-1]
        )
        conn.commit()

        query = """
                INSERT 
                INTO    tickets(th_name, IMDB_key, start_time, start_date, user_name, show_id)
                VALUES  (?, ?, ?, ?, ?, ?)
                """
        c.execute(
            query,
            [th_name, IMDB_key, start_time, start_date, user_name, show_id]   
        )
        conn.commit()

        query = """
                SELECT ticket_id
                FROM tickets
                WHERE rowid = last_insert_rowid();
                """
        c.execute(query)
        returnID = str(c.fetchall()[0][0])
        return "/tickets/" + returnID
    elif pwd == hash(password):
        return "No tickets left"

    elif remaining_seats > 0:
        return "There is no user tied to that password"

    else:
        return "ERROR"


@get('customers/<customerID>/tickets')
def get_customers(customerID):
    print(customerID)
    response.content_type = 'application/json'
    print("hej")
    query = """
            SELECT start_date, start_time, th_name, title, year, count() as count
            FROM customers
            JOIN tickets
            USING (user_name)
            JOIN movies
            USING IMDB_key
            WHERE customerID = ?
            GROUP BY show_id
            """
    c = conn.cursor()
    c.execute(query,
              [customerID])
    print(1)

    s = [{"start_date": start_date, "start_time": start_time, "th_name": th_name, "title": title, "year": year, "count": count}
         for (start_date, start_time, th_name, title, year, count) in c]
    response.status = 200
    return format_response({"data": s})

        


def hash(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

run(host='localhost', port=7007)
