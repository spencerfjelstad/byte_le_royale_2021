from flask import Flask, jsonify
from flask.wrappers import Request
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import request
from requests.models import HTTPError
import uuid, json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

db_conn = {}
with open('./conn_info.json') as fl:
    db_conn = json.load(fl)

conn = psycopg2.connect(
    host="localhost",
    database = db_conn["database"],
    user= db_conn["user"],
    password=db_conn["password"]
)

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


@app.route("/api/get_leaderboard", methods = ['post'])
def get_leaderboard():
    ell = request.json["include_inelligible"]
    sub_id = request.json["sub_id"]
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_leaderboard(%s, %s)).*", (ell, sub_id))
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

@app.route("/api/get_submissions_for_team", methods = ['post'])
def get_submissions_for_team():
    vid = request.json["vid"]
    cur = conn.cursor()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_submissions_for_team(%s)).*", (vid,))
    return jsonify(cur.fetchall())

@app.route("/api/get_file_from_submission", methods = ['post'])
def get_file_from_submission():
    vid = request.json["vid"]
    subid = request.json["submissionid"]
    cur = conn.cursor()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT get_file_from_submission(%s, %s)", (vid,subid))
    return cur.fetchone()["get_file_from_submission"]

@app.route("/api/get_runs_for_submission", methods = ['post'])
def get_runs_for_submission():
    vid = request.json["vid"]
    subid = request.json["submissionid"]
    cur = conn.cursor()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_runs_for_submission(%s, %s)).*", (vid,subid))
    return jsonify(cur.fetchall())

@app.route("/api/get_group_runs", methods = ['post'])
def get_group_runs():
    vid = request.json["vid"]
    subid = request.json["submissionid"]
    cur = conn.cursor()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT (get_runs_for_submission(%s, %s)).*", (vid,subid))
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
