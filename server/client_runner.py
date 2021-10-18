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
        self.group_id = 0
        #self.loop.run_in_executor(None, self.await_input)
        #self.loop.call_later(5, self.external_runner())
        # try:
        #     self.loop.run_forever()
        # except KeyboardInterrupt:
        #     self.close_server()


    def external_runner(self):
        clients = self.fetch_clients()
        self.group_id = self.insert_new_group_run()
        for i in range(1):
            res = Parallel(n_jobs = 1, backend="threading")(map(delayed(self.internal_runner), clients))


    def internal_runner(self, row):
        score = 0
        error = ""
        try:
            # Run game
            #self.log(f'Running client: {client}')
            team_id = row['team_id']
            if not os.path.exists(f'server/temp'):
                os.mkdir(f'server/temp')
            end_path = f'server/temp/{row["submission_id"]}'
            if not os.path.exists(end_path):
                os.mkdir(end_path)
            
            shutil.copy('launcher.pyz', end_path)

            with open(f'{end_path}/client_{row["team_id"]}.py', 'w') as f:
                f.write(row['file_text'])

            # Copy and run proper file
            f = open(os.devnull, 'w')
            if platform.system() == 'Linux':
                shutil.copy('server/runners/runner.sh', end_path)
                p = subprocess.Popen('bash runner.sh', stdout=f, cwd=end_path, shell=True)
                stdout, stderr = p.communicate()
            else:
                #server/runner.bat
                shutil.copy('server/runners/runner.bat', end_path)
                p = subprocess.Popen('runner.bat', stdout=f, cwd=end_path, shell=True)
                stdout, stderr = p.communicate()

            results = dict()
            if os.path.exists(end_path + '/logs/results.json'):
                with open(end_path + '/logs/results.json', 'r') as f:
                    results = json.load(f)
                score = results['player']['truck']['renown'] 

            # Save best log files? doesn't seem necessary (yet)

            if 'Error' in results and results['Error'] is not None:
                print("Run had error")
                error = results['Error']

                
            #shutil.rmtree(end_path)

            #self.current_running.insert(0, number)
            f.close()
        finally:
            self.insert_run(row["submission_id"], score, self.group_id, error)

    def fetch_clients(self):
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT * FROM fetch_latest_clients()")
        return cur.fetchall()

    def insert_new_group_run(self):
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT insert_group_run()")
        self.conn.commit()
        return cur.fetchall()[0]["insert_group_run"]

    def insert_run(self, subid, score, groupid, error):
        cur = self.conn.cursor()
        cur.execute("CALL insert_run(%s,%s,%s, %s)", (subid, score, groupid, error))
        self.conn.commit()

    def close_server(self):
        self.loop_continue = False

        while True:
            try:
                if os.path.exists('server/temp'):
                    shutil.rmtree('server/temp')
                break
            except PermissionError:
                continue
        while True:
            try:
                if os.path.exists('server/vis_temp'):
                    shutil.rmtree('server/vis_temp')
                break
            except PermissionError:
                continue

        self.server.close()

        os._exit(0)

        
if __name__ == "__main__":
    client_runner().external_runner()
