import os
import requests
import datetime
import hashlib
import json
import queries


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

#Read user's api keys from .env file
dev = os.getenv('DEVID')
authkey = os.getenv('AUTHKEY')
endpoint = "https://api.smitegame.com/smiteapi.svc/"

  
# Create session to the api
# To create a session you need to create a signature and you will need to create a signature for every API request.
# A signature is the dev ID, the querry, the authentication key, and the current time written as yyMMddmmss combined then hased with MD5 algorithm.
# A signature will need to be made for every request but a session needs to made once until it expires.
#------------------------------------------------------------------------------
def getTimeStamp():
    ts = datetime.datetime.strftime(datetime.datetime.utcnow() ,"%Y%m%d%H%M%S")
    ts = int((ts.split(".")[0]))
    return ts

def create_signature(querry):
    signature = dev + querry + authkey + str(getTimeStamp())
    signature = hashlib.md5(signature.encode())
    return signature.hexdigest()

def create_session_id():
    signature = create_signature("createsession")
    endpointURL = endpoint + "createsessionJson/" + dev + "/" + signature +"/" + str(getTimeStamp())
    r = requests.get(url= endpointURL)
    data = r.json()
    return(data['session_id'])

# Ping method to test connection
def ping():
    url = endpoint + "/pingjson"
    r = requests.get(url=url)
    data = r.json()
    print(data)
#------------------------------------------------------------


def main():
    #Create session ID
    session_id = create_session_id()

    #Check if there is a file holding the match ID's else tell user there is not.
    if os.path.isfile("matchID.txt"):
        # If there is a file with match ID's then read the file.
        with open("matchID.txt","r") as f:
            lines=f.read().split("\n")
            matchList = []
            # Break the match ID's into groups of 10.
            for i in range(0,len(lines),10):
                matchList.append(lines[i:i+10])
                data = []  # Empty list to hold game info
                # Cycle through the match ID's in groups of 10
                for alist in matchList:
                    matchString = alist[0]
                    # Format the group of 10 ID's so they can be added to the request
                    for i in alist[1:]:
                        matchString += "," +i
                    # This is the actual request for match ID's data. 
                    URL = endpoint + "getmatchdetailsbatch"+"Json/" + dev + "/" + create_signature("getmatchdetailsbatch") + \
                            "/" + session_id + "/" + str(getTimeStamp()) + "/" + matchString
                    r = requests.get(url=URL).json() # r contains a list of dictionaries of match data
                    print(URL)
                    # Since the API returns data for up to 10 matches per a request,
                    # each game's data needs to be added to a variable out side the loop.
                    for i in r:
                        data.append(i)
                    # Then write that variable to a text file.
                    with open("multiple.txt", "a+") as f:
                        f.write(json.dumps(data, indent=4))
    else:
        print("Missing match ID text file")


if __name__ == "__main__":
    main()
