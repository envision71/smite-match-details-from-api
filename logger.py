import os
import main
import queries
import json
import csv
import sheetAPI

def write_stats(data):
    fields = ["God","playername","kills","deaths","assists","player damage","minion damage","structure damage","Damage Mitigated","healing","wards"]
    with open ("stats.csv", "a",encoding='utf-8') as f:
        csvwriter = csv.writer(f, delimiter=",")
        csvwriter.writerow(data)
    pass

def write_to_sheets(data):
    sheetAPI.add_data(data)

def write_match_response(data):
    with open("response.txt", "a+") as f:
        f2data = '\n' + f.read()
        f.write(data)
    pass


def write_player_response(data):
    with open("player.txt", "w") as f:
        f.write(data)
    pass

def write_history_response(data):
    with open("history.txt", "w") as f:
        f.write(data)
    pass

def write_queue_response(data):
    with open("queue.txt", "w") as f:
        f.write(data)
    pass

def write_team_response(data):
    with open("team.txt", "w") as f:
        f.write(data)
    pass