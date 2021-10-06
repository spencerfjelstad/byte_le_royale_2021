from flask import Flask
from flask.wrappers import Request
import psycopg2
from flask import request

app = Flask(__name__)

conn = psycopg2.connect(
    host="localhost",
    database="ByteLeRoyaleDB",
    user="postgres",
    password="password")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/register", methods = ['POST'])
def insert_team():
    teamtype = request.form.get("type")
    name = request.form.get("name")
    uni = request.form.get("uni")
    cur = conn.cursor()
    cur.execute("INSERT INTO team (teamtype, teamname, uniid) VALUES ('{}', '{}', {})".format(teamtype, name, uni))
    cur.close()
    conn.commit()
    return "True"