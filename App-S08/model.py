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
# ========================
# Construccion de modelos
# ========================

def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    data_structs={"results": None,
                  "goalscorers": None,
                  "shootouts": None,
                  "scorers": None,
                  "home_team": None,
                  "away_team": None,
                  "tournament": None,
                  "date": None}
    
    data_structs['results'] = lt.newList('SINGLE_LINKED')
    data_structs['goalscorers'] = lt.newList('SINGLE_LINKED')
    data_structs['shootouts'] = lt.newList('SINGLE_LINKED') 

    data_structs["scorers"]=mp.newMap(10278,
                                    maptype='CHAINING',
                                    loadfactor=4,
                                    cmpfunction=None)
    data_structs['home_team']=mp.newMap(21468,
                                         maptype= 'CHAINING',
                                         loadfactor=4,
                                         cmpfunction=None)
    data_structs['away_team']=mp.newMap(21468,
                                         maptype= 'CHAINING',
                                         loadfactor=4,
                                         cmpfunction=None)
    data_structs['tournament']=mp.newMap(11190,
                                         maptype= 'CHAINING',
                                         loadfactor=4,
                                         cmpfunction=None)
    data_structs['date']=mp.newMap(10278,
                                         maptype= 'CHAINING',
                                         loadfactor=4,
                                         cmpfunction=None)
    return data_structs

# =============================================
# Funciones para agregar informacion al modelo
# =============================================

def addResult(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista results
    """
    lt.addFirst(data_structs['results'], data)
    addhometeam(data_structs,data, 1)
    addawayteam(data_structs,data, 1)
    addtournament(data_structs, data)
    addfecha(data_structs, data, 1)

def addGoalscorer(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista goalscorers
    """
    lt.addFirst(data_structs['goalscorers'], data)
    addScorer(data_structs,data)
    addhometeam(data_structs,data, 2)
    addawayteam(data_structs,data, 2)
    addfecha(data_structs, data, 2)

def addShootout(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista shootouts
    """
    lt.addFirst(data_structs['shootouts'], data)

def addScorer(data_structs,data):
    scorers=data_structs["scorers"]
    existscorer=mp.contains(scorers,data["scorer"])
    if existscorer: 
        entry=mp.get(scorers,data["scorer"])
        scorer=me.getValue(entry)
    else: 
        scorer=NewScorer(data)
        mp.put(scorers,data["scorer"],scorer)
    lt.addFirst(scorer["goal_data"],data)

def addhometeam(data_structs,data, archivo):
    teams=data_structs["home_team"]
    existscorer=mp.contains(teams,data["home_team"])
    if existscorer: 
        entry=mp.get(teams,data["home_team"])
        team=me.getValue(entry)
    else: 
        team=newhometeam(data)
        mp.put(teams,data["home_team"],team)
    if archivo==1:
        lt.addFirst(team["results_data"],data)
    elif archivo==2:
        lt.addFirst(team["goalscorers_data"],data)

def addawayteam(data_structs, data, archivo):
    teams=data_structs["away_team"]
    existscorer=mp.contains(teams,data["away_team"])
    if existscorer: 
        entry=mp.get(teams,data["away_team"])
        team=me.getValue(entry)
    else: 
        team=newhometeam(data)
        mp.put(teams,data["away_team"],team)
    if archivo==1:
        lt.addFirst(team["results_data"],data)
    elif archivo==2:
        lt.addFirst(team["goalscorers_data"],data)

def addtournament(data_structs, data):
    tournaments= data_structs["tournament"]
    existscorer=mp.contains(tournaments,data["tournament"])
    if existscorer: 
        entry=mp.get(tournaments,data["tournament"])
        tournament=me.getValue(entry)
    else: 
        tournament=newtournament(data)
        mp.put(tournaments,data["tournament"],tournament)
    lt.addFirst(tournament["data"],data)

def addfecha(data_structs, data, archivo):
    dates= data_structs["date"]
    existscorer=mp.contains(dates,data["date"])
    if existscorer: 
        entry=mp.get(dates,data["date"])
        date=me.getValue(entry)
    else: 
        date=newfecha(data)
        mp.put(dates,data["date"],date)
    if archivo==1:
        lt.addFirst(date["results_data"],data)
    elif archivo==2:
        lt.addFirst(date["goalscorers_data"],data)

# ===================================================
# Funciones auxiliares agregar información al modelo
# ===================================================

def NewScorer(data):
    scorer={"name":None, "goal_data":None}
    scorer["name"]=data["scorer"]
    scorer['goal_data'] = lt.newList('SINGLE_LINKED')
    return scorer

def newhometeam(data):
    team={"team":None, "results_data":None, "goalscorers_data":None}
    team["team"]=data["home_team"]
    team['results_data'] = lt.newList('SINGLE_LINKED')
    team['goalscorers_data'] = lt.newList('SINGLE_LINKED')
    team['shootouts_data'] = lt.newList('SINGLE_LINKED')
    return team

def newawayteam(data):
    team={"team":None, "results_data":None, "goalscorers_data":None}
    team["team"]=data["away_team"]
    team['results_data'] = lt.newList('SINGLE_LINKED')
    team['goalscorers_data'] = lt.newList('SINGLE_LINKED')
    team['shootouts_data'] = lt.newList('SINGLE_LINKED')
    return team

def newtournament(data):
    tournament={"tournament":None, "data":None}
    tournament["tournament"] = data["tournament"]
    tournament["data"] = lt.newList('SINGLE_LINKED')
    return tournament

def newfecha(data):
    date={"date":None, "results_data":None, "goalscorers_data": None}
    date["date"] = data["date"]
    date["results_data"] = lt.newList('SINGLE_LINKED')
    date["goalscorers_data"] = lt.newList('SINGLE_LINKED')
    return date
# =========================
# Funciones tamaños listas 
# =========================
def SizeList(control,key):
    return lt.size(control[key])

# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

def obtener_info(data, valor, type):
    pareja = mp.get(data, valor)
    x = None
    if pareja:
        if type==1:
            x  = me.getValue(pareja)['results_data']
        elif type==2:
            x  = me.getValue(pareja)['goalscorers_data']
        elif type==3:
            x  = me.getValue(pareja)['goal_data']
        elif type==4:
            x  = me.getValue(pareja)['data']
    return x

def req_1(data_structs, n, country, condicion):
    """
    Función que soluciona el requerimiento 1
    """
    equipos_totales = []
    for k in lt.iterator(mp.keySet(data_structs['home_team'])):
        if k not in equipos_totales:
            equipos_totales.append(k)
    for k in lt.iterator(mp.keySet(data_structs['away_team'])):
        if k not in equipos_totales:
            equipos_totales.append(k)
    equipos_totales = len(equipos_totales)
    home= obtener_info(data_structs['home_team'], country, 1)
    away= obtener_info(data_structs['away_team'], country, 1)
    juegos_pais = lt.size(home) + lt.size(away)
    juegos_condicion = 0
    answer= lt.newList('SINGLE_LINKED')
    if condicion=="indiferente":
        for element in lt.iterator(home):
                lt.addFirst(answer, element)
        for element in lt.iterator(away):
                lt.addFirst(answer, element)
        juegos_condicion= juegos_pais
    elif condicion=="home_team":
        for element in lt.iterator(home):
            if element["neutral"]=="False":
                lt.addFirst(answer, element)
                juegos_condicion+= 1
    elif condicion=="away_team":
        for element in lt.iterator(away):
            if element["neutral"]=="False":
                lt.addFirst(answer, element)
                juegos_condicion+= 1
    sa.sort(answer, sort_criteria_date_menor)
    size_a= lt.size(answer)
    if size_a>=n:
        answer=lt.subList(answer, 1, n)
    size= lt.size(answer)
    return answer, equipos_totales, juegos_pais, juegos_condicion, size

def req_2(data_structs, number, player):
    """
    Función que soluciona el requerimiento 2
    """
    data=data_structs["scorers"]
    existscorers=mp.contains(data,player)
    goal_number=lt.newList("SINGLE_LINKED")
    total_jugadores=lt.size(mp.keySet(data))
    if existscorers:
        entry=mp.get(data,player)
        value=me.getValue(entry)
        total_goals=lt.size(value['goal_data'])
        total_penaltis=0
        for juego in lt.iterator(value['goal_data']):
            if juego["penalty"]=="True":
                total_penaltis+=1
            lt.addFirst(goal_number, juego)
        sa.sort(goal_number, sort_criteria_date_menor)
        if lt.size(goal_number)<=number:
            size=lt.size(goal_number)
            return goal_number, total_jugadores, total_goals, total_penaltis, size
        else:
            answer=lt.subList(goal_number, 1, number)
            size=lt.size(answer)
            return answer, total_jugadores, total_goals, total_penaltis, size
    else: 
        return "El jugador no existe en la base de datos"


def req_3(data_structs, country, fecha_1, fecha_2):
    """
    Función que soluciona el requerimiento 3
    """
    equipos_totales = []
    for k in lt.iterator(mp.keySet(data_structs['home_team'])):
        if k not in equipos_totales:
            equipos_totales.append(k)
    for k in lt.iterator(mp.keySet(data_structs['away_team'])):
        if k not in equipos_totales:
            equipos_totales.append(k)
    equipos_totales = len(equipos_totales)
    home_r= obtener_info(data_structs['home_team'], country, 1)
    away_r= obtener_info(data_structs['away_team'], country, 1) 
    home_games=0
    away_games=0
    answer=lt.newList("SINGLE_LINKED") 
    for game_h_r in lt.iterator(home_r):
        dict_game= {}
        lista=game_h_r["date"].split("-")
        fecha=int((lista[0]+lista[1]+lista[2]))
        if (fecha>fecha_1 and fecha<fecha_2):
            home_games += 1
            dict_game["date"]=game_h_r["date"]
            dict_game["home_score"]=game_h_r["home_score"]
            dict_game["away_score"]=game_h_r["away_score"]
            dict_game["home_team"]=game_h_r["home_team"]
            dict_game["away_team"]=game_h_r["away_team"]
            dict_game["country"]=game_h_r["country"]
            dict_game["city"]=game_h_r["city"]
            dict_game["tournament"]=game_h_r["tournament"]
            dict_game["penalty"]="Unknown"
            dict_game["own_goal"]="Unknown"
            esta=mp.contains(data_structs["date"], game_h_r["date"])
            if esta:
                lista_fechas=obtener_info(data_structs['date'], game_h_r["date"], 2)
                for fecha in lt.iterator(lista_fechas):
                    if fecha['home_team']==game_h_r["home_team"] and fecha['away_team']==game_h_r["away_team"]:
                        if fecha["penalty"]!=None:
                            dict_game["penalty"]=fecha["penalty"]
                        if fecha["own_goal"]!=None:
                            dict_game["own_goal"]=fecha["own_goal"]
            lt.addFirst(answer, dict_game)
    for game_a_r in lt.iterator(away_r):
        dict_game= {}
        lista=game_a_r["date"].split("-")
        fecha=int((lista[0]+lista[1]+lista[2]))
        if (fecha>fecha_1 and fecha<fecha_2):
            away_games += 1
            dict_game["date"]=game_a_r["date"]
            dict_game["home_score"]=game_a_r["home_score"]
            dict_game["away_score"]=game_a_r["away_score"]
            dict_game["home_team"]=game_a_r["home_team"]
            dict_game["away_team"]=game_a_r["away_team"]
            dict_game["country"]=game_a_r["country"]
            dict_game["city"]=game_a_r["city"]
            dict_game["tournament"]=game_a_r["tournament"]
            dict_game["penalty"]="Unknown"
            dict_game["own_goal"]="Unknown"
            esta=mp.contains(data_structs["date"], game_a_r["date"])
            if esta:
                lista_fechas=obtener_info(data_structs['date'], game_a_r["date"], 2)
                for fecha in lt.iterator(lista_fechas):
                    if fecha['home_team']==game_a_r["home_team"] and fecha['away_team']==game_a_r["away_team"]:
                        if fecha["penalty"]!=None:
                            dict_game["penalty"]=fecha["penalty"]
                        if fecha["own_goal"]!=None:
                            dict_game["own_goal"]=fecha["own_goal"]
            lt.addFirst(answer, dict_game)
    sa.sort(answer, sort_criteria_date_mayor)
    total_games=lt.size(answer)
    return answer, equipos_totales, total_games, home_games, away_games
def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs, name, fecha_1, fecha_2):
    """
    Función que soluciona el requerimiento 5
    """
    jugadores_totales=[]
    for k in lt.iterator(mp.keySet(data_structs['scorers'])):
        if k not in jugadores_totales:
            jugadores_totales.append(k)
    jugadores_totales=len(jugadores_totales)
    scorers_r=obtener_info(data_structs['scorers'], name, 3)
    anotaciones=0
    penales=0
    autogoles=0
    torneos=0
    answer=lt.newList("SINGLE_LINKED") 
    for scorers_inf in lt.iterator(scorers_r):
        dict_game={}
        lista=scorers_inf["date"].split("-")
        fecha=int((lista[0]+lista[1]+lista[2]))
        if (fecha>fecha_1 and fecha<fecha_2):
            anotaciones+=1
            dict_game["date"]=scorers_inf["date"]
            dict_game["minute"]=scorers_inf["minute"]
            dict_game["home_team"]=scorers_inf["home_team"]
            dict_game["away_team"]=scorers_inf["away_team"]
            dict_game["team"]=scorers_inf["team"]
            dict_game["home_score"]="Unknown"
            dict_game["away_score"]="Unknown"
            dict_game["tournament"]="Unknown"
            dict_game["penalty"]=scorers_inf["penalty"]
            dict_game["own_goal"]=scorers_inf["own_goal"]
            if scorers_inf["own_goal"]==True:
                autogoles+=1
            if scorers_inf["penalty"]==True:
                penales+=1
            e=False
            n=1
            home_r= obtener_info(data_structs['home_team'], scorers_inf["team"], 1)
            while e==False and n<=lt.size(home_r):
                tourn_info=lt.getElement(home_r, n)
                lista=tourn_info["date"].split("-")
                fecha_g=int((lista[0]+lista[1]+lista[2]))
                if fecha_g==fecha and tourn_info["home_team"]==scorers_inf["home_team"] and tourn_info["away_team"]==scorers_inf["away_team"]:
                    if tourn_info["home_score"]!=None:
                        dict_game["home_score"]=tourn_info["home_score"]
                    if tourn_info["away_score"]!=None:
                        dict_game["away_score"]=tourn_info["away_score"]
                    if tourn_info["tournament"]!=None:
                        dict_game["tournament"]=tourn_info["tournament"]
                        torneos+=1
                    e=True
                n+=1
            e=False
            n=1
            away_r= obtener_info(data_structs['away_team'], scorers_inf["team"], 1)
            while e==False and n<=lt.size(away_r):
                tourn_info=lt.getElement(away_r, n)
                lista=tourn_info["date"].split("-")
                fecha_g=int((lista[0]+lista[1]+lista[2]))
                if fecha_g==fecha and tourn_info["home_team"]==scorers_inf["home_team"] and tourn_info["away_team"]==scorers_inf["away_team"]:
                    if tourn_info["home_score"]!=None:
                        dict_game["home_score"]=tourn_info["home_score"]
                    if tourn_info["away_score"]!=None:
                        dict_game["away_score"]=tourn_info["away_score"]
                    if tourn_info["tournament"]!=None:
                        dict_game["tournament"]=tourn_info["tournament"]
                        torneos+=1
                    e=True
                n+=1
            lt.addFirst(answer, dict_game)
    sa.sort(answer, sort_criteria_date_menor)
    total_games=lt.size(answer)
    return answer, jugadores_totales, torneos, penales, autogoles, anotaciones


def req_6(data_structs, torneo, anio, n_equipos):
    """
    Función que soluciona el requerimiento 3
    """
    anio_calendario_i=f"{anio}-01-01"
    anio_calendario_f=f"{anio}-12-31"

    t_torneos=0
    teams=[]
    ciudades=[]
    ciudades_t=[]
    paises=[]
    torneos_l=[]

    w=1
    results=data_structs["results"]

    while w<lt.size(results):
        game_r=lt.getElement(results, w)
        lista=game_r["date"].split("-")
        if anio==lista[0] and game_r["tournament"] not in torneos_l:
            t_torneos+=1
            torneos_l.append(game_r["tournament"])
        w+=1

    tournament=obtener_info(data_structs["tournament"],torneo,4)
    t_encuentros=0
    answer=lt.newList("SINGLE_LINKED") 
    for info_t in lt.iterator(tournament):
        dict_game={}
        dict_jugador={}
        lista=info_t["date"].split("-")
        if anio==lista[0]:
            t_encuentros += 1
            ciudades_t.append(info_t["city"])
            if info_t["city"] not in ciudades:
                ciudades.append(info_t["city"])
            if info_t["country"] not in paises:
                paises.append(info_t["country"])
            n=1
            home_g= obtener_info(data_structs['home_team'], info_t["home_team"], 1)
            home_r= obtener_info(data_structs['home_team'], info_t["home_team"], 2)
            away_g= obtener_info(data_structs['away_team'], info_t["home_team"], 1)
            away_r= obtener_info(data_structs['away_team'], info_t["home_team"], 2)
            puntos_penal=0
            puntos_autogol=0
            total_puntos=0
            goles_marcados=0
            goles_en_contra=0
            total_partidos_disputados=0
            victorias=0
            empates=0
            derrotas=0
            if home_g!=None:
                while n<=lt.size(home_g):
                    info_p_h=lt.getElement(home_g, n)
                    lista=info_p_h["date"].split("-")
                    if lista[0]==anio and info_p_h["tournament"]==torneo:
                        total_partidos_disputados+=1
                        goles_marcados+=int(info_p_h["home_score"])
                        goles_en_contra+=int(info_p_h["away_score"])
                        if int(info_p_h["home_score"])>int(info_p_h["away_score"]):
                            total_puntos+=3
                            victorias+=1
                        if  int(info_p_h["home_score"])==int(info_p_h["away_score"]):
                            total_puntos+=1
                            empates+=1
                        if int(info_p_h["home_score"])<int(info_p_h["away_score"]):
                            derrotas+=1
                    n+=1
            n=1
            if home_r!=None:
                while n<=lt.size(home_r):
                    info_h_r=lt.getElement(home_r, n)
                    lista=info_h_r["date"].split("-")
                    if lista[0]==anio and info_h_r["home_team"]==info_t["home_team"] and info_h_r["away_team"]== info_t["away_team"]:
                        if info_h_r["penalty"]=="True":
                            puntos_penal+=1
                        if info_h_r["own_goal"]=="True":
                            puntos_autogol+=1
                        if info_h_r["scorer"] not in dict_jugador:
                                dict_jugador[info_h_r["scorer"]]={"scorer":info_h_r["scorer"],
                                                                    "goals": 0,
                                                                    "matches":[],
                                                                    "avg_time [min]":0}
                        dict_jugador[info_h_r["scorer"]]["goals"]+=1
                        if info_h_r["date"] not in dict_jugador[info_h_r["scorer"]]["matches"]:
                            dict_jugador[info_h_r["scorer"]]["matches"].append(info_h_r["date"])
                        dict_jugador[info_h_r["scorer"]]["avg_time [min]"]+=float(info_h_r["minute"])
                    n+=1
            n=1
            if away_g!=None:
                while n<=lt.size(away_g):
                    info_p_w=lt.getElement(away_g, n)
                    lista=info_p_w["date"].split("-")
                    if lista[0]==anio and info_p_w["tournament"]==torneo:
                        total_partidos_disputados+=1
                        goles_marcados+=int(info_p_w["away_score"])
                        goles_en_contra+=int(info_p_w["home_score"])
                        if int(info_p_w["away_score"])>int(info_p_w["home_score"]):
                            total_puntos+=3
                            victorias+=1
                        if  int(info_p_w["away_score"])==int(info_p_w["home_score"]):
                            total_puntos+=1
                            empates+=1
                        if int(info_p_w["away_score"])<int(info_p_w["home_score"]):
                            derrotas+=1  
                    n+=1
            n=1
            if away_r!=None:
                while n<=lt.size(away_r):
                    info_p_r=lt.getElement(away_r, n)
                    lista=info_p_r["date"].split("-")
                    if lista[0]==anio and info_p_r["home_team"]==info_t["home_team"] and info_p_r["away_team"]== info_t["away_team"]:
                        if info_p_r["penalty"]=="True":
                            puntos_penal+=1
                        if info_p_r["own_goal"]=="True":
                            puntos_autogol+=1    
                        if info_p_r["scorer"] not in dict_jugador:
                            dict_jugador[info_p_r["scorer"]]={"scorer":info_p_r["scorer"],
                                                                "goals": 0,
                                                                "matches":[],
                                                                "avg_time [min]":0}
                        dict_jugador[info_p_r["scorer"]]["goals"]+=1
                        if info_p_r["date"] not in dict_jugador[info_p_r["scorer"]]["matches"]:
                            dict_jugador[info_p_r["scorer"]]["matches"].append(info_p_r["date"])
                        dict_jugador[info_p_r["scorer"]]["avg_time [min]"]+=float(info_p_r["minute"])
                    n+=1
                                         
                            
            dict_game["team"]= info_t["home_team"] #El nombre del equipo.
            teams.append(info_t["home_team"])
            dict_game["total_points"]=total_puntos #El total de puntos obtenidos(el total de puntos obtenidos es la suma de tres (3) puntos por cada partido ganado, uno (1) por cada empate y cero (0) por cada derrota.)
            dict_game["goal_difference"]=goles_marcados-goles_en_contra #La diferencia de goles(La diferencia de goles se calcula como el total de goles marcados menos el total de goles recibidos.)
            dict_game["matches"]=total_partidos_disputados #El total de partidos disputados.
            dict_game["penalty_points"]=puntos_penal #El total de puntos obtenidos desde la línea penal.
            dict_game["own_goal_points"]=puntos_autogol #El total de puntos recibidos por autogol.
            dict_game["wins"]=victorias #El total de victorias.
            dict_game["draws"]=empates #El total de empates.
            dict_game["losses"]=derrotas #El total de derrotas
            dict_game["goals_for"]=goles_marcados #El total de goles obtenidos por sus jugadores.
            dict_game["goals_against"]=goles_en_contra #El total de goles recibidos por el equipo.
            dict_game["top_scorer"]=dict_jugador
            if len(dict_game)!=0:
                lt.addFirst(answer, dict_game)
    for info_t in lt.iterator(tournament):
        dict_game= {}
        dict_jugador={}
        lista=info_t["date"].split("-")
        fecha=int((lista[0]+lista[1]+lista[2]))
        if anio==lista[0]:
            if info_t["away_team"] not in teams:
                n=1
                home_g=obtener_info(data_structs['home_team'], info_t["away_team"], 1)
                home_r=obtener_info(data_structs['home_team'], info_t["away_team"], 2)
                away_g=obtener_info(data_structs['away_team'], info_t["away_team"], 1)
                away_r=obtener_info(data_structs['away_team'], info_t["away_team"], 2)
                total_puntos=0
                goles_marcados=0
                goles_en_contra=0
                total_partidos_disputados=0
                victorias=0
                empates=0
                derrotas=0
                n=1
                if home_g!=None:
                    while n<=lt.size(home_g):
                        info_p_h=lt.getElement(home_g, n)
                        lista=info_p_h["date"].split("-")
                        if lista[0]==anio and info_p_h["tournament"]==torneo:
                            total_partidos_disputados+=1
                            goles_marcados+=int(info_p_h["home_score"])
                            goles_en_contra+=int(info_p_h["away_score"])
                            if int(info_p_h["home_score"])>int(info_p_h["away_score"]):
                                total_puntos+=3
                                victorias+=1
                            if  int(info_p_h["home_score"])==int(info_p_h["away_score"]):
                                total_puntos+=1
                                empates+=1
                            if int(info_p_h["home_score"])<int(info_p_h["away_score"]):
                                derrotas+=1
                        n+=1
                if home_r!=None:
                    while n<=lt.size(home_r):
                        info_h_r=lt.getElement(home_r, n)
                        lista=info_h_r["date"].split("-")
                        if lista[0]==anio and info_h_r["home_team"]==info_t["home_team"] and info_h_r["away_team"]== info_t["away_team"]:
                            if info_h_r["penalty"]=="True":
                                puntos_penal+=1
                            if info_h_r["own_goal"]=="True":
                                puntos_autogol+=1
                            if info_h_r["scorer"] not in dict_jugador:
                                dict_jugador[info_h_r["scorer"]]={"scorer":info_h_r["scorer"],
                                                                    "goals": 0,
                                                                    "matches":[],
                                                                    "avg_time [min]":0}
                            dict_jugador[info_h_r["scorer"]]["goals"]+=1
                            if info_h_r["date"] not in dict_jugador[info_h_r["scorer"]]["matches"]:
                                dict_jugador[info_h_r["scorer"]]["matches"].append(info_h_r["date"])
                            dict_jugador[info_h_r["scorer"]]["avg_time [min]"]+=float(info_h_r["minute"])
                        n+=1

                n=1
                if away_g!=None:
                    while n<=lt.size(away_g):
                        info_p_w=lt.getElement(away_g, n)
                        lista=info_p_w["date"].split("-")
                        if lista[0]==anio and info_p_w["tournament"]==torneo:
                            total_partidos_disputados+=1
                            goles_marcados+=int(info_p_w["away_score"])
                            goles_en_contra+=int(info_p_w["home_score"])
                            if int(info_p_w["away_score"])>int(info_p_w["home_score"]):
                                total_puntos+=3
                                victorias+=1
                            if  int(info_p_w["away_score"])==int(info_p_w["home_score"]):
                                total_puntos+=1
                                empates+=1
                            if int(info_p_w["away_score"])<int(info_p_w["home_score"]):
                                derrotas+=1  
                        n+=1
                n=1
                if away_r!=None:
                    while n<=lt.size(away_r):
                        info_p_r=lt.getElement(away_r, n)
                        lista=info_p_r["date"].split("-")
                        if lista[0]==anio and info_p_r["home_team"]==info_t["home_team"] and info_p_r["away_team"]== info_t["away_team"]:
                            if info_p_r["penalty"]=="True":
                                puntos_penal+=1
                            if info_p_r["own_goal"]=="True":
                                puntos_autogol+=1
                            if info_p_r["scorer"] not in dict_jugador:
                                dict_jugador[info_p_r["scorer"]]={"scorer":info_p_r["scorer"],
                                                                    "goals": 0,
                                                                    "matches":[],
                                                                    "avg_time [min]":0}
                            dict_jugador[info_p_r["scorer"]]["goals"]+=1
                            if info_p_r["date"] not in dict_jugador[info_p_r["scorer"]]["matches"]:
                                dict_jugador[info_p_r["scorer"]]["matches"].append(info_p_r["date"])
                            dict_jugador[info_p_r["scorer"]]["avg_time [min]"]+=float(info_p_r["minute"])
                        n+=1
                dict_game["team"]= info_t["away_team"] #El nombre del equipo.
                teams.append(info_t["away_team"])
                dict_game["total_points"]=total_puntos #El total de puntos obtenidos(el total de puntos obtenidos es la suma de tres (3) puntos por cada partido ganado, uno (1) por cada empate y cero (0) por cada derrota.)
                dict_game["goal_difference"]=goles_marcados-goles_en_contra #La diferencia de goles(La diferencia de goles se calcula como el total de goles marcados menos el total de goles recibidos.)
                dict_game["penalty_points"]=puntos_penal #El total de puntos obtenidos desde la línea penal.
                dict_game["matches"]=total_partidos_disputados #El total de partidos disputados.
                dict_game["own_goal_points"]=puntos_autogol #El total de puntos recibidos por autogol.
                dict_game["wins"]=victorias #El total de victorias.
                dict_game["draws"]=empates #El total de empates.
                dict_game["losses"]=derrotas #El total de derrotas
                dict_game["goals_for"]=goles_marcados #El total de goles obtenidos por sus jugadores.
                dict_game["goals_against"]=goles_en_contra #El total de goles recibidos por el equipo.
                dict_game["top_scorer"]=dict_jugador
                if len(dict_game)!=0:
                    lt.addFirst(answer, dict_game)
    respuesta=lt.newList("SINGLE_LINKED")
    for juego in lt.iterator(answer):
        top_scorer=-1
        for k, v in juego["top_scorer"].items():
            if v!="Desconocido":
                v["matches"]=len( v["matches"])
                v["avg_time [min]"]=v["avg_time [min]"]/v["matches"]
                if top_scorer==-1:
                    top_scorer=v
                else:
                    if top_scorer["goals"]<v["goals"]:
                        top_scorer=v
                    elif top_scorer["goals"]==v["goals"] and top_scorer["matches"]<v["matches"]:
                        top_scorer=v
                    elif top_scorer["goals"]==v["goals"] and top_scorer["matches"]==v["matches"] and top_scorer["avg_time [min]"]>v["avg_time [min]"]:
                        top_scorer=v
        if top_scorer==-1:
            top_scorer={"scorer":"Unknow",
                        "goals": 0,
                        "matches":0,
                        "avg_time [min]":0}
        juego["top_scorer"]=top_scorer
        lt.addFirst(respuesta, juego)
    sa.sort(respuesta, ord_req_6)
    lista=lt.subList(respuesta, 1, n_equipos)
    size=lt.size(lista)
    return lista, anio_calendario_i, anio_calendario_f, t_torneos, len(teams), t_encuentros, len(paises), len(ciudades), ciudades_t, size


def req_7(data_structs, torneo, numero):
    """
    Función que soluciona el requerimiento 7
    """
    n_torneos=mp.size(data_structs['tournament'])
    torneo_list=obtener_info(data_structs['tournament'], torneo, 4)
    jugadores= {}
    juegos= 0
    goles= 0 
    penales= 0
    autogoles= 0
    for elementos in lt.iterator(torneo_list):
        fecha_t=elementos["date"]
        pais_h_t=elementos["home_team"]
        pais_a_t=elementos["away_team"]
        esta=mp.contains(data_structs['date'], fecha_t)
        if esta:
            lista_g=obtener_info(data_structs['date'], fecha_t, 2)
            for elementos_g in lt.iterator(lista_g):
                pais_h_g=elementos_g["home_team"]
                pais_a_g=elementos_g["away_team"]
                if pais_h_t==pais_h_g and pais_a_t==pais_a_g:
                    juegos+=1
                    if elementos_g["scorer"] not in jugadores:
                      jugadores[elementos_g["scorer"]]={"scorer":elementos_g["scorer"],
                                                        "total_points":0,
                                                        "total_goals":0,
                                                        "penalty_goals":0,
                                                        "own_goals":0,
                                                        "avg_time [min]":0,
                                                        "scored_in_wins":0,
                                                        "scored_in_losses":0,
                                                        "scored_in_draws":0,
                                                        "last_goal":{}}
                      
                    dict=jugadores[elementos_g["scorer"]]
                    dict["total_points"] += 1
                    dict["total_goals"] += 1
                    goles += int(elementos["home_score"])+ int(elementos["away_score"])
                    if elementos_g["penalty"]=="True":
                        penales += 1
                        dict["total_points"] += 1
                        dict["penalty_goals"] += 1
                    if elementos_g["own_goal"]=="True":
                        autogoles += 1
                        dict["total_points"] -= 1
                        dict["own_goals"] += 1
                    dict["avg_time [min]"] += float(elementos_g["minute"])
                    if elementos["home_score"]==elementos["away_score"]:
                        dict["scored_in_draws"] += 1
                    elif elementos["home_team"]==elementos_g["team"]:
                        if elementos["home_score"]>elementos["away_score"]:
                            dict["scored_in_wins"] += 1
                        else:
                            dict["scored_in_losses"] += 1
                    else:
                        if elementos["home_score"]>elementos["away_score"]:
                            dict["scored_in_losses"] += 1
                        else:
                            dict["scored_in_wins"] += 1
                    goal_dict ={"date": elementos["date"],
                                "tournament": elementos["tournament"],
                                "home_team": elementos_g["home_team"],
                                "away_team": elementos_g["away_team"],
                                "home_score": elementos["home_score"],
                                "away_score": elementos["away_score"],
                                "minute":elementos_g["minute"],
                                "penalty": elementos_g["penalty"],
                                "own_goal": elementos_g["own_goal"]} 
                    if dict["last_goal"]=={}:
                        dict["last_goal"]=goal_dict
                    else:
                        lista_goal=dict["last_goal"]["date"].split("-")
                        date=int((lista_goal[0]+lista_goal[1]+lista_goal[2]))
                        lista_fecha=fecha_t.split("-")
                        fecha=int((lista_fecha[0]+lista_fecha[1]+lista_fecha[2]))
                        if date<fecha:
                            dict["last_goal"]= goal_dict
    answer=lt.newList("SINGLE_LINKED")
    n_juegadores=0
    for jugador in jugadores:
        n_juegadores+=1
        if jugadores[jugador]["total_points"] == numero:
            jugadores[jugador]["avg_time [min]"]=round(jugadores[jugador]["avg_time [min]"]/jugadores[jugador]["total_goals"], 1)
            lt.addFirst(answer, jugadores[jugador])
    sa.sort(answer, ord_req_7)
    size=lt.size(answer)

    return answer, n_torneos, n_juegadores, juegos, goles, penales, autogoles, size

def req_8(data_structs, nombre, fecha_1, fecha_2):
    """
    Función que soluciona el requerimiento 8
    """
    fechas=mp.keySet(data_structs["date"])
    anios=[]
    for fecha in lt.iterator(fechas):
        lista_1=fecha.split("-")
        date=int((lista_1[0]+lista_1[1]+lista_1[2]))
        if int(lista_1[0])>=fecha_1 and int(lista_1[0])<=fecha_2:
            if lista_1[0] not in anios:
                anios.append(lista_1[0])
    home=obtener_info(data_structs["home_team"], nombre, 1)
    away=obtener_info(data_structs["away_team"], nombre, 1)
    juegos_home=0
    juegos_away=0
    menor=-1
    mayor=[]
    lista_fechas=[]
    for juego in lt.iterator(home):
        lista_1=juego["date"].split("-")
        date=int((lista_1[0]+lista_1[1]+lista_1[2]))
        if int(lista_1[0])>=fecha_1 and int(lista_1[0])<=fecha_2:
            juegos_home+=1
            lista_fechas.append(juego["date"])
            dict={"date": juego["date"],
                  "home_team": juego["home_team"],
                  "away_team": juego["away_team"],
                  "home_score": juego["home_score"],
                  "away_score": juego["away_score"],
                  "country": juego["country"],
                  "city": juego["city"],
                  "tournament": juego["tournament"]}
            if menor==-1:
                menor=[date, juego["date"]]
            else:
                if menor[0]>date:
                    menor=[date, juego["date"]]
            if mayor==[]:
                mayor=[date, [dict]]
            else:
                if mayor[0]<date:
                    mayor=[date, [dict]]

    for juego in lt.iterator(away):
        lista_1=juego["date"].split("-")
        date=int((lista_1[0]+lista_1[1]+lista_1[2]))
        if int(lista_1[0])>=fecha_1 and int(lista_1[0])<=fecha_2: # and juego["neutral"]=="False":
            juegos_away+=1
            lista_fechas.append(juego["date"])
            dict={"date": juego["date"],
                  "home_team": juego["home_team"],
                  "away_team": juego["away_team"],
                  "home_score": juego["home_score"],
                  "away_score": juego["away_score"],
                  "country": juego["country"],
                  "city": juego["city"],
                  "tournament": juego["tournament"]}
            if menor[0]>date:
                menor=[date, juego["date"]]
            if mayor[0]<date:
                mayor=[date, [dict]]
    juegos_totales= juegos_away+juegos_home
    menor=menor[1]
    mayor=mayor[1]
    anios=len(anios)
    juegos={}
    juegos_lista=[]
    for fecha in lista_fechas:
        fechas_r=obtener_info(data_structs["date"], fecha, 1)
        esta=mp.contains(data_structs["date"], fecha)
        if esta:
            fechas_g=obtener_info(data_structs["date"], fecha, 2)
            for juego in lt.iterator(fechas_r):
                lista=juego["date"].split("-")
                if juego["home_team"]==nombre or juego["away_team"]==nombre:
                    if lista[0] not in juegos_lista:
                        juegos[lista[0]]={"year": lista[0],
                                        "juegos": 0,
                                        "puntos_totales": 0,
                                        "diferencia_goles": 0,
                                        "penales": 0,
                                        "autogoles": 0,
                                        "victorias": 0,
                                        "empates": 0,
                                        "derrotas": 0,
                                        "goles por jugadores": 0,
                                        "goles recibidos": 0,
                                        "top scorer":{}}
                        juegos_lista.append(lista[0])
                    dict=juegos[lista[0]]
                    dict["juegos"]+=1
                    if juego["home_score"]==juego["away_score"]:
                        dict["puntos_totales"]+=1
                        dict["empates"]+=1
                    elif nombre==juego["home_team"]:
                        if int(juego["home_score"])>int(juego["away_score"]):
                            dict["puntos_totales"]+=3
                            dict["goles por jugadores"]+=int(juego["home_score"])
                            dict["victorias"]+=1
                        else:
                            dict["goles recibidos"]+=int(juego["away_score"])
                            dict["derrotas"]+=1
                    else:
                        if int(juego["home_score"])<int(juego["away_score"]):
                            dict["puntos_totales"]+=3
                            dict["goles por jugadores"]+=int(juego["away_score"])
                            dict["victorias"]+=1
                        else:
                            dict["goles recibidos"]+=int(juego["home_score"])
                            dict["derrotas"]+=1
                    for juego_g in lt.iterator(fechas_g):
                        if juego_g["home_team"]==juego["home_team"] and juego_g["away_team"]==juego["away_team"]:
                            if juego_g["penalty"]=="True":
                                dict["penales"]+=1
                            if juego_g["own_goal"]=="True":
                                dict["autogoles"]+=1
                            if juego_g["scorer"] not in dict["top scorer"]:
                                dict["top scorer"]={juego_g["scorer"]:{"jugador":juego_g["scorer"],
                                                                    "goles": 0,
                                                                    "juegos":[],
                                                                    "avr_time (min)":0}}
                            dict["top scorer"][juego_g["scorer"]]["goles"]+=1
                            if juego_g["date"] not in dict["top scorer"][juego_g["scorer"]]["juegos"]:
                                dict["top scorer"][juego_g["scorer"]]["juegos"].append(juego_g["date"])
                            dict["top scorer"][juego_g["scorer"]]["avr_time (min)"]+=float(juego_g["minute"]) 

    answer=lt.newList("SINGLE_LINKED")
    for fecha in juegos:
        juegos[fecha]["diferencia_goles"]=juegos[fecha]['goles por jugadores']-juegos[fecha]["goles recibidos"]
        top_scorer=-1
        for k,v in juegos[fecha]["top scorer"].items():
            v["juegos"]=len(v["juegos"])
            v["avr_time (min)"]=v["avr_time (min)"]/v["juegos"]
            if top_scorer==-1:
                top_scorer=v
            else:
                if top_scorer["goles"]<v["goles"]:
                    top_scorer=v
                elif top_scorer["goles"]==v["goles"] and top_scorer["juegos"]<v["juegos"]:
                    top_scorer=v
                elif top_scorer["goles"]==v["goles"] and top_scorer["juegos"]==v["juegos"] and top_scorer["avr_time (min)"]>v["avr_time (min)"]:
                    top_scorer=v
        if top_scorer==-1:
            top_scorer={"jugador":"Unknow",
                        "goles": 0,
                        "juegos":0,
                        "avr_time (min)":0}
        juegos[fecha]["top scorer"]=top_scorer
        lt.addFirst(answer, juegos[fecha])
    sa.sort(answer, ord_req_8)
    size=lt.size(answer)

    return answer, anios, juegos_totales, juegos_home, juegos_away, menor, mayor, size

# Funciones de ordenamiento

def ord_req_6(pais_1, pais_2):

    rta=sort_criteria_mayor_int(pais_1["total_points"], pais_2["total_points"])
    if rta==None:
        rta=sort_criteria_mayor_int(pais_1["goal_difference"], pais_2["goal_difference"])
        if rta==None:
            rta=sort_criteria_mayor_int(pais_1["penalty_points"], pais_2["penalty_points"])
            if rta==None:
                rta=sort_criteria_menor_int(pais_1["matches"], pais_2["matches"])
                if rta==None:
                    rta=sort_criteria_menor_int(pais_1["own_goal_points"], pais_2["own_goal_points"])
                    
    return rta

def ord_req_7(jugador_1, jugador_2):

    rta=sort_criteria_mayor_int(jugador_1["total_points"], jugador_2["total_points"])
    if rta==None:
        rta=sort_criteria_mayor_int(jugador_1["total_goals"], jugador_2["total_goals"])
        if rta==None:
            rta=sort_criteria_mayor_int(jugador_1["penalty_goals"], jugador_2["penalty_goals"])
            if rta==None:
                rta=sort_criteria_menor_int(jugador_1["own_goals"], jugador_2["own_goals"])
                if rta==None:
                    rta=sort_criteria_menor_int(jugador_1["avg_time [min]"], jugador_2["avg_time [min]"])
                    
    return rta

def ord_req_8(dato_1, dato_2):
    rta=sort_criteria_mayor_int(int(dato_1["year"]), int(dato_2["year"]))
    if rta==None:
        rta=sort_criteria_mayor_int(dato_1["puntos_totales"], dato_2["puntos_totales"])
        if rta==None:
            rta=sort_criteria_mayor_int(dato_1["diferencia_goles"], dato_2["diferencia_goles"])
            if rta==None:
                rta=sort_criteria_mayor_int(dato_1["penales"], dato_2["penales"])
                if rta==None:
                    rta=sort_criteria_menor_int(dato_1["autogoles"], dato_2["autogoles"])
                    
    return rta

def sort_criteria_date_menor(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    lista_1=data_1["date"].split("-")
    date_1=int((lista_1[0]+lista_1[1]+lista_1[2]))

    lista_2=data_2["date"].split("-")
    date_2=int((lista_2[0]+lista_2[1]+lista_2[2]))
    
    if date_1 > date_2:
        return True
    elif date_2 > date_1:
        return False
    elif date_1==date_2:
        return None

def sort_criteria_date_mayor(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    lista_1=data_1["date"].split("-")
    date_1=int((lista_1[0]+lista_1[1]+lista_1[2]))

    lista_2=data_2["date"].split("-")
    date_2=int((lista_2[0]+lista_2[1]+lista_2[2]))
    
    if date_1 < date_2:
        return True
    elif date_2 < date_1:
        return False
    elif date_1==date_2:
        return None

def sort_criteria_mayor_int(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_

    """
    if data_1 > data_2:
        return True
    elif data_2 > data_1:
        return False
    elif data_1==data_2:
        return None
    
def sort_criteria_menor_int(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_

    """
    if data_1 < data_2:
        return True
    elif data_2 < data_1:
        return False
    elif data_1==data_2:
        return None

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    sa.sort(data_structs["shootouts"],sort_criteria_date_menor)
    sa.sort(data_structs["goalscorers"],sort_criteria_date_menor)
    sa.sort(data_structs["results"],sort_criteria_date_menor)