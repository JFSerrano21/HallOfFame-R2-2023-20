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
from datetime import datetime
from tabulate import tabulate
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs(struc_list, struc_map, load_factor):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    football_data = {'match_results': None,
               'goal_scorers': None,
               'shootouts': None,
               'scorer': None}

    football_data['match_results'] = lt.newList(datastructure=struc_list,
                                                cmpfunction=cmp_partidos_by_fecha_y_pais) 
    football_data['goal_scorers'] = lt.newList(datastructure=struc_list,
                                               cmpfunction=cmp_partidos_by_fecha_y_pais) 
    football_data['shootouts'] = lt.newList(datastructure=struc_list,
                                            cmpfunction=cmp_partidos_by_fecha_y_pais)
    football_data['scorer'] = mp.newMap(152,
                             maptype=struc_map,
                             loadfactor=load_factor)
    football_data['map_TeamResults'] = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    football_data['map_TeamGoalScorers'] = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    football_data['map_TeamShootouts'] = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    football_data['map_tournament'] = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    football_data['map_Req8'] = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    football_data["map_Req8_GoalScorers"]= mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)    
    football_data["id_goalscorers"]= mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    football_data["id_results"]= mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    #Req6
    football_data['map_ResultsDates'] = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    
    football_data['map_ScoresDates'] = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    return football_data


# Funciones para agregar informacion al modelo

def add_result(football_data, data, tipo):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    nuevo2 = new_result(data,tipo)
    lt.addLast(football_data[tipo], nuevo2)


# Funciones para creacion de datos

def new_result(data, tipo):
    """
    Crea una nueva estructura para modelar los datos
    """
    nuevo = None
    if tipo == "match_results":
        nuevo = {"date":data["date"],"home_team": data["home_team"],"away_team": data["away_team"],"home_score": data["home_score"],"away_score": data["away_score"],"tournament": data["tournament"],"city": data["city"],"country": data["country"]}
    elif tipo == "goal_scorers":
        nuevo = {"date":data["date"],"home_team": data["home_team"], "away_team":data["away_team"],"team": data["team"], "scorer": data["scorer"], "minute": data["minute"],"own_goal": data["own_goal"], "penalty": data["penalty"] }
    elif tipo == "shootouts":
        nuevo = {"date":data["date"],"home_team": data["home_team"],"away_team": data["away_team"],"winner": data["winner"]}
    return nuevo
#


def newScorer(GoalScorer):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'scorer': "", "datos": None}
    entry['scorer'] = GoalScorer
    entry['datos'] = lt.newList('SINGLE_LINKED', compareYears)
    return entry

def newResultReq8(llave):
    entry = {'team': "", "datos": None}
    entry['Equipo/año'] = llave
    entry['datos'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newResult(team):
    """
    Esta funcion crea la estructura de libros asociados
    a un año.
    """
    entry = {'team': "", "datos": None}
    entry['team'] = team
    entry['datos'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newResultTournament(tournament):
    entry = {'tournament': "", "datos": None}
    entry['tournament'] = tournament
    entry['datos'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newDateEntry(date):
    entry = {}
    entry['date'] = date
    entry['datos'] = lt.newList('ARRAY_LIST')
    return entry




    
def new_Id(id):
    entry = {'id': "", "datos": None}
    entry['id'] = id
    entry['datos'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def add_Scorer(football_data, datos, GoalScorer):
    scorers = football_data['scorer']
    try:
        existyear = mp.contains(scorers, GoalScorer)
        if existyear:
            entry = mp.get(scorers, GoalScorer)
            scorer = me.getValue(entry)
        else:
            scorer = newScorer(GoalScorer)
            mp.put(scorers, GoalScorer, scorer)
        lt.addLast(scorer['datos'], datos)
    except Exception:
        return None
    
def add_MapReq8(football_data, datos, home, away, año):
    teams = football_data['map_Req8']
    llave1 = (home, año)
    llave2 = (away, año)
    try:    
        ExistHome = mp.contains(teams, llave1)
        ExistAway = mp.contains(teams, llave2)
        if ExistHome == True:
            entry = mp.get(teams, llave1)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResultReq8(llave1)
            mp.put(teams, llave1, team_i)
            lt.addLast(team_i['datos'], datos)
        if ExistAway == True:
            entry = mp.get(teams, llave2)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResultReq8(away)
            mp.put(teams, llave2, team_i)
            lt.addLast(team_i['datos'], datos)
    except Exception:
        return None
    
def add_MapResult(football_data, datos, home, away, type):
    if type == "Result":
        teams = football_data['map_TeamResults']
    elif type == "GoalScorer":
        teams = football_data['map_TeamGoalScorers']
    elif type == "Shootout":
        teams = football_data['map_TeamShootouts']
    try:    
        ExistHome = mp.contains(teams, home)
        ExistAway = mp.contains(teams, away)
        if ExistHome == True:
            entry = mp.get(teams, home)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResult(home)
            mp.put(teams, home, team_i)
            lt.addLast(team_i['datos'], datos)
        if ExistAway == True:
            entry = mp.get(teams, away)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResult(away)
            mp.put(teams, away, team_i)
            lt.addLast(team_i['datos'], datos)
    except Exception:
        return None

def add_MapTournament(football_data, datos, torneo):
    tournaments = football_data['map_tournament']
    try:    
        ExistTourment = mp.contains(tournaments, torneo)
        if ExistTourment == True:
            entry = mp.get(tournaments, torneo)
            torneo_i = me.getValue(entry)
        else:
            torneo_i = newResultTournament(torneo)
            mp.put(tournaments, torneo, torneo_i)
        lt.addLast(torneo_i['datos'], datos)
    except Exception:
        return None

def add_MapYears(football_data, datos, year):
    dates = football_data['map_ResultsDates']
    ExistDate = mp.contains(dates, year)
    if ExistDate == True:
        entry = mp.get(dates, year)
        torneo_i = me.getValue(entry)
    else:
        torneo_i = newDateEntry(year)
        mp.put(dates, year , torneo_i)
    lt.addLast(torneo_i['datos'], datos )

def add_MapDatesScores(football_data, datos, date):
    dates = football_data['map_ScoresDates']
    ExistDate = mp.contains(dates, date)
    if ExistDate == True:
        entry = mp.get(dates, date)
        torneo_i = me.getValue(entry)
    else:
        torneo_i = newDateEntry(date)
        mp.put(dates, date, torneo_i)
    lt.addLast(torneo_i['datos'], datos )   
    
def add_idGoalscorers(football_data,GoalScorer):
    ids=football_data["id_goalscorers"]
    id = GoalScorer["date"]+"_"+GoalScorer["home_team"]+"_"+GoalScorer["away_team"]
    try:    
        ExistTourment = mp.contains(ids, id)
        if ExistTourment == True:
            entry = mp.get(ids, id)
            id_i = me.getValue(entry)
        else:
            id_i = new_Id(id)
            mp.put(ids, id, id_i)
        lt.addLast(id_i['datos'], GoalScorer)
    except Exception:
        return None
    
def add_idResults(football_data,Results):
    ids=football_data["id_results"]
    id = Results["date"]+"_"+Results["home_team"]+"_"+Results["away_team"]
    try:    
        ExistResult = mp.contains(ids, id)
        if ExistResult == True:
            entry = mp.get(ids, id)
            id_i = me.getValue(entry)
        else:
            id_i = new_Id(id)
            mp.put(ids, id, id_i)
        lt.addLast(id_i['datos'], Results)
    except Exception:
        return None 
    
    
def add_map_Req8_GoalScorers(football_data, datos, home, away, año):
    teams = football_data['map_Req8_GoalScorers']
    llave1 = (home, año)
    llave2 = (away, año)
    try:    
        ExistHome = mp.contains(teams, llave1)
        ExistAway = mp.contains(teams, llave2)
        if ExistHome == True:
            entry = mp.get(teams, llave1)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResultReq8(llave1)
            mp.put(teams, llave1, team_i)
            lt.addLast(team_i['datos'], datos)
        if ExistAway == True:
            entry = mp.get(teams, llave2)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResultReq8(away)
            mp.put(teams, llave2, team_i)
            lt.addLast(team_i['datos'], datos)
    except Exception:
        return None
    
def add_map_Req8_GoalScorers(football_data, datos, home, away, año):
    teams = football_data['map_Req8_GoalScorers']
    llave1 = (home, año)
    llave2 = (away, año)
    try:    
        ExistHome = mp.contains(teams, llave1)
        ExistAway = mp.contains(teams, llave2)
        if ExistHome == True:
            entry = mp.get(teams, llave1)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResultReq8(llave1)
            mp.put(teams, llave1, team_i)
            lt.addLast(team_i['datos'], datos)
        if ExistAway == True:
            entry = mp.get(teams, llave2)
            team_i = me.getValue(entry)
            lt.addLast(team_i['datos'], datos)
        else:
            team_i = newResultReq8(away)
            mp.put(teams, llave2, team_i)
            lt.addLast(team_i['datos'], datos)
    except Exception:
        return None
    
def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(football_data):
    """
    Retorna el tamaño de la lista de datos
    """
    return lt.size(football_data)

def get_firts_and_last_3(model, type):
    primeros = lt.subList(model[type],1, 3)
    ultimos = lt.subList(model[type],lt.size(model[type])-2,3)
    datos = (ultimos,primeros)
    results = [None, None, None, None, None, None]
    for i in range(1,4):
                results[3-i] = get_datos(datos[0],i)
                results[6-i] = get_datos(datos[1],i)
    return results  

def get_datos(datos, pos):
    valores_lista = [valor for valor in lt.getElement(datos,pos).values()]
    return valores_lista

def req_1(data_structs,num,equipo,condicion):
    """
    Función que soluciona el requerimiento 1
    """
    
    mapa = data_structs["map_TeamResults"]
    total_equipos = mp.size(mapa)
    entry = mp.get(mapa, equipo)
    lista_equipo = me.getValue(entry)["datos"]
    neutral = lt.newList('ARRAY_LIST')
    home = lt.newList('ARRAY_LIST')
    away = lt.newList('ARRAY_LIST')
    
    for match in lt.iterator(lista_equipo):
        if match['neutral'] == 'True':
            lt.addLast(neutral, match)
        if match['neutral'] == 'False' and match['home_team'] == equipo:
            lt.addLast(home, match)
        if match['neutral'] == 'False' and match['away_team'] == equipo:
            lt.addLast(away, match)
            
    if condicion.lower() == 'local' or condicion.lower() == 'home':
        x = sa.sort(home, sort_criteria_req1)
        if lt.size(x) > num:
            SubListN = lt.subList(x, 1,num)
        else: 
             SubListN = x
    if condicion.lower() == 'indiferente' or condicion.lower() == 'neutral':
        x = sa.sort(neutral, sort_criteria_req1)
        if lt.size(x) > num:
            SubListN = lt.subList(x, 1,num)
        else:
            SubListN = x

    if condicion.lower() == 'visitante' or condicion.lower() == 'away':
        x = sa.sort(away, sort_criteria_req1)
        if lt.size(x) > num:
            SubListN = lt.subList(x, 1,num)
        else:
            SubListN = x
    
    total_partidos = lt.size(lista_equipo)
    total_condicion = lt.size(SubListN)
    
    if lt.size(SubListN) <= 6:
        return SubListN, total_equipos, total_partidos, total_condicion
    else:
        return FirstandALst(SubListN), total_equipos, total_partidos, total_condicion
        
def sort_criteria_req1(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] == data_2["date"]:
        if data_1['home_score'] > data_2['home_score']:
            return True
        else:
            return False


def req_2(data_structs,num,jugador):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    datos = data_structs["scorer"]
    total_anotaciones = mp.size(datos)
    lista_jugador = me.getValue(mp.get(datos,jugador))["datos"]
    lista_jugador_ordenada = ordenar_req_2(lista_jugador)
    goles_goleador = lt.size(lista_jugador_ordenada[0])
    penales = lista_jugador_ordenada[1]
    goles_interes = lt.newList("ARRAY_LIST")
    para_printear = lt.newList("ARRAY_LIST")
    if num <= goles_goleador:
        for i in range(0,num):
            dato = lt.getElement(lista_jugador_ordenada[0],i)
            lt.addLast(goles_interes,dato)
    else:
        for i in range(0,goles_goleador):
            dato = lt.getElement(lista_jugador_ordenada[0],i)
            lt.addLast(goles_interes,dato)
            
    if lt.size(goles_interes)>=6:
        num_tabla = "Goal scorers results hass more than 6 records..."
        for i in range(1, 4):
            lt.addLast(para_printear,lt.getElement(goles_interes,i))
        for i in range(lt.size(goles_interes)-2, lt.size(goles_interes)+1):
            lt.addLast(para_printear,lt.getElement(goles_interes,i))
    else:
        num_tabla = "Goal scorers results hass less than 6 records..."
        for i in range(1, lt.size(goles_interes)+1):
            lt.addLast(para_printear,lt.getElement(goles_interes,i))
    return total_anotaciones , goles_goleador , penales , para_printear, num_tabla

def ordenar_req_2(ingreso):
    penals = 0
    quk.sort(ingreso,criterio_1_2)
    datos = lt.newList("ARRAY_LIST")
    for i in lt.iterator(ingreso):
        lt.addLast(datos,i)
        if i["penalty"] == "True" or i["penalty"] == True:
            penals+=1
    return datos , penals

def criterio_1_2(data_1,data_2):
    if data_1["date"] > data_2["date"]:
        return True
    else:
        return False



def req_3(control, Equipo, Inicio, Final):
    """
    Función que soluciona el requerimiento 3
    """
    local = 0
    visitante = 0
    respuesta = lt.newList("ARRAY_LIST")
    mapa = control['map_TeamResults']
    entry = mp.get(mapa, Equipo)
    SubLista1 = me.getValue(entry)
    SubLista1 = SubLista1["datos"]
    listaOrd1 = merg.sort(SubLista1, sort_criteria_eng)
    entry = mp.get(control["map_TeamGoalScorers"], Equipo)
    SubLista2 = me.getValue(entry)['datos']
    listaOrd2 = merg.sort(SubLista2, sort_criteria_eng)
    for game in lt.iterator(listaOrd1):
        fecha = game["date"]
        if fecha >= Inicio and fecha <= Final:
            Pos  = busqueda_binaria_req3(listaOrd2, fecha)
            diccionario_i = game
            if game["home_team"] == Equipo: 
                local += 1
            elif game["away_team"] == Equipo:
                visitante += 1
            if Pos > 0:
                diccionario_gsc = lt.getElement(listaOrd2, Pos)
                diccionario_i["AutoGol"] =  diccionario_gsc["penalty"]
                diccionario_i["Penalty"] =  diccionario_gsc["own_goal"]
                lt.addLast(respuesta, diccionario_i)
            elif Pos == -1:
                diccionario_i["AutoGol"] = "Desconocido"
                diccionario_i["Penalty"] =  "Desconocido"
                lt.addLast(respuesta, diccionario_i)
    return respuesta, local, visitante


def req_4(control,torneo,inicio,final):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    torneos = control["map_tournament"]
    llave_valor_torneo = mp.get(torneos,torneo)
    valor_torneo = me.getValue(llave_valor_torneo)
    lista_considerar = ordenar_req_4(valor_torneo,inicio,final)
    pre_printeo = lt.newList("ARRAY_LIST")
    para_printear = lt.newList("ARRAY_LIST")

    total_torneos = mp.size(torneos)
    total_partidos_torneo = lt.size(lista_considerar)
    countries = lt.newList("ARRAY_LIST")
    cities = lt.newList("ARRAY_LIST")
    shoot = lt.newList("ARRAY_LIST")
    for i in range(1, lt.size(lista_considerar)+1):
        dato_primitivo = lt.getElement(lista_considerar,i)
        dato = {
                "date":dato_primitivo["date"],
                "tournament":dato_primitivo["tournament"],
                "country":dato_primitivo["country"],
                "city":dato_primitivo["city"],
                "home_team":dato_primitivo["home_team"],
                "away_team":dato_primitivo["away_team"],
                "home_score":dato_primitivo["home_score"],
                "away_score":dato_primitivo["away_score"],
                "winner":None,
            }
        if not lt.isPresent(cities,dato_primitivo["city"]):
            lt.addLast(cities,dato_primitivo["city"])
            
        if not lt.isPresent(countries,dato_primitivo["country"]):
            lt.addLast(countries,dato_primitivo["country"])
        
        aparecio = buscar_shoot(control,dato_primitivo["date"],dato_primitivo["home_team"])
        if aparecio[0] == -1:
            dato["winner"] = "Unavailable"
        else:
            dato["winner"] = aparecio[1]
            if not lt.isPresent(shoot, dato["winner"]+dato["date"]) and aparecio[0] !=-1:
                lt.addLast(shoot,dato["winner"]+dato["date"])
        lt.addLast(pre_printeo,dato)
    if lt.size(pre_printeo)>=6:
        num_tabla = "The tournament results hass more than 6 records..."
        for i in range(1, 4):
            lt.addLast(para_printear,lt.getElement(pre_printeo,i))
        for i in range(lt.size(lista_considerar)-2, lt.size(lista_considerar)+1):
            lt.addLast(para_printear,lt.getElement(pre_printeo,i))
    else:
        num_tabla = "The tournament results hass less than 6 records..."
        for i in range(1, lt.size(pre_printeo)+1):
            lt.addLast(para_printear,lt.getElement(pre_printeo,i))
    return  para_printear , total_torneos , total_partidos_torneo , lt.size(countries) , lt.size(cities) , lt.size(shoot),num_tabla




def buscar_shoot(control,fecha,local):
    izq = 0
    der = lt.size(control["shootouts"])
    while izq <= der:
        punto_medio = (izq+der)//2   
        cosiderado = lt.getElement(control["shootouts"], punto_medio)
        date = cosiderado["date"]  
        if date == fecha: 
            if local == cosiderado["home_team"]:
                return punto_medio , lt.getElement(control["shootouts"], punto_medio)["winner"]
            else:
                return search_req4(control,fecha,local,punto_medio)
        if date  > fecha:
            der = punto_medio - 1
        if date  < fecha:
            izq = punto_medio + 1
    return -1 , lt.getElement(control["shootouts"], punto_medio)["winner"]


def search_req4(control,fecha,local,pos):
    i = pos
    while lt.getElement(control["shootouts"], i-1)["date"]==fecha:
        i-=1 
    while lt.getElement(control["shootouts"], i)["date"]==fecha:
            if lt.getElement(control["shootouts"], i)["home_team"]==local:
                return i , lt.getElement(control["shootouts"], i)["winner"]
            else:
                i+=1
    return -1 , lt.getElement(control["shootouts"], i)["winner"]

def ordenar_req_4(ingreso,inicio,final):
    lista = ingreso
    ordenado_entre_fecha = lt.newList("ARRAY_LIST")
    for partido in lt.iterator(lista['datos']):
        if partido["date"]>=inicio and partido["date"]<=final:
            lt.addLast(ordenado_entre_fecha,partido)
    quk.sort(ordenado_entre_fecha,criterio_4)

    return ordenado_entre_fecha

def criterio_4(data_1,data_2):
    if data_1["date"] > data_2["date"]:
        return True
    else:
        return False


def req_5(control, player, Inicio, Final):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    
    mapa_results = control['map_TeamResults']
    mapa_scorers = control['scorer']
    
    entry = mp.get(mapa_scorers, player)
    player_list = me.getValue(entry)['datos']
    
    total_scores = lt.size(player_list)
    total_players = mp.size(mapa_scorers)
    
    solution = lt.newList('ARRAY_LIST')
    tournaments = lt.newList('ARRAY_LIST')
    shootouts = 0
    own_goals = 0
    
    formato = "%Y-%m-%d"
    for score in lt.iterator(player_list):
        if datetime.strptime(score["date"], formato) > datetime.strptime(Inicio, formato) and datetime.strptime(score["date"], formato) < datetime.strptime(Final, formato):
            team = score['team']
            date = score['date']
            entry = mp.get(mapa_results, team)
            team_list = me.getValue(entry)['datos']
            sort_team_list = sa.sort(team_list, sort_criteria_eng)
            dict_match = busqueda_binaria_req5(sort_team_list, date ) 
            score_format = {}
            score_format['date'] = date
            score_format['minute'] = score['minute']
            score_format['home_team'] = score['home_team']
            score_format['away_team'] = score['away_team']
            score_format['team'] = score['team']
            score_format['home_score'] = dict_match['home_score']
            score_format['away_score'] = dict_match['away_score']
            score_format['tournament'] = dict_match['tournament']
            score_format['penalty'] = score['penalty'] 
            score_format['own_goal'] = score['own_goal']
            
            lt.addLast(solution, score_format)
            if not(lt.isPresent(tournaments, score_format['tournament'])):
                lt.addLast(tournaments,score_format['tournament'] )
            
            if score['penalty'] == 'True':
                shootouts += 1
            if score['own_goal'] == 'True':
                own_goals += 1

    total_tournaments = lt.size(tournaments)
    sorted_solution = sa.sort(solution, sort_criteria_req5)
    if lt.size(solution) <= 6:     
        return sorted_solution, total_players, total_scores, total_tournaments, shootouts, own_goals
    else:
        final_solution = FirstandALst(sorted_solution)
        return final_solution, total_players, total_scores, total_tournaments, shootouts, own_goals

                


def sort_criteria_req5(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] == data_2["date"]:
        if data_1['minute'] > data_2['minute']:
            return True
        else:
            return False
    
    return False

def req_6(control, torneo, año, n):
    """
    Función que soluciona el requerimiento 6
    """
    map_torneos = control['map_tournament']
    map_dates = control['map_ScoresDates']
    map_years = control['map_ResultsDates']  
    map_teams_goals= mp.newMap(100,
                             maptype="CHAINING",
                             loadfactor=4)
    
    entry = mp.get(map_torneos, torneo)
    matches_list = me.getValue(entry)['datos']
    inicio = str(año) + '-01-01'
    final = str(año) + '-12-31' 
    formato = "%Y-%m-%d"
    teams = lt.newList('ARRAY_LIST')
    ranking = lt.newList('ARRAY_LIST')
    torneos = lt.newList('ARRAY_LIST')
    countries = lt.newList('ARRAY_LIST')
    citiesUnique = lt.newList('ARRAY_LIST')
    citiesMatches = lt.newList('ARRAY_LIST')
    totalmatches = 0
    
    entryyear = mp.get(map_years, año)
    yearlst = me.getValue(entryyear)['datos']
    # Iteracion para encontrar el total de torneos
    for partido in lt.iterator(yearlst):
        if not (lt.isPresent( torneos, partido['tournament'])):
            lt.addLast(torneos, partido['tournament'])  
            
    #iteracion sobre los partidos de un torneo
    for match in lt.iterator(matches_list):
        home_added = False
        if datetime.strptime(match["date"], formato) > datetime.strptime(inicio, formato) and datetime.strptime(match["date"], formato) < datetime.strptime(final, formato):
            totalmatches += 1
            lt.addLast(citiesMatches, match['city'])
            #Cuantas ciudades
            if not (lt.isPresent(citiesUnique, match['city'])):
                lt.addLast(citiesUnique, match['city'])
            #Cuantos paises
            if not(lt.isPresent(countries, match['country'])):
                lt.addLast(countries, match['country'])
    
            entry1 = mp.get(map_dates, match['date'])
            if entry1 is not None:           
                date_list = me.getValue(entry1)
                date_list1 = date_list['datos']
                #Encontrar los datos de los goels del partido
                golinmatch = encontrar_diccionario(date_list1, match['home_team'], match['away_team'] )
                penalty_goals_home, penalty_goals_away  = penalty_points(golinmatch)
                own_goals_home, own_goals_away = own_points(golinmatch)
                #agrego goles a mapa auxiliar de goles de un equipo en el torneo
                addgoalsHome(golinmatch, map_teams_goals)
            
            #Suma informacion al ranking
            if lt.isPresent(teams, match['home_team']) and lt.isPresent(teams, match['away_team']):
                home_team_dict = encontrar_diccionario_home(ranking, match['home_team'])
                away_team_dict = encontrar_diccionario_home(ranking, match['away_team'])
                #agrega los puntos y vicorias derrotas y empates
                if int(match['home_score']) > int(match['away_score']):
                    home_team_dict['total_points'] += 3
                    home_team_dict['wins'] += 1
                    away_team_dict['losses'] += 1        
                elif int(match['home_score']) == int(match['away_score']):
                    home_team_dict['total_points'] += 1
                    away_team_dict['total_points'] += 1
                    home_team_dict['draws'] += 1
                    away_team_dict['draws'] += 1
                else:
                    away_team_dict['total_points'] += 3
                    away_team_dict['wins'] +=1
                    home_team_dict['losses'] += 1
                
                #agrega la diferencia de gol
                home_team_dict['goal_difference'] += int(match['home_score']) - int(match['away_score'])
                away_team_dict['goal_difference'] += int(match['away_score']) - int(match['home_score'])
                
                #agrega los penalty points
                if entry1 is not None:
                    home_team_dict['penalty_points'] += penalty_goals_home
                    away_team_dict['penalty_points'] += penalty_goals_away
                
                #agraga llave matches
                home_team_dict['matches'] += 1
                away_team_dict['matches'] += 1
                
                # agrega los own goal points
                if entry1 is not None:
                    home_team_dict['own_goal_points'] += own_goals_home
                    away_team_dict['own_goal_points'] += own_goals_away
                
                #total de goles
                home_team_dict['goals_for'] += int(match['home_score'])
                away_team_dict['goals_for'] += int(match['away_score'])
                
                # total goles en contra
                home_team_dict['goals_against'] += int(match['away_score'])
                away_team_dict['goals_against'] += int(match['home_score'])
                
                 
            #Creación de paises en el ranking en caso de no existir   
            if not lt.isPresent(teams, match['home_team']):
                lt.addLast(teams, match['home_team'])
                away_team_dict = encontrar_diccionario_home(ranking, match['away_team'])
                team_format ={}
                #Agrega el nombre del equpo
                team_format['team'] = match['home_team']
                
                #agrega los puntos y vicorias derrotas y empates
                if int(match['home_score']) > int(match['away_score']):
                    team_format['total_points'] = 3
                    team_format['wins'] = 1
                    team_format['draws'] = 0
                    team_format['losses'] = 0
                    if lt.isPresent(teams, match['away_team']):
                        away_team_dict['losses'] += 1                  
                elif int(match['home_score']) == int(match['away_score']):
                    team_format['total_points'] = 1
                    team_format['wins'] = 0
                    team_format['draws'] = 1
                    team_format['losses'] = 0
                    if lt.isPresent(teams, match['away_team']):
                        away_team_dict['draws'] += 1 
                        away_team_dict['total_points'] += 1
                else:
                    team_format['total_points'] = 0
                    team_format['wins'] = 0
                    team_format['draws'] = 0
                    team_format['losses'] = 1
                    if lt.isPresent(teams, match['away_team']):
                        away_team_dict['wins'] += 1
                        away_team_dict['total_points'] += 3
                        
                #agrega la diferencia de gol
                team_format['goal_difference'] = int(match['home_score']) - int(match['away_score'])
                if lt.isPresent(teams, match['away_team']):
                    away_team_dict['goal_difference'] += int(match['away_score']) - int(match['home_score'])

                #agrega los penalty points
                if entry1 is None:
                    team_format['penalty_points'] = 0
                else:   
                    team_format['penalty_points'] = penalty_goals_home
                    if lt.isPresent(teams, match['away_team']):
                        away_team_dict['penalty_points'] += penalty_goals_away
                        
                #agraga llave matches
                team_format['matches'] = 1
                if lt.isPresent(teams, match['away_team']):
                    away_team_dict['matches'] += 1
                    
                # agrega los own goal points
                if entry1 is None:
                    team_format['own_goal_points'] = 0
                else:
                    team_format['own_goal_points'] = own_goals_home
                    if lt.isPresent(teams, match['away_team']):
                        away_team_dict['own_goal_points'] += own_goals_away
                        
                #total de goles
                team_format['goals_for'] = int(match['home_score'])
                if lt.isPresent(teams, match['away_team']):
                    away_team_dict['goals_for'] += int(match['away_score'])
                    
                # total goles en contra
                team_format['goals_against'] = int(match['away_score'])
                if lt.isPresent(teams, match['away_team']):
                    away_team_dict['goals_against'] += int(match['home_score'])
                                    
                lt.addLast(ranking, team_format)
                home_added = True
                
                
            if not lt.isPresent(teams, match['away_team']):
                lt.addLast(teams, match['away_team'])
                home_team_dict = encontrar_diccionario_home(ranking, match['home_team'])
                team_format ={}
                #Agrega el nombre del equpo
                team_format['team'] = match['away_team']
                
                #agrega los puntos y vicorias derrotas y empates
                if int(match['home_score']) > int(match['away_score']):
                    team_format['total_points'] = 0
                    team_format['wins'] = 0
                    team_format['draws'] = 0
                    team_format['losses'] = 1
                           
                    if lt.isPresent(teams, match['home_team']) and home_added == False:
                        home_team_dict['wins'] += 1 
                        home_team_dict['total_points'] += 3 
                        
                elif int(match['home_score']) == int(match['away_score']):
                    team_format['total_points'] = 1
                    team_format['wins'] = 0
                    team_format['draws'] = 1
                    team_format['losses'] = 0  
                    if lt.isPresent(teams, match['home_team']) and home_added == False:
                        home_team_dict['draws'] += 1
                        home_team_dict['total_points'] += 1  
                else:
                    team_format['total_points'] = 3
                    team_format['wins'] = 1
                    team_format['draws'] = 0
                    team_format['losses'] = 0
                    if lt.isPresent(teams, match['home_team']) and home_added == False:
                        home_team_dict['losses'] += 1
                        
                #agrega la diferencia de gol
                team_format['goal_difference'] = int(match['away_score']) - int(match['home_score'])
                if lt.isPresent(teams, match['home_team']) and home_added == False:
                    home_team_dict['goal_difference'] += int(match['home_score']) - int(match['away_score'])
                    
                #agrega los penalty points
                if entry1 is None:
                    team_format['penalty_points'] = 0
                else:   
                    team_format['penalty_points'] = penalty_goals_away
                    if lt.isPresent(teams, match['home_team']) and home_added == False:
                        home_team_dict['penalty_points'] += penalty_goals_home
                        
                #agraga llave matches
                team_format['matches'] = 1
                if lt.isPresent(teams, match['home_team']) and home_added == False:
                    home_team_dict['matches'] += 1
                    
                # agrega los own goal points
                if entry1 is None:
                    team_format['own_goal_points'] = 0
                else:
                    team_format['own_goal_points'] = own_goals_away
                    if lt.isPresent(teams, match['home_team'])  and home_added == False :
                        home_team_dict['own_goal_points'] += own_goals_home
                        
                        
                #total de goles
                team_format['goals_for'] = int(match['away_score'])
                if lt.isPresent(teams, match['home_team']) and home_added == False:
                        home_team_dict['goals_for'] += int(match['home_score'])
                # total goles en contra
                team_format['goals_against'] = int(match['home_score'])
                
                if lt.isPresent(teams, match['home_team']) and home_added == False :
                        home_team_dict['goals_against'] += int(match['away_score'])
                        
                lt.addLast(ranking, team_format)
                
    rankingF = addScorer_Req6(ranking, map_teams_goals)
    orderRanking = sa.sort(rankingF, sort_crit_ranking_7)
    añosTotales = mp.size(map_years)
    torneosTotales = lt.size(torneos)
    totalequipos = lt.size(ranking)
    totalcountries = lt.size(countries)
    citiesUniqueN = lt.size(citiesUnique)
    mostPopCity = str_mas_repetido(citiesMatches)
    
    if lt.size(orderRanking) > n:
        TopnList = lt.subList(orderRanking, 1, n)
    else:
        TopnList = orderRanking
    
    if lt.size(TopnList) <= 6:
        return TopnList, añosTotales, torneosTotales, totalequipos, totalmatches, totalcountries, citiesUniqueN, mostPopCity
    else:
        newTop = FirstandALst(TopnList)
        return newTop, añosTotales, torneosTotales, totalequipos, totalmatches, totalcountries, citiesUniqueN, mostPopCity




def str_mas_repetido(lista):
    conteo = {}
    mas_repetido = None
    max_apariciones = 0
    
    for elemento in lt.iterator(lista):
        if elemento in conteo:
            conteo[elemento] += 1
        else:
            conteo[elemento] = 1
        
        if conteo[elemento] > max_apariciones:
            max_apariciones = conteo[elemento]
            mas_repetido = elemento
    
    return mas_repetido

def FirstandALst(top):
    n = lt.size(top)
    topF = lt.newList('ARRAY_LIST')
    lt.addLast(topF, lt.getElement(top, 1))
    lt.addLast(topF, lt.getElement(top, 2))
    lt.addLast(topF, lt.getElement(top, 3))
    lt.addLast(topF, lt.getElement(top, n-2))
    lt.addLast(topF, lt.getElement(top, n-1))
    lt.addLast(topF, lt.getElement(top, n))
    
    return topF
    
def sort_crit_ranking_7(dato1, dato2):
    
    
    if dato1['total_points'] > dato2['total_points']:
        return True
    elif dato1['total_points'] == dato2['total_points']:
        if dato1['goal_difference'] > dato2['goal_difference']:
            return True
        elif dato1['goal_difference'] == dato2['goal_difference']: 
            if dato1['penalty_points'] >  dato2['penalty_points']:
                return True
            elif dato1['penalty_points'] ==  dato2['penalty_points']:
                if dato1['matches'] < dato2['matches']:
                    return True
                elif dato1['matches'] == dato2['matches']:
                    if dato1['goals_against'] < dato2['goals_against']:
                        return True
                    else:
                        return False
    return False

def addScorer_Req6(ranking, mapa):
    name = 'unavailable'
    for teamDict in lt.iterator(ranking):
        if mp.contains(mapa, teamDict['team']):
            teamDict['top_scorer'] = TeamScorer(teamDict['team'], mapa)
        else:
            scorer = createScorerReq6(name)
            scorer['goals'] = 0
            teamDict['top_scorer'] = scorer
    
    return ranking 
            
def createScorerReq6(name):
    scorer = {}
    scorer['scorer'] = name
    scorer['goals'] = lt.newList('ARRAY_LIST')
    scorer['matches'] = 0
    scorer['avg_time'] = 0.0 
    return scorer

def TeamScorer(pais, mapa):
    players = lt.newList('ARRAY_LIST')
    entry = mp.get(mapa, pais)
    
    scoresList = me.getValue(entry)['datos']
    scorers = lt.newList('ARRAY_LIST')
    
    for gol in lt.iterator(scoresList):
        if not(lt.isPresent( players, gol['scorer'])):
            scorer = createScorerReq6(gol['scorer'])
            if gol['minute'] != None and gol['minute'] != '': 
                scorer['avg_time'] += float(gol['minute'])
            lt.addLast(players, gol['scorer'])   
            lt.addLast(scorer['goals'], gol)
            lt.addLast(scorers, scorer)
        else:
           dictscorer =  encontrar_diccionario_scorer(scorers, gol['scorer'])
           lt.addLast(dictscorer['goals'], gol)
           if gol['minute'] != None and gol['minute'] != '': 
                dictscorer['avg_time'] += float(gol['minute'])
           
    playermax = None
    for player in lt.iterator(scorers):
        if playermax == None or lt.size(player['goals']) > lt.size(playermax['goals']):
            playermax = player
    
    goalsplayermax = playermax['goals']
    matchplayermax = 0
    dates = lt.newList('ARRAY_LIST')
    for goal in lt.iterator(goalsplayermax):
        if not (lt.isPresent(dates, goal['date'])):
            lt.addLast(dates, goal['date'])
            matchplayermax += 1
    
    playermax['goals'] = lt.size(goalsplayermax)
    playermax['matches'] = matchplayermax
    playermax['avg_time'] = playermax['avg_time'] / float(playermax['goals'])
    
    return playermax 
                
def encontrar_diccionario_home(lista, valor_esperado):
    for diccionario in lt.iterator(lista):
        dictTeam = diccionario.get("team") 
        if dictTeam == valor_esperado:
            return diccionario

def encontrar_diccionario_scorer(lista, valor_esperado):
    for diccionario in lt.iterator(lista):
        dictTeam = diccionario.get("scorer") 
        if dictTeam == valor_esperado:
            return diccionario

def encontrar_diccionario_away(lista, valor_esperado):
    for diccionario in lt.iterator(lista):
        dictTeam = diccionario.get("team")
        if  dictTeam == valor_esperado:
            return diccionario
    
def entrymapReq6(team):
    entry = {}
    entry['team'] = team
    entry['datos'] = lt.newList('ARRAY_LIST')
    return entry

def add_teamReq6(mapa, datos, team):

    existTeam = mp.contains(mapa, team)
    if existTeam:
        entry = mp.get(mapa, team)
        teamentry = me.getValue(entry)
    else:
        teamentry = entrymapReq6(team)
        mp.put(mapa, team, teamentry)
    lt.addLast(teamentry['datos'], datos)
    
    return mapa

def addgoalsHome(goles, mapa):
    for gol in  lt.iterator(goles):
        add_teamReq6(mapa, gol, gol['team'])
                  

def penalty_points(goles):
    penalty_goals = 0 
    penalty_goals_home = 0
    penalty_goals_away = 0
     
    for gol in lt.iterator(goles):
        if gol['penalty'] == 'True':
            penalty_goals += 1
        if gol['penalty'] == 'True' and gol['team'] == gol['home_team']:
            penalty_goals_home += 1
        if gol['penalty'] == 'True' and gol['team'] == gol['away_team']:
            penalty_goals_away += 1       
            
    return penalty_goals_home, penalty_goals_away

def own_points(goles):
    own_goals = 0 
    own_goals_home = 0
    own_goals_away = 0
     
    for gol in lt.iterator(goles):
        if gol['own_goal'] == 'True':
            own_goals += 1
        if gol['own_goal'] == 'True' and gol['team'] == gol['home_team']:
            own_goals_home += 1
        if gol['own_goal'] == 'True' and gol['team'] == gol['away_team']:
            own_goals_away += 1       
            
    return own_goals_home, own_goals_away

def encontrar_diccionario(lista, home_team, away_team):
    goals = lt.newList('ARRAY_LIST')
    for diccionario in lt.iterator(lista):
        if diccionario['home_team'] == home_team and diccionario['away_team'] == away_team:
            lt.addLast(goals, diccionario)
    return goals
    


                
                
def req_7(data_structs,torneo,puntos):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    goles = 0
    penales = lt.newList("ARRAY_LIST")
    autogoles = lt.newList("ARRAY_LIST")
    partidos_torneos = data_structs["map_tournament"]
    torneo = me.getValue(mp.get(partidos_torneos,torneo))["datos"]
    total_torneos = mp.size(partidos_torneos)
    total_partidos_torneo = lt.size(torneo)
    puntajes_jugadores = mp.newMap(152,
                             maptype="CHAINING",
                             loadfactor=4)
    for dato in lt.iterator(torneo):
        goles+=int(dato["home_score"])
        goles+=int(dato["away_score"])
        añadir_jugador(dato,data_structs,puntajes_jugadores,goles,penales,autogoles)
        
    jugadores = mp.valueSet(puntajes_jugadores)
    total_jugadores = mp.size(puntajes_jugadores)
    jugadores_match = lt.newList("ARRAY_LIST")
    for dato in lt.iterator(jugadores):
        if dato["total_points"]==puntos:
            dato["avg_time [min]"] = dato["avg_time [min]"]//dato["total_goals"]
            lt.addLast(jugadores_match,dato)
    quk.sort(jugadores_match,criterio_req_7)
    jugadores_match_1_6 = lt.newList("ARRAY_LIST")
    
    if lt.size(jugadores_match)>=6:
        num_tabla = "The tournament results hass more than 6 records..."
        for i in range(1, 4):
            lt.getElement(jugadores_match,i)["last_goal"] = ultimogol(lt.getElement(jugadores_match,i)["scorer"],data_structs)
            lt.addLast(jugadores_match_1_6,lt.getElement(jugadores_match,i))
        for i in range(lt.size(jugadores_match)-2, lt.size(jugadores_match)+1):
            lt.getElement(jugadores_match,i)["last_goal"] = ultimogol(lt.getElement(jugadores_match,i)["scorer"],data_structs)
            lt.addLast(jugadores_match_1_6,lt.getElement(jugadores_match,i))
    else:
        num_tabla = "The tournament results hass less than 6 records..."
        for i in range(1, lt.size(jugadores_match)+1):
            lt.getElement(jugadores_match,i)["last_goal"] = ultimogol(lt.getElement(jugadores_match,i)["scorer"],data_structs)
            lt.addLast(jugadores_match_1_6,lt.getElement(jugadores_match,i))
    return jugadores_match_1_6 , total_torneos , total_jugadores , total_partidos_torneo , goles , lt.size(penales) , lt.size(autogoles), lt.size(jugadores_match) , num_tabla

def ultimogol(jugador,mapa):
    resultadosgoal = me.getValue(mp.get(mapa["scorer"],jugador))["datos"]
    quk.sort(resultadosgoal,criterio_ultimo_gol)
    datos = lt.getElement(resultadosgoal,1)
    id = datos["date"]+"_"+datos["home_team"]+"_"+datos["away_team"]
    resultadosresults = lt.getElement(me.getValue(mp.get(mapa["id_results"],id))["datos"],1)
    dato = lt.newList("ARRAY_LIST")
    data = {
        "date":str(datos["date"]),
        "tournament": resultadosresults["tournament"],
        "home_team":datos["home_team"],
        "away_team":datos["away_team"],
        "home_score": resultadosresults["home_score"],
        "away_score": resultadosresults["away_score"] ,
        "minute":datos["minute"],
        "penalty":datos["penalty"],
        "own_goal":datos["own_goal"],
    }
    lt.addLast(dato,data)
    return tabulate(dato["elements"] , headers= 'keys', tablefmt = 'grid')

def criterio_ultimo_gol(dato1,dato2):
    if dato1["date"] > dato2["date"]:
        return True
    else:
        return False

def criterio_req_7(dato1,dato2):
    if dato1["total_points"]!=dato2["total_points"]:
        return dato1["total_points"]>dato2["total_points"]
    elif dato1["total_goals"]!=dato2["total_goals"]:
        return dato1["total_goals"]>dato2["total_goals"]
    elif dato1["penalty_goals"]!=dato2["penalty_goals"]:
        return dato1["penalty_goals"]>dato2["penalty_goals"]
    elif dato1["own_goals"]!=dato2["own_goals"]:
        return dato1["own_goals"]<dato2["own_goals"]
    else:
        return dato1["avg_time [min]"]<dato2["avg_time [min]"]


def añadir_jugador(dato,data_structs,puntajes_jugadores,goles,penales,autogoles):
    ids = data_structs["id_goalscorers"]
    id = dato["date"]+"_"+dato["home_team"]+"_"+dato["away_team"]
    if mp.contains(ids,id):
        partido = me.getValue(mp.get(ids,id))["datos"]
        for gol in lt.iterator(partido):
            if not mp.contains(puntajes_jugadores,gol["scorer"]):
                jugador = {"scorer":gol["scorer"],
                           "total_points":0,
                           "total_goals":0,
                           "penalty_goals":0,
                           "own_goals":0,
                           "avg_time [min]":0,
                           "scored in wins":0,
                           "scored in losses":0,
                           "scored in draws":0,
                           "last_goal":None
                           }
                mp.put(puntajes_jugadores,gol["scorer"],jugador)
            if mp.contains(puntajes_jugadores,gol["scorer"]):
                goleador = me.getValue(mp.get(puntajes_jugadores,gol["scorer"]))
                goleador["total_goals"]+=1
                goleador["total_points"]+=1
                if gol["minute"] != None and gol["minute"] != "":
                    goleador["avg_time [min]"]+=float(gol["minute"])
                if gol["team"] == dato["home_team"]:
                    if int(dato["home_score"])>int(dato["away_score"]):
                        goleador["scored in wins"]+=1
                    elif int(dato["home_score"])<int(dato["away_score"]):
                        goleador["scored in losses"]+=1
                    else:
                        goleador["scored in draws"]+=1
                        
                if gol["team"] == dato["away_team"]:
                    if int(dato["home_score"])<int(dato["away_score"]):
                        goleador["scored in wins"]+=1
                    elif int(dato["home_score"])>int(dato["away_score"]):
                        goleador["scored in losses"]+=1
                    else:
                        goleador["scored in draws"]+=1
                        
                if gol["penalty"] == "True" or gol["penalty"] == True:
                    lt.addLast(penales,id)
                    goleador["penalty_goals"]+=1
                    goleador["total_points"]+=1
                elif gol["own_goal"] == "True" or gol["own_goal"] == True:
                    lt.addLast(autogoles,id)
                    goleador["own_goals"]+=1
                    goleador["total_points"]-=1
    



def req_8(control, Equipo, Inicio, Final):
    """
    Función que soluciona el requerimiento 8
    """
    mapa = control['map_Req8']
    año_inicio = int(Inicio[0:4])
    año_final = int(Final[0:4])
    a = 0
    matches = 0
    winner = 0
    losses = 0
    draws = 0
    total_points = 0
    diferencia_goles = 0
    penalties = 0
    own_goals = 0
    goals_for = 0
    goals_against = 0
    jugadores = {}
    ListaRespuesta = lt.newList("ARRAY_LIST")
    total_home = 0
    total_away = 0
    for a in range(año_final-año_inicio+1):
        año = año_inicio + a
        a += 1
        llave = (Equipo, str(año))
        entry = mp.get(mapa, llave)
        if entry != None:
            ListaGoleador = lt.newList("ARRAY_LIST")
            last_game =  lt.newList("ARRAY_LIST")
            SubLista = me.getValue(entry)
            SubLista = SubLista['datos']
            ListaOrd = merg.sort(SubLista, sort_criteria_eng)
            size = lt.size(ListaOrd)
            i = 0
            for game in lt.iterator(ListaOrd):
                torneo = game['tournament']
                fecha = game['date']
                if torneo != "Friendly" and fecha >= Inicio and fecha <= Final:
                    matches +=1
                    winner = winner_losses_team(control, game, Equipo, fecha)[0] + winner
                    losses = winner_losses_team(control, game, Equipo, fecha)[1] + losses
                    draws = winner_losses_team(control, game, Equipo, fecha)[2] + draws
                    diferencia_goles = diferencia_goles_def(game, Equipo) + diferencia_goles
                    penalties = penalties_def(control, game, Equipo, fecha)[0] + penalties
                    own_goals = penalties_def(control, game, Equipo, fecha)[1] + own_goals
                    goals_for = goals_def(game, Equipo)[0] + goals_for
                    goals_against = goals_def(game, Equipo)[1] + goals_against
                    if game["home_team"] == Equipo:
                        total_home += 1
                    elif game["away_team"] == Equipo:
                        total_away += 1 
                i +=1
                if i == size:
                    last_game = game
            if matches > 0:
                total_points = (winner*3) + draws
                jugadores = jugadores_def(control, game, Equipo, fecha, jugadores)
                if jugadores:
                    maximo_jugador, maximo_goles = max(jugadores.items(), key=lambda x: x[1])
                else:
                    maximo_jugador, maximo_goles = ("Nadie", 0)
                avg_time = avg_time_def(control, game, año, maximo_jugador, maximo_goles, Equipo)
                lt.addLast(ListaGoleador, {'player': maximo_jugador, 'goals': maximo_goles, 'matches': matches, 'avg time': avg_time})
                lt.addLast(ListaRespuesta, {'year': año, 'matches': matches,'total points': total_points,'goal_diference': diferencia_goles,
                                                                    'penalties': penalties, 'own_goals': own_goals, 'winner':winner, 'draws': draws, 'losses': losses, 'goals_for': goals_for, 'goals_against': goals_against, 'top_scorer': ListaGoleador})
                matches = 0
                winner = 0                        
                losses = 0
                draws = 0
                diferencia_goles = 0
                total_points = 0
                penalties = 0
                own_goals = 0
                goals_for = 0
                goals_against = 0
                jugadores = {}
    return ListaRespuesta, last_game, total_home, total_away

def avg_time_def(control, game, año, maximo_jugador, maximo_goles, Equipo):
    if maximo_jugador == "Nadie":
        return -1
    else:
        mapa = control['map_Req8_GoalScorers']
        año = str(año)
        llave = (Equipo, año[0:4])
        entry = mp.get(mapa, llave)
        if entry != None:
            SubLista = me.getValue(entry)
            SubLista = SubLista['datos']
            listaOrd = quk.sort(SubLista, sort_criteria_eng)
            minutos_totales = 0
            for game in lt.iterator(listaOrd):
                Own_goal = game['own_goal']
                scorer = game['scorer']
                minuto = int(float(game['minute']))
                team = game['team']
                if  scorer == maximo_jugador and Own_goal == 'False' and team == Equipo:
                    minutos_totales = minutos_totales + minuto
            return minutos_totales/maximo_goles
        else:
            return -1
    
    
def jugadores_def(control, game, Equipo, fecha, jugadores):
    mapa = control['map_Req8_GoalScorers']
    llave = (Equipo, str(fecha[0:4]))
    entry = mp.get(mapa, llave)
    if entry != None:
        SubLista = me.getValue(entry)
        SubLista = SubLista['datos']
        listaOrd = quk.sort(SubLista, sort_criteria_eng)
        for game in lt.iterator(listaOrd):
            team = game['team']
            own_goal = game['own_goal']
            if team == Equipo and own_goal == 'False':
                nombre_jugador = game['scorer']
                if nombre_jugador in jugadores:
                    jugadores[nombre_jugador] += 1
                else:
                    jugadores[nombre_jugador] = 1
        return jugadores
                
def goals_def(game, Equipo):
    away_score = int(game["away_score"])
    home_score = int(game["home_score"])
    away_team = game["away_team"]
    home_team = game["home_team"]
    if home_team == Equipo:
        return home_score, away_score
    elif away_team == Equipo:
        return away_score, home_score
    
def penalties_def(control, game, Equipo, fecha):
    if int(game["home_score"]) > 0 or int(game["away_score"]) > 0:
        mapa = control['map_Req8_GoalScorers']
        llave = (Equipo, str(fecha[0:4]))
        entry = mp.get(mapa, llave)
        if entry != None:
            SubLista = me.getValue(entry)
            SubLista = SubLista['datos']
            listaOrd = quk.sort(SubLista, sort_criteria_eng)
            total_penalties = 0
            total_autogoles = 0
            for game in lt.iterator(listaOrd):
                team = game['team']
                penalty = game['penalty']
                own_goal = game['own_goal']
                if team == Equipo and penalty == 'True':
                    total_penalties += 1
                if team == Equipo and own_goal == 'True':
                    total_autogoles += 1
            return total_penalties, total_autogoles
        else:
            return 0, 0
    else:
        return 0, 0 
                                            
def diferencia_goles_def(game, Equipo):
    away_score = int(game["away_score"])
    home_score = int(game["home_score"])
    away_team = game["away_team"]
    home_team = game["home_team"]
    if away_team == Equipo:
        return away_score - home_score
    elif home_team == Equipo:
        return home_score - away_score
    
def winner_losses_team(control, game, Equipo, fecha):
    if game["home_team"] == Equipo:
        if game["home_score"] > game["away_score"]:
            return 1, 0, 0
        elif game["home_score"] < game["away_score"]:
            return 0, 1, 0
        else:
            mapa = control['map_TeamShootouts']
            entry = mp.get(mapa, Equipo)
            if entry != None:
                SubLista = me.getValue(entry)
                SubLista = SubLista['datos']
                listaOrd = quk.sort(SubLista, sort_criteria_eng)
                Pos = busqueda_binaria_req3(listaOrd, fecha)
                datos = lt.getElement(listaOrd, Pos)
                winner = datos["winner"]
                if winner == Equipo:
                    return 1, 0, 0
                else: 
                    return 0, 1, 0
            else:
                return 0, 0, 1
    if game["away_team"] == Equipo:
        if game["home_score"] < game["away_score"]:
            return 1, 0, 0
        elif game["home_score"] > game["away_score"]:
            return 0, 1, 0
        else:
            mapa = control['map_TeamShootouts']
            entry = mp.get(mapa, Equipo)
            if entry != None:
                SubLista = me.getValue(entry)
                SubLista = SubLista['datos']
                listaOrd = quk.sort(SubLista, sort_criteria_eng)
                Pos = busqueda_binaria_req3(listaOrd, fecha)
                datos = lt.getElement(listaOrd, Pos)
                winner = datos["winner"]
                if winner == Equipo:
                    return 1, 0, 0
                else: 
                    return 0, 1, 0
            else: 
                return 0, 0, 1
    
    



def busqueda_binaria_req5(lista, valor):
    izq = 0
    der = lt.size(lista)
    while izq <= der:
        punto_medio = (izq+der)//2   
        dict = lt.getElement(lista, punto_medio)
        fecha = dict["date"]  
        if fecha == valor:
            return dict
        if fecha  > valor:
            der = punto_medio - 1
        if fecha  < valor:
            izq = punto_medio + 1
    return -1

def busqueda_binaria_req3(lista, valor):
    izq = 0
    der = lt.size(lista)
    while izq <= der:
        punto_medio = (izq+der)//2   
        fecha = lt.getElement(lista, punto_medio)
        fecha = fecha["date"]  
        if fecha == valor:
            return punto_medio
        if fecha  > valor:
            der = punto_medio - 1
        if fecha  < valor:
            izq = punto_medio + 1
    return -1


# Funciones utilizadas para comparar elementos dentro de una lista

def cmp_partidos_by_fecha_y_pais(resultado1, resultado2):
    if resultado1["date"] < resultado2["date"]:
        return 1
    elif resultado1["date"] == resultado2["date"]:
        if resultado1["away_team"][0] < resultado2["away_team"][0]:
            return 1
        else:
            return -1 
    else: 
        return -1
    
def compareYears(year1, year2):
    if (int(year1) == int(year2)):
        return 0
    elif (int(year1) > int(year2)):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1
    
# Funciones de ordenamiento


def sort_criteria_eng(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    if data_1["date"] < data_2["date"]:
        return True
    elif data_1["date"] == data_2["date"]:
        if data_1["away_team"][0] < data_2["away_team"][0]:
            return True
        else:
            return False
    else: 
        return False

def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    if data_1["date"] < data_2["date"]:
        return True
    elif data_1["date"] == data_2["date"]:
        if data_1["home_team"][0] < data_2["home_team"][0]:
            return True
        else:
            return False
    else: 
        return False
    
def sort(data_structs, metodo):
    """
    Función encargada de ordenar la lista con los datos
    """
    sub_list1 = lt.subList(data_structs["match_results"],1,lt.size(data_structs["match_results"]))
    sub_list2 = lt.subList(data_structs["goal_scorers"],1,lt.size(data_structs["goal_scorers"]))
    sub_list3 = lt.subList(data_structs["shootouts"],1,lt.size(data_structs["shootouts"]))
    if metodo == 1:
        se.sort(sub_list1, sort_criteria)
        se.sort(sub_list2, sort_criteria)
        se.sort(sub_list3, sort_criteria)
    elif metodo == 2:
        ins.sort(sub_list1, sort_criteria)
        ins.sort(sub_list2, sort_criteria)
        ins.sort(sub_list3, sort_criteria)
    elif metodo == 3:
        sa.sort(sub_list1, sort_criteria)
        sa.sort(sub_list2, sort_criteria)
        sa.sort(sub_list3, sort_criteria)
    elif metodo == 4:
        quk.sort(sub_list1, sort_criteria)
        quk.sort(sub_list2, sort_criteria)
        quk.sort(sub_list3, sort_criteria)
    elif metodo == 5:
        merg.sort(sub_list1, sort_criteria)
        merg.sort(sub_list2, sort_criteria)
        merg.sort(sub_list3, sort_criteria)
    data_structs["match_results"] = sub_list1
    data_structs["goal_scorers"] = sub_list2
    data_structs["shootouts"] = sub_list3
