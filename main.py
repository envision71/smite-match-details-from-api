import os
from urllib import response
import requests
import datetime
import json
import csv
import hashlib


import queries
import logger
import response_reader
from dotenv import load_dotenv
load_dotenv()

# API Access Limits

# To throttle API Developer access various limits have been setup to prevent over use of the API (either intentional, more likely unintentional “over use”).

# Here are the default initial limitations for API Developers:

# concurrent_sessions:  50
# sessions_per_day: 500
# session_time_limit:  15 minutes
# request_day_limit:  7500
# queues pop every 6

dev = os.getenv('DEVID')
authkey = os.getenv('AUTHKEY')
endpoint = os.getenv('ENDPOINT')


timestamp = int(datetime.datetime.strftime( datetime.datetime.utcnow() + datetime.timedelta(minutes=15),"%Y%m%d%H%M%S"))
queueIDs = {426:"Conquest",435:"Qrena Queue",448:"Joust Queued [3v3]",445:"Assult",466:"Clash",10195:"Under 30 Arena",
                      504:"Conquest Ranked Controller",451:"Conquest Ranked",434:"MOTD",10193:"Under 30 Conquest",
                      10197:"Under 30 Joust",459:"Siege 4v4",503:"Joust 3v3 Ranked Controller",441:"Joust Challenege",
                      468:"Arena [va AI][Medium]",508:"Adventures ch11 Corrupted Arena v3",450:"Joust 3v3 Ranked",
                      456:"Joust [vs AI][Medium]",461:"Conquest[vs AI][Medium]",502:"Joust Ranked 1v1 Controller",
                      462:"Arena Tutorial",440:"Joust Ranked[1v1]",10190:"Duel Custom",10152:"S7 Joust Custom",
                      429:"Conquest Challenge",438:"Arena Challenge",10161:"Conquest [va AI][Hard]",10162:"Joust [vs AI][Very Hard]",
                      457:"Arena [vs AI][Very Easy]",10158:"Arena [vs AI][Very Hard]",476:"Conquest [vs AI][Easy]",
                      10177:"Clasic Joust Custom",474:"Joust [vs AI][Very Easy]",467:"Clash Challenge",472:"Arena Practice [Medium]",
                      443:"Arena Practice [Easy]",10167:"Arena Practice [Hard]",446:"Assult Challenge",478:"Clash [vs AI][Easy]",
                      469:"Clash [vs AI][Medium]",10160:"Clash [vs AI][Hard]",473:"Joust Practice [Medium]",
                      10171:"Joust Practice [Hard]",10159:"Assault [vs AI][Hard]",454:"Assault [va AI][Medium]",
                      10189:"Slash",460:"Siege Challenge",458:"Conquest Practice Easy",475:"Conquest Practice [Medium]",
                      10170:"Conquest Practice [Hard]",464:"Joust Practice [East]",10151:"Adventures Ch11 Corupted Arena",
                      479:"Assault Practice [Easy]",477:"Clash Practice [Medium]",470:"Clash Practice [Easy]",
                      10169:"Clash Practice [Hard]",480:"Assault Practice [Medium]",10168:"Assault Practice [Hard]",
                      10191:"Slash Custom",10201:"Slash Practice [Easy]",10198:"Slash [vs AI][Easy]",
                      10199:"Slash [vs AI][Medium]",10200:"Slash [vs AI][Hard]",10203:"Slash Practice [Hard]",
                      10202:"Slash Practice [Medium]",436:"Basic Tutorial" }
ranks = {1:"Bronze V",2:"Bronze IV",3:"Bronze III",4:"Bronze II",5:"Bronze I",
                    6:"Silver V",7:"Silver IV",8:"Silver III",9:"Silver II",10:"Silver I",
                    11:"Gold V",12:"Gold IV",13:"Gold III",14:"Gold II",15:"Gold I",
                    16:"Platinum V",17:"Platinum IV",18:"Platinum III",19:"Platinum II",20:"Platinum I",
                    21:"Diamond V",22:"Diamond IV",23:"Diamond III",24:"Diamond II",25:"Diamond I",
                    26:"Masters",27:"GrandMasters"}
portal_ids = {1:"Hirez",5:"Steam",9:"PS4",10:"Xbox",22:"Switch",25:"Discord",28:"Epic"}

def queue_id_conversion_int2str(id):
    if id in queueIDs:
        return(queueIDs[id])

def queue_id_conversion_str2int(id):
    if id in queueIDs.values():
        return list(queueIDs.keys())[list(queueIDs.values()).index(id)]

def portal_id_conversion_int2str(id):
    if id in portal_ids.values():
        return(portal_ids[id])

def portal_id_conversion_str2int(id):
    if id in portal_ids.values():
        return list(portal_ids.keys())[list(portal_ids.values()).index(id)]

def ranks_conversion_int2str(rank):
    if rank in ranks:
        return ranks[rank]

def ranks_conversion_str2int(rank):
    if rank in ranks.values():
        return list(ranks.keys())[list(ranks.values()).index(rank)]
    

# Create session
def create_signature(querry):
    signature = dev + querry + authkey + str(getTimeStamp())
    signature = hashlib.md5(signature.encode())
    return signature.hexdigest()

def create_session_id():
    global timestamp
    signature = create_signature("createsession")
    endpointURL = endpoint + "createsessionJson/" + dev + "/" + signature +"/" + str(getTimeStamp())
    # r = requests.get(url= endpointURL, verify=False)
    r = requests.get(url= endpointURL)
    data = r.json()
    return(data['session_id'])
    # global session_id
    # session_id = data['session_id']

def ping():
    url = endpoint + "/pingjson"
    r = requests.get(url=url)
    data = r.json()
    print(data)


def session_expired_check():
    if int(timestamp) >= int(datetime.datetime.strftime( datetime.datetime.utcnow() + datetime.timedelta(minutes=15),"%Y%m%d%H%M%S")):
        print(">=" + str(timestamp))
        create_session_id()
    else:
        print(timestamp)
        
def getTimeStamp():
    ts = datetime.datetime.strftime(datetime.datetime.utcnow() ,"%Y%m%d%H%M%S")
    ts = int((ts.split(".")[0]))
    return ts


def send_querry(querry):
    URL = endpoint + querry+"Json/" + dev + "/" + create_signature(querry) + "/" + session_id + "/" + str(getTimeStamp()) + "/1233435661"
    r = requests.get(url=URL)
    data = r.json()
    print(json.dumps(data, indent=4))
    logger.write_match_response(json.dumps(data, indent=4))
    
session_id=None
session_id = create_session_id()
def main():

    # queries.get_match_reports_for_league()
    # response_reader.read_multiple_response()


    #queries.getplayer("Tdog13")
    queries.get_clanplayers("700337698")
    #queries.get_getmatchhistory("Tdog13")
    #queries.getqueuestats("Tdog13","426")
    

if __name__ == "__main__":
    main()