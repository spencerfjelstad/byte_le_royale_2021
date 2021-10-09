import asyncio
import os

#from game.config import CLIENT_DIRECTORY, CLIENT_KEYWORD
from client_utils import ClientUtils

CLIENT_DIRECTORY = ""
CLIENT_KEYWORD = ""


class Client:
    def __init__(self):
        self.utils = ClientUtils()
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.handle_client())

    # Determines what action the client wants to do
    async def handle_client(self):
        out = f'Select an action:\n'
        out += f'Register: {self.utils.REGISTER_COMMANDS}\n'
        out += f'Submit client: {self.utils.SUBMIT_COMMANDS}\n'
        out += f'View stats: {self.utils.VIEW_STATS_COMMANDS}\n'
        out += f'Check leaderboard: {self.utils.LEADERBOARD_COMMANDS}\n'
        print(out)
        command = input('Enter: ')

        if command not in self.utils.REGISTER_COMMANDS + self.utils.SUBMIT_COMMANDS + self.utils.VIEW_STATS_COMMANDS + self.utils.LEADERBOARD_COMMANDS:
            print('Not a recognized command.')
            return

        await asyncio.sleep(0.1)

        if command in self.utils.REGISTER_COMMANDS:
            await self.register()
        elif command in self.utils.SUBMIT_COMMANDS:
            await self.submit()
        elif command in self.utils.VIEW_STATS_COMMANDS:
            await self.get_stats()
        elif command in self.utils.LEADERBOARD_COMMANDS:
            await self.get_leaderboard()

    async def register(self):
        # Check if vID already exists and cancel out
        if os.path.isfile('vID'):
            print('You have already registered.')
            return

        # Ask for teamname
        teamname = input("Enter your teamname: ")

        if teamname == '':
            print("Teamname can't be empty.")
            return

        unis = self.utils.get_unis()

        print("Select a university (id)")
        self.utils.to_table(unis)

        uniid = int(input())

        if uniid not in map(lambda x : x['uniid'] ,unis):
            print("Not a valid uni id")
            return

        team_types = self.utils.get_team_types()

        print("Select a team type (id)")
        self.utils.to_table(team_types)

        team_type = int(input())

        if team_type not in map(lambda x : x['teamtypeid'] ,team_types):
            print("Not a valid team type")
            return

        response = self.utils.register({"type": team_type, "uni" : uniid, "name" : teamname})

        if not response.ok:
            print('Teamname contains illegal characters or is already taken.')
            return

        # Receive uuid
        # vID = await self.reader.read(BUFFER_SIZE)
        # vID = vID.decode()

        v_id = response.content
        if v_id == '':
            print('Something broke.')
            return

        # Put uuid into file for verification (vID)
        with open('vID', 'w+') as f:
            f.write(str(v_id))

        print("Registration successful.")
        print("You have been given an ID file in your Byte-le folder. Don't move or lose it!")
        print("You can give a copy to your teammates so they can submit and view stats.")

    async def submit(self):
        cont = await self.verify()

        if cont == 'False':
            print('Cannot submit at this time.')
            return

        # Check and verify client file
        file = None
        for filename in os.listdir(CLIENT_DIRECTORY):
            if CLIENT_KEYWORD.upper() not in filename.upper():
                # Filters out files that do not contain CLIENT_KEYWORD in their filename
                continue

            if os.path.isdir(os.path.join(CLIENT_DIRECTORY, filename)):
                # Skips folders
                continue

            user_check = input(f'Submitting {filename}, is this ok? (y/n): ')
            if 'y' in user_check.lower():
                file = filename
                break
        else:
            file = input('Could not find file: please manually type file name: ')

        if not os.path.isfile(file):
            print('File not found.')
            return

        # Send client file
        print('Submitting file.')
        f = open(file, 'rb')
        #line = f.read(BUFFER_SIZE)
        # while line:
        #     self.writer.write(line)
        #     line = f.read(BUFFER_SIZE)
        #     await self.writer.drain()

        print('File sent successfully.')

    async def get_stats(self):
        cont = await self.verify()

        if cont == 'False':
            print('Verification failure.')

        # Receive stats
        #stats = await self.reader.read(BUFFER_SIZE)
        #stats = stats.decode()
        #print(stats)

    async def get_leaderboard(self):
        cont = await self.verify()

        if cont == 'False':
            print('Verification failure.')

        # Receive leaderboard
        #lb = await self.reader.read(BUFFER_SIZE)
        #lb = lb.decode()
        #print(lb)

    async def verify(self):
        # Check vID for uuid
        if not os.path.isfile('vID'):
            print("Cannot find vID, please register first.")
            return

        tid = ''
        with open('vID', 'r') as f:
            tid = f.read()

        # Send uuid
        self.writer.write(tid.encode())
        await self.writer.drain()

        # Receive state of server
        #cont = await self.reader.read(BUFFER_SIZE)
        #cont = cont.decode()
        #return cont


if __name__ == '__main__':
    cli = Client()
