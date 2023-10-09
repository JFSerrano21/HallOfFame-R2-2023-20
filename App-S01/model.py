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
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from tabulate import tabulate
assert cf
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_historial_FIFA(list):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    historial_FIFA = {
        "results": None,
        "goalscorers": None,
        "shootouts": None,
        "torneos": None,
        "paises": None,
        "equipo_goles": None,
        "partidos_oficiales": None}

    # definicion de arreglos
    historial_FIFA["results"] = lt.newList(datastructure=list, cmpfunction=comparepenales_o_partidos)
    historial_FIFA["goalscorers"] = lt.newList(datastructure=list, cmpfunction=comparegoles)
    historial_FIFA["shootouts"] = lt.newList(datastructure=list, cmpfunction=comparepenales_o_partidos)
    historial_FIFA["torneos"] = lt.newList('ARRAY_LIST', cmpfunction=comparetorneos)
    historial_FIFA["paises"] = lt.newList("ARRAY_LIST", cmpfunction=compare_equipos) 
    historial_FIFA["equipos_goles"] = lt.newList("ARRAY_LIST", cmpfunction=compare_equipos)
    historial_FIFA["partidos_oficiales"] = lt.newList("ARRAY_LIST", cmpfunction=comparepenales_o_partidos)
    return historial_FIFA
    


# Funciones para agregar informacion al modelo

def add_result(historial_FIFA, result):
    """
    Función para agregar nuevos elementos a la lista
    """
    rs = new_result(result["date"], result["home_team"], result["away_team"], result["home_score"], result["away_score"],result["country"], result["city"], result["tournament"] )
    lt.addLast( historial_FIFA["results"], rs)
    # Cada pais se grega a la lista de paises
    paises = rs["home_team"], rs["away_team"]
    for pais in paises:
        add_pais(historial_FIFA, pais.strip(), rs)
    #Cada torneo se agrega a la lista de torneos
    torneo = rs["tournament"]
    add_torneo(historial_FIFA, torneo.strip(), rs)
    #Se agrega a la lista de partidos oficiales si es oficial.
    if torneo != "Friendly":
        add_partido_oficial(historial_FIFA, rs)
    return historial_FIFA

def add_partido_oficial(historial_FIFA, rs):
    lt.addLast(historial_FIFA["partidos_oficiales"] , rs )
    return historial_FIFA
    

def add_pais(historial_FIFA, pais, rs):
    paises = historial_FIFA["paises"]
    pospais = lt.isPresent(paises, pais)
    if pospais > 0:
        pais = lt.getElement(paises, pospais)
    else:
        pais = new_pais(pais)
        lt.addLast(paises,pais)
    partido_de_pais = new_partido_de_pais(rs)
    if pais["team"] == rs["home_team"]:
        lt.addLast(pais["local"], partido_de_pais)
    elif pais["team"] == rs["away_team"]:
        lt.addLast(pais["visitante"], partido_de_pais)
    lt.addLast(pais["indiferente"], partido_de_pais)
    return historial_FIFA
              

def add_torneo(historial_FIFA, torneo, rs):
    torneos = historial_FIFA["torneos"]
    postorneo =lt.isPresent(torneos, torneo)
    if postorneo > 0:
        torneo = lt.getElement(torneos, postorneo)
    else:
        torneo = new_torneo(torneo)
        lt.addLast(torneos, torneo)
        
    winner = "Unknown"
    penales = historial_FIFA["shootouts"]
    pospartido_penal = lt.isPresent(penales, rs)
    if pospartido_penal > 0:
        penal = lt.getElement(penales, pospartido_penal)
        winner = penal["winner"]
    partido = new_partido_en_torne(rs["date"], rs["tournament"], rs["country"], rs["city"], rs["home_team"], rs["away_team"], rs["home_score"], rs["away_score"], winner)
    lt.addLast(torneo["partidos"], partido)

    return historial_FIFA
    
def add_goal(historial_FIFA, goal):
    """
    Agrega un elemento a la lista de lo goles
    """
    lt.addFirst(historial_FIFA["goalscorers"], goal)
    
    #Se agrega el equipo a las lista de equipos_goles
    equipos_goles = historial_FIFA["equipos_goles"]
    equipo = goal["team"]
    posequipo = lt.isPresent(equipos_goles, equipo)
    if posequipo > 0:
         equipo = lt.getElement(equipos_goles, posequipo)
    else:
        equipo = new_equipo_goles(equipo)
        lt.addLast(equipos_goles, equipo) 
           
    goles = equipo["goles"]
    lt.addLast(goles, goal)
    
    return historial_FIFA

def add_shootout(historial_FIFA, shootout):
    lt.addLast(historial_FIFA["shootouts"] , shootout )
    return historial_FIFA

# Funciones para creacion de datos


# ===================================================== FUNCIONES new_algo =====================================================
#--------------------------------------- Para carga de datos--------------------

def new_result(date, home_team, away_team, home_score, away_score, country, city, tournament):
    rs = {"date": date, "home_team": home_team, "away_team": away_team, "home_score": home_score, "away_score": away_score,"country": country, "city": city, "tournament":tournament}
    return rs

def new_pais(pais):
    ps = {"team": None, 
          "visitante": None, 
          "local": None, "indiferente": None} 
    ps["team"] = pais
    ps["visitante"] = lt.newList("ARRAY_LIST")
    ps["local"] = lt.newList("ARRAY_LIST")
    ps["indiferente"] = lt.newList("ARRAY_LIST")
    
    return ps

def new_partido_de_pais(rs):
    pr = {"date": rs["date"], "home_team": rs["home_team"],"away_team": rs["away_team"], "home_score": rs["home_score"], "away_score": rs["away_score"], "country": rs["country"], "city": rs["city"], "tournament": rs["tournament"] }
    return pr


def new_torneo(torneo):
    tr = {"name": torneo,"partidos": None }
    tr["partidos"] = lt.newList('ARRAY_LIST')
    return tr

def new_partido_en_torne(date, tournament, country, city, home_team, away_team, home_score, away_score, winner):
    partido = {"date": date, 
               "tournament": tournament, 
               "country": country, 
               "city": city,
               'home_team': home_team, 
               "away_team": away_team, 
               'home_score': home_score, 
               "away_score": away_score,
               'winner': winner}
    return partido

def new_equipo_goles(equipo):
    eqg = {"team": equipo, "goles": None}
    eqg["goles"] = lt.newList("ARRAY_LIST", cmpfunction=comparegoles)
    return eqg

#--------------------------- Para los requerimientos ------------------------

#Para req5
def new_jugador(jugador, partido):
    player={"date": partido["date"],
            "minute": jugador["minute"],
            "home_team": jugador["home_team"],
            "away_team": jugador["away_team"],
            "team": jugador["team"],
            "home_score": partido["home_score"],
            "away_score":partido["away_score"],
            "tournament": partido["tournament"],
            "penalty": jugador["penalty"],
            "own_goal":jugador["own_goal"]}
    return player

#Para req6
def new_ciudad(ciudad):
    cd = {"name": ciudad, "num_encuentros": 1}
    return cd

def new_equipo(equipo):
    eq = {"team": equipo, 
          "total_points": 0, 
          "goal_difference": 0, 
          "penalty_points": 0,
          "matches":0,
          "own_goal_points": 0,
          "wins": 0,
          "draws": 0,
          "losses": 0,
          "goals_for": 0,
          "goals_against": 0,
          "top_scorer": None}
    return eq

def new_goleador(goleador):
    scr = {"scorer": goleador,
           "goals": 0, "matches": 0,
           "avg_time [min]": 0}
    #En la utltima llave, a lo largo del programa se guardará realmente la sumatoria de minutos
    #Cuando se sepa que es el mejor jugador, se calculará, con esa sumatoria el promedio (diidiendola en el total de goles anotados)
    return scr

def new_equipo_goleadores(equipo):
    eqg = {"team": equipo, "goleadores": None}
    eqg["goleadores"] = lt.newList("ARRAY_LIST", cmpfunction=comparescorers)
    return eqg

# Para req7
def new_anotador(anotador):
    an = {"scorer": anotador,
          "total_points": 0, #se calcula al final de todo
          "total_goals": 0,
          "penalty_goals": 0,
          "own_goals": 0,
          "avg_time [min]": 0, #es sumatoria hatsa el final
          "total_tournaments": 0,
          "scored_in_wins": 0,
          "scored_in_losses": 0,
          "scored_in_draws": 0,
          "last_goal": None}
    return an

def new_goles_torneo_anotador(anotador):
    an = {"scorer": anotador,
          "goles": None,
          "torneos": None}
    an["goles"] = lt.newList("ARRAY_LIST")
    an["torneos"] = lt.newList("ARRAY_LIST")
    return an

def new_gol_anotador(gol, partido):
    gl = {"date": gol["date"],
          "tournament": partido["tournament"],
          "home_team": gol["home_team"],
          "away_team": gol["away_team"],
          "home_score": partido["home_score"],
          "away_score": partido["away_score"],
          "minute": gol["minute"],
          "penalty": gol["penalty"],
          "own_goal": gol["own_goal"]}
    return gl

#================================================== REQUERIMIENTOS ========================================================

# REQUERIMIENTO 1
def listar_partido_pais(historial_FIFA, n, pais, condicion ):
    """
    Función que soluciona el requerimiento 1
    """
    paises = historial_FIFA["paises"]
    pospais = lt.isPresent(paises, pais)
    pais = lt.getElement(paises, pospais)
    
    #Se verifica la condicón que entra por parámetro
    
    if condicion.lower() == "local":
        partidos = sa.sort(pais["local"], cmp_fecha)
        sz = lt.size(partidos)
    
    elif condicion.lower() == "visitante":
        partidos = sa.sort(pais["visitante"], cmp_fecha)
        sz = lt.size(partidos)
    
    elif condicion.lower() == "indiferente":
        partidos = sa.sort(pais["indiferente"], cmp_fecha)
        sz = lt.size(partidos)  
        
    if n < sz:      
        n_list = lt.subList(partidos, 1, n) 
    else:
        n_list = partidos
        
    return n_list, sz

def req_2(historial_FIFA, player , goals):
    """
    Función que soluciona el requerimiento 2
    """
    goalscorers= historial_FIFA["goalscorers"]

    player_goals= lt.newList('ARRAY_LIST')
    for gol in lt.iterator(goalscorers) :

        if gol["scorer"] == player:
            lt.addLast(player_goals, gol)
    total_goals= lt.size(player_goals)  
    if total_goals > goals:
        player_goals = lt.subList(player_goals, goals)
 
    player_goals= sa.sort(player_goals,cmp_fecha_minuto)

    return player_goals , total_goals , player

#REQUERIMIENTO 3 
def req_3(historial_FIFA, team_name , start_date , end_date):
    """
    Función que soluciona el requerimiento 3
    Consultar los partidos que disputó un equipo durante un periodo especifico
    
    """
    equipos= historial_FIFA["paises"]
    goalscorers= historial_FIFA["goalscorers"]
    list_team= lt.newList('ARRAY_LIST')
    total_local= 0
    total_visitante= 0
    for equipo in lt.iterator(equipos) :

        if  equipo["team"]== team_name :
        
            for partido in lt.iterator(equipo["local"]):

                if partido["date"]<= end_date and partido["date"]>= start_date:
                    sub_list= {"date": partido["date"], 
                               "home_team": partido["home_team"],
                               "away_team": partido["away_team"],  
                               "home_score": partido["home_score"], 
                               "away_score": partido["away_score"], 
                               "country": partido["country"],  
                               "city": partido["city"], 
                               "tournament": partido["tournament"] , 
                               "own_goal":None,  "penalty": None}
                    lt.addLast(list_team,sub_list)
                   
                    total_local +=1
                    
            sub_list= lt.newList('ARRAY_LIST')
            for partidos in lt.iterator(equipo["visitante"]):
                if partidos["date"]<= end_date and partidos["date"]>= start_date:
                    sub_list= {"date": partidos["date"], 
                               "home_team": partidos["home_team"],
                               "away_team": partidos["away_team"],  
                               "home_score": partidos["home_score"], 
                               "away_score": partidos["away_score"], 
                               "country": partidos["country"],  
                               "city": partidos["city"], 
                               "tournament": partidos["tournament"] ,  
                               "own_goal":None,  
                               "penalty": None}
                    
                    lt.addLast(list_team,sub_list)
    
                    total_visitante +=1
              

    own_goal = lt.newList("ARRAY_LIST")
    penalty= lt.newList("ARRAY_LIST")

    for partido in lt.iterator(list_team):
        day_match= partido["date"]
        home_team = partido["home_team"]
    
        for gol in lt.iterator(goalscorers):

            if gol["date"] == day_match and gol["home_team"] == home_team:
                own_goal=gol["own_goal"]
                penalty=gol["penalty"]
                if own_goal =="": 
                    partido["own_goal"]= "Unknown"

                else:

                    partido["own_goal"]= own_goal
                if penalty == "": 
                    partido["penalty"]= "Unknown"

                else:
                    partido["penalty"]= penalty
    total_partidos= lt.size(list_team)

    list_team= sa.sort(list_team , cmp_fecha)


    return list_team , total_partidos , total_local , total_visitante


                    
        

#REQUERIMIENTO 4
def get_torneo(historial_FIFA, nombre_torneo, fecha_inicio, fecha_fin):
    """
    Función que soluciona el requerimiento 4
    """
    torneos = historial_FIFA["torneos"]    
    #Hacer busqueda binaria
    postorneo = busqueda_binaria(torneos, nombre_torneo,"name")
    if postorneo < 1:
        postorneo = lt.isPresent(torneos, nombre_torneo)
    torneo = lt.getElement(torneos, postorneo)
    partidos_torneo = lt.newList('ARRAY_LIST', cmpfunction=comparetorneos)
    paises = lt.newList("ARRAY_LIST")
    ciudades = lt.newList("ARRAY_LIST")
    partidos = torneo["partidos"]
    num_penales = 0
    
    for partido in lt.iterator(partidos):
        if partido["date"] >= fecha_inicio and partido["date"] <= fecha_fin:
            lt.addLast(partidos_torneo, partido)
            pais = partido["country"]
            pospais = lt.isPresent(paises, pais)
            if pospais < 1:
                lt.addLast(paises, pais)
            ciudad = partido["city"]
            posciudad = lt.isPresent(ciudades, ciudad)
            if posciudad < 1:
                lt.addLast(ciudades, ciudad)
            if partido["winner"] != "Unknown":
                num_penales += 1
                  
            
    partidos_torneo = sa.sort(partidos_torneo, cmp_fecha_pais_ciudad)
        
    cd = lt.size(ciudades)
    ps = lt.size(paises)
    
    return partidos_torneo, cd, ps, num_penales

#Requerimiento 5
def anotaciones_jugador(historial_FIFA, nombre, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 5
    """  
    lst_goals= historial_FIFA["goalscorers"]
    jugador= lt.newList("ARRAY_LIST", comparepenales_o_partidos)
    #lista de todos los goles del jugador
    for dic in lt.iterator(lst_goals):
        if dic["scorer"] == nombre and dic["date"] <= fecha_f and dic["date"] >= fecha_i: 
            lt.addLast(jugador, dic)
            
    #lista de los goles del jugador en el periodo determinado
    lst_results= historial_FIFA["results"]
    listado= lt.newList("ARRAY_LIST")
    #lista para numero de torneos
    lst_torn= []
    for goal in lt.iterator(jugador):
        pos= lt.isPresent(lst_results, goal)
        partido= lt.getElement(lst_results,pos)
        torn= partido["tournament"]
        if torn not in lst_torn:
            lst_torn.append(torn)
        player= new_jugador(goal, partido)
        lt.addLast(listado, player)
                         
    num_penal= 0
    num_auto= 0
    for player in lt.iterator(jugador):
        if player["penalty"]== "True":
            num_penal += 1
        if player["own_goal"]== "True":
            num_auto += 1
            
    num_torn= len(lst_torn)
    num_anot= lt.size(jugador)
    sa.sort(listado, cmp_fecha_minuto_req5)
    
    return num_anot, num_torn, num_penal, num_auto, listado

#opcion de verificación
def contar_equipos(historial_FIFA,fecha_i, fecha_f, torneo):
    equipos = lt.newList("ARRAY_LIST")
    partidos = historial_FIFA["results"]
    for partido in lt.iterator(partidos):
        if partido["date"] >= fecha_i and partido["date"] <= fecha_f and partido["tournament"] == torneo:
            pos1 = lt.isPresent(equipos, partido["home_team"])
            if pos1 < 1:
                lt.addLast(equipos, partido["home_team"])
            pos2 = lt.isPresent(equipos, partido["away_team"])
            if pos2 < 1:
                lt.addLast(equipos, partido["away_team"])
    return lt.size(equipos)

def req_6(historial_FIFA, torneo, n, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 6
    """
    torneos = historial_FIFA["torneos"]
    pos_torneo = busqueda_binaria(torneos, torneo,"name")
    if pos_torneo < 0:
        lt.isPresent(torneos, torneo)
    torneo = lt.getElement(torneos, pos_torneo)
    partidos_torneo = torneo["partidos"]
    
    #Lista en la que se pondrán los partidos que están en el rango de fechas
    partidos_en_periodo = lt.newList("ARRAY_LIST")
    
    #Listas auxiliares para contar cosas
    ciudades = lt.newList("ARRAY_LIST", cmpfunction=compareciudades)
    paises = lt.newList("ARRAY_LIST")
    #Lista de equipos, cada lista tiene dentro una lista de sus jugadores que han anotado gol.
    equipo_jugador = lt.newList("ARRAY_LIST", cmpfunction=compare_equipos) 
    
    
    #Lista que quedará con toda la información final necesaria para ser impresa.
    equipos_lista = lt.newList("ARRAY_LIST", cmpfunction=compare_equipos)
    
    #Se fitran los partidos segun la fecha
    
    for partido in lt.iterator(partidos_torneo):
        
        if partido["date"] >= fecha_i and partido["date"] <= fecha_f:
            lt.addLast(partidos_en_periodo, partido)
            
            #Agrega la ciudad a la lista de ciudades
            ciudad = partido["city"]
            posciudad = lt.isPresent(ciudades, ciudad)
            if posciudad > 0:
                ciudad = lt.getElement(ciudades, posciudad)
                ciudad["num_encuentros"] += 1
            else:
                ciudad = new_ciudad(ciudad)
                lt.addLast(ciudades, ciudad)
            
            #Agrega el pais a la lista de paises.
            pais = partido["country"]
            pospais = lt.isPresent(paises, pais)
            if pospais > 0:
                pais = lt.getElement(paises, pospais)
            else:
                lt.addLast(paises, pais)
            
            #Se trabaja ahora con cada uno de los equípos actualiando o creando sus estadisticas.
            equipos = partido["home_team"], partido["away_team"]
            
            for equipo in equipos:
                estadistica_equipo(historial_FIFA, equipos_lista, partido, equipo, equipo_jugador)
                
    #Se mira el total de ciudades y se encuentra la ciudad donde se realizaaron más partidos
    num_ciudades = lt.size(ciudades)
    sa.sort(ciudades, cmp_ciudades_num_encuentros)
    if lt.size(ciudades) > 0:      
        cm = lt.lastElement(ciudades)
        ciudad_mayor = cm["name"]
    else:
        ciudad_mayor = "Unknown" 
    
    #Se mira el numero de pises
    num_paises = lt.size(paises)
            
    #Se ven el total de encuentros disputados en el periodo y de equipos.
    num_encuentros = lt.size(partidos_en_periodo)
    num_equipos = lt.size(equipos_lista)
    
    #Se ordena la lista para por el criterio solicitado en el rquerimiento
    equipos_lista_o = sa.sort(equipos_lista, cmp_estadisticas)

    #Se extraen los n mejores si la lista tiene más de n elementos
    if n < num_equipos:
        equipos_n = lt.subList(equipos_lista_o, 1, n)
    else:
        equipos_n = equipos_lista
        
    for equipo in lt.iterator(equipos_lista):
        equipo_n = equipo["team"]
        posequipo = lt.isPresent(equipo_jugador, equipo_n)
        if posequipo > 0:
            equipo_j = lt.getElement(equipo_jugador, posequipo)
            jugadores = equipo_j["goleadores"]
            jugadores = sa.sort(jugadores, cmp_num_goles_avg)
            mejor = lt.firstElement(jugadores)
            mejor["avg_time [min]"] = mejor["avg_time [min]"] / mejor["goals"]
            equipo["top_scorer"] = tabulate([[mejor["scorer"], mejor["goals"], mejor["matches"], mejor["avg_time [min]"]]], headers=["scorer", "goals", "matches", "avg_time [min]"], tablefmt="grid", showindex=False, maxcolwidths=[10, None, None, None])
        else:
            equipo["top_scorer"] = "Unknown"
    
    
    return num_equipos, num_encuentros, num_paises, num_ciudades, ciudad_mayor, equipos_n #6 elementos en la tupla.

#FUNCION AUXILIAR PARA EL REQUERIMIENTO 6 
def estadistica_equipo(historial_FIFA, equipos_lista, partido, equipo, equipo_jugador):
    
    #PRIMERA PARTE
    posequipo = lt.isPresent(equipos_lista, equipo)
    if posequipo > 0:
        equipo_e = lt.getElement(equipos_lista, posequipo)
    else:
        equipo_e = new_equipo(equipo)
        lt.addLast(equipos_lista, equipo_e)
    
    #Se agrega un partido a al total de disputados.
    equipo_e["matches"] += 1
    
    #Para saber los puntos de penla
    hay_penal = False
    
    #Se verifica si hay penal, más adelante se verá a quien corresponde los puntos de penales.
    pospenal = lt.isPresent(historial_FIFA["shootouts"], partido)
    if pospenal > 0:
        penal = lt.getElement(historial_FIFA["shootouts"], pospenal)
        hay_penal = True
        
    if hay_penal and equipo_e["team"] == penal["winner"]:
        equipo_e["wins"] += 1
        #equipo["total_point"] += 3
        #equipo_e["penalty_points"] += 1
    elif hay_penal and equipo_e["team"]  != penal["winner"]:
        equipo_e["losses"] += 1
        
    elif not hay_penal:
        if partido["home_score"] == partido["away_score"]:
            equipo_e["total_points"] += 1
            equipo_e["draws"] += 1
    # se verifica cual de los dos equipos es, para poder sumar los goles, esto se tien que hacer haya no haya habido penal
    if equipo_e["team"] == partido["home_team"]:
        equipo_e["goals_for"] += int(partido["home_score"])
        equipo_e["goals_against"] += int(partido["away_score"])
        
        if not hay_penal: #si hubo penal se recorrerian estas lineas inecesariamente pues claramnete los puntos muestran empate
            if partido["home_score"] > partido["away_score"]:
                equipo_e["total_points"] += 3
                equipo_e["wins"] += 1
                            
            elif partido["away_score"] > partido["home_score"]:
                equipo_e["losses"] += 1
                
    elif equipo_e["team"] == partido["away_team"]:
        equipo_e["goals_for"] += int(partido["away_score"])
        equipo_e["goals_against"] += int(partido["home_score"])
        
        if not hay_penal:
            if partido["away_score"] > partido["home_score"]:
                equipo_e["wins"] += 1
                equipo_e["total_points"] += 3
            elif partido["home_score"] > partido["away_score"]:
                equipo_e["losses"] += 1
    
    equipo_e["goal_difference"] = int(equipo_e["goals_for"])-int(equipo_e["goals_against"])
    # filtrar los goles que corresponden a ese partido.
    goles_equipo_partido = lt.newList("ARRAY_LIST")
    equipo_goleadores = historial_FIFA["equipos_goles"]
    posequipo = lt.isPresent(equipo_goleadores, equipo)
    
    #De aquí en adelante todo se trabaja dentro del if, si no hay goleadores en ese equipo no vale la pena seguir trabajando
    if posequipo > 0:
        #Se extrae la lista de goleadores de ese equipo
        goles_eq = lt.getElement(equipo_goleadores, posequipo)
        goles = goles_eq["goles"]
        for gol in lt.iterator(goles):
            #Se filtran solo los que son del partido especifico del torneo.
            if gol["date"] == partido["date"] and gol["home_team"] == partido["home_team"]:
                lt.addLast(goles_equipo_partido, gol)
                
        #Para cada gol especifico del partido del torneo se anotan las estadisticas del goleador.       
        for gol in lt.iterator(goles_equipo_partido):
            #Se extrae la lista de goleadores (que ya tienen sus estadisticas) del equipo 
            posequipo_g = lt.isPresent(equipo_jugador, equipo)
            if posequipo_g > 0:
                equipo_g = lt.getElement(equipo_jugador, posequipo_g)
            else:
                equipo_g = new_equipo_goleadores(equipo)
                lt.addLast(equipo_jugador, equipo_g) 
                
            goleadores =  equipo_g["goleadores"]
            #Se trabaja con el goleador    
            scorer = gol["scorer"]
            #Se verifica si el goleador ya está, si no se crea
            pos_scorer = lt.isPresent(goleadores, scorer)
            if pos_scorer > 0:
                scorer = lt.getElement(goleadores, pos_scorer)
            else:
                scorer = new_goleador(scorer)
                lt.addLast(goleadores, scorer)      
            #Se actualizan su estadistias
            if gol["minute"] != "":    
                scorer["avg_time [min]"] += float(gol["minute"])
            scorer["matches"] += 1
            scorer["goals"] += 1
            
            if gol["own_goal"] == "True":
                equipo_e["own_goal_points"] += 1
            
            if gol["penalty"] == "True":
                equipo_e["penalty_points"] += 1        
    # "equipo_e/g  y scorer" es un diccionario y los diccionarios son mutables, por eso no hay return en esta función, no es necesario
            

def n_mejores_anotadores(historial_FIFA, n, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 7
    """
    #Listas auxiliares
    goleadores = lt.newList("ARRAY_LIST", cmpfunction=comparescorers)
    goles_torneos_goleador = lt.newList("ARRAY_LIST", cmpfunction=comparescorers)
    
    #Listas de la estructura que se utilizarán
    partidos_oficiales = historial_FIFA["partidos_oficiales"]
    goles = historial_FIFA["goalscorers"]
    
    #Listas auxiliares para contar
    torneos_periodo = lt.newList("ARRAY_LIST")
    #torneos_total = lt.newList("ARRAY_LIST")
    encuentros = lt.newList("ARRAY_LIST", cmpfunction=comparepenales_o_partidos)
    total_goles = 0
    total_penales = 0
    total_autogoles = 0
    
    for gol in lt.iterator(goles):
        if gol["date"] >= fecha_i and gol["date"] <= fecha_f:
            total_goles += 1
            pospartido_o = lt.isPresent(partidos_oficiales, gol)
            if pospartido_o > 0: #Si no pasa, es que el gol no fue de partido oficila y lo ignoramos. Desde ahora todo es dentro de este if.
                partido = lt.getElement(partidos_oficiales, pospartido_o) #Este es el partido en el que se anptó el gol.
                
                #Se verifica si el encuentro ya fué contavilizado con la lista auxiliar
                pospartido_n = lt.isPresent(encuentros, partido)
                if pospartido_n < 1:
                    lt.addLast(encuentros, partido)
                #Se crea el goleador en ambas litas.
                goleador = gol["scorer"]
                posgoleador_d = lt.isPresent(goleadores, goleador)
                if posgoleador_d > 0:
                    goleador_d = lt.getElement(goleadores, posgoleador_d)
                else:
                    goleador_d = new_anotador(goleador)
                    lt.addLast(goleadores, goleador_d)     
                posgoleador_gt = lt.isPresent(goles_torneos_goleador, goleador)
                if posgoleador_gt > 0:
                    goleador_gt = lt.getElement(goles_torneos_goleador, posgoleador_gt)
                else:
                    goleador_gt = new_goles_torneo_anotador(goleador)
                    lt.addLast(goles_torneos_goleador, goleador_gt)   
                #Se trabajan con las listas actualisando las estadisticas.
                if gol["penalty"] == "True":
                    goleador_d["penalty_goals"] += 1
                    total_penales += 1
                if gol["own_goal"] == "True": 
                    goleador_d["own_goals"] += 1
                    total_autogoles += 1   
                if gol["minute"] != '':
                    goleador_d["avg_time [min]"] += float(gol["minute"])
                torneo = partido["tournament"]
                #Se verifica si el torneo está contavilizado en la lista de todos los torneos de todos los jugadores
                postorneo_g = lt.isPresent(torneos_periodo, torneo)
                if postorneo_g < 1:
                    lt.addLast(torneos_periodo, torneo)
                #se verifica si el torneo se ha contavilisado en las estadisticas del goleador
                postorneo_d = lt.isPresent(goleador_gt["torneos"], torneo)
                if postorneo_d < 1: 
                    lt.addLast(goleador_gt["torneos"], torneo)
                    goleador_d["total_tournaments"] += 1
                
                hay_penal = False  
                pospenal = lt.isPresent(historial_FIFA["shootouts"], partido)
                if pospenal > 0:
                    penal = lt.getElement(historial_FIFA["shootouts"], pospenal)
                    hay_penal = True
                
                if hay_penal and gol["team"] == penal["winner"]:
                    goleador_d["scored_in_wins"] += 1
                    
                elif hay_penal and gol["team"] != penal["winner"]:
                    goleador_d["scored_in_losses"] += 1
                    
                elif not hay_penal:
                    if gol["team"] == partido["home_team"]:
                        if partido["home_score"] > partido["away_score"]:
                            goleador_d["scored_in_wins"] += 1
                        elif partido["home_score"] < partido["away_score"]:
                            goleador_d["scored_in_losses"] += 1
                        else:
                            goleador_d["scored_in_draws"] += 1
                    elif gol["team"] == partido["away_team"]:
                        if partido["away_score"] > partido["home_score"]:
                            goleador_d["scored_in_wins"] += 1
                        elif partido["away_score"] < partido["home_score"]:
                            goleador_d["scored_in_losses"] += 1
                        else:
                            goleador_d["scored_in_draws"] += 1
                            
                gol = new_gol_anotador(gol,partido)
                lt.addLast(goleador_gt["goles"], gol)
                
    for goleador in lt.iterator(goleadores):
        goleador["total_goals"] = goleador["scored_in_wins"] + goleador["scored_in_draws"] + goleador["scored_in_losses"]
        goleador["total_points"] = goleador["total_goals"] + goleador["penalty_goals"] - goleador["own_goals"]
        goleador["avg_time [min]"] = goleador["avg_time [min]"] / goleador["total_goals"]
        if goleador["avg_time [min]"] == 0:
            goleador["avg_time [min]"] = "Unknown"
        
        #Para determinar su ultimo gol
        scr = goleador["scorer"]
        posgoleador = lt.isPresent(goles_torneos_goleador, scr)
        goleador_gt = lt.getElement(goles_torneos_goleador, posgoleador)
        goles = goleador_gt["goles"]
        goles = quk.sort(goles, cmp_fecha)
        ultimo_gol = lt.firstElement(goles)
        goleador["last_goal"] = tabulate([[ultimo_gol["date"], ultimo_gol["tournament"], ultimo_gol["home_team"], ultimo_gol["away_team"], ultimo_gol["home_score"], ultimo_gol["away_score"], ultimo_gol["minute"], str(ultimo_gol["penalty"]), str(ultimo_gol["own_goal"]) ]], headers=["date", "tournament", "home_team", "away_team", "home_score", "away_score", "minute", "penalty", "own_goal"], tablefmt = "grid", showindex=False, maxcolwidths=[None, 12, None, None, None, None, None, None,None])
        
    goleadores = quk.sort(goleadores, cmp_puntos_goles_penales)
    if int(n) < lt.size(goleadores):
        listado = lt.subList(goleadores, 1, int(n))
    else: 
        listado = goleadores
    #se sacan los totales
    t_anotadores = lt.size(goleadores)
    t_torneos = lt.size(torneos_periodo)
    t_partidos = lt.size(encuentros)
        
    return t_anotadores, t_partidos, t_torneos, total_goles, total_penales, total_autogoles, listado
    

#----------------------------------FUNCIONES DE COMPARACIÓN CMP PARA BUSQUEDA-----------------------------------

def comparetorneos(torneo1, torneo):
    """
    Función encargada de comparar dos datos
    """
    if torneo1.lower() == torneo["name"].lower():
        return 0
    elif torneo1.lower() > torneo["name"].lower():
        return 1
    return -1

def compare_equipos(pais1, pais):
    if pais1.lower() == pais["team"].lower():
        return 0
    elif pais1.lower() > pais["team"].lower():
        return 1
    return -1
"""
def comparepaises(pais1, pais):
    if pais1.lower() == pais["name"].lower():
        return 0
    elif pais1.lower() > pais["name"].lower():
        return 1
    return -1
"""

def comparepenales_o_partidos(partido1, partido2):
    #Para buscar un partido en la lista de penales no basta con la fecha, dos partidos pueden haberse disputado con la misma fecha
    #Por lo tanto no existe un unico "identificador propio" de un partido sino que son tanto la fecha como el equipo local (un equipo no guega dos veces el mismo día)
    #Por eso esta cmp es diferente.
    if partido1["date"].lower() == partido2["date"].lower():
        if partido1["home_team"].lower() == partido2["home_team"].lower():
            return 0
        if partido1["home_team"].lower() > partido2["home_team"].lower():
            return 1
        else: 
            return -1
    elif partido1["date"].lower() > partido2["date"].lower():
        return 1
    else:
        return -1
    
def comparegoles(partido1, partido2):
    # El criterio de busqueda es compuesto bajo razonamiento analogo al del criterio de busqueda de los penales.
    if partido1["date"].lower() == partido2["date"].lower():
        if partido1["team"].lower() == partido2["team"].lower():
            return 0
        if partido1["team"].lower() > partido2["team"].lower():
            return 1
        else: 
            return -1
        return 0
    elif partido1["date"].lower() > partido2["date"].lower():
        return 1
    else:
        return -1
    
def compareciudades(ciudad, ciudad1):
    if ciudad.lower() == ciudad1["name"].lower():
        return 0
    elif ciudad.lower() > ciudad1["name"].lower():
        return 1
    else:
        return -1
def comparescorers(scr, scr1):
    if scr.lower() == scr1["scorer"].lower():
        return 0
    elif scr.lower() > scr1["scorer"].lower():
        return 1
    else:
        return -1     

#-------------------------------------------FUNCIONES DE DE COMPARACIÓN PARA ORDENAR--------------------------------------

def cmp_goles_por_fecha_minuto_jugador(gol1, gol2):
    #Criterio compuesto de ordenamiento de goles solicitado para la impresión de la carga de datos
    if gol1["date"] == gol2["date"]:
        if gol1["minute"] == gol2["minute"]:
            if gol1["scorer"] < gol2["scorer"]:
                return True
            else:
                return False
        elif gol1["minute"] < gol2["minute"]:
            return True
        else:
            return False
                
    elif gol1["date"] > gol2["date"]:
        return True
    else:
        return False
    
def cmp_partidos_by_fecha_y_pais(resultado1, resultado2):
    if resultado1["date"] < resultado2["date"]:
        return True
    elif resultado1["date"]>resultado2["date"]:
        return False
    else:
        if resultado1["country"] == resultado2["country"]:

            return False 
        else:
            return True
    

def cmp_penales_por_fecha_equipo(penal1, penal2):
    if penal1["date"] == penal2["date"]:
        if penal1["home_team"] == penal2["home_team"]:
            if penal1["away_team"] < penal2["away_team"]:
                return True
            else:
                return False
        elif penal1["home_team"] < penal2["home_team"]:
            return True
        else:
            return False
    elif penal1["date"] > penal2["date"]:
        return True
    else: 
        return False
    
def cmp_partidos_por_fecha_puntaje(rs1,rs2):
    if rs1["date"] == rs2["date"]:
        if rs1["home_score"] == rs2["home_score"]:
            if rs1["away_score"] < rs2["away_score"]:
                return True
            else:
                return False
        elif rs1["home_score"] < rs2["home_score"]:
            return True
        else:
            return False
    elif rs1["date"]> rs2["date"]:
        return True
    else:
        return False
        
def cmp_fecha_pais_ciudad(rs1, rs2):
    if rs1["date"] == rs2["date"]:
        if rs1["country"] == rs2["country"]:
            if rs1["city"] < rs2["city"]:
                return True
            else:
                return False
        elif rs1["country"] < rs2["country"]:
            return True
        else:
            return False
    elif rs1["date"]> rs2["date"]:
        return True
    else:
        return False
    
def cmp_fecha(rs1,rs2):
    if rs1["date"] > rs2["date"]:
        return True
    else:
        return False

def cmp_fecha_minuto(gl1, gl2):
    if gl1["date"] == gl2["date"]:
        if gl1["minute"] < gl2["minute"]:
            return True
        else:
            return False
    elif gl1["date"] < gl2["date"]:
        return True
    else:
        return False
    
def cmp_fecha_minuto_req5(gl1, gl2):
    if gl1["date"] == gl2["date"]:
        if gl1["minute"] < gl2["minute"]:
            return True
        else:
            return False
    elif gl1["date"] > gl2["date"]:
        return True
    else:
        return False
    
def cmp_torneos_alfabetico(tr1, tr2):
    if tr1["name"] < tr2["name"]:
        return True
    else:
        return False
    
def cmp_ciudades_num_encuentros(cd1, cd2):
    if cd1["num_encuentros"] < cd2["num_encuentros"]:
        return True
    else:
        return False

def cmp_estadisticas(eq1, eq2):
    if eq1["total_points"] == eq2["total_points"]:
        if eq1["goal_difference"] == eq2["goal_difference"]:
            if eq1["penalty_points"] == eq2["penalty_points"]:
                #por menor...
                if eq1["matches"] == eq2["matches"]:
                    if eq1["own_goal_points"] < eq2["own_goal_points"]:
                        return True
                    else:
                        return False
                elif eq1["matches"] < eq2["matches"]:
                    return True
                else:
                    return False
            elif eq1["penalty_points"] > eq2["penalty_points"]:
                return True
            else:
                return False
        elif eq1["goal_difference"] > eq2["goal_difference"]:
            return True
        else:
            return False
    elif eq1["total_points"] > eq2["total_points"]:
        return True
    else:
        return False
        
def cmp_num_goles_avg(g1, g2):
    if g1["goals"] == g2["goals"]:
        if g1["avg_time [min]"] < g2["avg_time [min]"]:
            return True
        else:
            return False
    elif g1["goals"] > g2["goals"]:
        return True
    else:
        return False
    
def cmp_puntos_goles_penales(sr1, sr2):
    if sr1["total_points"] == sr2["total_points"]:
        if sr1["total_goals"] == sr2["total_goals"]:
            if sr1["penalty_goals"] == sr2["penalty_goals"]:
                if sr1["avg_time [min]"] == "Unknown":
                    return True
                elif sr2["avg_time [min]"] == "Unknown":
                    return False
                elif sr1["avg_time [min]"] < sr2["avg_time [min]"]:
                    return True
                else: return False 
            elif sr1["penalty_goals"] > sr2["penalty_goals"]:
                return True
            else:
                return False
        elif sr1["total_goals"] > sr2["total_goals"]:
            return True
        else:
            return False
    elif sr1["total_points"] > sr2["total_points"]:
        return True
    else:
        return False
# ------------------------------------------- FUNCIONES DE ORDENAMIENTO ------------------------------------------

def ordenar_goles(historial_FIFA):
    historial_FIFA["goalscorers"] = sa.sort(historial_FIFA["goalscorers"], sort_crit=cmp_goles_por_fecha_minuto_jugador)
    return historial_FIFA

def ordenar_penales(historial_FIFA):
    historial_FIFA["shootouts"] = sa.sort(historial_FIFA["shootouts"], sort_crit=cmp_penales_por_fecha_equipo)
    return historial_FIFA

def ordenar_partidos(historial_FIFA):
    historial_FIFA["results"] = sa.sort(historial_FIFA["results"], sort_crit=cmp_partidos_por_fecha_puntaje)
    return historial_FIFA

def ordenar_torneos(historial_FIFA):
    historial_FIFA["torneos"] = sa.sort(historial_FIFA["torneos"], sort_crit=cmp_torneos_alfabetico)
    return historial_FIFA

#---------------------------- Funciones de ordenamiento lab 4-5 (opción 10 menú) ----------------------------------------

def ordenamiento_shell(historial_FIFA):
 
   historial_FIFA["results"] = sa.sort(historial_FIFA["results"], sort_crit= cmp_partidos_by_fecha_y_pais)
   historial_FIFA["results"] = sa.sort(historial_FIFA["results"], sort_crit= cmp_partidos_by_fecha_y_pais)
   
   return historial_FIFA 

def ordenamiento_insertion(historial_FIFA):
    historial_FIFA["results"]= ins.sort(historial_FIFA["results"], sort_crit= cmp_partidos_by_fecha_y_pais)
    return historial_FIFA 


def ordenamiento_selection(historial_FIFA):
    historial_FIFA["results"]= se.sort(historial_FIFA["results"], sort_crit= cmp_partidos_by_fecha_y_pais)
    return historial_FIFA 


def ordenamiento_quick(historial_FIFA):
    historial_FIFA["results"] = quk.sort(historial_FIFA["results"], cmp_partidos_by_fecha_y_pais)
    return historial_FIFA


def ordenamiento_merg(historial_FIFA):
    historial_FIFA["results"] = merg.sort(historial_FIFA["results"], cmp_partidos_by_fecha_y_pais)
    return historial_FIFA    
    
#------------------------------BUSQUEDA BINARIA-------------------------------------

def busqueda_binaria(lista, elemento, key):
    """
    Busqueda binaria para cualquier lista con cualquier llave con la que se busca el elemento

    Args:
        lista: dnde se realizará la busqueda binaria (debe estar ordenada de MENOR a MAYOR según la llave de busqueda "key")
        elemento: Que se quiere buscar en la lista
        key: Llave que es el identificador con el que se busca un elemento en la lista para comparar.

    Returns:
        pos: la posición del elemento 
    """
    f = lt.size(lista)
    i = 0
    pos = 0
    encontro = False
    while i <= f and not encontro:
        m = (i+f)//2 
        elem = lt.getElement(lista, m)
        if elem[key].lower() == elemento.lower():
            pos = m
            encontro = True
        elif elemento.lower() < elem[key].lower():
            f = m-1
        else:
            i = m+1
    return pos