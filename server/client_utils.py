import requests
import json

class ClientUtils:
    def __init__(self):
        self.IP = 'http://127.0.0.1:5000/api/'
        self.PORT = 5007

        self.REGISTER_COMMANDS = ['register', 'r']
        self.SUBMIT_COMMANDS = ['submit', 's']
        self.VIEW_STATS_COMMANDS = ['view stats', 'view', 'v']
        self.LEADERBOARD_COMMANDS = ['leaderboard', 'l']

    def get_team_types(self):
        resp = requests.get(self.IP + "get_team_types")
        return json.loads(resp.content)

    def get_unis(self):
        resp = requests.get(self.IP + "get_unis")
        return json.loads(resp.content)

    def register(self, reg_data):
        resp = requests.post(self.IP + "register", reg_data)
        return resp

    def to_table(self,json):
        json_atribs = json[0].keys()
        row_format ="{:>20}" * (len(json_atribs))
        print(row_format.format(*json_atribs))
        for row in json:
            print(row_format.format(*row.values()))
