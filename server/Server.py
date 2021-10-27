from flask import Flask, jsonify
from flask.wrappers import Request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request
from requests.models import HTTPError
import uuid

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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
    cur.execute("SELECT (get_universities()).*")
    return jsonify(cur.fetchall())

@app.route("/api/get_team_types", methods = ['get'])
def get_team_types():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_team_types()).*")
    return jsonify(cur.fetchall())

@app.route("/api/get_teams", methods = ['get'])
def get_teams():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_teams()).*")
    return jsonify(cur.fetchall())


@app.route("/api/get_eligible_leaderboard", methods = ['get'])
def get_eligible_leaderboard():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_eligible_leaderboard()).*")
    return jsonify(cur.fetchall())

@app.route("/api/get_entire_leaderboard", methods = ['get'])
def get_entire_leaderboard():
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_entire_leaderboard()).*")
    return jsonify(cur.fetchall())

@app.route("/api/get_submission_stats", methods = ['post'])
def get_stats():
    vid = request.json["vid"]
    cur = conn.cursor()
    cur.execute("SELECT (get_latest_submission(%s)).*", (vid,))
    res = cur.fetchone()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_stats_for_submission(%s, %s)).*", res)
    return jsonify({"data": cur.fetchall(), "sub_id" : res[0], "run_group_id" : res[1]})

@app.route("/api/get_team_score_over_time", methods = ['post'])
def get_team_score_over_time():
    vid = request.json["vid"]
    cur = conn.cursor()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_team_score_over_time(%s)).*", (vid,))
    return jsonify(cur.fetchall())

@app.route("/api/register", methods = ['POST'])
def insert_team():
    teamtype = request.form.get("type")
    name = request.form.get("name")
    uni = request.form.get("uni")
    cur = conn.cursor()
    cur.execute("SELECT insert_team(%s, %s, %s)", (teamtype, name, uni))
    conn.commit()
    return cur.fetchone()[0]

@app.route("/api/submit", methods = ['POST'])
def submit_file():
    file = request.json["file"]
    vid = request.json["vid"]
    bad_words = check_illegal_keywords(file)
    if bad_words:
        return HTTPError("Contained illegal keywords {0}".format(bad_words))
    cur = conn.cursor()
    cur.execute("CALL submit_code_file(%s, %s)", (file, vid))
    conn.commit()
    return "True"

def check_illegal_keywords(file):
    '''This should be expanded on, made better'''
    bad_words_list = ['open', 'os', 'import']
    rtn_bad_words = []
    for bad_word in rtn_bad_words:
        if bad_word in file:
            rtn_bad_words.append(bad_word)
