from textwrap import indent
import main
import requests
import logger
import json
import pprint

dev = main.dev
session_id = main.session_id
endpoint = main.endpoint
def setVars():
    print(main.dev,main.session_id,main.endpoint)
    dev = main.dev
    session_id = main.session_id
    endpoint = main.endpoint

def getleagueleaderboard(queue):
    URL = endpoint + "getleagueleaderboardjson" + "/" + dev + "/" + main.create_signature("getleagueleaderboard") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + queue \
        + "/" + "27" + "/" + "1"
    print(URL)
    r = requests.get(url=URL)
    data = r.json()
    logger.write_queue_response(json.dumps(data, indent=4))


def getqueuestats(player,queue):
    URL = endpoint + "getqueuestatsjson" + "/" + dev + "/" + main.create_signature("getqueuestats") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + \
                    str(get_playerID()) + "/" + queue
    r = requests.get(url=URL)
    data = r.json()
    logger.write_queue_response(json.dumps(data, indent=4))

def getleagueseasons(queue):
    URL = endpoint + "getleagueseasonsjson" + "/" + dev + "/" + main.create_signature("getleagueseasons") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + queue
    r = requests.get(url=URL)
    data = r.json()
    logger.write_queue_response(json.dumps(data, indent=4))

def getmatchidsbyqueue(queue):
    URL = endpoint + "getmatchidsbyqueuejson" + "/" + dev + "/" + main.create_signature("getmatchidsbyqueue") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + queue \
                        + "/" + "20220409" + "/" + "12"
    r = requests.get(url=URL)
    data = r.json()
    logger.write_queue_response(json.dumps(data, indent=4))

def getmatchhistory(player):
    URL = endpoint + "getmatchhistoryjson" + "/" + dev + "/" + main.create_signature("getmatchhistory") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + str(get_playerID())
    r = requests.get(url=URL)
    data = r.json()
    logger.write_history_response(json.dumps(data, indent=4))

def getmatchdetailsbatch(matchList):
    data = []
    for alist in matchList:
        matchString = alist[0]
        for i in alist[1:]:
            matchString += "," +i
        URL = endpoint + "getmatchdetailsbatch"+"Json/" + dev + "/" + main.create_signature("getmatchdetailsbatch") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + matchString
        #r = requests.get(url=URL, verify=False).json()
        r = requests.get(url=URL).json() # r contains a list of dictionaries of match data
        print(URL)
        for i in r:
            data.append(i)

    logger.write_match_response(json.dumps(data, indent=4))

# Player related querries
def getplayer(player):
    URL = endpoint + "getplayerjson" + "/" + dev + "/" + main.create_signature("getplayer") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + player
    print(URL)
    r = requests.get(url=URL)
    print(r)
    data = r.json()
    #pprint.pprint(data)
    logger.write_player_response(json.dumps(data, indent=4))

def get_playerID():
    f = open("player.txt", "r+").read()
    j = json.loads(f)
    for i in j:
        playerID = i["ActivePlayerId"]
    if playerID != None:
        return playerID
    else:
        return None

def get_match_reports_for_league():
    with open("game match ids\matchID.txt","r") as f:
        lines=f.read().split("\n")
        matchList = []
        for i in range(0,len(lines),10):
            matchList.append(lines[i:i+10])
        getmatchdetailsbatch(matchList)

def get_getmatchhistory(player):
    URL = endpoint + "getmatchhistoryjson" + "/" + dev + "/" + main.create_signature("getmatchhistory") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + player
    print(URL)
    r = requests.get(url=URL)
    data = r.json()
    logger.write_player_response(json.dumps(data, indent=4))

def get_clanplayers(clan): #Wyerd
    URL = endpoint + "getteamplayersjson" + "/" + dev + "/" + main.create_signature("getteamplayers") + "/" + session_id + "/" + str(main.getTimeStamp()) + "/" + clan
    print(URL)
    r = requests.get(url=URL)
    data = r.json()
    logger.write_team_response(json.dumps(data, indent=4))
