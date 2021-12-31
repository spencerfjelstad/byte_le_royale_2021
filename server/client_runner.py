import os, shutil
from typing import NewType
import psycopg2
import subprocess
import json
import platform
import zipfile
from psycopg2.extras import RealDictCursor
from joblib import Parallel, delayed
import asyncio

from tqdm import std
import time

class client_runner:

    def __init__(self):

        db_conn = {}
        with open('./server/conn_info.json') as fl:
            db_conn = json.load(fl)

        self.conn = psycopg2.connect(
            host="localhost",
            database=db_conn["database"],
            user=db_conn["user"],
            password=db_conn["password"]
        )
        self.loop = asyncio.get_event_loop()

        # The group run ID. will be set by insert_new_group_run
        self.group_id = 0

        self.NUMBER_OF_RUNS_FOR_CLIENT = 5

        self.SLEEP_TIME_SECONDS_BETWEEN_RUNS = 150

        self.tpc_id = -1

        # Maps a seed_index to a database seed_id
        self.index_to_seed_id = {}
        
        self.version = self.get_version_number()


        # self.loop.run_in_executor(None, self.await_input)
        # self.loop.call_later(5, self.external_runner())
        try:
            while True:
                self.tpc_id = self.conn.xid(1,"1","branch_qualifier")
                self.conn.tpc_begin(self.tpc_id)
                self.external_runner()
                self.conn.tpc_prepare()
                self.conn.tpc_commit()
                print(f"Sleeping for {self.SLEEP_TIME_SECONDS_BETWEEN_RUNS} seconds")
                time.sleep(150)
        except (KeyboardInterrupt, Exception) as e:
            print("Ending server due to {0}".format(e))
            self.close_server()


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

        # repeat the clients list by the number of times defined in the constant
        clients = clients * (self.NUMBER_OF_RUNS_FOR_CLIENT)
 
        #then run them in paralell using their index as a unique identifier
        res = Parallel(n_jobs = 5, backend="threading")(map(delayed(self.internal_runner), clients, [i for i in range(len(clients))]))
        shutil.rmtree("server/temp/seeds")

    def internal_runner(self, row, index):
        score = 0
        error = ""
        print("running run {0} for submission {1}".format(index, row["submission_id"]))
        try:
            # Run game
            # Create a folder for this client and seed
            end_path = f'server/temp/{index}'
            if not os.path.exists(end_path):
                os.mkdir(end_path)
            
            shutil.copy('launcher.pyz', end_path)

            # Write the client into the folder
            with open(f'{end_path}/client_{index}.py', 'w') as f:
                f.write(row['file_text'])

            # Determine what seed this run needs based on it's serial index
            seed_index = int(index / self.NUMBER_OF_RUNS_FOR_CLIENT)

            # Copy the seed into the run folder
            if os.path.exists(f"server/temp/seeds/{seed_index}/logs/game_map.json"):
                os.mkdir(f"{end_path}/logs")
                shutil.copyfile(f"server/temp/seeds/{seed_index}/logs/game_map.json", f"{end_path}/logs/game_map.json")

            res = self.run_runner(end_path, "server/runners/runner")

            results = dict()
            if os.path.exists(end_path + '/logs/results.json'):
                with open(end_path + '/logs/results.json', 'r') as f:
                    results = json.load(f)
            
            # CHANGE THIS LINE TO GET CORRECT SCORE FOR GAME
            score = results['player']['truck']['renown']

            # Save best log files? doesn't seem necessary (yet)

            if 'Error' in results and results['Error'] is not None:
                print("Run had error")
                error = results['Error']

                
            shutil.rmtree(end_path)

            #self.current_running.insert(0, number)
            f.close()
        finally:
            breakpoint()
            self.insert_run(row["submission_id"], score, self.group_id, error, self.index_to_seed_id[seed_index])

    def fetch_clients(self):
        '''
        Returns the latest clients for every team
        '''
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT * FROM fetch_latest_clients()")
        return cur.fetchall()

    def run_runner(self, end_path, runner):
        '''
        runs a script in the runner folder. 
        end path is where the runner is located
        runner is the name of the script (no extension) 
        '''
        f = open(os.devnull, 'w')
        if platform.system() == 'Linux':
            shutil.copy( runner + '.sh', f"{end_path}/runner.sh")
            p = subprocess.Popen('bash runner.sh', stdout=f, cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            return stdout
        else:
            #server/runner.bat
            shutil.copy(runner + '.bat', f"{end_path}/runner.bat")
            p = subprocess.Popen('runner.bat', stdout=f, cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            return stdout


    def get_version_number(self):
        '''
        runs a script in the runner folder. 
        end path is where the runner is located
        runner is the name of the script (no extension) 
        '''
        
        stdout = ""
        if platform.system() == 'Linux':
            p = subprocess.Popen('server/runners/version.sh',stdout=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
        else:
            p = subprocess.Popen('runner.bat', stdout=f, shell=True)
            stdout, stderr = p.communicate()
        return stdout.decode("utf-8") 

            

    def insert_new_group_run(self):
        '''
        Inserts a new group run. Relates all the runs in this process together
        '''
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT insert_group_run(%s, %s)", (self.version, self.NUMBER_OF_RUNS_FOR_CLIENT))
        return cur.fetchall()[0]["insert_group_run"]

    def insert_seed_file(self, seed):
        '''
        inserts the seed file into the database. 
        Returns it's seed_id
        '''
        cur = self.conn.cursor(cursor_factory= RealDictCursor)
        cur.execute("SELECT insert_seed(%s)", seed)
        return cur.fetchall()[0]["insert_seed"]

    def insert_run(self, subid, score, groupid, error, seed_id):
        '''
        Inserts a run into the DB
        '''
        cur = self.conn.cursor()
        cur.execute("CALL insert_run(%s,%s,%s, %s, %s)", (subid, score, groupid, error, seed_id))

    def start_transaction(self):
        print("starting transaction")
    
    def commit_transaction(self):
        print("committing transaction")

    def rollback_transaction(self):
        print("starting transaction")

    def close_server(self):
        self.conn.tpc_prepare()
        self.conn.tpc_rollback()
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
        os._exit(0)

        
if __name__ == "__main__":
    client_runner().external_runner()
