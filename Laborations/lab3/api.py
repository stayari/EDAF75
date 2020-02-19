from bottle import get
from bottle import run
import sqlite3
import json

conn = sqlite3.connect("applications.sqlite")

@get('/students')
def get_students():
    c = conn.cursor()
    c.execute(
        """
        SELECT s_id, s_name, gpa, size_hs
        FROM   students
        """
    )
    s = [{"id": id, "name": name, "gpa": gpa, "hsSize": hs_size}
         for (id, name, gpa, hs_size) in c]
    return json.dumps({"data": s}, indent=4)


run(host='localhost', port=7007)