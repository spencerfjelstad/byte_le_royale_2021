import os, shutil
import psycopg2
import subprocess
import json
import platform
import zipfile
from psycopg2.extras import RealDictCursor
from joblib import Parallel, delayed
import asyncio

class client_runner:

    def __init__(self):
        self.temp = ""
        self.conn = psycopg2.connect(
        host="localhost",
        database="ByteLeRoyaleDB",
        user="postgres",
        password="password")
        self.loop = asyncio.get_event_loop()
        #self.loop.run_in_executor(None, self.await_input)
        #self.loop.call_later(5, self.external_runner())
        # try:
        #     self.loop.run_forever()
        # except KeyboardInterrupt:
        #     self.close_server()


    def external_runner(self):
        clients = self.fetch_clients()
        group_id = self.insert_new_group_run()
        res = Parallel(n_jobs = 1, backend="threading")(map(delayed(self.internal_runner), clients))


    def internal_runner(self, row):
        # Run game
        #self.log(f'Running client: {client}')
        teamid = row['teamid']
        if not os.path.exists(f'scrimmage/temp'):
            os.mkdir(f'scrimmage/temp')
        end_path = f'scrimmage/temp/{row["submissionid"]}'
        if not os.path.exists(end_path):
            os.mkdir(end_path)
        
        shutil.copy('launcher.pyz', end_path)

        with open(f'{end_path}/{row["teamid"]}', 'wb') as f:
            f.write(row['filetext'])

        # Copy and run proper file
        f = open(os.devnull, 'w')
        if platform.system() == 'Linux':
            shutil.copy('scrimmage/runner.sh', end_path)
            p = subprocess.Popen('bash runner.sh', stdout=f, cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
        else:
            shutil.copy('scrimmage/runner.bat', end_path)
            p = subprocess.Popen('runner.bat', stdout=f, cwd=end_path, shell=True)
            stdout, stderr = p.communicate()

        results = dict()
        with open(end_path + '/logs/results.json', 'r') as f:
            results = json.load(f)

        score = results['player']['truck']['renown']

        self.insert_score()

        #entry = [x for x in self.db_collection.find({'_id': client})][0]

        #self.db_collection.update_one({'_id': client}, {'$set': {'best_run': score}})

        # Save best log files? doesn't seem necessary (yet)

        if 'Error' in results and results['Error'] is not None:
            #self.db_collection.update_one({'_id': client}, {'$set': {'error': results['Error']}})
            print("TODO Add error")

        shutil.rmtree(end_path)

        #self.current_running.insert(0, number)
        f.close()

    def fetch_clients(self):
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT * FROM fetch_latest_clients()")
        return cur.fetchall()

    def insert_new_group_run(self):
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT insert_group_run()")
        return cur.fetchall()

    def close_server(self):
        self.loop_continue = False

        while True:
            try:
                if os.path.exists('scrimmage/temp'):
                    shutil.rmtree('scrimmage/temp')
                break
            except PermissionError:
                continue
        while True:
            try:
                if os.path.exists('scrimmage/vis_temp'):
                    shutil.rmtree('scrimmage/vis_temp')
                break
            except PermissionError:
                continue

        self.server.close()

        os._exit(0)

        
if __name__ == "__main__":
    client_runner().external_runner()
