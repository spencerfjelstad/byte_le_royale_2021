from flask import Flask, jsonify
from flask.wrappers import Request
import psycopg2
from psycopg2.extras import RealDictCursor
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


@app.route("/api/get_unis", methods = ['get'])
def get_unis():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT uniid, uniname FROM university")
    return jsonify(cur.fetchall())

@app.route("/api/get_team_types", methods = ['get'])
def get_team_types():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT teamtypeid, teamtypename FROM teamtype")
    return jsonify(cur.fetchall())

@app.route("/api/get_teams", methods = ['get'])
def get_teams():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT teamname, uniname, teamtypename FROM team JOIN university ON team.uniid = university.uniid JOIN teamtype ON team.teamtypeid = teamtype.teamtypeid")
    return jsonify(cur.fetchall())

@app.route("/api/register", methods = ['POST'])
def insert_team():
    teamtype = request.form.get("type")
    name = request.form.get("name")
    uni = request.form.get("uni")
    cur = conn.cursor()
    cur.execute("INSERT INTO team (teamtypeid, teamname, uniid) VALUES ('{}', '{}', {})  RETURNING teamid".format(teamtype, name, uni))
    return cur.fetchone()[0]