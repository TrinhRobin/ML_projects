import requests
import json
##NO API KEy

#Metadata

##teams endpoint
def get_games(filename,id_seasons=2021,id_teams=[1,2]):
    url_games = "https://www.balldontlie.io/api/v1/games" 
    parameters = f"?seasons[]={id_seasons}"+"".join([f"&team_ids[]={i}" for i in id_teams])

    volume = requests.get(url_games+parameters).json()
    nb_page = volume["meta"]["total_pages"]
    print(nb_page)
    print(volume["meta"]["total_count"])
    
    all_games =[ requests.get(url_games+parameters+f"&page={i}").json() for i in range(1,1+nb_page)]
    ids_games = [g["id"]  for games in all_games for g in games["data"]]
    print(all_games[-1])
    with open(filename, 'w') as f:
        json.dump(all_games,f)
    return ids_games

#get_games('data/all_games.json')
#print(requests.get("https://www.balldontlie.io/api/v1/games??seasons[]=2021&team_ids[]=1&page=9").json())

def get_teams(list_teams=["Phoenix Suns","Atlanta Hawks","LA Clippers","Milwaukee Bucks"]):
    teams_data = requests.get("https://www.balldontlie.io/api/v1/teams").json()
    #"filename=[name.replace(r" ", r"") for name in list_teams]
    #with open(f"data/{''.join(filename)}.json", 'w') as f:
    with open(f"data/teams.json", 'w') as f:
        json.dump(teams_data,f)
    return [team["id"]for team in teams_data['data'] if team["full_name"]in list_teams]
#in ["Phoenix Suns","Atlanta Hawks","Los Angeles Clippers","Milwaukee Bucks"]
#print(teams_data)

def catch(func, *args, handle=lambda e : e, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        pass
        #return handle(e)

def request_stat(url):
    return requests.get(url).json()

def get_stats(filename,list_games_id,season):
    url_stats = "https://www.balldontlie.io/api/v1/stats" 
    parameters =f"?seasons[]={season}"+ "".join([f"&game_ids[]={i}" for i in list_games_id])
    nb_page = requests.get(url_stats+parameters+"&page=1").json()["meta"]["total_pages"]
    print(nb_page)
    
    all_stats =[ catch(request_stat ,url_stats+parameters+f"&page={i}") for i in range(1,1+nb_page)]
    print(all_stats[-1])
    with open(filename, 'w') as f:
        json.dump(all_stats,f)


#get_games('data/all_games.json')
id_teams = get_teams()
id_games = get_games("data/games_exam.json",2021,id_teams)
get_stats("data/stats_exam.json",id_games ,2021)
#print(id_games)

url_stats = "https://www.balldontlie.io/api/v1/stats" 
parameters ="?seasons[]=2021"+ "".join([f"&game_ids[]={i}" for i in id_games])
#print(parameters)
#for i in range(385):
 #        try :
  #            requests.get(url_stats +parameters+f"&page={i}")
   #      except :
    #          print(i)
 #   if i !=43:
  
      #  print(i)
        
   

   # print(requests.get(url_stats +parameters+f"&page={i}").json())

#"https://www.balldontlie.io/api/v1/stats?game_ids[]="