import os, shutil
import psycopg2
import subprocess
import json
import platform
import zipfile
from psycopg2.extras import RealDictCursor
from joblib import Parallel, delayed
import asyncio
import random

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

        self.NUMBER_OF_RUNS_FOR_CLIENT = 5
        self.index_to_seed_id = {}
        #self.loop.run_in_executor(None, self.await_input)
        #self.loop.call_later(5, self.external_runner())
        # try:
        #     self.loop.run_forever()
        # except KeyboardInterrupt:
        #     self.close_server()


    def external_runner(self):
        clients = self.fetch_clients()
        self.group_id = self.insert_new_group_run()

        if not os.path.exists(f'server/temp'):
            os.mkdir(f'server/temp')
        if not os.path.exists(f'server/temp/seeds'):
            os.mkdir(f'server/temp/seeds')

        for index in range(self.NUMBER_OF_RUNS_FOR_CLIENT):
            path = f'server/temp/seeds/{index}'
            os.mkdir(path)
            shutil.copy('launcher.pyz', path)
            self.run_runner(path, "server/runners/generator")
            fltext = ""
            with open(f'{path}/logs/game_map.json') as fl:
                fltext = fl.readlines()
            self.index_to_seed_id[index] = self.insert_seed_file(fltext)


        # run each client 5 times, then run them in paralell using their index as a unique identifier
        clients = clients * self.NUMBER_OF_RUNS_FOR_CLIENT
        res = Parallel(n_jobs = 5, backend="threading")(map(delayed(self.internal_runner), clients, [i for i in range(len(clients))]))
        shutil.rmtree("server/temp/seeds")

    def internal_runner(self, row, index):
        score = 0
        error = ""
        print(index)
        try:
            # Run game
            #self.log(f'Running client: {client}')
            end_path = f'server/temp/{index}'
            if not os.path.exists(end_path):
                os.mkdir(end_path)
            
            shutil.copy('launcher.pyz', end_path)

            with open(f'{end_path}/client_{index}.py', 'w') as f:
                f.write(row['file_text'])

            seed_index = int(index / self.NUMBER_OF_RUNS_FOR_CLIENT)

            
            shutil.copy(f'server/temp/seeds/{seed_index}/logs/game_map.json', f'{end_path}/game_map.json')

            if os.path.exists(f"server/temp/seeds/{seed_index}/logs/game_map.json"):
                os.mkdir(f"{end_path}/logs")
                shutil.copyfile(f"server/temp/seeds/{seed_index}/logs/game_map.json", f"{end_path}/logs/game_map.json")

            res = self.run_runner(end_path, "server/runners/runner")

            results = dict()
            seed = ""
            if os.path.exists(end_path + '/logs/results.json'):
                with open(end_path + '/logs/results.json', 'r') as f:
                    results = json.load(f)
                score = results['player']['truck']['renown'] 

            # Save best log files? doesn't seem necessary (yet)

            if 'Error' in results and results['Error'] is not None:
                print("Run had error")
                error = results['Error']

                
            shutil.rmtree(end_path)

            #self.current_running.insert(0, number)
            f.close()
        finally:
            self.insert_run(row["submission_id"], score, self.group_id, error, self.index_to_seed_id[seed_index])

    def fetch_clients(self):
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT * FROM fetch_latest_clients()")
        return cur.fetchall()

    def run_runner(self, end_path, runner):
        # Copy and run proper file
        f = open(os.devnull, 'w')
        if platform.system() == 'Linux':
            shutil.copy( runner + '.sh', f"{end_path}/runner.sh")
            p = subprocess.Popen('bash runner.sh', stdout=f, cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
        else:
            #server/runner.bat
            shutil.copy(runner + '.bat', f"{end_path}/runner.bat")
            p = subprocess.Popen('runner.bat', stdout=f, cwd=end_path, shell=True)
            stdout, stderr = p.communicate()

    def insert_new_group_run(self):
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT insert_group_run()")
        self.conn.commit()
        return cur.fetchall()[0]["insert_group_run"]

    def insert_seed_file(self, seed):
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT insert_seed(%s)", seed)
        self.conn.commit()
        return cur.fetchall()[0]["insert_seed"]

    def insert_run(self, subid, score, groupid, error, seed_id):
        cur = self.conn.cursor()
        cur.execute("CALL insert_run(%s,%s,%s, %s, %s)", (subid, score, groupid, error, seed_id))
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
