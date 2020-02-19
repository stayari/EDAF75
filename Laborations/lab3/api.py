from bottle import get
from bottle import run
import sqlite3
import json

conn = sqlite3.connect("applications.sqlite")

@get('/ping')
def return_pong():
    return "pong"




run(host='localhost', port=7007)