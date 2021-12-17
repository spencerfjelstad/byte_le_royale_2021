import os
import shutil
import psycopg2
import subprocess
import json
import platform
import zipfile
from psycopg2.extras import RealDictCursor
from joblib import Parallel, delayed
import asyncio
import random
import time

if __name__ == "__main__":
    db_conn = {}
    with open('./server/conn_info.json') as fl:
        db_conn = json.load(fl)

    conn = psycopg2.connect(
        host="localhost",
        database=db_conn["database"],
        user=db_conn["user"],
        password=db_conn["password"]
    )

    tpc_id = conn.tpc_recover()
    conn.tpc_rollback(tpc_id[0])
