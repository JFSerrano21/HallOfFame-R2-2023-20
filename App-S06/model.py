"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from datetime import datetime
from tabulate import tabulate
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""
#########################################################################################
# Construccion de modelos


def new_data_structs(tipo_mapa,load_factor):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    catalog = {'results': None,
               'goalscorers': None,
               'shootouts': None,
               'home_teams': None,
               'away_teams': None,
               'teams': None,
               "years": None,
               "results2": None,
               "scorers": None}

    catalog['results'] = mp.newMap(10000,
                                   maptype=tipo_mapa,
                                   loadfactor=load_factor,
                                   cmpfunction=cmp_fecha)
    catalog['goalscorers'] = lt.newList("ARRAY_LIST")
    catalog['shootouts'] = mp.newMap(10000,
                                   maptype=tipo_mapa,
                                   loadfactor=load_factor,
                                   cmpfunction=cmp_fecha)
    catalog['home_teams'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=load_factor,
                                   cmpfunction=cmp_fecha)
    catalog['away_teams'] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["teams"] = lt.newList("ARRAY_LIST")
    catalog["years"] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["results2"] = mp.newMap(10000,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["years1"] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["scorers"] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["t_req_4"] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["tournaments_req7"]= mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["scorers2"]= mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["num_tournaments_req7"]= lt.newList("ARRAY_LIST")
    catalog["loqfalta"]= mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    catalog["loqfalta_total_goals"]= mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    return catalog

   
def new_result(data):
    result = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None, 
              "neutral": None}
    result['date'] = data["date"]
    result['home_team'] = data["home_team"]
    result['away_team'] = data["away_team"]
    result['home_score'] = data["home_score"]
    result['away_score'] = data["away_score"]
    result['tournament'] = data["tournament"]
    result['city'] = data["city"]
    result['country'] = data["country"]
    result['neutral'] = data["neutral"]
    return result

def new_shootout(data):
    shootout = {'date': None,
              "home_team": None,
              "away_team": None,
              "winner": None}
    shootout['date'] = data["date"]
    shootout['home_team'] = data["home_team"]
    shootout['away_team'] = data["away_team"]
    shootout['winner'] = data["winner"]
    return shootout

def new_home_team(data_structs, data):
    if not mp.contains(data_structs["home_teams"], data["home_team"]):
        lista = lt.newList("ARRAY_LIST")
        team = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        if "home_score" in data:
            team["home_score"] = data["home_score"]
            team["away_score"] = data["away_score"]
            team["tournament"] = data["tournament"]
            team["city"] = data["city"]
            team["country"] = data["country"]
            if team not in lista["elements"]:
                lt.addLast(lista, team)
    else:
        key_value = mp.get(data_structs["home_teams"], data['home_team'])
        lista = me.getValue(key_value)
        team = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        if "home_score" in data:
            team["home_score"] = data["home_score"]
            team["away_score"] = data["away_score"]
            team["tournament"] = data["tournament"]
            team["city"] = data["city"]
            team["country"] = data["country"]
            if team not in lista["elements"]:
                lt.addLast(lista, team)
        elif "own_goal" in data:
            i = 1
            for partido in lt.iterator(lista):
                if partido["date"] == data["date"]:
                    partido.update({"own_goal": data["own_goal"], "penalty": data["penalty"]})
                    lt.changeInfo(lista, i, partido)
                i += 1
    return lista


def new_away_team(data_structs, data):
    if not mp.contains(data_structs["away_teams"], data["away_team"]):
        lista = lt.newList("ARRAY_LIST")
        team = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        if "home_score" in data:
            team["home_score"] = data["home_score"]
            team["away_score"] = data["away_score"]
            team["tournament"] = data["tournament"]
            team["city"] = data["city"]
            team["country"] = data["country"]
            if team not in lista["elements"]:
                lt.addLast(lista, team)
    else:
        key_value = mp.get(data_structs["away_teams"], data['away_team'])
        lista = me.getValue(key_value)
        team = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        if "home_score" in data:
            team["home_score"] = data["home_score"]
            team["away_score"] = data["away_score"]
            team["tournament"] = data["tournament"]
            team["city"] = data["city"]
            team["country"] = data["country"]
            if team not in lista["elements"]:
                lt.addLast(lista, team)
        elif "own_goal" in data:
            i = 1
            for partido in lt.iterator(lista):
                if partido["date"] == data["date"]:
                    partido.update({"own_goal": data["own_goal"], "penalty": data["penalty"]})
                    lt.changeInfo(lista, i, partido)
                i += 1
    return lista

def new_result2(data_structs, data):
    result = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None, 
              "neutral": None}
    result['date'] = data["date"]
    result['home_team'] = data["home_team"]
    result['away_team'] = data["away_team"]
    result['home_score'] = data["home_score"]
    result['away_score'] = data["away_score"]
    result['tournament'] = data["tournament"]
    result['city'] = data["city"]
    result['country'] = data["country"]
    result['neutral'] = data["neutral"]
    return result

def new_year(data_structs, data):
    anio = data["date"].split("-")[0]
    if "home_score" in data:
        torneo = data["tournament"]
        year = {torneo: None}
        tournament = {"equipos": None,
                    "encuentros": 0,
                        "countries": None,
                        "cities1": None,
                        "cities2": None,
                        "equipos2": None}
        tournament["equipos"] = lt.newList("ARRAY_LIST")
        lt.addLast(tournament["equipos"], data["home_team"])
        lt.addLast(tournament["equipos"], data["away_team"])
        tournament["encuentros"] += 1
        tournament["countries"] = lt.newList("ARRAY_LIST")
        lt.addLast(tournament["countries"], data["country"])
        tournament["cities1"] = lt.newList("ARRAY_LIST")
        lt.addLast(tournament["cities1"], data["city"])
        tournament["cities2"] = {}
        ciudad = data["city"]
        tournament["cities2"][ciudad] = 1
        tournament["equipos2"] = {}
        total_points_home = 0
        total_points_away = 0
        wins_home = 0
        wins_away = 0
        draws = 0
        losses_home = 0
        losses_away = 0
        if data["home_score"] > data["away_score"]:
            total_points_home = 3
            wins_home = 1
            losses_away = 1
        elif data["home_score"] == data["away_score"]:
            total_points_home = 1
            total_points_away = 1
            draws = 1
        else:
            total_points_away = 3
            wins_away = 1
            losses_home = 1
        goals_difference_home = int(data["home_score"]) - int(data["away_score"])
        goals_difference_away = int(data["away_score"]) - int(data["home_score"])
        goals_for_home = int(data["home_score"])
        goals_for_away = int(data["away_score"])
        mat = lt.newList("ARRAY_LIST")
        lt.addLast(mat, data["date"])
        tournament["equipos2"][data["home_team"]] = {"team": data["home_team"],
                                                     "total_points": total_points_home,
                                                     "goal_difference": goals_difference_home,
                                                     "matches": mat,
                                                     "penalty_points": 0,
                                                     "own_goal_points": 0,
                                                     "wins": wins_home,
                                                     "draws": draws,
                                                     "losses": losses_home,
                                                     "goals_for": goals_for_home,
                                                     "goals_against": goals_for_away,
                                                     "top_scorer": [{"scorer": "Unavailable", "goals": 0, "matches": None, "avg_time [min]": None}]}
        tournament["equipos2"][data["away_team"]] = {"team": data["away_team"],
                                                     "total_points": total_points_away,
                                                     "goal_difference": goals_difference_away,
                                                     "matches": mat,
                                                     "penalty_points": 0,
                                                     "own_goal_points": 0,
                                                     "wins": wins_away,
                                                     "draws": draws,
                                                     "losses": losses_away,
                                                     "goals_for": goals_for_away,
                                                     "goals_against": goals_for_home,
                                                     "top_scorer": [{"scorer": "Unavailable", "goals": 0, "matches": None, "avg_time [min]": None}]} 
        if not mp.contains(data_structs["years"], anio):
            year[torneo] = tournament
        else:
            tournaments = me.getValue(mp.get(data_structs["years"], anio))
            if (torneo not in tournaments):
                tournaments[torneo] = tournament
                year = tournaments
            else:
                antiguo = tournaments[torneo]

                pos1 = lt.isPresent(antiguo["equipos"], data["home_team"])
                if pos1 == 0:
                    lt.addLast(antiguo["equipos"], data["home_team"])
                pos2 = lt.isPresent(antiguo["equipos"], data["away_team"])
                if pos2 == 0:
                    lt.addLast(antiguo["equipos"], data["away_team"])

                antiguo["encuentros"] += 1

                pos3 = lt.isPresent(antiguo["countries"], data["country"])
                if pos3 == 0:
                    lt.addLast(antiguo["countries"], data["country"])

                pos4 = lt.isPresent(antiguo["cities1"], data["city"])
                if pos4 == 0:
                    lt.addLast(antiguo["cities1"], data["city"])

                if ciudad in antiguo["cities2"]:
                    antiguo["cities2"][ciudad] += 1
                else:
                    antiguo["cities2"][ciudad] = 1

                home_team = data["home_team"]
                away_team = data["away_team"]
                if home_team in antiguo["equipos2"]:
                    total_points = antiguo["equipos2"][home_team]["total_points"]
                    wins = antiguo["equipos2"][home_team]["wins"]
                    draws = antiguo["equipos2"][home_team]["draws"]
                    losses = antiguo["equipos2"][home_team]["losses"]
                    if data["home_score"] > data["away_score"]:
                        total_points += 3
                        wins += 1
                    elif data["home_score"] == data["away_score"]:
                        total_points += 1
                        draws += 1
                    else:
                        losses += 1
                    goals_difference = antiguo["equipos2"][home_team]["goal_difference"] + (int(data["home_score"]) - int(data["away_score"]))
                    goals_for = antiguo["equipos2"][home_team]["goals_for"] + (int(data["home_score"]))
                    matches = antiguo["equipos2"][home_team]["matches"]
                    lt.addLast(matches, data["date"])
                    penalty_points = antiguo["equipos2"][home_team]["penalty_points"]
                    own_goal_points = antiguo["equipos2"][home_team]["own_goal_points"]
                    goals_against = antiguo["equipos2"][home_team]["goals_against"] + (int(data["away_score"]))
                    top_scorer = antiguo["equipos2"][home_team]["top_scorer"]
                    antiguo["equipos2"][home_team] = {"team": home_team,
                                                     "total_points": total_points,
                                                     "goal_difference": goals_difference,
                                                     "matches": matches,
                                                     "penalty_points": penalty_points,
                                                     "own_goal_points": own_goal_points,
                                                     "wins": wins,
                                                     "draws": draws,
                                                     "losses": losses,
                                                     "goals_for": goals_for,
                                                     "goals_against": goals_against,
                                                     "top_scorer": top_scorer}
                else:
                    antiguo["equipos2"][home_team] = tournament["equipos2"][home_team]
                if away_team in antiguo["equipos2"]:
                    total_points = antiguo["equipos2"][away_team]["total_points"]
                    wins = antiguo["equipos2"][away_team]["wins"]
                    draws = antiguo["equipos2"][away_team]["draws"]
                    losses = antiguo["equipos2"][away_team]["losses"]
                    if data["away_score"] > data["home_score"]:
                        total_points += 3
                        wins += 1
                    elif data["home_score"] == data["away_score"]:
                        total_points += 1
                        draws += 1
                    else:
                        losses += 1
                    goals_difference = antiguo["equipos2"][away_team]["goal_difference"] + (int(data["away_score"]) - int(data["home_score"]))
                    goals_for = antiguo["equipos2"][away_team]["goals_for"] + (int(data["away_score"]))
                    matches = antiguo["equipos2"][away_team]["matches"]
                    lt.addLast(matches, data["date"])
                    penalty_points = antiguo["equipos2"][away_team]["penalty_points"]
                    own_goal_points = antiguo["equipos2"][away_team]["own_goal_points"]
                    goals_against = antiguo["equipos2"][away_team]["goals_against"] + (int(data["home_score"]))
                    top_scorer = antiguo["equipos2"][away_team]["top_scorer"]
                    antiguo["equipos2"][away_team] = {"team": away_team,
                                                     "total_points": total_points,
                                                     "goal_difference": goals_difference,
                                                     "matches": matches,
                                                     "penalty_points": penalty_points,
                                                     "own_goal_points": own_goal_points,
                                                     "wins": wins,
                                                     "draws": draws,
                                                     "losses": losses,
                                                     "goals_for": goals_for,
                                                     "goals_against": goals_against,
                                                     "top_scorer": top_scorer}
                else:
                    antiguo["equipos2"][away_team] = tournament["equipos2"][away_team]

                tournaments[torneo] = antiguo 
                year = tournaments  
    elif "own_goal" in data:
        antiguo = me.getValue(mp.get(data_structs["years"], anio))
        home_team = data["home_team"]
        away_team = data["away_team"]
        scorer = data["scorer"]
        goals = 1
        matches = lt.newList("ARRAY_LIST")
        lt.addLast(matches, data["date"])
        avg_time = lt.newList("ARRAY_LIST")
        if data["minute"] != '':
            lt.addLast(avg_time, float(data["minute"]))     
        own_goal_points = 0
        penalty_points = 0
        if data["own_goal"] == "True":
            own_goal_points = 1
        if data["penalty"] == "True":
            penalty_points = 1
        llave = f"{data['date']}, {data['home_team']}, {data['away_team']}"
        tournament = mp.get(data_structs["results2"], llave)["value"]["tournament"]
        antiguo[tournament]["equipos2"][data["team"]]["own_goal_points"] += own_goal_points
        antiguo[tournament]["equipos2"][data["team"]]["penalty_points"] += penalty_points
        dic = {"scorer": scorer, "goals": goals, "matches": matches, "avg_time [min]": avg_time}
        esta = False
        i = -1
        while (not esta) and ((i+1) < len(antiguo[tournament]["equipos2"][data["team"]]["top_scorer"])):
            i += 1
            jugador = antiguo[tournament]["equipos2"][data["team"]]["top_scorer"][i]
            if jugador["scorer"] == scorer:
                esta = True
        if not esta:
            antiguo[tournament]["equipos2"][data["team"]]["top_scorer"].append(dic)
        else:
            antiguo[tournament]["equipos2"][data["team"]]["top_scorer"][i]["goals"] += 1
            if lt.isPresent(antiguo[tournament]["equipos2"][data["team"]]["top_scorer"][i]["matches"], data["date"]) == 0:
                lt.addLast(antiguo[tournament]["equipos2"][data["team"]]["top_scorer"][i]["matches"], data["date"])
            if data["minute"] != '':
                lt.addLast(antiguo[tournament]["equipos2"][data["team"]]["top_scorer"][i]["avg_time [min]"], float(data["minute"]))
        year = antiguo
    return year

def new_scorer2(data_structs, data):
    scorer = {'date': None,
              "home_team": None,
              "away_team": None,
              "team": None,
              "scorer": None, 
              "minute": None,
              "own_goal": None, 
              "penalty": None}
    scorer['date'] = data["date"]
    scorer['home_team'] = data["home_team"]
    scorer['away_team'] = data["away_team"]
    scorer['team'] = data["team"]
    scorer['scorer'] = data["scorer"]
    scorer['minute'] = data["minute"]
    scorer['own_goal'] = data["own_goal"]
    scorer['penalty'] = data["penalty"]
    if data["scorer"] in data_structs["scorers"]:
        entregar = mp.get(data_structs["scorers"], data["scorer"])
        lt.addLast(entregar, scorer)
    else:
        entregar = lt.newList("ARRAY_LIST")
        lt.addLast(entregar, scorer)
    return entregar


def new_year1(data_structs, data):
    
    year = data["date"].split("-")[0]
    if not mp.contains(data_structs["years1"], year):
        lista = lt.newList("ARRAY_LIST")
        team = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        if "home_score" in data:
            team["home_score"] = data["home_score"]
            team["away_score"] = data["away_score"]
            team["tournament"] = data["tournament"]
            team["city"] = data["city"]
            team["country"] = data["country"]
            if team not in lista["elements"]:
                lt.addLast(lista, team)
        elif "own_goal" in data:
            if team["own_goal"] != "":
                team["own_goal"] = data["own_goal"]
            if team["penalty"] != "":
                team["penalty"] = data["penalty"]
    else:
        key_value = mp.get(data_structs["years1"], year)
        lista = me.getValue(key_value)
        team = {'date': None,
              "home_team": None,
              "away_team": None,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "city": None, 
              "country": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        if "home_score" in data:
            team["home_score"] = data["home_score"]
            team["away_score"] = data["away_score"]
            team["tournament"] = data["tournament"]
            team["city"] = data["city"]
            team["country"] = data["country"]
            if team not in lista["elements"]:
                lt.addLast(lista, team)
        elif "own_goal" in data:
            i = 1
            for partido in lt.iterator(lista):
                if partido["date"] == data["date"] and partido["home_team"] == data["home_team"] and partido["away_team"] == data["away_team"]:
                    partido.update({"own_goal": data["own_goal"], "penalty": data["penalty"]})
                    lt.changeInfo(lista, i, partido)
                i += 1
    return lista
def new_scorer(data_structs, data):
    
    anio_goalscorer=data["date"].split("-")[0]
    a = data_structs["scorers"]
    b = data["scorer"]
    c = data_structs["years1"]
    if not mp.contains(data_structs["scorers"], data["scorer"]):
        lista = lt.newList("ARRAY_LIST")
        team = {'date': None,
              "minute":0,
              "home_team": None,
              "away_team": None,
              "team":0,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        team['team'] = data["team"]
        team['minute'] = data["minute"]
        if team["own_goal"] != "":
            team["own_goal"] = data["own_goal"]
        if team["penalty"] != "":
            team["penalty"] = data["penalty"]
        valor_hash=mp.get(data_structs["years1"],anio_goalscorer)["value"]
        #valor_hash=tupla_llave_valor_hash[1]
        for partido in lt.iterator(valor_hash):
            if partido["date"] == data["date"] and partido["home_team"] == data["home_team"] and partido["away_team"] == data["away_team"]:
               team["home_score"] = partido["home_score"]
               team["away_score"] = partido["away_score"]
               team["tournament"] = partido["tournament"]
        if team not in lista["elements"]:
            lt.addLast(lista, team)
    else:
        key_value = mp.get(data_structs["scorers"], data["scorer"])
        lista = me.getValue(key_value)
        team = {'date': None,
              "minute":"",
              "home_team": None,
              "away_team": None,
              "team":0,
              "home_score": 0,
              "away_score": 0, 
              "tournament": None,
              "own_goal": "unkown",
              "penalty": "unkown"}
        team['date'] = data["date"]
        team['minute'] = data["minute"]
        team['home_team'] = data["home_team"]
        team['away_team'] = data["away_team"]
        team['team'] = data["team"]
        if team["own_goal"] != "":
            team["own_goal"] = data["own_goal"]
        if team["penalty"] != "":
            team["penalty"] = data["penalty"]
        llave_valor_hash = mp.get(data_structs["years1"],anio_goalscorer)
        valor_hash=llave_valor_hash["value"]
        for partido in lt.iterator(valor_hash):
            if partido["date"] == data["date"] and partido["home_team"] == data["home_team"] and partido["away_team"] == data["away_team"]:
               team["home_score"] = partido["home_score"]
               team["away_score"] = partido["away_score"]
               team["tournament"] = partido["tournament"]
        if team not in lista["elements"]:
            lt.addLast(lista, team)
    return lista
                
def new_tournament_req7(data_structs, data):
    anio_goalscorer=data["date"].split("-")[0]
    lista = lt.newList("ARRAY_LIST")
    team = {'date': None,
            "minute":0,
            "home_team": None,
            "away_team": None,
            "team":None,
            "home_score": 0,
            "away_score": 0,
            "country": None,
            "city":None, 
            "tournament": None,
            "scorer": "",
            "own_goal": "unkown",
            "penalty": "unkown"}
    team['date'] = data["date"]
    team['home_team'] = data["home_team"]
    team['away_team'] = data["away_team"]
    team['team'] = data["team"]
    team['scorer'] = data["scorer"]
    if data["minute"]!="":
        team['minute'] = float(data["minute"])
    else:
        team['minute'] = -1
    if team["own_goal"] != "":
        team["own_goal"] = data["own_goal"]
    if team["penalty"] != "":
        team["penalty"] = data["penalty"]
    valor_hash=me.getValue(mp.get(data_structs["years1"],anio_goalscorer))
    for partido in lt.iterator(valor_hash):
        if partido["date"] == data["date"] and partido["home_team"] == data["home_team"] and partido["away_team"] == data["away_team"]:
           team["home_score"] = float(partido["home_score"])
           team["away_score"] = float(partido["away_score"])
           team["city"] = partido["city"]
           team["country"] = partido["country"]
           team["tournament"] = partido["tournament"]
    if not mp.contains(data_structs["tournaments_req7"], team["tournament"]):
        if team not in lista["elements"]:
            lt.addLast(lista, team)
    else:
        key_value = mp.get(data_structs["tournaments_req7"], team["tournament"])
        lista = me.getValue(key_value)
        if team not in lista["elements"]:
            lt.addLast(lista, team)
    return lista,team["tournament"]

def new_t_req_4(data_structs,data):
    p = {'date': None,
            "home_team": None,
            "away_team": None,
            "home_score": 0,
            "away_score": 0,
            "country": None,
            "city":None, 
            "tournament": None,
            "winner":None}
    p['date'] = data["date"]
    p['home_team'] = data["home_team"]
    p['away_team'] = data["away_team"]
    p["home_score"] = data["home_score"]
    p["away_score"] = data["away_score"]
    p["city"] = data["city"]
    p["country"] = data["country"]
    p["tournament"] = data["tournament"]
    p["winner"] = "Unkown"
    
    if mp.contains(data_structs["t_req_4"], p["tournament"]) == False:
        lst = lt.newList("ARRAY_LIST")
        lt.addLast(lst,p)
    elif mp.contains(data_structs["t_req_4"], p["tournament"] )== True:
        lst = me.getValue(mp.get(data_structs["t_req_4"],p["tournament"]))
        lt.addLast(lst,p)

    return lst

##################################################################################################################################################################################
# Funciones para agregar informacion al modelo
def convert_time(text):
    return datetime.strptime(text,"%Y-%m-%d")

def add_result(data_structs, data):
    newresult = new_result(data)
    mp.put(data_structs['results'], f"{data['date']}, {data['home_score']}, {data['away_score']}, {data['home_team']}, {data['away_team']}", newresult)

def add_goalscorer(data_structs, data):
    lt.addLast(data_structs["goalscorers"],data)
    
def add_shootout(data_structs, data):
    newshootout = new_shootout(data)
    mp.put(data_structs['shootouts'], f"{data['date']}, {data['home_team']}, {data['away_team']}", newshootout)

def add_home_team(data_structs, data):
    newhometeam = new_home_team(data_structs, data)
    mp.put(data_structs['home_teams'], data['home_team'], newhometeam)

def add_away_team(data_structs, data):
    newawayteam = new_away_team(data_structs, data)
    mp.put(data_structs['away_teams'], data['away_team'], newawayteam)

def add_team(data_structs, data):
    if lt.isPresent(data_structs["teams"], data["home_team"]) == 0:
        lt.addLast(data_structs["teams"], data["home_team"])
    if lt.isPresent(data_structs["teams"], data["away_team"]) == 0:
        lt.addLast(data_structs["teams"], data["away_team"])

def add_result2(data_structs, data):
    newresult = new_result2(data_structs, data)
    mp.put(data_structs['results2'], f"{data['date']}, {data['home_team']}, {data['away_team']}", newresult)

def add_year(data_structs, data):
    anio = data["date"].split("-")[0]
    newyear = new_year(data_structs, data)
    mp.put(data_structs["years"], anio, newyear)

def add_scorer2(data_structs, data):
    newscorer = new_scorer(data_structs, data)
    mp.put(data_structs["scorers"], data["scorer"], newscorer)
def add_year1(data_structs, data):
    anio = data["date"].split("-")[0]
    newyear1=new_year1(data_structs, data)
    mp.put(data_structs["years1"], anio, newyear1)

def add_scorer(data_structs, data):
    nombre=data["scorer"]
    info= new_scorer(data_structs, data)
    mp.put(data_structs["scorers"],nombre,info)

def add_tournament_req7(data_structs, data):
    
    info= new_tournament_req7(data_structs, data)
    
    mp.put(data_structs["tournaments_req7"],info[1],info[0])

def add_num_tournaments_req7(data_structs, data):
    lt.addLast(data_structs["num_tournaments_req7"], data["tournament"])


    
def add_t_req_4(data_structs,data):

    ez = new_t_req_4(data_structs,data)

    mp.put(data_structs["t_req_4"], data["tournament"], ez)

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass

def results_size(data_structs):
    return mp.size(data_structs['results'])

def goalscorers_size(data_structs):
    return mp.size(data_structs['goalscorers'])

def shootouts_size(data_structs):
    return mp.size(data_structs['shootouts'])

def map_a_lista_results(data_structs):
    keys_ = mp.keySet(data_structs["results"])
    keys = lt.newList("ARRAY_LIST")
    for i in lt.iterator(keys_):
        lt.addLast(keys, i)
    results = lt.newList("ARRAY_LIST")
    keys = merg.sort(keys, fecha)
    for i in range(1, 4):
        key = lt.getElement(keys, i)
        key_value = mp.get(data_structs["results"], key)
        lt.addLast(results, key_value)
    for j in range(mp.size(keys) - 2, mp.size(keys)+1):
        key = lt.getElement(keys, j)
        key_value = mp.get(data_structs["results"], key)
        lt.addLast(results, key_value)
    return results

def sublista_generalizada(list,cmp):
    list = merg.sort(list, cmp)
    primeros=None
    ultimos=None
    if lt.size(list)>=6:
        primeros= lt.subList(list,1,3)
        ultimos = lt.subList(list,(lt.size(list))-2,3)
    else:
        primeros=list
    return primeros,ultimos 
def sublist(list):
    list = merg.sort(list, cmp_goalscorers)
    primeros=None
    ultimos=None
    if lt.size(list)>=6:
        primeros= lt.subList(list,1,3)
        ultimos = lt.subList(list,(lt.size(list))-2,3)
    else:
        primeros=list
    return primeros,ultimos 

def map_a_lista_goalscorers (list):
    primeros,ultimos = list
    if primeros != None and ultimos != None:
        primeros = primeros['elements']
        ultimos = ultimos['elements']
        total= []
        for linea in primeros:
            lista1=[linea["date"], linea["home_team"],linea["away_team"],linea["team"],linea["scorer"],linea["minute"],linea["own_goal"],linea["penalty"]]
            total.append(lista1)
        for linea in ultimos:
            lista2=[linea["date"], linea["home_team"],linea["away_team"],linea["team"],linea["scorer"],linea["minute"],linea["own_goal"],linea["penalty"]]
            total.append(lista2)
    return total

def map_a_lista_shootouts(data_structs):
    keys_ = mp.keySet(data_structs["shootouts"])
    keys = lt.newList("ARRAY_LIST")
    for i in lt.iterator(keys_):
        lt.addLast(keys, i)
    shootouts = lt.newList("ARRAY_LIST")
    keys = merg.sort(keys, fecha)
    for i in range(1, 4):
        key = lt.getElement(keys, i)
        key_value = mp.get(data_structs["shootouts"], key)
        lt.addLast(shootouts, key_value)
    for j in range(mp.size(keys) - 2, mp.size(keys)+1):
        key = lt.getElement(keys, j)
        key_value = mp.get(data_structs["shootouts"], key)
        lt.addLast(shootouts, key_value)
    return shootouts  
def un_gol_mas(data_structs,data):
    data_structs["goles_totales"]+=1
def add_loqfalta(data_structs,data):
    if not mp.contains(data_structs["loqfalta"], data["tournament"]):
        mp.put(data_structs["loqfalta"], data["tournament"],1)
    else:
        valor=me.getValue(mp.get(data_structs["loqfalta"],data["tournament"]))
        mp.put(data_structs["loqfalta"], data["tournament"],valor +1)
        
def add_loqfalta_total_goals(data_structs,data):
    if not mp.contains(data_structs["loqfalta_total_goals"], data["tournament"]):
        mp.put(data_structs["loqfalta_total_goals"], data["tournament"],int(data["home_score"])+int(data["away_score"]))
    else:
        valor=me.getValue(mp.get(data_structs["loqfalta_total_goals"],data["tournament"]))
        mp.put(data_structs["loqfalta_total_goals"], data["tournament"],valor +int(data["home_score"])+int(data["away_score"]))
        
def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

##################################################################################################################################################################################
def req_1(data_structs, num_equipos, nombre_equipo, condicion_equipo):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    lista_respuesta = lt.newList("ARRAY_LIST")
    lista_final = lt.newList("ARRAY_LIST")
    total_teams = 0
    total_matches = 0
    total_matches_condicion = 0
    indiferente=False
    if condicion_equipo =="home":
        lista_respuesta=me.getValue(mp.get(data_structs["model"]["home_teams"],nombre_equipo))
        for partido in lt.iterator(lista_respuesta):
            fecha_partido =partido["date"]
            home_team_partido = partido["home_team"]
            away_team_partido = partido["away_team"]
            home_score_partido = partido["home_score"]
            away_score_partido = partido["away_score"]
            llave_neutral = f"{fecha_partido}, {home_score_partido}, {away_score_partido}, {home_team_partido}, {away_team_partido}"
            diccionario_neutral = me.getValue(mp.get(data_structs["model"]["results"],llave_neutral))
            if diccionario_neutral["neutral"] =="False":
                lt.addLast(lista_final,partido)
                total_matches_condicion+=1
        total_teams = lt.size(data_structs["model"]["teams"])
        total_matches = lt.size(lista_respuesta)+lt.size(me.getValue(mp.get(data_structs["model"]["away_teams"],nombre_equipo)))
        
    elif condicion_equipo =="away":
        lista_respuesta=me.getValue(mp.get(data_structs["model"]["away_teams"],nombre_equipo))
        for partido in lt.iterator(lista_respuesta):
            fecha_partido =partido["date"]
            home_team_partido = partido["home_team"]
            away_team_partido = partido["away_team"]
            home_score_partido = partido["home_score"]
            away_score_partido = partido["away_score"]
            llave_neutral = f"{fecha_partido}, {home_score_partido}, {away_score_partido}, {home_team_partido}, {away_team_partido}"
            diccionario_neutral = me.getValue(mp.get(data_structs["model"]["results"],llave_neutral))
            if diccionario_neutral["neutral"] =="False":
                lt.addLast(lista_final,partido)
                total_matches_condicion+=1
        total_teams = lt.size(data_structs["model"]["teams"])
        total_matches = lt.size(lista_respuesta)+lt.size(me.getValue(mp.get(data_structs["model"]["home_teams"],nombre_equipo)))
    elif condicion_equipo=="indiferente":
        indiferente = True
        lista_duplicada = lt.newList("ARRAY_LIST")
        valor_hash = me.getValue(mp.get(data_structs["model"]["away_teams"],nombre_equipo))
        lista_respuesta=me.getValue(mp.get(data_structs["model"]["home_teams"],nombre_equipo))
        total_teams = lt.size(data_structs["model"]["teams"])
        total_matches = lt.size(lista_respuesta)+lt.size(me.getValue(mp.get(data_structs["model"]["away_teams"],nombre_equipo)))
        total_matches_condicion =lt.size(lista_respuesta)
        for partido in lt.iterator(valor_hash):
            lt.addLast(lista_duplicada,partido)
            total_matches_condicion+=1
        for partido in lt.iterator(lista_respuesta):
            lt.addLast(lista_duplicada,partido)
        lista_respuesta = lista_duplicada
    else:
        print("opcion no valida")
    pass
    if indiferente == True:
        lista_respuesta = merg.sort(lista_respuesta,cmp_fecha_req1)
    else:
        lista_respuesta = merg.sort(lista_final,cmp_fecha_req1)
        
    if num_equipos<lt.size(lista_respuesta):
        lista_respuesta = lt.subList(lista_respuesta,1,num_equipos)
    
    lista_final = [ ]
    respuesta = [ ]
    for i in lt.iterator(lista_respuesta):
        lista_final.append(list(i.values()))
    respuesta=lista_final
    if len(lista_final)>5:
        respuesta = lista_final[:3]+lista_final[-3:]
    for i in range(len(respuesta)):
        respuesta[i] = respuesta[i][:-2]
        
    
    return respuesta,total_teams,total_matches,total_matches_condicion

def req_2(data_structs,jugador,ngoles):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    
    
    rf = mp.get(data_structs["scorers"],jugador)
    scorer_results = me.getValue(rf)
    organizar = merg.sort(scorer_results,cmp_req_2)
    nelem = lt.size(organizar)
    
    if nelem >= ngoles:
        r_final = lt.subList(organizar,1,ngoles)
    
    elif nelem < ngoles:
        r_final = lt.subList(organizar,1,nelem)

    return r_final



def req_3(data_structs, equipo, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    try:
        home_team_ = mp.get(data_structs["home_teams"], equipo)
        away_team_ = mp.get(data_structs["away_teams"], equipo)
        home_team = me.getValue(home_team_)
        away_team = me.getValue(away_team_)
        home_team_orden = merg.sort(home_team, cmp_req_3)
        away_team_orden = merg.sort(away_team, cmp_req_3)
        home_team_filtrado = lt.newList("ARRAY_LIST")
        todo = lt.newList("ARRAY_LIST")
        for game in lt.iterator(home_team_orden):
            if fecha_inicial <= game["date"] <= fecha_final:
                lt.addLast(home_team_filtrado, game)
                lt.addLast(todo, game)
        away_team_filtrado = lt.newList("ARRAY_LIST")
        for game in lt.iterator(away_team_orden):
            if fecha_inicial <= game["date"] <= fecha_final:
                lt.addLast(away_team_filtrado, game)
                lt.addLast(todo, game)
        total_equipos_registrados = lt.size(data_structs["teams"])
        total_partidos = lt.size(home_team_filtrado) + lt.size(away_team_filtrado)
        partidos_local = lt.size(home_team_filtrado)
        partidos_visitante = lt.size(away_team_filtrado)
        todo = merg.sort(todo, cmp_req_3)
        tabulear = []
        tamanio = lt.size(todo)
        if tamanio <= 6:
            for i in range(tamanio):
                tabulear.append(lt.getElement(todo, i))
        if tamanio > 6:
            for i in range(1, 4):
                tabulear.append(lt.getElement(todo, i))
            for j in range(lt.size(todo)-2, lt.size(todo)+1):
                tabulear.append(lt.getElement(todo, j))
        return (total_equipos_registrados, total_partidos, partidos_local, partidos_visitante, tabulear)
    except:
        total_equipos_registrados = lt.size(data_structs["teams"])
        return total_equipos_registrados, 0, 0, 0, []


def req_4(data_structs,tournament,f1,f2):
    """
    Función que soluciona el requerimiento 4
    """
    
    resultos = lt.newList("ARRAY_LIST")
    shoots = data_structs["shootouts"]
    tournaments = data_structs["t_req_4"]
    todos_los_t = lt.size(mp.keySet(tournaments))
    t = mp.get(tournaments,tournament)
    torneos = me.getValue(t)
    
    for r in lt.iterator(torneos):
        rta = "Unknow"
        if  r["date"] >= f1 and r["date"] <= f2 :
            c = mp.get(shoots,f"{r['date']}, {r['home_team']}, {r['away_team']}") 
            if c!=None:
                rt = me.getValue(c) 
                rta = rt["winner"]
            ciudad = r["city"]
            pais = r["country"]
            lt.addLast(resultos,{"date": r["date"], "tournament": r["tournament"], "country":pais, 
                                  "city":ciudad, "home_team":r["home_team"], "away_team":r["away_team"],
                                  "home_score":r["home_score"], "away_score":r["away_score"], "winner":rta})
    
    final = merg.sort(resultos,cmp_req_4)
    finalisimo = {"total_tournamens":todos_los_t,"data":final}
    return finalisimo


def req_5(data_structs, anotador, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    total_players=mp.size(data_structs["model"]["scorers"])
    lista_para_tabulate=lt.newList("ARRAY_LIST")
    llave_valor_jugador=mp.get(data_structs["model"]["scorers"],anotador)
    valor_jugador = llave_valor_jugador["value"]
    fecha_final = convert_time(fecha_final)
    fecha_inicial = convert_time(fecha_inicial)
    torneos = lt.newList("ARRAY_LIST")
    goles=0
    penales=0
    autogoles=0
    for partido in lt.iterator(valor_jugador):
        fecha_partido=convert_time(partido["date"])
        if fecha_partido>=fecha_inicial and fecha_partido<=fecha_final:
            goles+=1
            lt.addLast(torneos,partido["tournament"])
            lt.addLast(lista_para_tabulate,partido)
            if partido["penalty"]=="True":
                penales+=1
            if partido["own_goal"]=="True":
                autogoles+=1
    lista_para_tabulate = merg.sort(lista_para_tabulate,cmp_req5)
    torneos=lt.quitar_repetidos_ltDISCLIB(torneos)
    return total_players,sublista_generalizada(lista_para_tabulate,cmp=cmp_req5), lt.size(torneos),goles,penales,autogoles
    


def req_6(data_structs, n, tournament, year):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    try:
        info_anio = mp.get(data_structs["years"], year)
        try: 
            torneo = me.getValue(info_anio)[tournament]
            total_tournaments = 0
            for i in info_anio["value"]:
                total_tournaments  += 1
            total_teams = lt.size(torneo["equipos"])
            total_matches = torneo["encuentros"]
            total_countries = lt.size(torneo["countries"])
            total_cities = lt.size(torneo["cities1"])
            most_matches = 0
            city_most_matches = None
            for city in torneo["cities2"]:
                if torneo["cities2"][city] > most_matches:
                    most_matches = torneo["cities2"][city]
                    city_most_matches = city
                elif torneo["cities2"][city] == most_matches:
                    if city < city_most_matches:
                        city_most_matches = city
            info_para_tabla = lt.newList("ARRAY_LIST")
            for equipo in torneo["equipos2"]:
                lt.addLast(info_para_tabla, torneo["equipos2"][equipo])
            info_para_tabla_ordenada = merg.sort(info_para_tabla, cmp_req_6)
            tabulear = []
            if lt.size(info_para_tabla_ordenada) <= 6:
                if n > lt.size(info_para_tabla_ordenada):
                    for i in range(1, lt.size(info_para_tabla_ordenada)+1):
                        tabulear.append(lt.getElement(info_para_tabla_ordenada, i))
                elif n < lt.size(info_para_tabla_ordenada):
                    for i in range(1, n+1):
                        tabulear.append(lt.getElement(info_para_tabla_ordenada, i))
            elif n <= lt.size(info_para_tabla_ordenada):
                if n >= 6:
                    for i in range(1, 4):
                        tabulear.append(lt.getElement(info_para_tabla_ordenada, i))
                    for j in range(n-2, n+1):
                        tabulear.append(lt.getElement(info_para_tabla_ordenada, j))
                elif n < 6:
                    for i in range(1, n+1):
                        tabulear.append(lt.getElement(info_para_tabla_ordenada, i))
            else:
                for i in range(1, 4):
                    tabulear.append(lt.getElement(info_para_tabla_ordenada, i))
                for j in range(lt.size(info_para_tabla_ordenada)-2, lt.size(info_para_tabla_ordenada)+1):
                    tabulear.append(lt.getElement(info_para_tabla_ordenada, j))
            return total_tournaments, total_teams, total_matches, total_countries, total_cities, city_most_matches, tabulear
        except:
            total_tournaments = 0
            for i in info_anio["value"]:
                total_tournaments  += 1
            return total_tournaments, 0, 0, 0, 0, None, []
    except:
        return 0, 0, 0, 0, 0, None, []


def req_7(data_structs, puntaje_jugador, torneo):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    
    goles=0
    penales= 0
    autogoles = 0
    players_con_puntos = 0
    respuesta= lt.newList("ARRAY_LIST")
    mapa_respuesta = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    try:
        lista_torneo=me.getValue(mp.get(data_structs["model"]["tournaments_req7"],torneo))
        for partido in lt.iterator(lista_torneo):
                if not mp.contains(mapa_respuesta, partido["scorer"]):
                    jugador = lt.newList("ARRAY_LIST")
                    lt.addLast(jugador,partido["scorer"]) #1
                    lt.addLast(jugador,0) #2
                    lt.addLast(jugador,0) #3
                    if partido["penalty"]=="True":
                        lt.addLast(jugador,1) #4
                        penales +=1
                    else:
                        lt.addLast(jugador,0) #4
                    if partido["own_goal"]=="True":
                        lt.addLast(jugador,1) #5
                        autogoles +=1
                    else:
                        lt.addLast(jugador,0) #5
                    if partido["minute"]!= "":
                        lt.addLast(jugador,partido["minute"]) #6
                    else: 
                        lt.addLast(jugador,-1)#6
                    if partido["home_score"]==partido["away_score"]:
                        lt.addLast(jugador,0)#7
                        lt.addLast(jugador,0)#8
                        lt.addLast(jugador,1)#9     
                    if partido["team"]==partido["home_team"]:
                        if partido["home_score"]>partido["away_score"]:
                            lt.addLast(jugador,1)#7
                            lt.addLast(jugador,0)#8
                            lt.addLast(jugador,0)#9
                        if partido["home_score"]<partido["away_score"]:
                            lt.addLast(jugador,0)#7
                            lt.addLast(jugador,1)#8
                            lt.addLast(jugador,0)#9
                    elif partido["team"]==partido["away_team"]:
                        if partido["home_score"]<partido["away_score"]:
                            lt.addLast(jugador,1)#7
                            lt.addLast(jugador,0)#8
                            lt.addLast(jugador,0)#9
                        if partido["home_score"]>partido["away_score"]:
                            lt.addLast(jugador,0)#7
                            lt.addLast(jugador,1)#8
                            lt.addLast(jugador,0)#9
                    ultimo_partido = lt.newList("ARRAY_LIST")
                    lt.addLast(ultimo_partido,convert_time(partido["date"]))
                    lt.addLast(ultimo_partido,partido["tournament"])
                    lt.addLast(ultimo_partido,partido["home_team"])
                    lt.addLast(ultimo_partido,partido["away_team"])
                    lt.addLast(ultimo_partido,partido["home_score"])
                    lt.addLast(ultimo_partido,partido["away_score"])
                    lt.addLast(ultimo_partido,partido["minute"])
                    lt.addLast(ultimo_partido,partido["penalty"])
                    lt.addLast(ultimo_partido,partido["own_goal"])
                    lt.addLast(jugador, ultimo_partido)#10
                    #actualizo
                    posicion = jugador["elements"]
                    lt.actualizar_lista(jugador,3,(posicion[6]+posicion[7]+posicion[8]))
                    lt.actualizar_lista(jugador,2,(posicion[2]-posicion[4]+posicion[3]))
                    mp.put(mapa_respuesta,partido["scorer"],jugador)
                else:
                    valor_hash=me.getValue(mp.get(mapa_respuesta,partido["scorer"]))
                    posicion = valor_hash["elements"]
                    if partido["penalty"]=="True": 
                        lt.actualizar_lista(valor_hash,4,(posicion[3]+1))
                    if partido["own_goal"]=="True": 
                        lt.actualizar_lista(valor_hash,5,(posicion[4]+1))
                    if partido["minute"]!= "":
                        lt.actualizar_lista(valor_hash,6,((posicion[5]+partido["minute"])/2))
                    if partido["team"]==partido["home_team"]:
                        if partido["home_score"]>partido["away_score"]:
                            lt.actualizar_lista(valor_hash,7,(posicion[6]+1))#7
                        if partido["home_score"]<partido["away_score"]:
                            lt.actualizar_lista(valor_hash,8,(posicion[7]+1))#8
                    elif partido["team"]==partido["away_team"]:
                        if partido["home_score"]<partido["away_score"]:
                            lt.actualizar_lista(valor_hash,7,(posicion[6]+1))#7
                        if partido["home_score"]>partido["away_score"]:
                            lt.actualizar_lista(valor_hash,8,(posicion[7]+1))#8
                    if partido["home_score"]==partido["away_score"]:
                        lt.actualizar_lista(valor_hash,9,(posicion[8]+1))#9
                    lt.actualizar_lista(valor_hash,3,(posicion[6]+posicion[7]+posicion[8]))
                    lt.actualizar_lista(valor_hash,2,(posicion[2]-posicion[4]+posicion[3]))
                    tabulate_ultimo_gol =lt.getElement(valor_hash,10)
                    if lt.getElement(tabulate_ultimo_gol,1)>convert_time(partido["date"]):
                        ultimo_partido = lt.newList("ARRAY_LIST")
                        lt.addLast(ultimo_partido,convert_time(partido["date"]))
                        lt.addLast(ultimo_partido,partido["tournament"])
                        lt.addLast(ultimo_partido,partido["home_team"])
                        lt.addLast(ultimo_partido,partido["away_team"])
                        lt.addLast(ultimo_partido,partido["home_score"])
                        lt.addLast(ultimo_partido,partido["away_score"])
                        lt.addLast(ultimo_partido,partido["minute"])
                        lt.addLast(ultimo_partido,partido["penalty"])
                        lt.addLast(ultimo_partido,partido["own_goal"])
                        lt.actualizar_lista(valor_hash,10,ultimo_partido)
                    mp.put(mapa_respuesta,partido["scorer"],valor_hash)
                    valores_finales = mp.valueSet(mapa_respuesta)
                    for jugador in lt.iterator(valores_finales):
                        lt.addLast(respuesta,jugador) 
        lista_auxiliar=lt.newList("ARRAY_LIST")
        for i in lt.iterator(respuesta):
                if lt.getElement(i,2)==puntaje_jugador and i["elements"] not in lista_auxiliar["elements"]:
                    players_con_puntos+=1
                    lt.addLast(lista_auxiliar,i["elements"])
        respuesta=lista_auxiliar
        respuesta = merg.sort(respuesta,cmp_req7)
        num_jugadores = mp.size(mapa_respuesta)
        num_torneos = lt.size(lt.quitar_repetidos(data_structs["model"]["num_tournaments_req7"]))
            ###### Me olvido de DISClib y vuelvo a listas canónicas para retornar algo fácil de tabulatear################
        for i in lt.iterator(respuesta):      
                i[9]=i[9]["elements"]
            
        primeros=None
        ultimos=None
        lista_dentro = respuesta["elements"]
        if len(lista_dentro)>5:
                primeros = lista_dentro[:3]
                ultimos = lista_dentro[-3:]
        else:
                lista_dentro=primeros
        headers_ultimo_gol=["date","tournament","home_team","away_team","home_score","away_score","minute","penalty","own_goal"]
        for i in primeros:
                posicion_para_tabulate = [headers_ultimo_gol,i[9]]
                i[9]=tabulate(posicion_para_tabulate, headers="firstrow")
        for i in ultimos:
                posicion_para_tabulate = [headers_ultimo_gol,i[9]]
                i[9]=tabulate(posicion_para_tabulate, headers="firstrow")
        todo = [ ]
        for i in primeros:
                todo.append(i)
        for i in ultimos:
                todo.append(i)
        partidos_totales = me.getValue(mp.get(data_structs["model"]["loqfalta"],torneo))
        goles=me.getValue(mp.get(data_structs["model"]["loqfalta_total_goals"],torneo))
        return todo,ultimos,num_jugadores,num_torneos,goles,partidos_totales,penales,autogoles, players_con_puntos
    except:
        return [ ],[ ],"invalid", "invalid","invalid","invalid","invalid","invalid","invalid"      
    """       
        jugador = {"scorer": "unkown",#1
                   "total_points": 0,#2
                   "total_goals": 0,#3
                   "penalty_goals": 0,#4
                   "own_goals": 0,#5
                   "avg_time": 0,#6
                   "scored_in_wins": 0,#7
                   "scored_in_losses": 0,#8
                   "scored_in_draws":0,#9
                   "last_goal":0}#10
        jugador["scorer"]=partido["scorer"]
        if partido["penalty"]=="True":
            jugador["penalty_goals"]+=1
        if partido["own_goal"]=="True":
            jugador["own_goals"]+=1
        if partido["minute"]!= "":
            jugador["avg_time"]=partido["minute"]
        else: 
            jugador["avg_time"]=-1
        if jugador["avg_time"]
    """
def add_req_8(mapo, data, team):

    d8 = {"year":None,
           "matches":0,
           "total_points": 0,
           "goal_diference":0,
           "penalties":0,
           "own_goals":0,
           "wins":0,
           "draws":0,
           "losses":0,
           "goals_for":0,
           "goals_againts":0}
    
    year = str(data["date"].split("-")[0])
    matches = 0
    puntos = 0
    wins = 0
    losses = 0
    draws = 0
    goalsf = 0
    goalsg =0
    owng = 0
    penalty = 0
    listo = lt.newList("SINGLE_LINKED")
    if mp.contains(mapo,year) == False:
        matches += 1
        if data["home_team"] == team:

            if data["home_score"] > data["away_score"]:
                wins+=1

            elif data["home_score"] < data["away_score"]:
                losses+=1

            else:
                draws+=1
            goalsg = int(data["away_score"])
            goalsf = int(data["home_score"])

        elif data["away_team"] == team:
                     
            if data["home_score"] > data["away_score"]:
                losses+=1
            elif data["home_score"] < data["away_score"]:
                wins+=1
            else:
                draws+=1
            goalsf = int(data["away_score"])
            goalsg = int(data["home_score"])
            
        if data["own_goal"]!="False":
            owng += 1
        if data["penalty"]!="False":
            penalty+=1
        
        goaldif = int(goalsf) - int(goalsg)
        puntos = int(wins)*3 + int(draws)
        d8["year"] = year
        d8["matches"] = matches
        d8["total_points"] = puntos
        d8["goal_diference"] = goaldif
        d8["wins"] = wins
        d8["goals_for"] = int(goalsf)
        d8["goals_againts"] = int(goalsg)
        d8["draws"] = draws
        d8["losses"] = losses
        d8["penalties"] = penalty
        d8["own_goals"] = owng
        
        lt.addFirst(listo,d8)

    elif mp.contains(mapo,year) == True:
        listo = me.getValue(mp.get(mapo,year))
        cf = lt.firstElement(listo)
        matches += 1
        if data["home_team"] == team:
                if data["home_score"] < data["away_score"]:
                    losses= 1 + cf["losses"]
                elif data["home_score"] > data["away_score"]:
                    wins = 1 + cf["wins"]
                else:
                    draws= 1 + cf["draws"]
                goalsf = int(data["home_score"]) + cf["goals_for"]
                goalsg = int(data["awat_score"]) + cf["goals_againts"]

        elif data["away_team"] == team:
            if data["home_score"] > data["away_score"]:
                    losses = 1 + cf["losses"]
            elif data["home_score"] < data["away_score"]:
                    wins = 1 + cf["wins"]
            else:
                    draws = 1 + cf["draws"]
            goalsf = int(data["away_score"]) + cf["goals_for"]
            goalsg = int(data["home_score"]) + cf["goals_againts"]
        
        if data["penalty"] != "False":
            penalty = 1 + cf["penaltis"]
        if data["penalty"]!="False":
            owng = 1 + cf["own_goals"]

        
        goaldif = goalsf - goalsg
        puntos = wins*3 + draws
        d8["year"] = year
        d8["matches"] = matches + cf["matches"]
        d8["total_points"] = puntos
        d8["goal_diference"] = goaldif
        d8["wins"] = wins
        d8["goals_for"] = goalsf
        d8["goals_againts"] = goalsg
        d8["draws"] = draws
        d8["losses"] = losses
        d8["own_goals"] = owng
        d8["penalties"] = penalty

        lt.addFirst(listo,d8)

    return listo

        



def req_8(data_structs,pais,f1,f2):

    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    years = lt.newList("ARRAY_LIST")
    parasortear2 = lt.newList("ARRAY_LIST")
    parasortear = lt.newList("ARRAY_LIST") 
    
    mapo_resulto = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4,
                                   cmpfunction=cmp_fecha)
    
    paway = data_structs["away_teams"]
    phome = data_structs["home_teams"]
    away = me.getValue(mp.get(paway,pais))
    home = me.getValue(mp.get(phome,pais))
    npaway = 0
    nphome = 0

    #Logica para sacar el total de partidos away y crear el mapa que tiene como llaves los años
    #Tambien se sacan los partidos completos para sortearlos y sacar asi el más reciente
    for z in lt.iterator(away):
        if (f1 <= yearo or yearo <= f2) and z["tournament"] != "Friendly":
            year = z["date"].split("-")[0]
            npaway+=1
            lt.addLast(parasortear2,z)
            #agregar año a lista para iterar despues
            if int(npaway) == 1:
                lt.addLast(years,year)
            elif lt.isPresent(years,year)==0:
                lt.addLast(years,year)
            mr8 = add_req_8(mapo_resulto,z,pais)
            mp.put(mapo_resulto,year,mr8)

            
    #ahora le agrego el mapa los resultados de home

    for z in lt.iterator(home):
        yearo = int(z["date"].split("-")[0])
        if (f1 <= yearo or  yearo <= f2) and z["tournament"] != "Friendly":
            year = z["date"].split("-")[0]
            lt.addLast(parasortear2,z)
            nphome+=1

            if int(nphome) == 1:
                lt.addLast(years,year)
            elif lt.isPresent(years,year)==0:
                lt.addLast(years,year)
            mr8 = add_req_8(mapo_resulto,z,pais)
            mp.put(mapo_resulto,year,mr8)
    #Pasar de mapa a lista
    for y in lt.iterator(years):
        g = mp.get(mapo_resulto,y)
        f = me.getValue(g)
        lt.addLast(parasortear,f)
        
        #Sotera y arreglar detalles para el utlmio return
        psorteados = merg.sort(parasortear2,cmp_req_4)
        pr = lt.firstElement(psorteados)
        l_tabulate=[]
        l_aux = [pr["date"],pr["home_team"],pr["away_team"],pr["away_score"],pr["country"],pr["city"],pr["tournament"]]
        l_tabulate.append(l_aux)
        pviejo = lt.lastElement(psorteados)
        dviejo = pviejo["date"]
        
        mp_sorted = merg.sort(parasortear,cmp_req_8)
        respuesta = {"away_m":npaway,
                     "home_m":nphome,
                     "last_match":l_tabulate,
                     "f_date":dviejo,
                     "data": mp_sorted}
        return respuesta


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def cmp_req_8(dato1,dato2):
    
    if dato1["year"]>dato2["year"]:
        return True
    elif dato1["year"] == dato2["year"]:
        if dato1["total_points"] > dato2["total_points"]:
            return True
        elif dato1["total_points"] < dato2["total_points"]:
            return False
        else:
            if dato1["goal_diference"] > dato2["goal_diference"]:
                return True
            elif dato1["goal_diference"] < dato2["goal_diference"]:
                return False
            else:
                if dato1["penalties"] > dato2["penalties"]:
                    return True
                elif dato1["penalties"] < dato2["penalties"]:
                    return False
                else:
                    if dato1["matches"] < dato2["matches"]:
                        return True 
                    elif dato1["matches"] > dato2["matches"]:
                        return False
                    else:
                        if dato1["own_goals"] <= dato2["own_goals"]:
                            return True
                        else:
                            return False
    else: 
        return False
    

def cmp_req_4(d1,d2):
    
    if d1["date"] > d2["date"]:
        return True
    
    elif d1["date"]==d2["date"]:
        if d1["country"] < d2["country"]:
            return True
        elif d1["country"]==d2["country"]: 
            if d1["city"] < d2["city"]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def cmp_req_2(d1,d2):
    
    if d1["date"] < d2["date"]:
        return True
    
    elif d1["date"]==d2["date"]:
        if d1["minute"] < d2["minute"]:
            return True
        else: 
            return False
    else:
        return False


def cmp_req_3(dato1, dato2):
    if dato1["date"] >= dato2["date"]:
        return False
    else:
        return True
    
def cmp_req_6(dato1, dato2):
    if dato1["total_points"] > dato2["total_points"]:
        return True
    elif dato1["total_points"] < dato2["total_points"]:
        return False
    else:
        if dato1["goal_difference"] > dato2["goal_difference"]:
            return True
        elif dato1["goal_difference"] < dato2["goal_difference"]:
            return False
        else:
            if dato1["penalty_points"] > dato2["penalty_points"]:
                return True
            elif dato1["penalty_points"] < dato2["penalty_points"]:
                return False
            else:
                if lt.size(dato1["matches"]) < lt.size(dato2["matches"]):
                    return True 
                elif lt.size(dato1["matches"]) > lt.size(dato2["matches"]):
                    return False
                else:
                    if dato1["own_goal_points"] <= dato2["own_goal_points"]:
                        return True
                    else:
                        return False

def cmp_fecha(fecha1, dic):
    fecha2 = me.getKey(dic)
    if (fecha1 == fecha2):
        return 0
    elif fecha1 > fecha2:
        return 1
    else:
        return -1
    
def fecha(fecha1, fecha2):
    if (fecha1 <= fecha2):
        return False
    else:
        return True
def cmp_fecha_req1(dato1,dato2):
    if convert_time(dato1["date"]) <= convert_time(dato2["date"]):
        return False
    else:
        return True
def cmp_goalscorers(dato1, dato2):
    if dato1["date"] < dato2["date"]:
        return False
    elif dato1["date"] > dato2["date"]:
        return True
    elif dato1["date"] == dato2["date"]:
        if dato1["minute"] < dato2["minute"]:
            return False
        elif dato1["minute"] > dato2["minute"]:
            return True
        elif dato1["minute"] == dato2["minute"]:
            if dato1["scorer"] >= dato2["scorer"]:
                return True
            else:
                return False
def cmp_req5(dato1,dato2):
    if convert_time(dato1["date"]) < convert_time(dato2["date"]):
        return False
    elif convert_time(dato1["date"]) > convert_time(dato2["date"]):
        return True
    else:
        if dato1["minute"] < dato2["minute"]:
            return False
        elif dato1["minute"] >= dato2["minute"]:
            return True

def cmp_req7(dato1,dato2):
    if dato1[1]>dato2[1]:
        return True
    elif dato1[1]<dato2[1]:
        return False
    else:
        if dato1[2]>dato2[2]:
            return True
        elif dato1[2]<dato2[2]:
            return False
        else:
            if dato1[3]>dato2[3]:
                return True
            elif dato1[3]<dato2[3]:
                return False
            else: 
                if (type(dato1[5])==str and (type(dato2[5])==int or type(dato2[5])==float)) or (type(dato1[5])==str and type(dato2[5])==str):
                    return False
                elif (type(dato2[5])==str and (type(dato1[5])==int or type(dato1[5])==float)):
                    return True
                else:
                    if dato1[5]<dato2[5]:
                        return True
                    else:
                        return False