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
from tabulate import tabulate

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {'results': None,
                    'goalscorers': None,
                    'shootouts': None,
                    'scorers_map': None,
                    'req1': None,
                    'req3': None,    
                    'req4': None,
                    'req5': None,
                    'req6': None,
                    'req7': None}
    
    data_structs['results'] = lt.newList('ARRAY_LIST', 
                                         cmpfunction=compare_results)
    data_structs['goalscorers'] = lt.newList('ARRAY_LIST', 
                                             cmpfunction=compare_goalscorers)
    data_structs['shootouts'] = lt.newList('ARRAY_LIST',
                                           cmpfunction=compare_shootouts)
    
    data_structs['scorers_map'] = mp.newMap(1000,
                                            maptype='CHAINING',
                                            loadfactor=5)
    data_structs['req1'] = lt.newList('ARRAY_LIST')
    data_structs['req3'] = lt.newList('ARRAY_LIST')
    data_structs['req4'] = lt.newList('ARRAY_LIST')
    data_structs['req5'] = lt.newList('ARRAY_LIST')
    data_structs['req6'] = lt.newList('ARRAY_LIST')
    data_structs['req7'] = lt.newList('ARRAY_LIST')
    
    return data_structs


# Funciones para agregar informacion al modelo

def add_data(data_structs, data, file_name):
    """
    Función para agregar nuevos elementos a la lista
    """
    req_data_structs(data_structs, data, file_name)

    lt.addLast(data_structs[file_name], data)
    
    return data_structs


# Funciones para creacion de mapas y demás estructuras de datos

def req_data_structs(data_structs, data, file_name):
    """
    Crea una nueva estructura para modelar los datos
    """
    if file_name == 'results':
        results_maps(data_structs, data)
    elif file_name == 'goalscorers':
        goalscorers_maps(data_structs, data)
    elif file_name == 'shootouts':
        shootouts_maps(data_structs, data)

def new_column_data(info):
    ncol = []
    for key in info:
        ncol.append(key)
    return ncol

def results_maps(data_structs, data):
    req4_results_map(data_structs, data)
    req5_results_map(data_structs, data)
    req6_results_map(data_structs, data)
    req7_results_map(data_structs, data)

def goalscorers_maps(data_structs, data):
    map_by_scorers(data_structs, data)
    req4_goalscorers_map(data_structs, data)
    req6_goalscorers_map(data_structs, data)
    req7_goalscorers_map(data_structs, data)
    
def shootouts_maps(data_structs, data):
    req4_shootouts_map(data_structs, data)
    req6_shootouts_map(data_structs, data)
    req7_shootouts_map(data_structs, data)

def map_by_scorers(data_structs, data):
    # sacar el mapa de los scorers
    scorers = data_structs['scorers_map']
    # guardar el nombre del scorer
    data_scorer_name = data['scorer']
    # determinar si existe o no el scorer
    exists_scorer = mp.contains(scorers, data_scorer_name)
    # si existe, obtener el valor asociado
    if exists_scorer:
        entry = mp.get(scorers, data_scorer_name)
        scorer = me.getValue(entry)
    # si no existe, crear el valor y la llave del scorer
    # en el mapa de scorers
    else:
        scorer = {'scorer':data_scorer_name,
                  'goals': None}
        scorer['goals'] = lt.newList('ARRAY_LIST')
        mp.put(scorers, data_scorer_name, scorer)
    # añadir el gol la lista del scorer en el mapa de
    # scorers
    lt.addLast(scorer['goals'], data)

### Requerimientos

# REQ 4

def req4_results_map(data_structs, data):
    # sacar la lista del requerimiento 4
    req4 = data_structs['req4']
    # determinar si el mapa no existe
    if lt.size(req4) == 0:
        # crear el mapa
        new_map = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        lt.addFirst(req4, new_map)
    # sacar el mapa de resultados del requerimiento 4
    tournaments_map = lt.getElement(req4, 1)
    # sacar el torneo
    data_tournament = data['tournament']
    # determinar si existe o no el torneo
    exists_tournament = mp.contains(tournaments_map, data_tournament)
    # si existe, obtener el valor asociado
    if exists_tournament:
        entry = mp.get(tournaments_map, data_tournament)
        tournament = me.getValue(entry)
    # si no existe, crear el valor y la llave del torneo
    # en el mapa de torneos del requerimiento
    else:
        tournament = {'tournament':data_tournament,
                      'matches':None}
        tournament['matches'] = lt.newList('ARRAY_LIST')
        mp.put(tournaments_map, data_tournament, tournament)
    # añadir la partida a la lista del torneo en el mapa de 
    # torneos del requerimiento
    lt.addLast(tournament['matches'], data)

def req4_goalscorers_map(data_structs, data):
    req4 = data_structs['req4']
    # determinar si el mapa no existe
    if lt.size(req4) == 1:
        # crear el mapa
        empty = ''
        lt.addLast(req4, empty)
# TODO REQ4
def req4_shootouts_map(data_structs, data):
    # sacar la lista del requerimiento 4
    req4 = data_structs['req4']
    # determinar si el mapa no existe
    if lt.size(req4) == 2:
        # crear el mapa
        new_map = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        lt.addLast(req4, new_map)
    # sacar el mapa de shootouts del requerimiento 4
    dates_map = lt.getElement(req4, 3)
    # sacar el torneo
    data_date = data['date']
    # determinar si existe o no la fecha
    exists_date = mp.contains(dates_map, data_date)
    # si existe, obtener el valor asociado
    if exists_date:
        entry = mp.get(dates_map, data_date)
        date = me.getValue(entry)
    # si no existe, crear el valor y la llave del torneo
    # en el mapa de torneos del requerimiento
    else:
        date = {'date':data_date,
                'matches':None}
        date['matches'] = lt.newList('ARRAY_LIST')
        mp.put(dates_map, data_date, date)
    # añadir la partida a la lista del torneo en el mapa de 
    # torneos del requerimiento
    lt.addLast(date['matches'], data)
    
    
#REQ 5
def req5_results_map(data_structs, data):
    req5 = data_structs['req5']
    #revisar si la lista está vacia para agregar el mapa
    if lt.isEmpty(req5): 
        map_results = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        lt.addFirst(req5,map_results)
    #si existe entonces se sapa el mapa para usarlo
    map_results = lt.getElement(req5,1)
    #Se procede a crear el codigo que agrega información
    date_info = data['date']
    date_exist = mp.contains(map_results,date_info)
    if date_exist:
        #si existe se agrega la info a dicha llave existente
        entry = mp.get(map_results, date_info)
        date = me.getValue(entry)
    #si no existe se crea la pareja llave valor en el mapa
    else:
        date = {'date':date_info,
                'matches':None}
        date['matches'] = lt.newList('ARRAY_LIST')
        mp.put(map_results, date_info, date)
    lt.addLast(date['matches'], data)
# REQ 6

def req6_results_map(data_structs, data):
    # sacar la lista del requerimiento 4
    req6 = data_structs['req6']
    # determinar si el mapa no existe
    if lt.size(req6) == 0:
        # crear el mapa
        new_map = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        lt.addFirst(req6, new_map)
    # sacar el mapa de resultados del requerimiento 6
    tournaments_map = lt.getElement(req6, 1)
    # sacar el torneo
    data_tournament = data['tournament']
    # determinar si existe o no el torneo
    exists_tournament = mp.contains(tournaments_map, data_tournament)
    # si existe, obtener el valor asociado
    if exists_tournament:
        entry = mp.get(tournaments_map, data_tournament)
        tournament = me.getValue(entry)
    # si no existe, crear el valor y la llave del torneo
    # en el mapa de torneos del requerimiento
    else:
        tournament = {'tournament':data_tournament,
                      'teams':None}
        tournament['teams'] = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        mp.put(tournaments_map, data_tournament, tournament)
    # adquirir el mapa de equipos del torneo
    entry = mp.get(tournaments_map, data_tournament)
    tournament_teams_map = me.getValue(entry)['teams']
    # sacar los equipos involucrados en el partido
    data_home_team = data['home_team']
    data_away_team = data['away_team']
    # determinar si existen o no en el mapa de equipos en el torneo
    exists_home_team = mp.contains(tournament_teams_map, data_home_team)
    exists_away_team = mp.contains(tournament_teams_map, data_away_team)
    # si existe el home_team, obtener el valor asociado
    if exists_home_team:
        entry = mp.get(tournament_teams_map, data_home_team)
        home_team = me.getValue(entry)
    # si no existe, crear el valor y la llave del home_team
    # en el mapa de teams del requerimiento
    else:
        home_team = {'team':data_home_team,
                      'matches': None}
        home_team['matches'] = lt.newList('ARRAY_LIST')
        mp.put(tournament_teams_map, data_home_team, home_team)
    # si existe el away_team, obtener el valor asociado
    if exists_away_team:
        entry = mp.get(tournament_teams_map, data_away_team)
        away_team = me.getValue(entry)
    # si no existe, crear el valor y la llave del away_team
    # en el mapa de teams del requerimiento
    else:
        away_team = {'team':data_away_team,
                      'matches': None}
        away_team['matches'] = lt.newList('ARRAY_LIST')
        mp.put(tournament_teams_map, data_away_team, away_team)
    # añadir la partida a la lista del equipo en el mapa de 
    # teams del requerimiento
    lt.addLast(home_team['matches'], data)
    lt.addLast(away_team['matches'], data)

def req6_goalscorers_map(data_structs, data):    
    # sacar la lista del requerimiento 6
    req6 = data_structs['req6']
    # determinar si el mapa no existe
    if lt.size(req6) == 1:
        # crear el mapa
        new_map = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        lt.addLast(req6, new_map)
    # sacar el mapa de shootouts del requerimiento 6
    dates_map = lt.getElement(req6, 2)
    # sacar la fecha
    data_date = data['date']
    # determinar si existe o no la fecha
    exists_date = mp.contains(dates_map, data_date)
    # si existe, obtener el valor asociado
    if exists_date:
        entry = mp.get(dates_map, data_date)
        date = me.getValue(entry)
    # si no existe, crear el valor y la llave de la fecha
    # en el mapa de fechas del requerimiento
    else:
        date = {'date':data_date,
                'matches':None}
        date['matches'] = lt.newList('ARRAY_LIST')
        mp.put(dates_map, data_date, date)
    # añadir la partida a la lista de la fecha en el mapa de 
    # fechas del requerimiento
    lt.addLast(date['matches'], data)

def req6_shootouts_map(data_structs, data):
    req6 = data_structs['req6']
    # determinar si el mapa no existe
    if lt.size(req6) == 2:
        # crear el mapa
        empty = ''
        lt.addLast(req6, empty)

# REQ 7

def req7_results_map(data_structs, data):
    # sacar la lista del requerimiento 7
    req7 = data_structs['req7']
    # determinar si el mapa no existe
    if lt.size(req7) == 0:
        # crear el mapa
        new_map = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        lt.addFirst(req7, new_map)
    # sacar el mapa de resultados del requerimiento 7
    dates_map = lt.getElement(req7, 1)
    # sacar la fecha
    data_date = data['date']
    # determinar si existe o no la fecha
    exists_date = mp.contains(dates_map, data_date)
    # si existe, obtener el valor asociado
    if exists_date:
        entry = mp.get(dates_map, data_date)
        date = me.getValue(entry)
    # si no existe, crear el valor y la llave de la fecha
    # en el mapa de fechas del requerimiento
    else:
        date = {'date':data_date,
                'matches':None}
        date['matches'] = lt.newList('ARRAY_LIST')
        mp.put(dates_map, data_date, date)
    # añadir la partida a la lista de la fecha en el mapa de 
    # fechas del requerimiento
    lt.addLast(date['matches'], data)

def req7_goalscorers_map(data_structs, data):    
    # sacar la lista del requerimiento 7
    req7 = data_structs['req7']
    # determinar si el mapa no existe
    if lt.size(req7) == 1:
        # crear el mapa
        new_map = mp.newMap(1000,maptype='CHAINING',loadfactor=5)
        lt.addLast(req7, new_map)
    # sacar el mapa de goalscorers del requerimiento 7
    scorers_map = lt.getElement(req7, 2)
    # sacar el scorer
    data_scorer = data['scorer']
    # determinar si existe o no el scorer
    exists_scorer = mp.contains(scorers_map, data_scorer)
    # si existe, obtener el valor asociado
    if exists_scorer:
        entry = mp.get(scorers_map, data_scorer)
        scorer = me.getValue(entry)
    # si no existe, crear el valor y la llave del scorer
    # en el mapa de scorers del requerimiento
    else:
        scorer = {'scorer':data_scorer,
                'matches':None}
        scorer['matches'] = lt.newList('ARRAY_LIST')
        mp.put(scorers_map, data_scorer, scorer)
    # añadir la partida a la lista del scorer en el mapa de 
    # scorers del requerimiento
    lt.addLast(scorer['matches'], data)

def req7_shootouts_map(data_structs, data):
    req7 = data_structs['req7']
    # determinar si el mapa no existe
    if lt.size(req7) == 2:
        # crear el mapa
        empty = ''
        lt.addLast(req7, empty)


# Funciones de consulta

def get_data(data_structs, id, file_name=None):
    """finds and returns an element from a data structure

    Args:
        data_structs (dict or list): data structure where element is found 
        id (int): position of element
        file_name (str, optional): If not None, this arguement
            will serve as a key within the datastructure. Defaults to None.

    Returns:
        same as element: the element found is returned
    """
    if file_name != None:
        return lt.getElement(data_structs[file_name], id)
    else:
        return lt.getElement(data_structs, id)

def data_size(data_structs, file_name=None):
    """returns the size of a data structure

    Args:
        data_structs (list): data structure
        file_name (str, optional): If not None, this arguement
            will serve as a key within the datastructure. Defaults to None.

    Returns:
        int: returns the size of the data structure
    """
    if file_name != None:
        return lt.size(data_structs[file_name])
    else:
         return lt.size(data_structs)
     
     
def new_top3bot3_sublist(sorted_list):
    """creates a list that contains the first 3 and last 3 elements of
        a data structure

    Args:
        data_structs (list): original data structure

    Returns:
        list: a list containing the first 3 and last 3 elements of the original list
    """
    top3bot3 = lt.newList('ARRAY_LIST')
    toplist = lt.subList(sorted_list, 1, 3)
    botlist = lt.subList(sorted_list, data_size(sorted_list)-2, 3)
    
    for elem in lt.iterator(toplist):
        list_elem = []
        if type(elem) is dict:
            for value in elem.values():
                list_elem.append(value)
        elif type(elem) is list:
            for value in elem:
                list_elem.append(value)
        lt.addLast(top3bot3, list_elem)
    
    for elem in lt.iterator(botlist):
        list_elem = []
        if type(elem) is dict:
            for value in elem.values():
                list_elem.append(value)
        elif type(elem) is list:
            for value in elem:
                list_elem.append(value)
        lt.addLast(top3bot3, list_elem)
        
    return top3bot3


### Requerimientos

# REQ 1
def first_last(informacion):
    
    if lt.size(informacion) < 6:
        return informacion
    primeros = lt.subList(informacion,1,3)
    ultimos = lt.subList(informacion,lt.size(informacion)-2,3)
    respuesta = lt.newList('ARRAY_LIST')
    for i in lt.iterator(primeros):
        lt.addLast(respuesta,i)
    for i1 in lt.iterator(ultimos):
        lt.addLast(respuesta,i1) 
    return respuesta

def print_games_played(data_structs,games,team,condition):
    """
    Función que soluciona el requerimiento 1
    """
    
    req1 = data_structs['req1']
    results = data_structs['results']
    list1 = lt.newList("SINGLE_LINKED")
    total_teams = 0
    total_matches_team = 0
    total_matches_condition = 0
    for val in lt.iterator(results):
        total_teams +=1 
        if val["home_team"] == team or val["away_team"] == team:
            total_matches_team +=1
        if condition == "home":
            if val["home_team"] == team:
                total_matches_condition +=1 
                lt.addLast(list1,val)  
        if condition == "away":
            if val["away_team"] == team:
                total_matches_condition +=1
                lt.addLast(list1,val)
        if condition == "indiferent":
            if val["home_team"] == team:
                total_matches_condition +=1
                lt.addLast(list1,val)
            if val["away_team"] == team:
                total_matches_condition +=1
                lt.addLast(list1,val)  
                      
    list2 = lt.newList("SINGLE_LINKED")
    count = 0
    for num in lt.iterator(list1):  
        if count < games:
            lt.addLast(list2,num)
            count += 1   

    return first_last(list2),total_teams,total_matches_team,total_matches_condition


# REQ 2

def Goals_for_player(data_structs,n_goals,player):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    
    goalscorers = data_structs['goalscorers']
    list1 = lt.newList("SINGLE_LINKED")
    list2 = lt.newList("SINGLE_LINKED")
    total_goals = 0
    goals_penalty = 0
    for i in lt.iterator(goalscorers):
        total_goals += 1
        if i["scorer"] == player:
            if i["penalty"] == "True":
                goals_penalty += 1
            lt.addLast(list1,i)
     
    size_goals_player = lt.size(list1)
    count = 0
    for num in lt.iterator(list1):
        if count < n_goals:
            lt.addLast(list2,num)
            count += 1

    return first_last(list2),total_goals,size_goals_player,goals_penalty


# REQ 3

def filter_date(list,fecha_inicial,fecha_final):
    filter = lt.newList("SINGLE_LINKED")
    for p in lt.iterator(list):
        if(p["date"]) <= fecha_final and (p["date"]) >= fecha_inicial:
            lt.addLast(filter,p)
    return filter   

def Consult_Period_Matches(data_structs,team,start_date,end_date):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    results = data_structs['results']
    lst1 = lt.newList("SINGLE_LINKED")
    lst2 = lt.newList("SINGLE_LINKED")
    home_games = lt.newList("SINGLE_LINKED")
    away_games = lt.newList("SINGLE_LINKED")
    total_teams = 0
    total_games_team = 0
    for pl in lt.iterator(results):
        total_teams  +=1  
    for pl in lt.iterator(filter_date(results,start_date,end_date)):        
        if pl["home_team"] == team:
            total_games_team += 1
            lt.addLast(lst1,pl)
            lt.addLast(home_games,pl)
        if pl["away_team"] == team:
            total_games_team += 1
            lt.addLast(lst1,pl)
            lt.addLast(away_games,pl)
    
    for y in lt.iterator(lst1):
        lt.addFirst(lst2,y)

    return first_last(lst2),total_teams,total_games_team,lt.size(home_games),lt.size(away_games)


# REQ 4

def tournament_matches(data_structs, tournament, start_date, end_date):
    """
    Función que soluciona el requerimiento 4
    """
    # Realizar el requerimiento 4
    req4 = data_structs['req4']
    start_date = create_date_value({'date':start_date})
    end_date = create_date_value({'date':end_date})
    matches_list, count = tournament_matches_list(req4, tournament, start_date, end_date)
    if lt.isEmpty(matches_list):
        return None, count
    else:
        sort(matches_list, 'req4')
        return matches_list, count
    
def tournament_matches_list(req4, tournament, start_date, end_date):
    r_req4 = lt.getElement(req4, 1) # mapa de torneos
    # determinar si existe o no el torneo en el mapa
    exists_tournament = mp.contains(r_req4, tournament)
    if not exists_tournament:
        empty_list = lt.newList()
        return empty_list, None
    # si existe, obtener la lista
    entry = mp.get(r_req4, tournament)
    tournament_list = me.getValue(entry)['matches']
    # obtener el mapa de shootouts
    s_req4 = lt.getElement(req4, 3) # mapa de shootouts por fecha
    # crear la lista respuesta
    matches_list = lt.newList('ARRAY_LIST')
    # adquirir la cantidad total de torneos en el mapa
    tournaments_in_map = mp.keySet(r_req4)
    total_tournaments = lt.size(tournaments_in_map)
    # aquirir la cantidad de partidos del torneo
    tournament_matches = lt.size(tournament_list)
    # inicializar los contadores
    count = {'total_tournaments':total_tournaments,
             'total_tournament_matches':tournament_matches,
             'total_matches_in_range':0,
             'total_involved_countries':[],
             'total_involved_cities':[],
             'total_penalty_matches':0
             }
    # iterar la lista del torneo
    for match in lt.iterator(tournament_list):
        match_date_value = create_date_value(match)
        # verificar si la partida está en el rango de fechas
        if (match_date_value > start_date) and (match_date_value < end_date):
            count['total_matches_in_range'] += 1
            # crear el elemento de la partida
            element = tournament_matches_element(match, s_req4, count)
            # añadir el elemento de la partida a la lista respuesta
            lt.addFirst(matches_list, element)
    # cambiar contadores
    count['total_involved_countries'] = len(count['total_involved_countries'])
    count['total_involved_cities'] = len(count['total_involved_cities'])
    # retornar la lista respuesta y el contador
    return matches_list, count

def tournament_matches_element(match, s_req4, count):
    # modificar contadores
    match_country = match['country']
    match_city = match['city']
    if match_country not in count['total_involved_countries']:
        count['total_involved_countries'].append(match_country)
    if match_city not in count['total_involved_cities']:
        count['total_involved_cities'].append(match_city)
    # crear el elemento vacío
    element = ['Unkown']*10
    # añadir los valores pertinentes del partido
    # al elemento
    i = 0
    for value in match.values():
        if i < len(match)-1:
            element[i] = value
            i += 1
    # determinar si la fecha se encuentra en el mapa
    # de shootouts
    match_date = match['date']
    exists_date = mp.contains(s_req4, match_date)
    # si se encuentra, añadir los valores pertientes
    # al elemento
    found = False
    if exists_date:
        # adquirir la lista de partidos de la fecha
        entry = mp.get(s_req4, match_date)
        date_list = me.getValue(entry)['matches']
        # adquirir los valores pertinentes del partido
        match_home_team = match['home_team']
        match_away_team = match['away_team']
        # buscar el partido en la lista de la fecha
        for shootout_match in lt.iterator(date_list):
            count['total_penalty_matches'] += 1
            shootout_home_team = shootout_match['home_team']
            shootout_away_team = shootout_match['away_team']
            if match_home_team == shootout_home_team and match_away_team == shootout_away_team:
                found = True
                element[8] = True
                element[9] = shootout_match['winner']
                return element
    if not found:  
        element[8] = False 
    return element
      

# REQ 5

def sort_crit_req5(data_1,data_2):
    if create_date_value(data_1) != create_date_value(data_2):
        return create_date_value(data_1) > create_date_value(data_2)
    else:
        return data_1['minute'] < data_2['minute']

def req_5(data_structs, scorer, start_date, end_date):
    """
    Función que soluciona el requerimiento 5
    """
    #Función de ordenamiento
    # TODO: Realizar el requerimiento 5
    #creación de lista respuesta
    start_date_usable = create_date_value_from_date(start_date)
    end_date_usable = create_date_value_from_date(end_date)
    req5 = data_structs['req5']
    map_dates = lt.getElement(req5, 1)
    map_scorers = data_structs['scorers_map']
    answer_list = lt.newList('ARRAY_LIST')
    scorer_entry = mp.get(map_scorers, scorer)
    scorer_goals_list = me.getValue(scorer_entry)['goals']
    contadores = {'anotaciones_jugador':0,
                  'total_jugadores_disponibles':None,
                  'total_torneos_marcados':None,
                  'numero_torneos_marcados': None,
                  'total_goles_penales':0,
                  'total_autogoles':0}
    contadores['total_torneos_marcados'] = lt.newList('ARRAY_LIST')
    contadores['total_jugadores_disponibles'] = lt.size(mp.keySet(map_scorers))
    #recorrer la lista de goles en busca de info relevante
    for goal in lt.iterator(scorer_goals_list):
        if create_date_value_from_date(goal['date'])> start_date_usable and create_date_value_from_date(goal['date'])< end_date_usable:
            contadores['anotaciones_jugador'] += 1
            date_list_entry = mp.get(map_dates,goal['date'])
            date_list_matches = me.getValue(date_list_entry)['matches'] 
            if goal['own_goal'] == True:
                contadores['total_autogoles'] += 1
            if goal['penalty'] == True:
                contadores['total_goles_penales'] += 1
            element = {'date':goal['date'], 'minute': goal['minute'], 'home_team': goal['home_team'], 'away_team':goal['away_team'], 'scorer_team': goal['team'], 'home_score': None, 'away_score': None, 'tournament': None, 'penalty':goal['penalty'], 'own_goal': goal['own_goal']}
            for goal_2 in lt.iterator(date_list_matches):
                if goal_2['home_team'] == goal['home_team'] and goal_2['away_team'] == goal['away_team']:
                    if lt.isPresent(contadores['total_torneos_marcados'],goal_2['tournament']) == 0:
                        lt.addLast(contadores['total_torneos_marcados'],goal_2['tournament'])
                    element['tournament'] = goal_2['tournament']
                    element['home_score'] = goal_2['home_score']
                    element['away_score'] = goal_2['away_score']
            lt.addLast(answer_list,element)
    contadores['numero_torneos_marcados'] = lt.size(contadores['total_torneos_marcados'])
    sorted_answer_list = sa.sort(answer_list,sort_crit_req5)
    return sorted_answer_list, contadores         
  

# REQ 6

def classify_teams(data_structs, n, tournament, year):
    """
    Función que soluciona el requerimiento 6
    """
    # Realizar el requerimiento 6
    req6 = data_structs['req6']
    year = float(year)
    classified_teams, count = classify_teams_list(req6, tournament, year)
    
    if count != None:
        p = 0
        popular_city = 'Unkown'
        for city in count['cities']:
            if count['cities'][city] > p:
                p = count['cities'][city]
                popular_city = city     
        count['total_teams'] = len(count['total_teams'])
        
    if lt.isEmpty(classified_teams):
        return None, None, None
    else:
        sort(classified_teams, 'req6')
        top_n_classified_teams = top_n_classified_teams_list(classified_teams, n)
        return top_n_classified_teams, count, popular_city

def classify_teams_list(req6, tournament, year):
    classified_teams = lt.newList('ARRAY_LIST')
    # sacar las estructuras de datos organizadas para el Req 6 del ADT List req6
    r_req6 = lt.getElement(req6, 1) # mapa de torneos, cada uno con un diccionario de equipos
    # determinar si existe o no el torneo
    exists_tournament = mp.contains(r_req6, tournament)
    if not exists_tournament:
        return classified_teams, None
    # encontrar la cantidad total de torneos para contarlos
    tournaments_keys = mp.keySet(r_req6)
    # encontrar el mapa de equipos del torneo
    entry = mp.get(r_req6,tournament)
    teams_map = me.getValue(entry)['teams']
    # sacar las llaves de los equipos en el mapa
    team_keys = mp.keySet(teams_map)
    total_teams = lt.size(team_keys)
    count = {'total_tournaments': lt.size(tournaments_keys), # cantidad total de torneos
             'total_teams': [], # lista con los equipos del torneo en el rango
             'matches_in_range':0, # partidos evaluados
             'countries':[], # cada valor es el nombre del país
             'cities':{}} # ciudades totales, cada valor es el número de ocurrencias
    # obtener el mapa de fechas de goalscorers
    g_req6 = lt.getElement(req6, 2)
    # hacer el recorrido de los paises del torneo
    for team_name in lt.iterator(team_keys):
        # crear las variables respuesta
        elem = []
        team_scorers = {}
        team_values = {'total_points':0,
                        'matches':0,
                        'goal_difference':0,
                        'penalty_points':0,
                        'own_goal_points':0,
                        'wins':0,
                        'draws':0,
                        'losses':0,
                        'goals_for':0,
                        'goals_against':0}
        # encontrar el la lista de partidos del torneo
        entry = mp.get(teams_map,team_name)
        matches_list = me.getValue(entry)['matches']
        # sacar las llaves de los equipos en el mapa
        for match in lt.iterator(matches_list):
            match_date_value = create_date_value(match)
            # evaluar el partido si está en el rango de fechas
            if (match_date_value>=year) and (match_date_value<=year+1):
                # contar las ciudades
                count_countries_and_cities(match, count)
                # contar los partidos en el rango al igual que los equipos
                count['matches_in_range'] += 1
                if match['home_team'] not in count['total_teams']:
                    count['total_teams'].append(match['home_team'])
                if match['away_team'] not in count['total_teams']:
                    count['total_teams'].append(match['away_team'])
                # cambiar contadores del equipo
                classify_teams_match_values(match, team_name, team_values, team_scorers, g_req6)
        # calcular diferencia de goles del equipo
        team_values['goal_difference'] = team_values['goals_for'] - team_values['goals_against']
        # calcular el mejor goleador
        top_team_scorer = top_scorer(team_scorers)
        # crear el elemento para agregar a la lista respuesta
        classify_teams_element(elem, team_name, team_values, top_team_scorer)
        # añadir el elemento a la lista respuesta
        lt.addFirst(classified_teams, elem)
            
    return classified_teams, count

def count_countries_and_cities(match, count):
    """Evaluates the city and country of the match


    Args:
        match (dict): dictionary with the match's information
        count (dict): dictionary with all the pertinent counters
    """
    match_country = match['country']
    match_city = match['city']
    if match_country not in count['countries']:
        count['countries'].append(match_country)
    if match_city not in count['cities']:
        count['cities'][match_city] = 1
    else:
        count['cities'][match_city] += 1
        
def classify_teams_match_values(match, team_name, team_values, team_scorers, g_req6):
    # sacar informacion pertinente de los resultados del partido
    match_date = match['date']
    match_home_team = match['home_team']
    match_away_team = match['away_team']
    match_home_score = int(match['home_score'])
    match_away_score = int(match['away_score'])
    team_values['matches'] += 1
    # contar los puntos en las categorias pertinentes de acuerdo a los resultados
    # (goals_for, goals_against, wins, total_points)
    if team_name==match_home_team:
        team_values['goals_for'] += match_home_score
        team_values['goals_against'] += match_away_score
        if match_home_score > match_away_score:
            team_values['wins'] += 1
            team_values['total_points'] += 3
        elif match_home_score < match_away_score:
            team_values['losses'] += 1
        else:
            team_values['draws'] += 1
            team_values['total_points'] += 1
    elif team_name==match_away_team:
        team_values['goals_for'] += match_away_score
        team_values['goals_against'] += match_home_score
        if match_home_score > match_away_score:
            team_values['losses'] += 1
        elif match_home_score < match_away_score:
            team_values['wins'] += 1
            team_values['total_points'] += 3
        else:
            team_values['draws'] += 1
            team_values['total_points'] += 1
    ### contar información e los goleadores (penalty, own_goal y scorers)}
    # verificar que exista la fecha
    exists_date = mp.contains(g_req6, match_date)
    if exists_date:
        # encontrar el mapa de equipos del torneo
        entry = mp.get(g_req6, match_date)
        goalscorers_list = me.getValue(entry)['matches']
        # recorrer la lista
        for goalscorer in lt.iterator(goalscorers_list):
            goalscorer_team = goalscorer['team']
            if goalscorer_team == team_name:
                # añadir o modificar goleador en team_scorers
                goalscorer_name = goalscorer['scorer']
                
                goalscorer_minute = goalscorer['minute']
                if goalscorer_minute == '':
                    goalscorer_minute = 0
                else:
                    goalscorer_minute = float(goalscorer_minute)
                    
                if goalscorer_name not in team_scorers:
                    team_scorers[goalscorer_name] = {'name': goalscorer_name,
                                                     'goals': 1,
                                                     'matches': 1,
                                                     'total_minutes': goalscorer_minute,
                                                     'played_matches':[match_date]}
                else:
                    team_scorers[goalscorer_name]['goals'] += 1
                    team_scorers[goalscorer_name]['total_minutes'] += goalscorer_minute
                    if match_date not in team_scorers[goalscorer_name]['played_matches']:
                        team_scorers[goalscorer_name]['played_matches'].append(match_date)
                        team_scorers[goalscorer_name]['matches'] += 1
                # determinar si hubo o no penalty/own_goal y cambiar el contador
                goalscorer_own_goal = str(goalscorer['own_goal']).lower()
                goalscorer_penalty = str(goalscorer['penalty']).lower()
                if goalscorer_own_goal == 'true':
                    team_values['own_goal_points'] += 1
                if goalscorer_penalty == 'true':
                    team_values['penalty_points'] += 1

def top_scorer(scorers):
    top_scorer = ['Unknown', 0, 1, 100*100]
    for scorer in scorers.values():
        if scorer['goals'] > top_scorer[1]:
            if (scorer['total_minutes']/scorer['matches']) < (top_scorer[3]/top_scorer[2]):
                top_scorer[0] = scorer['name']
                top_scorer[1] = scorer['goals']
                top_scorer[2] = scorer['matches']
                top_scorer[3] = scorer['total_minutes']
    if top_scorer[2] != 0:
        top_scorer[3] = round(top_scorer[3]/top_scorer[2], 2)
        
    if top_scorer[0] == 'Unknown':
        top_scorer = ['N/D','N/D','N/D','N/D']
        
    return top_scorer

def classify_teams_element(elem, team_name, team_values, top_team_scorer):
    #team_name = team_name[0].upper() + team_name[1:]
    elem.append(team_name)
    elem.append(team_values['total_points'])
    elem.append(team_values['matches'])
    elem.append(team_values['goal_difference'])
    elem.append(team_values['penalty_points'])
    elem.append(team_values['own_goal_points'])
    elem.append(team_values['wins'])
    elem.append(team_values['draws'])
    elem.append(team_values['losses'])
    elem.append(team_values['goals_for'])
    elem.append(team_values['goals_against'])
    columns = ['scorer', 'goals', 'matches', 'avg_time']
    top_team_scorer = [top_team_scorer]
    top_scorer_table = tabulate(top_team_scorer, headers=columns, tablefmt="grid", maxcolwidths=[None,5,5,5])
    elem.append(top_scorer_table)

def top_n_classified_teams_list(classified_teams, n):
    top_n_classified_teams = lt.subList(classified_teams, 1, n)
    
    return top_n_classified_teams


# REQ 7

def top_scorers(data_structs, tournament, n):
    """
    Función que soluciona el requerimiento 7
    """
    # Realizar el requerimiento 7
    req7 = data_structs['req7']
    req6 = data_structs['req6']
    
    scorers, count = top_scorers_list(req7, req6, tournament)
    
    sort(scorers, 'req7')
    
    top_n_scorers = top_n_scorers_list(scorers, n)
    count['total_scorers_in_range'] = lt.size(top_n_scorers)
    return top_n_scorers, count

def top_scorers_list(req7, req6, tournament):
    scorers = lt.newList('ARRAY_LIST')
    # sacar las estructuras de datos pertinentes
    r_req7 = lt.getElement(req7, 1) # mapa de fechas
    g_req7 = lt.getElement(req7, 2) # mapa de goleadores
    tournaments = lt.getElement(req6, 1) # mapa de torneos
    # sacar la lista de torneos
    tournament_keys = mp.keySet(tournaments)
    # inicializar contadores
    count = {'total_tournaments':lt.size(tournament_keys),
             'total_matches':0,
             'total_scorers': [],
             'total_scorers_in_range':0,
             'total_goals_in_range':0,
             'total_penalty_points':0,
             'total_own_goals':0,}
    # sacar todas las llaves de los goleadores
    scorers_keys = mp.keySet(g_req7)
    # recorrer el mapa de goleadores
    for scorer in lt.iterator(scorers_keys):
        elem = []
        scorer_values = {'total_points':0,
                        'total_goals':0,
                        'penalty_points':0,
                        'own_goals':0,
                        'matches':[],
                        'scorer_minutes':0,
                        'scorer_tournaments':[],
                        'scored_in_wins':0,
                        'scored_in_losses':0,
                        'scored_in_draws':0}
        # obtener la lista de partidos del jugador
        entry = mp.get(g_req7, scorer)
        scorer_matches_list = me.getValue(entry)['matches']
        # recorrer la lista
        for match in lt.iterator(scorer_matches_list):
            # obtener valores del goleador y modificar contador
            scorers_match_value(match, scorer_values, tournament, r_req7, count)
            # obtener el último gol
            last_goal = scorer_last_goal(scorer_matches_list, r_req7, tournament)
            # construir elemento del jugador
            top_scorers_element(elem, scorer, scorer_values, last_goal)
        # agregar elemento del jugador a la lista respuesta
        lt.addFirst(scorers, elem)
    # retornar contador y lista respuesta
    return scorers, count

def scorers_match_value(match, scorer_values, tournament, r_req7, count):
    # sacar los datos pertinentes del match
    match_date = match['date']
    match_home_team = match['home_team']
    match_away_team = match ['away_team']
    scorer_team = match['team']
    minute = match['minute']
    if minute != '':
        minute = float(minute)
    else:
        minute = 0
    own_goal = str(match['own_goal']).lower()
    penalty = str(match['penalty']).lower()
    # determinar si la fecha está en resultador
    exists_date = mp.contains(r_req7, match_date)
    if exists_date:
        # obtener la lista de la fecha
        entry = mp.get(r_req7, match_date)
        date_matches_list = me.getValue(entry)['matches']
        # recorrer la fecha en busca de el resultado de 
        for result in lt.iterator(date_matches_list):
            result_home_team = result['home_team']
            result_away_team = result['away_team']
            result_tournament = result['tournament']
            if (match_home_team == result_home_team) and (match_away_team == result_away_team):
                # modificar contadores relacionados al torneo
                match_tourn = result['tournament']
                #if match_tourn not in count['total_tournaments']:
                    #count['total_tournaments'].append(match_tourn)
                if match_tourn not in scorer_values['scorer_tournaments']:
                    scorer_values['scorer_tournaments'].append(match_tourn)
                # verificar si la partida es del torneo en cuestion
                if match_tourn.lower() == tournament.lower():
                    # modificar contador de jugadores del torneo
                    match_scorer = match['scorer']
                    if match_scorer not in count['total_scorers']:
                        count['total_scorers'].append(match_scorer)
                    # modificar sentinela de torneo
                    is_tournament = True
                else:
                    is_tournament = False
                
                if is_tournament and match_date not in scorer_values['matches']:
                    scorer_values['matches'].append(match_date)
                    count['total_matches'] += 1
                
                result_home_score = int(result['home_score'])
                result_away_score = int(result['away_score'])
                if is_tournament and scorer_team == result_home_team:
                    if result_home_score > result_away_score:
                        scorer_values['scored_in_wins'] += 1
                    elif result_home_score < result_away_score:
                        scorer_values['scored_in_losses'] += 1
                    else:
                        scorer_values['scored_in_draws'] += 1
                    scorer_values['total_goals'] += 1
                elif is_tournament and scorer_team == result_away_team:
                    if result_home_score > result_away_score:
                        scorer_values['scored_in_losses'] += 1
                    elif result_home_score < result_away_score:
                        scorer_values['scored_in_wins'] += 1
                    else:
                        scorer_values['scored_in_draws'] += 1
                    scorer_values['total_goals'] += 1
                    
    scorer_values['scorer_minutes'] += minute
    
    if is_tournament:
        count['total_goals_in_range'] += 1
        if own_goal == 'true':
            scorer_values['own_goals'] += 1
            count['total_own_goals'] += 1
            scorer_values['total_points'] -= 1
        if penalty == 'true':
            scorer_values['penalty_points'] += 1
            count['total_penalty_points'] += 1
            scorer_values['total_points'] += 1

def scorer_last_goal(scorer, r_req7, tournament):

    columns = ['date', 'tournament', 'home_team', 'away_team', 'home_score', 'away_score',
               'minute', 'penalty', 'own_goal']
    last_goal = []
    
    for match in lt.iterator(scorer):
        match_date = match['date']
        match_home_team = match['home_team']
        match_away_team = match ['away_team']
        scorer_team = match['team']
        if match['minute'] != '':
            minute = float(match['minute'])
        else:
            minute = 0
        own_goal = match['own_goal']
        penalty = match['penalty']
        
        exists_date = mp.contains(r_req7, match_date)
        if exists_date:
            entry = mp.get(r_req7, match_date)
            result_list = me.getValue(entry)['matches']
            for result in lt.iterator(result_list):
                result_home_team = result['home_team']
                result_away_team = result['away_team']
                result_tournament = result['tournament']
                if (match_home_team == result_home_team) and (match_away_team == result_away_team) and (result_tournament.lower() == tournament.lower()):
                    
                    result_home_score = int(result['home_score'])
                    result_away_score = int(result['away_score'])
                    
                    last_goal.append(match_date)
                    last_goal.append(result_tournament)
                    last_goal.append(result_home_team)
                    last_goal.append(result_away_team)
                    last_goal.append(result_home_score)
                    last_goal.append(result_away_score)
                    last_goal.append(minute)
                    last_goal.append(own_goal)
                    last_goal.append(penalty)
                    
                    last_goal = [last_goal]
                    last_goal = tabulate(last_goal, headers=columns, tablefmt="grid", maxcolwidths=[None, 10, 10, 10, 5, 5, 5])
                    
                    return last_goal
                
    last_goal = ['Unkown', 'Unkown', 'Unkown', 'Unkown', 'Unkown', 'Unkown',
               'Unkown', 'Unkown', 'Unkown']     
      
    return last_goal

def top_scorers_element(elem, name, scorer_values, last_goal):
    elem.append(name)
    
    total_points = scorer_values['total_points'] + scorer_values['total_goals']
    elem.append(total_points)
    
    elem.append(scorer_values['total_goals'])
    elem.append(scorer_values['penalty_points'])
    elem.append(scorer_values['own_goals'])
    
    if len(scorer_values['matches']) != 0:
        avg_time = scorer_values['scorer_minutes'] / len(scorer_values['matches'])
    else:
        avg_time = 'Unkown'
    elem.append(avg_time)
    
    elem.append(len(scorer_values['scorer_tournaments']))
    elem.append(scorer_values['scored_in_wins'])
    elem.append(scorer_values['scored_in_losses'])
    elem.append(scorer_values['scored_in_draws'])
    elem.append(last_goal)
    
def top_n_scorers_list(scorers, n):
    top_n_scorers = lt.newList('ARRAY_LIST')
    for scorer in lt.iterator(scorers):
        scorer_total_points = scorer[1]
        if scorer_total_points == n:
            lt.addLast(top_n_scorers, scorer)
    return top_n_scorers



# REQ 8

def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare_results(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    score1_home = data_1['home_score']
    score2_home = data_2['home_score']
    score1_away = data_1['away-score']
    score2_away = data_2['away_score']

    if score1_home == score2_home:
        if score1_away == score2_away:
            return 0
        elif score1_away > score2_away:
            return 1
    elif score1_home > score2_home:
        return 1
    return -1

def compare_goalscorers(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    minute1 = data_1['minute']
    minute2 = data_2['minute']
    name1 = data_1['scorer'].lower()
    name2 = data_2['scorer'].lower()
    
    if minute1 == minute2:
        if name1 == name2:
            return 0
        elif name1 > name2:
            return 1
    elif minute1 > minute2:
        return 1
    return -1

def compare_shootouts(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    team1_home = data_1['home_team'].lower()
    team2_home = data_2['home_team'].lower()
    team1_away = data_1['away_team'].lower()
    team2_away = data_2['away_team'].lower()
    
    if team1_home == team2_home:
        if team1_away == team2_away:
            return 0
        elif team1_away > team2_away:
            return 1
    elif team1_home > team2_home:
        return 1
    return -1


####### Funciones de ordenamiento

# Funciones de condiciones generales

def create_date_value(data):
    """creates a date value


    Args:
        data1 (list): a list where the first element (data1[0]) is a date formatted as
            (%Y-%M-%D)


    Returns:
        int: the sum of the date in years
    """
    #Data 1 Info
    date_str = data['date'].split('-')
    #Date 1 Value
    date_year = int(date_str[0])
    date_month = int(date_str[1])/12
    date_day = int(date_str[2])/365.25
    date_value = date_year + date_month + date_day
    
    return date_value
def create_date_value_from_date(date):
    """creates a date value


    Args:
        data1 (list): a list where the first element (data1[0]) is a date formatted as
            (%Y-%M-%D)


    Returns:
        int: the sum of the date in years
    """
    #Data 1 Info
    date_str = date.split('-')
    #Date 1 Value
    date_year = int(date_str[0])
    date_month = int(date_str[1])/12
    date_day = int(date_str[2])/365.25
    date_value = date_year + date_month + date_day
    
    return date_value

# Criterios de ordenamiento

def sort_results_criteria(data1, data2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento


    Args:
        data1 (type): description
        data2 (type): description

    Returns:
        type: description
    """
    
    #Data 1 Info
    date1_value = create_date_value(data1)
    date2_value = create_date_value(data2)
    home1_score = data1['home_score']
    home2_score = data2['home_score']
    away1_score = data1['away_score']
    away2_score = data2['away_score']
    
    if date1_value == date2_value:
        if home1_score != home2_score:
            return home1_score > home2_score
        else:
            return away1_score > away2_score   
    else:
        return date1_value > date2_value
        
def sort_goalscorers_criteria(data1, data2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento


    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_


    Returns:
        _type_: _description_
    """
    
    #Data 1 Info
    date1_value = create_date_value(data1)
    date2_value = create_date_value(data2)
    minute1 = data1['minute']
    minute2 = data2['minute']
    name1 = data1['scorer'].lower()
    name2 = data2['scorer'].lower()
    
    if date1_value == date2_value:
        if minute1 != minute2:
            return minute1 > minute2
        else: 
            return name1 > name2
    else:
        return date1_value > date2_value
        
def sort_shootouts_criteria(data1, data2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (type): description
        data2 (type): description

    Returns:
        _type_: _description_
    """
    
    #Data 1 Info
    date1_value = create_date_value(data1)
    date2_value = create_date_value(data2)
    team1_home = data1['home_team'].lower()
    team2_home = data2['home_team'].lower()
    team1_away = data1['away_team'].lower()
    team2_away = data2['away_team'].lower()
    
    if date1_value == date2_value:
        if team1_home != team2_home:
            return team1_home > team2_home
        else: 
            return team1_away > team2_away
    else:
        return date1_value > date2_value
    
def sort_req4_criteria(data1, data2):
    #Data Info
    date1_value = create_date_value({'date':data1[0]})
    date2_value = create_date_value({'date':data2[0]})
    team1_country = data1[6].lower()
    team2_country = data2[6].lower()
    team1_city = data1[7].lower()
    team2_city = data2[7].lower()
    
    if date1_value == date2_value:
        if team1_country != team2_country:
            return team1_country > team2_country
        else: 
            return team1_city > team2_city
    else:
        return date1_value > date2_value
    
def sort_req6_criteria(data1, data2):
    total1 = int(data1[1])
    total2 = int(data2[1])
    diff1 = int(data1[3])
    diff2 = int(data2[3])
    penalty1 = int(data1[4])
    penalty2 = int(data2[4])
    matches1 = int(data1[2])
    matches2 = int(data2[2])
    auto1 = int(data1[5])
    auto2 = int(data2[5])
    for1 = int(data1[9])
    for2 = int(data2[9])
    ag1 = int(data1[10])
    ag2 = int(data2[10])
    
    if total1 == total2:
        if diff1 != diff2:
            return diff1 > diff2
        elif penalty1 != penalty2:
            return penalty1 > penalty2
        elif matches1 != matches2:
            return matches1 < matches2
        elif auto1 != auto2:
            return auto1 < auto2
        elif for1 != for2:
            return for1 > for2
        else:
            return ag1 < ag2
    else:
        return total1 > total2

def sort_req7_criteria(data1, data2):
    total1 = int(data1[1])
    total2 = int(data2[1])
    goals1 = int(data1[2])
    goals2 = int(data2[2])
    penalty1 = int(data1[3])
    penalty2 = int(data2[3])
    auto1 = int(data1[4])
    auto2 = int(data2[4])
    minutes1 = data1[5]
    minutes2 = data2[5]
    
    if minutes1 == 'Unkown':
        minutes1 = 0
    else:
        minutes1 = int(minutes1)
    if minutes2 == 'Unkown':
        minutes2 = 0
    else:
        minutes2 = int(minutes2)
    
    if total1 == total2:
        if goals1 != goals2:
            return goals1 > goals2
        elif penalty1 != penalty2:
            return penalty1 > penalty2
        elif auto1 != auto2:
            return auto1 < auto2
        else:
            return minutes1 < minutes2
    else:
        return total1 > total2


def sort(data_structs, file_name):
    """
    Función encargada de ordenar la lista con los datos
    """
    if file_name == 'results':
        criteria = sort_results_criteria
        merg.sort(data_structs[file_name], criteria)
    elif file_name == 'goalscorers':
        criteria = sort_goalscorers_criteria
        merg.sort(data_structs[file_name], criteria)
    elif file_name == 'shootouts':
        criteria = sort_shootouts_criteria
        merg.sort(data_structs[file_name], criteria)
    elif file_name == 'req4':
        criteria = sort_req4_criteria
        merg.sort(data_structs, criteria)
    elif file_name == 'req6':
        criteria = sort_req6_criteria
        merg.sort(data_structs, criteria)
    elif file_name == 'req7':
        criteria = sort_req7_criteria
        merg.sort(data_structs, criteria)
    elif file_name == 'g_req7':
        criteria = sort_goalscorers_criteria
        req7 = data_structs['req7']
        g_req7 = lt.getElement(req7, 2)
        scorer_keys = mp.keySet(g_req7)
        for scorer in lt.iterator(scorer_keys):
            entry = mp.get(g_req7, scorer)
            scorer_list = me.getValue(entry)['matches']
            merg.sort(scorer_list, criteria)
        
        