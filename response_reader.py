from pprint import pprint
import main
import queries
import logger
import json
from datetime import datetime
from datetime import timedelta
import pprint


def read_game(game):
    for i in game:
                #God,playername,picked, win,loss, w/l%, kills,deaths,assists,player damage,minion damage, structure damage, Damage Mitigated, healing, wards
        kills = i["Kills_Player"]
        deaths = i["Deaths"]
        assists = i["Assists"]
        
        if i["Win_Status"] == "Winner":
            picked = 1
            Win = 1
            Loss = 0
            WL = 100
        else:
            picked = 1
            Win = 0
            Loss = 1
            WL = 0

        if deaths != 0:
            KDA = round (((kills + (assists/2))/deaths),2)
        else:
            KDA = round (((kills + (assists/2))/1),2)
        if i["hz_player_name"] == None:
            stats = [i["Reference_Name"],i["hz_gamer_tag"], picked, Win, Loss, WL, i["Kills_Player"],  i["Deaths"], i["Assists"], KDA , i["Damage_Player"], \
                    i["Damage_Bot"], i["Structure_Damage"],  i["Damage_Mitigated"], i["Healing"], i["Wards_Placed"]]
        else:
            stats = [i["Reference_Name"],i["hz_gamer_tag"], picked, Win, Loss, WL, i["Kills_Player"],  i["Deaths"], i["Assists"], KDA , i["Damage_Player"], \
                    i["Damage_Bot"], i["Structure_Damage"],  i["Damage_Mitigated"], i["Healing"], i["Wards_Placed"]]
        logger.write_stats(stats)    

def read_single_response():
    f = open("response.txt", "r+").read()
    j = json.loads(f)
    read_game(j)

def read_multiple_response():
    f = open("response.txt", "r+").read()
    print(len(f))
    j = json.loads(f)
    data =[]
    for i in j:
                #God,playername,picked, win,loss, w/l%, kills,deaths,assists,player damage,minion damage, structure damage, Damage Mitigated, healing, wards
        ret_msg = " "        
        if i["ret_msg"] != None:
            ret_msg = i["ret_msg"]
        if  not "They will be available approximately 7 days after" in ret_msg:
            kills = i["Kills_Player"]
            deaths = i["Deaths"]
            assists = i["Assists"]
            hidden = "Hidden Account"
            ban_list = i["Ban1"] +", "+ i["Ban2"] +", "+ i["Ban3"] +", "+ i["Ban4"] +", "+ i["Ban5"] +", "+  \
                        i["Ban6"] +", "+ i["Ban7"] +", "+ i["Ban8"] +", "+ i["Ban9"] +", "+ i["Ban10"]
            item_list = i["Item_Purch_1"] +", "+ i["Item_Purch_1"] +", "+ i["Item_Purch_1"] +", "+ i["Item_Purch_1"] +", "+ i["Item_Purch_1"] +", "+  \
                        i["Item_Purch_1"] +", "+ i["Item_Purch_1"] +", "+ i["Item_Purch_1"] +", "+ i["Item_Purch_1"] +", "+ i["Item_Purch_1"]
            if i["Win_Status"] == "Winner":
                picked = 1
                Win = 1
                Loss = 0
                WL = 100
            else:
                picked = 1
                Win = 0
                Loss = 1
                WL = 0

            if deaths != 0:
                KDA = round (((kills + (assists/2))/deaths),2)
            else:
                KDA = round (((kills + (assists/2))/1),2)
            if i["hz_player_name"] == None:
                stats = [i["hz_gamer_tag"],i["Reference_Name"], i["Kills_Player"],  i["Deaths"], i["Assists"], KDA , i["Damage_Player"], \
                        i["Damage_Bot"], i["Structure_Damage"],  i["Damage_Mitigated"], i["Healing"], i["Healing_Player_Self"], i["Wards_Placed"],i["Entry_Datetime"], \
                        str(ban_list),str(item_list)]
            elif i["hz_gamer_tag"] == None:
                stats = [i["hz_player_name"],i["Reference_Name"], i["Kills_Player"],  i["Deaths"], i["Assists"], KDA , i["Damage_Player"], \
                        i["Damage_Bot"], i["Structure_Damage"],  i["Damage_Mitigated"], i["Healing"], i["Healing_Player_Self"], i["Wards_Placed"],i["Entry_Datetime"], \
                        str(ban_list),str(item_list)]
            elif  i["hz_player_name"] != None and i["hz_gamer_tag"] != None and i["ret_msg"] == None:
                stats = [i["hz_gamer_tag"],i["Reference_Name"], i["Kills_Player"],  i["Deaths"], i["Assists"], KDA , i["Damage_Player"], \
                        i["Damage_Bot"], i["Structure_Damage"],  i["Damage_Mitigated"], i["Healing"], i["Healing_Player_Self"], i["Wards_Placed"],i["Entry_Datetime"], \
                        str(ban_list),str(item_list)]  
            elif  i["hz_player_name"] != None and i["hz_gamer_tag"] != None and i["ret_msg"] != None:
                stats = [hidden,i["Reference_Name"], i["Kills_Player"],  i["Deaths"], i["Assists"], KDA , i["Damage_Player"], \
                        i["Damage_Bot"], i["Structure_Damage"],  i["Damage_Mitigated"], i["Healing"], i["Healing_Player_Self"], i["Wards_Placed"],i["Entry_Datetime"], \
                        str(ban_list),str(item_list)]
                print("An error with the response for " + str(i["Match"]) +" has happened. " + i["ret_msg"]) 
            else:
                #Player Privacy Flag set for this player.
                print("An error has happened")

            data.append(stats)
        else:
            print("An error with the response for " + str(i["Match"]) +" has happened. " + i["ret_msg"])
    logger.write_to_sheets(data)

def read_games_queue():
    f= open("queue.txt", "r+").read()
    j= json.loads(f)
    matchID = []
    for i in j:
        matchID.append(i["Match"])
    matchList = [matchID[i:i +10] for i in range(0,len(matchID),10)]
    for i in matchList:
        queries.getmatchdetailsbatch(i)

def read_match_history():
    f= open("history.txt", "r+").read()
    j= json.loads(f)
    match_history_stats = []
    for i in j:
        stats = match_history_stats.append({"God":i["God"],"Player Damage":i["Damage"],"Structure Damage":i["Damage_Structure"],
                                            "Damage Mitigated":i["Damage_Mitigated"],"Damage Taken":i["Damage_Taken"],
                                            "Healing":i["Healing"],"Self Healing":i["Healing_Player_Self"],
                                            "Kills":i["Kills"],"Deaths":i["Deaths"],"Assists":i["Assists"],
                                            "Role":i["Role"],"Game Mode":i["Match_Queue_Id"],
                                            "GPM":int(i["Gold"]/i["Minutes"]),"PlayerID":i["playerId"]})
        logger.write_stats(stats)

def read_queue():
    f = open ("queue.txt", "r+").read()
    j = json.loads(f)
    id_list = []
    for i in j:
        id_list.append(i["Match"])
    print(id_list)

def read_matchdetailsbatch():
    f = open("matchdetailsbatch.txt","r+").read()
    j=json.loads(f)
    id_list = {}
    for i in j:
        MatchID = i["Match"]                        #   MatchID {
        Win_Status = i["Win_Status"]                #               Winers[]
        Rank = i["Conquest_Tier"]                   #               Losers[]
                                                    #           }
        matchstart = datetime.strptime(i["Entry_Datetime"], '%m/%d/%Y %I:%M:%S %p') - timedelta(seconds=(i["Time_In_Match_Seconds"]+75))
        if i["Match"] in id_list:                   
            if Win_Status == "Winner":
                id_list[MatchID]["Winners"].append(Rank)
            elif Win_Status == "Loser":
                id_list[MatchID]["Losers"].append(Rank)
        elif i["Match"] not in id_list.keys():
            if Win_Status == "Winner":
                id_list.update({MatchID:{"Winners":[Rank],"Losers":[],"Start datetime":datetime.strftime(matchstart,'%m/%d/%Y %I:%M:%S %p')}})
            elif Win_Status == "Loser":
                id_list.update({MatchID:{"Winners":[],"Losers":[Rank],"Start datetime":datetime.strftime(matchstart,'%m/%d/%Y %I:%M:%S %p')}})
            else:
                id_list.update({MatchID:"a"})
        else:
            pass
    print(id_list)

def get_conquest_info():
    f = open("history.txt","r+").read()
    j=json.loads(f)
    for i in j:
        if i["Match_Queue_Id"] == main.queue_id_conversion_str2int("Conquest"):
            role = i["Role"]
            god = i["God"]
            gpm = i["Gold_Per_Minute"]
            minion_damage = i["Damage_Bot"]
            player_damage = i["Damage"]
            structure_damage = i["Damage_Structure"]
            damage_mitigated = i["Damage_Mitigated"]
            damage_taken = i["Damage_Taken"]
            damage_taken_magical = i["Damage_Taken_Magical"]
            damage_taken_physical = i["Damage_Taken_Physical"]
            healing = i["Healing"]
            self_healing = i["Healing_Player_Self"]
            kills = i["Kills"]
            deaths = i["Deaths"]
            assists = i["Assists"]
            wards_placed = i["Wards_Placed"]
            result = i["Win_Status"]
            stats = str('Role: {0}, God: {1}, GPM: {2}, Minion Damage: {3}, Player Damage: {4}, Structure Damage: {5}, Damage Mitigated: {6}, Damage Taken: {7}, '
                        'Magical Damage Taken: {8}, Physical Damage Taken: {9}, Player Healing: {10}, Self Healing: {11}, Kills: {12}, Deaths: {13}, Assists: {14}, '
                        'Wards Placed: {15}, Result: {16}').format(role,god,gpm,minion_damage,player_damage,structure_damage,damage_mitigated,damage_taken, 
                        damage_taken_magical,damage_taken_physical,healing,self_healing,kills,deaths,assists,wards_placed,result)
            print(stats)