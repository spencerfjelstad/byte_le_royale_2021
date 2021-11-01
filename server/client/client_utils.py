import requests
import json


class ClientUtils:
    def __init__(self):
        self.IP = 'http://127.0.0.1:5000/api/'
        self.PORT = 5007

        self.commands = {
            'register': ['register', 'r'],
            'submit': ['submit', 's'],
            'help' : ['help', 'h'],
            'view': {
                'c': ['view stats', 'view', 'v'],
                'f': {
                    
                }
            },
            'leaderboard': {
                'c': ['leaderboard', 'l'],
                'f': {
                    'a': ['all', 'a'],
                    'e': ['elligible', 'e'],
                    'o': ['score_over_time', 'over', 'o']
                }
            }
        }
    def get_team_types(self):
        resp = requests.get(self.IP + "get_team_types")
        return json.loads(resp.content)

    def get_unis(self):
        resp = requests.get(self.IP + "get_unis")
        return json.loads(resp.content)

    def register(self, reg_data):
        resp = requests.post(self.IP + "register", reg_data)
        return resp

    def submit_file(self, file, vid):
        data = {"file": file, "vid": vid}
        resp = requests.post(self.IP + "submit", json=data)
        return resp

    def get_leaderboard(self, include_inelligible, sub_id):
        data = {"include_inelligible": include_inelligible, "sub_id": sub_id}
        resp = requests.post(self.IP + "get_leaderboard", json=data)
        jsn = json.loads(resp.content)
        print("The following is the leaderboard for eligible contestants")
        self.to_table(jsn)

    def get_team_score_over_time(self, vid):
        resp = requests.post(
            self.IP + "get_team_score_over_time", json={"vid": vid})
        jsn = json.loads(resp.content)
        print("The following is your team's performance in each group run")
        self.to_table(jsn)

    def get_submission_stats(self, vid):
        resp = requests.post(
            self.IP + "get_submission_stats", json={"vid": vid})
        return json.loads(resp.content)

    def get_longest_cell_in_cols(self, json, json_atribs):
        col_longest_length = {}
        for key in json_atribs:
            col_longest_length[key] = (len(key))
        for col in json_atribs:
            for row in json:
                if len(str(row[col])) > col_longest_length[col]:
                    col_longest_length[col] = len(row[col])
        return col_longest_length

    def get_seperator_line(self, col_longest_length, padding):
        rtn = ""
        for key in col_longest_length:
            rtn += "+" + ("-" * (col_longest_length[key] + padding))
        return rtn + "+"

    def to_table(self, json):
        padding = 4
        json_atribs = json[0].keys()
        col_longest_length = self.get_longest_cell_in_cols(json, json_atribs)
        line_seperator = self.get_seperator_line(col_longest_length, padding)
        row_format = ""
        for key in json_atribs:
            row_format += "|{:^" + str(col_longest_length[key] + padding) + "}"
        row_format += "|"
        print(line_seperator)
        print(row_format.format(*json_atribs))
        for row in json:
            print(line_seperator)
            print(row_format.format(*row.values()))
        print(line_seperator)
