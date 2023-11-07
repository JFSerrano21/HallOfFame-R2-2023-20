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
from tabulate import tabulate
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_historial_FIFA(type_scorers, loadfactor_scorers):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de 
    
    
    historial_FIFA={"results":None,
                    "goalscorers":None,
                    "shootouts":None,
                    'scorers': None,
                    "torneos": None,
                    "anios": None,
                    "equipos_bono": None, 
                    "paises_req1": None}
    
    # TRES PRIMERAS EXTRUCTURAS EXCLUSIVAS PARA IMPRIMIR DATOS LUEGO DE LA CARGA DE DATOS (No se trabaja con ellas en el resto del reto)
    historial_FIFA["results"] = lt.newList(datastructure="ARRAY_LIST")
    historial_FIFA["goalscorers"] = lt.newList(datastructure="ARRAY_LIST")
    historial_FIFA["shootouts"] = lt.newList(datastructure="ARRAY_LIST")
    historial_FIFA['scorers'] = mp.newMap(1009, maptype=type_scorers, loadfactor=loadfactor_scorers)
    historial_FIFA['torneos_req4'] = mp.newMap(149, maptype="CHAINING", loadfactor=0.5)
    historial_FIFA["torneos_req7"] = mp.newMap(149, maptype="CHAINING", loadfactor=0.5)
    historial_FIFA["shootouts_map"]=mp.newMap(1129, maptype="CHAINING", loadfactor=0.5)
    historial_FIFA["results_map"] = mp.newMap(89533)
    historial_FIFA["goalscorers_map"] = mp.newMap(82237)
    historial_FIFA["anios"]= mp.newMap(maptype="CHAINING")
    historial_FIFA["paises_req1"] = mp.newMap()
    historial_FIFA["equipos_bono"] = mp.newMap()

    
    return historial_FIFA
    

# Funciones para agregar informacion al modelo

def add_result(historial_FIFA, result):
    """
    Función para agregar nuevos elementos al mapa
    """
    rs = new_result(result["date"], result["home_team"], result["away_team"], result["home_score"], result["away_score"],result["country"], result["city"], result["tournament"] )
    lt.addLast( historial_FIFA["results"], rs)
    key = str(rs["date"]) + str(rs["home_team"])
    mp.put(historial_FIFA["results_map"], key, rs)
    torneo = result["tournament"]
    add_torneo(historial_FIFA, torneo, result)
    
    if result["tournament"].lower() != "friendly":
        anio1 = add_equipo_bono(historial_FIFA, result["home_team"], result)
        anio2 = add_equipo_bono(historial_FIFA, result["away_team"], result)
        actulizar_estadisticas_equipo_req6_anio_bono(historial_FIFA, anio1, anio2, result)
        
    #add paises
    pais = result["home_team"]
    add_pais(historial_FIFA, pais , result)

    pais = result["away_team"]
    add_pais(historial_FIFA, pais , result)

    anio = result["date"][:4]
    anio_info = mp.get(historial_FIFA["anios"], anio)
    if anio_info:
        anio_info = me.getValue(anio_info)
    else:
        anio_info = new_anio_req6()
        mp.put(historial_FIFA["anios"], anio, anio_info)
    #----
    #-----  add equipos
    torneo_info = mp.get(anio_info["torneos"], result["tournament"])
    if torneo_info:
         torneo_info = me.getValue(torneo_info) 
    else:
        torneo_info = new_torneo_req6()
        mp.put(anio_info["torneos"], result["tournament"], torneo_info)
    torneo_info["partidos"] += 1
    eq1 = mp.get(torneo_info["equipos"], result["home_team"])
    if eq1:
        eq1 = me.getValue(eq1)
    else:
        eq1 = new_pais_req6(result["home_team"])
        mp.put(torneo_info["equipos"], result["home_team"], eq1)
        
    eq2 = mp.get(torneo_info["equipos"], result["away_team"])
    if eq2:
        eq2 = me.getValue(eq2)
    else:
        eq2 = new_pais_req6(result["away_team"])
        #Meterlo
        mp.put(torneo_info["equipos"], result["away_team"], eq2)
        
    actulizar_estadisticas_equipo_req6_anio_bono(historial_FIFA, eq1, eq2, result)
    
    paises_info= mp.get(torneo_info["paises"], result["country"])
    if paises_info:
        nuevo_valor= (me.getValue(paises_info)) + 1
        me.setValue(paises_info, nuevo_valor )
    else: 
        mp.put(torneo_info["paises"],result["country"], 1)
    ciudades_info= mp.get(torneo_info["ciudades"], result["city"])
    if ciudades_info:
        dic_ciudad= me.getValue(ciudades_info)
    else: 
        dic_ciudad= new_ciudad_req6(result["city"])
        mp.put(torneo_info["ciudades"],result["city"], dic_ciudad)
    dic_ciudad["num_partidos"] += 1
    
    return historial_FIFA




#Carga para el req 1 
def add_pais(historial_FIFA, pais, rs):
    paises = historial_FIFA["paises_req1"]
    paises_info = mp.get(paises, pais)
    if  paises_info:
        paises_info = me.getValue(paises_info)
    else:
        paises_info = new_pais(pais)
        mp.put(paises, pais, paises_info)
    
    partido_de_pais = new_partido_de_pais(rs)
    lt.addLast(paises_info["indiferente"], partido_de_pais)
    if paises_info["team"] == rs["home_team"] and rs["neutral"]== "False" :
        lt.addLast(paises_info["local"], partido_de_pais)
    elif paises_info["team"] == rs["away_team"] and rs["neutral"]== "False":
        lt.addLast(paises_info["visitante"], partido_de_pais)
    

    return historial_FIFA


#Carga para el bono
def add_equipo_bono(historial_FIFA, equipo, result):
    equipo_info = mp.get(historial_FIFA["equipos_bono"], equipo)
    if equipo_info:
        equipo_info = me.getValue(equipo_info)
    else: 
        equipo_info = new_equipo_bono(equipo)
        mp.put(historial_FIFA["equipos_bono"], equipo, equipo_info)
    #Se trabaja con el año.  
    anio = result["date"][:4]
    estadisticas = mp.get(equipo_info["estadisticas_anios"], anio)
    if estadisticas:
        estadisticas = me.getValue(estadisticas)
    else:
        estadisticas = new_estadisticas_anio(anio)
        mp.put(equipo_info["estadisticas_anios"], anio, estadisticas)
    result_bono = new_result_bono(result)
    lt.addLast(estadisticas["partidos"], result_bono)
    #if result["neutral"] == "False":
    if result["home_team"] == equipo:
        estadisticas["local"] += 1
    elif result["away_team"] == equipo:
        estadisticas["visitante"] += 1
            
    anio_info = mp.get(equipo_info["anios"], anio)
    if anio_info:
        anio_info = me.getValue(anio_info)
    else:
        anio_info = new_anio_bono(anio)
        mp.put(equipo_info["anios"], anio, anio_info)
    return anio_info

# Carga para el req 4 
def add_torneo(historial_FIFA, torneo, result):
    torneos4 = historial_FIFA["torneos_req4"]
    torneo_info = mp.get(torneos4, torneo)
    if torneo_info:
        torneo_info = me.getValue(torneo_info)
    else:
        torneo_info = new_torneo_req4(torneo)
        mp.put(torneos4, torneo, torneo_info)
    penalty = "Unknown"   
    key_penalty = str(result["date"]) + str(result["home_team"])
    penalty_info = mp.get(historial_FIFA["shootouts_map"], key_penalty)
    if penalty_info:
        penalty_info = me.getValue(penalty_info)
        if penalty_info["winner"] != "":
            penalty = penalty_info["winner"]        
    result = new_result_req4(result, penalty)
    lt.addLast(torneo_info, result)
    return historial_FIFA

def add_goal_map(historial_FIFA, goal):
    lt.addLast(historial_FIFA["goalscorers"], goal)
    scorer = goal['scorer']
    
    key = str(goal["date"]) + str(goal["home_team"])
    goal_info = mp.get(historial_FIFA["goalscorers_map"], key)
    if goal_info:
        goal_info=me.getValue(goal_info)
    else: 
        goal_info= new_goal_list()
        mp.put(historial_FIFA["goalscorers_map"], key, goal_info)
    lt.addLast(goal_info, goal)
    
def add_goal(historial_FIFA, goal):
    lt.addLast(historial_FIFA["goalscorers"], goal)
    scorer = goal['scorer']
    
    key = str(goal["date"]) + str(goal["home_team"])
    
    add_scorer_lab7(historial_FIFA, scorer, goal)
    
    result = mp.get(historial_FIFA["results_map"], key)
    result = me.getValue(result)
    
    #--- add
    torneo_info = mp.get(historial_FIFA["torneos_req7"], result["tournament"])
    if torneo_info:
        torneo_info = me.getValue(torneo_info)
    else:
        torneo_info = new_torneo_req7()
        mp.put(historial_FIFA["torneos_req7"], result["tournament"], torneo_info)
    jugadores = torneo_info["jugadores"]
    goleador = mp.get(jugadores, scorer)
    if goleador:
        goleador = me.getValue(goleador)
    else:
        goleador = new_goleador_req7(goal)
        mp.put(jugadores, goal["scorer"], goleador)
        
    actualizar_estadisticas_goleador_req7(goleador, goal, result)  
    actualizar_estadistica_torneo_req7(torneo_info, goal, key, result)  

    return historial_FIFA

def add_scorer_lab7(historial_FIFA, scorer, goal):
    scorers = historial_FIFA["scorers"]
    scorer_goals = mp.get(scorers, scorer)
    if scorer_goals:
        scorer_goals = me.getValue(scorer_goals)
    else:
        scorer_goals = new_scorer(scorer)
        mp.put(scorers, scorer, scorer_goals) 
    lt.addLast(scorer_goals, goal) 
    return historial_FIFA
    
    
def add_shootout(historial_FIFA, shootout):
    lt.addLast(historial_FIFA["shootouts"] , shootout )
    key = str(shootout["date"]) + str(shootout["home_team"])
    mp.put(historial_FIFA["shootouts_map"],key, shootout )
    return historial_FIFA

def add_data(historial_FIFA, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar ele  mentos a una lista
    pass
        

def add_anios_req6 (historial_FIFA, date): 
    años= historial_FIFA["anios_req6"]



    

#=================== Funciones para creacion de datos
def new_result(date, home_team, away_team, home_score, away_score, country, city, tournament):
    rs = {"date": date, 
          "home_team": home_team, 
          "away_team": away_team, 
          "home_score": home_score, 
          "away_score": away_score,
          "country": country, 
          "city": city, 
          "tournament":tournament}
    return rs

def new_scorer(scorer):
    scorer = lt.newList("ARRAY_LIST")
    return scorer

# Para req 1 TEMPORAL SACADA DEL RETO 1 
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

def new_torneo_req4(torneo):
    torneo = lt.newList("ARRAY_LIST")
    return torneo

def new_result_req4(result, penalty):
    result = {"date": result["date"], 
              "tournament": result["tournament"],
              "country": result["country"],
              "city": result["city"],
              "home_team": result["home_team"],
              "away_team": result["away_team"],
              "home_score": result["home_score"],
              'away_score': result['away_score'],
              "winner": penalty}
    return result

def new_torneo_req7():
    torneo = {"jugadores": None,
              "goles": 0,
              "penales": 0,
              "autogoles": 0,
              "partidos": None}
    torneo["jugadores"] = mp.newMap(37)
    torneo["partidos"] = mp.newMap()
    return torneo

def new_goal_req7(goal, torneo, result):
    goal = {"date": goal["date"],
            "tournament": torneo,
            "home_team": goal["home_team"],
            "away_team": goal["away_team"],
            "home_score": result["home_score"],
            'away_score': result['away_score'],
            "minute": goal["minute"],
            "penalty": goal["penalty"],
            'own_goal': goal["own_goal"]}
    return goal
    
def new_goleador_req7(goal):
    goleador = {"scorer": goal["scorer"],
                "total_points": 0,
                'total_goals': 0,
                "penalty_goals": 0,
                "own_goals": 0,
                "avg_time [min]": 0,
                "scored_in_wins": 0,
                "scored_in_losses": 0,
                "scored_in_draws": 0,
                "last_goal": None}
    goleador["last_goal"] = lt.newList("ARRAY_LIST")
    return goleador

def new_anio_req6():
    anio = {"torneos": None}
    anio["torneos"] = mp.newMap(1000)  
    return anio

 
  
def new_pais_req6(pais):
    mapa= mp.newMap(maptype= "CHAINING")
    
    pais= {"team": pais, 
     "total_points": 0, 
     "goal_difference": 0,
     "penalty_points": 0,
     "matches": 0,
     "own_goal_points": 0, 
     "wins": 0,
     "draws": 0,
     "losses": 0,
     "goals_for": 0, 
     "goals_against": 0,
     "top_scorer": mapa}
    
    return pais
    
def new_top_scorer_req6(goal): #valor del mapa de arriba 
    jugador= {"scorer":goal["scorer"], 
              "goals": 0,
              "matches": 0, 
              "avg_time [min]": 0}
    
    return jugador

def new_torneo_req6():
    torneo_info= {"equipos": None,
                  "partidos": 0,
                  "paises": None,
                  "ciudades": None}
    torneo_info["ciudades"] = mp.newMap(1000) #valor contador
    torneo_info["paises"] = mp.newMap(1000) 
    #llaves son equipos
    torneo_info["equipos"]=mp.newMap(numelements=3456)
    return torneo_info

def new_ciudad_req6(ciudad):
    ciudades= {"ciudad":ciudad, "num_partidos": 0}
    return ciudades

def new_jugador_req_5(jugador, partido):
    
 player ={"date": partido["date"],
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

def new_goal_list():
    goal_list=lt.newList("ARRAY_LIST")
    return goal_list

def new_equipo_bono(equipo):
    equipo_bono = {"anios": None,
                   "estadisticas_anios" :None}
    equipo_bono["anios"] = mp.newMap()
    equipo_bono["estadisticas_anios"] = mp.newMap()
    return equipo_bono
    
def new_estadisticas_anio(anio):
    estadisticas = {"anio": anio,
                    "partidos": None,
                    "local": 0,
                    "visitante": 0}
    estadisticas["partidos"] = lt.newList()
    return estadisticas

    
def new_anio_bono(anio):
    anio_info = {"year": anio,
                 "matches": 0,
                 "total_points": 0,
                 "goal_diference": 0,
                 "penalties": 0,
                 "own_goals": 0,
                 "wins": 0,
                 "draws": 0,
                 "losses": 0,
                 "goals_for": 0,
                 "goals_against": 0,
                 "top_scorer": None}
    
    anio_info["top_scorer"] = mp.newMap()
    return anio_info

def new_result_bono(result):
    result = {"date": result["date"],
              "home_team": result["home_team"],
              "away_team": result["away_team"],
              "home_score": result["home_score"],
              "away_score": result["away_score"],
              "country": result["country"],
              "city": result["city"],
              "tournament": result["tournament"]}
    return result


    
def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(historial_FIFA, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(historial_FIFA):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


#============= Funciones auxiliares =============
def actulizar_estadisticas_equipo_req6_anio_bono(historial_FIFA, eq1, eq2, result):
    #Es o eq1 o eq2 o bien anio1, anio2 lo que entra por parametro.
    eq1["goals_for"] += int((result["home_score"]))
    eq2["goals_for"] += int((result["away_score"]))
    eq1["goals_against"] += int((result["away_score"]))
    eq2["goals_against"] += int((result["home_score"]))
    if result["home_score"] > result["away_score"]:
        eq1["wins"] += 1
        eq1["total_points"]+= 3
        eq2["losses"] += 1
    if result["home_score"] < result["away_score"]:
        eq2["wins"] += 1
        eq2["total_points"]+= 3
        eq1["losses"] += 1
    elif result["home_score"] == result["away_score"]:
        eq2["total_points"] += 1
        eq1["total_points"] += 1
        eq2["draws"]+= 1
        eq1["draws"]+= 1
    key = str(result["date"]) + str(result["home_team"])
    goles = mp.get(historial_FIFA["goalscorers_map"], key)
    if goles:
        goles = me.getValue(goles)
        for gol in lt.iterator(goles):
            if gol["penalty"]== "True":
                if gol["team"]== gol["home_team"]:
                    if "penalty_points" in eq1:
                        eq1["penalty_points"]+= 1
                    else:
                        eq1["penalties"] += 1 #Esto sucede si es un anio
                else: 
                    if "penalty_points" in eq1:
                        eq2["penalty_points"] +=1
                    else:
                        eq2["penalties"] += 1
            if gol["own_goal"] == "True": 
                if gol["team"]== gol["home_team"]:
                    if "penalty_points" in eq1: #Para ver si entraron años por parametro
                        eq1["own_goal_points"]+= 1
                    else:
                        eq1["own_goals"] += 1
                else: 
                    if "penalty_points" in eq1: #Para ver si entraron años por parametro
                        eq2["own_goal_points"] +=1
                    else:
                        eq2["own_goals"] += 1
                    
    eq1["matches"]+= 1
    eq2["matches"]+= 1
    
    if goles:
        for gol in lt.iterator(goles):
            
            if gol["team"]== gol["home_team"]:
                player_info= mp.get(eq1["top_scorer"], gol["scorer"])
                if player_info:
                    player_info= me.getValue(player_info)
                else:  
                    player_info=new_top_scorer_req6(gol)
                    mp.put(eq1["top_scorer"], gol["scorer"], player_info)
                if gol["minute"] != "":
                    player_info["avg_time [min]"] += float(gol["minute"])
                player_info["goals"]+= 1
                player_info["matches"] += 1
                
            if gol["team"]== gol["away_team"]:
                player_info= mp.get(eq2["top_scorer"], gol["scorer"])
                if player_info:
                    player_info= me.getValue(player_info)
                else:  
                    player_info=new_top_scorer_req6(gol)
                    mp.put(eq2["top_scorer"], gol["scorer"], player_info)
                if gol["minute"] != "":
                    player_info["avg_time [min]"] += float(gol["minute"])
                player_info["goals"]+= 1
                player_info["matches"] += 1

def actualizar_estadisticas_goleador_req7(goleador, goal, result):
    # Se actualizan sus estadisticas
    goleador["total_points"] += 1
    goleador["total_goals"] += 1
    if str(goal["penalty"]) == "True":
        goleador["penalty_goals"] += 1
        goleador["total_points"] += 1
    if str(goal["own_goal"]) == "True":
        goleador["own_goals"] += 1
        goleador["total_points"] -= 1
    if goal["minute"] != "":
        goleador["avg_time [min]"] += float(goal["minute"])
        
    if goal["team"] == result["home_team"]:
        if result["home_score"] > result["away_score"]:
            goleador["scored_in_wins"] += 1
        elif result["home_score"] < result["away_score"]:
            goleador["scored_in_losses"] += 1
        else:
            goleador["scored_in_draws"] += 1
    else:
        if result["away_score"] > result["home_score"]:
            goleador["scored_in_wins"] += 1
        elif result["away_score"] < result["home_score"]:
            goleador["scored_in_losses"] += 1
        else:
            goleador["scored_in_draws"] += 1 
    goal = new_goal_req7(goal, result["tournament"], result) 
    lt.addLast(goleador["last_goal"], goal)
   # no tiene retorno, los diccionarios los tipos de datos y estructuras usadas son mutables.
   
def actualizar_estadistica_torneo_req7(torneo, goal, key, result):
    torneo["goles"] += 1
    if str(goal["penalty"]) == "True":
        torneo["penales"] += 1
    if str(goal["own_goal"]) == "True":
        torneo["autogoles"] += 1
    result_info = mp.get(torneo["partidos"], key)
    if not result_info:
        mp.put(torneo["partidos"], key, result)
        
    

    #No hay retorno, los diccionarios son mutables 

#Funcion aux req  3
def aux_partidos_filtrados_req3(partido_actual, penalti , autogol):

    partido_completo= {"date": partido_actual["date"],
            "home_score": partido_actual["home_score"], 
            "away_score": partido_actual["away_score"],
            "home_team": partido_actual["home_team"], 
            "away_team": partido_actual["away_team"], 
            "country": partido_actual["country"], 
            "city": partido_actual["city"], 
            "tournament": partido_actual["tournament"], 
            "penalty": penalti, 
            "own_goal":autogol}
                    

    return partido_completo    
    
 
def req_1(historial_FIFA, equipo , condicion , num_partidos):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    num_equipos_total= mp.size(historial_FIFA["paises_req1"])
    equipo_info= mp.get(historial_FIFA["paises_req1"], equipo)
    equipo_info= me.getValue(equipo_info)
    

    #CREO LAS LISTAS DONDE SE VA A GUARDAR ESO INFO
    lista_partidos_indiferente= lt.newList('ARRAY_LIST')
    lista_partidos_local= lt.newList('ARRAY_LIST')
    lista_partidos_visitante= lt.newList('ARRAY_LIST')
    
    #Saco la info de cada llave visitante, local e indiferente
    info_visitante= equipo_info["visitante"]
    lista_partidos_visitante=info_visitante

    info_local= equipo_info["local"]
    lista_partidos_local= info_local

    info_todos= equipo_info["indiferente"]
    lista_partidos_indiferente=info_todos

    num_partidos_equipo=lt.size(lista_partidos_indiferente)

    partidos_filtrados= lt.newList()

    
    if condicion.lower() == "local":

        partidos_filtrados= lista_partidos_local


    if condicion.lower() == "visitante":

        partidos_filtrados= lista_partidos_visitante

    if condicion.lower() == "indiferente":
    
        partidos_filtrados= lista_partidos_indiferente

    num_partidos_condicion= lt.size(partidos_filtrados)
    
    lista_final= sa.sort(partidos_filtrados, cmp_fecha_req7)
    
    lista_final= lt.newList()


    if num_partidos_condicion > num_partidos :
        lista_final= lt.subList(partidos_filtrados, 1 , num_partidos)

    else:
        lista_final = partidos_filtrados

    return  num_equipos_total , num_partidos_equipo , num_partidos_condicion , lista_final

def req_2(historial_FIFA, n_goles , nombre):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2

    map_jugadores= historial_FIFA["scorers"]
    n_jugadores_total= mp.size(map_jugadores)
    jugador= mp.get(map_jugadores, nombre)
    list_goles= me.getValue(jugador)
    list_anotaciones_jugador= lt.newList()
    n_anotaciones_penalty= 0
    for gol in lt.iterator(list_goles):
        if gol["penalty"] == "True":
            n_anotaciones_penalty +=1       
        lt.addLast(list_anotaciones_jugador, gol)


    list_anotaciones_jugador= sa.sort(list_anotaciones_jugador, cmp_fecha_req2)

    n_anotaciones_jugador= lt.size(list_anotaciones_jugador)
    anotaciones_jugador= lt.newList()
    if n_anotaciones_jugador > n_goles:
        
        anotaciones_jugador= lt.subList(list_anotaciones_jugador, 0, n_goles)

    else:
        anotaciones_jugador= list_anotaciones_jugador

    return n_jugadores_total , n_anotaciones_jugador, n_anotaciones_penalty , anotaciones_jugador


def req_3(historial_FIFA, equipo , f_inicial , f_final):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    num_equipos_total= mp.size(historial_FIFA["paises_req1"])
    equipo_info= mp.get(historial_FIFA["paises_req1"], equipo)
    equipo_info= me.getValue(equipo_info)
    

    #CREO LAS LISTAS DONDE SE VA A GUARDAR ESO INFO
    lista_partidos_indiferente= lt.newList('ARRAY_LIST')
    lista_partidos_local= lt.newList('ARRAY_LIST')
    lista_partidos_visitante= lt.newList('ARRAY_LIST')
    
    #Saco la info de cada llave visitante, local e indiferente
    info_visitante= equipo_info["visitante"]
    lista_partidos_visitante=info_visitante

    info_local= equipo_info["local"]
    lista_partidos_local= info_local

    info_todos= equipo_info["indiferente"]
    lista_partidos_indiferente=info_todos
    
    partidos_filtrados= lt.newList('ARRAY_LIST')
    lista_final_req3= lt.newList('ARRAY_LIST')
    
    num_partidos_local= lt.size(lista_partidos_local)
    num_partidos_visitante=lt.size(lista_partidos_visitante)
    total_partidos_equipo=lt.size(lista_partidos_indiferente)

    
    for partido in lt.iterator(lista_partidos_indiferente):

        if partido["date"]<= f_final and partido["date"]>= f_inicial:
            lt.addLast(partidos_filtrados, partido)

    partidos_filtrados = sa.sort(partidos_filtrados, cmp_fecha)


    map_jugadores= historial_FIFA["scorers"]
    listado_goles= lt.newList('ARRAY_LIST')
    keys_goles = mp.keySet(map_jugadores)

    

    for jugador in lt.iterator(keys_goles):
        actual_llave= mp.get(map_jugadores, jugador)
        actual_llave= me.getValue(actual_llave)
        for gol in lt.iterator(actual_llave): 
            lt.addLast(listado_goles, gol)


    for partido_filtrado in lt.iterator(partidos_filtrados):

        
        for partido in lt.iterator(listado_goles) :

            if partido["date"] == partido_filtrado["date"] and partido["home_team"] == partido_filtrado["home_team"]:

                penalti= partido["penalty"]
                autogol= partido["own_goal"]
                partido_completo = aux_partidos_filtrados_req3(partido_filtrado, penalti , autogol)
                
                lt.addLast(lista_final_req3 ,partido_completo)
    
            

    lista_final_req3= sa.sort(lista_final_req3, cmp_fecha_req7)

    if lt.size(lista_final_req3) > 6:
        lista_final_req3=lt.subList(lista_final_req3, 0, 6)

        
    else:
        lista_final_req3 = lista_final_req3

    
    for partido in lt.iterator(lista_final_req3):
        if partido["penalty"]=="" or partido["penalty"]=="":
            partido["penalty"]= "Unknown"

        if partido["own_goal"]=="" or partido["own_goal"]=="":
            partido["own_goal"]= "Unknown"



    return num_equipos_total , total_partidos_equipo,num_partidos_local , num_partidos_visitante  , lista_final_req3

 


def req_4(historial_FIFA, torneo, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 4
    """
    #=========== Accediendo a la información del torneo =======
    torneo_info = mp.get(historial_FIFA["torneos_req4"], torneo)
    torneo_info = me.getValue(torneo_info) #Lista de partios
    
    # Lista filtrada que se imprimirá
    partidos_en_fecha = lt.newList()
    
    #============= Para contar==========
    paises = mp.newMap(maptype="CHAINING")
    ciudades = mp.newMap(maptype="CHAINING")
    penales = 0
    
    #=========== filtrando lista  =========
    for partido in lt.iterator(torneo_info):
        if partido["date"] >= fecha_i and partido["date"] <= fecha_f:
            lt.addLast(partidos_en_fecha, partido)
            pais = partido["country"]
            pais = mp.get(paises, partido["country"])
            if not pais:
                mp.put(paises, partido["country"], "")
            ciudad = mp.get(ciudades, partido["city"])
            if not ciudad:
                mp.put(ciudades, partido["city"], "")
            if partido["winner"] != "Unknown":
                penales += 1          
    quk.sort(partidos_en_fecha, cmp_req4)
    #======== Obteniendo datos para entregar=========   
             
    total_torneos = mp.size(historial_FIFA["torneos_req4"])
    total_paises = mp.size(paises)
    total_ciudades = mp.size(ciudades)
    
    return  total_torneos, total_paises, total_ciudades, penales, partidos_en_fecha
    
    

def req_5(historial_FIFA, nombre, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 5
    """
    
    map_jugadores= historial_FIFA["scorers"]
    jugador= mp.get(map_jugadores, nombre)
    list_goles= me.getValue(jugador)
    list= lt.newList("ARRAY_LIST")
    listado= lt.newList("ARRAY_LIST")
    
    num_penal= 0
    num_auto= 0
    partidos= historial_FIFA["results"]
    torneos= []
    
    for gol in lt.iterator(list_goles):
        if gol["date"]> fecha_i and gol["date"]< fecha_f: 
            #meterlo en vez de sacarlo
            lt.addLast(list,gol)
        if gol["penalty"]== "True": 
            num_penal += 1
        if gol["own_goal"]== "True":
            num_auto += 1
        for rs in lt.iterator(partidos): 
            if rs["date"] == gol["date"] and rs["home_team"] == gol["home_team"]:
                lt.addLast(listado, new_jugador_req_5(gol, rs))
                if rs["tournament"] not in torneos: 
                    torneos.append(rs["tournament"])
                    
    num_torn= len(torneos)
    num_anot= lt.size(list)        
    t_jugadores_anot= mp.size(map_jugadores)
    sa.sort(listado, cmp_fecha_minuto_req5)

    return t_jugadores_anot, num_anot, num_torn, num_penal, num_auto, listado

def req_6(historial_FIFA, torneo, n, anio):
    """
    Función que soluciona el requrimiento 6
    """
    t_eq_torn = 0
    t_match_torneo = 0
    t_paises = 0
    t_ciudades = 0
    max_ciudad = ""
    lista_values_equipos = lt.newList()
    
    # TODO: Realizar el requerimiento 6
    map_total= historial_FIFA["anios"] 
    t_anios= mp.size(map_total)
    year_tupla= mp.get(map_total, anio)
    year= me.getValue(year_tupla)
    mapa_torneos= year["torneos"]
    t_torneos= mp.size(mapa_torneos)
    mapa_equipos_tupla= mp.get(mapa_torneos, torneo)
    if mapa_equipos_tupla:
        torneo = me.getValue(mapa_equipos_tupla)
        mapa_equipos = torneo["equipos"]
        t_match_torneo = torneo["partidos"]
        t_eq_torn= mp.size(mapa_equipos)

        t_paises= mp.size(torneo["paises"])
        t_ciudades= mp.size(torneo["ciudades"])
        list_ciudades= mp.valueSet(torneo["ciudades"])
        quk.sort(list_ciudades, cmp_ciudades)
        max_ciudad = lt.firstElement(list_ciudades)
        max_ciudad = max_ciudad["ciudad"]
        
    sub_partidos= lt.newList("ARRAY_LIST")   
    partidos = historial_FIFA["results"]
    for partido in lt.iterator(partidos):
        if partido["date"][:4] == anio:
            lt.addLast(sub_partidos, partido)
    t_match_anio= lt.size(sub_partidos)

    if mapa_equipos_tupla:
        lista_values_equipos= mp.valueSet(mapa_equipos)
        for equipo in lt.iterator(lista_values_equipos): 
            equipo["goal_difference"]= equipo["goals_for"] - equipo["goals_against"]
            if "datastructure" in equipo["top_scorer"]:
                lista_players= mp.valueSet(equipo["top_scorer"]) 
                vacio = lt.isEmpty(lista_players)
                if not vacio:
                    quk.sort(lista_players, cmp_top_scorer)
                    top_scorer= lt.lastElement(lista_players)
                    top_scorer["avg_time [min]"]= (top_scorer["avg_time [min]"])/top_scorer["goals"]
                    equipo["top_scorer"]= tabulate([top_scorer], headers="keys", tablefmt="grid", showindex= False)
                else: 
                    equipo["top_scorer"] = tabulate([["Unknown", 0, 0, 0]], headers=["scorer", "goals", "matches", "avg_time [min]"], tablefmt="grid", showindex=False)
        
        quk.sort(lista_values_equipos, cmp_estadisticas)
        
    if lt.size(lista_values_equipos) > int(n):
        lista_values_equipos= lt.subList(lista_values_equipos, 1, int(n))  
        
    return t_anios, t_torneos, t_eq_torn, t_match_anio, t_match_torneo, t_paises, t_ciudades, max_ciudad, lista_values_equipos  
    


def req_7(historial_FIFA, torneo, puntos):
    """
    Función que soluciona el requerimiento 7
    """
    torneo_info = mp.get(historial_FIFA["torneos_req7"], torneo)
    torneo_info = me.getValue(torneo_info)
    jugdores = mp.valueSet(torneo_info["jugadores"])
    quk.sort(jugdores, cmp_req7)
    goleadores_filtrados = lt.newList()
    
    i = 1
    working = True
    while i <= lt.size(jugdores) and working:
        jugador = lt.getElement(jugdores, i)
        if jugador["total_points"] == puntos:
            lt.addLast(goleadores_filtrados, jugador)
            if jugador["avg_time [min]"] != 0:
                jugador["avg_time [min]"] = jugador["avg_time [min]"]/ jugador["total_goals"]
            else:
                jugador["avg_time [min]"] = "Unknown"
                #Arreglar existencia de la lista
            goles = jugador["last_goal"]
            if "datastructure" in goles:
                quk.sort(goles, cmp_fecha_req7)
                last = lt.lastElement(goles)
                jugador["last_goal"] = tabulate([[last["date"], 
                                                last["tournament"], 
                                                last["home_team"], 
                                                last["away_team"], 
                                                last["home_score"], 
                                                last["away_score"], 
                                                last["minute"], 
                                                last["penalty"], 
                                                last["own_goal"]]], 
                                                headers=["date", "tournament", "home_team", "away_team", "home_score", "away_score", "minute", "penalty", "own_goal" ],tablefmt = "grid", showindex=False)
        elif jugador["total_points"] < puntos:
            working = False
        i += 1
    total_torneos = mp.size(historial_FIFA["torneos_req4"])
    total_anotadores = mp.size(torneo_info["jugadores"])
    total_encuentros = mp.size(torneo_info["partidos"])
    total_anotaciones = torneo_info["goles"]
    total_penales = torneo_info["penales"]
    total_autogoles = torneo_info["autogoles"]
    
    return total_torneos, total_anotadores, total_encuentros, total_anotaciones, total_penales, total_autogoles, goleadores_filtrados



def req_8(historial_FIFA, equipo, anio_i, anio_f):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    equipo_info = mp.get(historial_FIFA["equipos_bono"], equipo)
    equipo_info = me.getValue(equipo_info)
    anios = mp.valueSet(equipo_info["anios"])
    anios_filtrados = lt.newList()
    for anio in lt.iterator(anios):
        if anio["year"] >= anio_i and anio["year"] <= anio_f:
            lt.addLast(anios_filtrados, anio)
            
            anio["goal_diference"] = anio["goals_for"] - anio["goals_against"]
            if "datastructure" in anio["top_scorer"]:
                scorers = mp.valueSet(anio["top_scorer"])
                empty = lt.isEmpty(scorers)
                if not empty:
                    quk.sort(scorers, cmp_top_scorer)
                    top = lt.firstElement(scorers)
                    anio["top_scorer"] = tabulate([[top["scorer"], top["goals"], top["matches"], top["avg_time [min]"]]], headers=["scorer", "goals", "matches", "avg_time [min]"], tablefmt="grid", showindex=False)
                else:
                    anio["top_scorer"] = tabulate([["Unknown", 0, 0, 0]], headers=["scorer", "goals", "matches", "avg_time [min]"], tablefmt="grid", showindex=False)
    quk.sort(anios_filtrados, cmp_bono)
    
    total_partidos = lt.newList()
    total_local = 0
    total_visitante = 0
    estadisticas_anios = mp.valueSet(equipo_info["estadisticas_anios"])
    for anio in lt.iterator(estadisticas_anios):
        if anio["anio"] >= anio_i and anio["anio"] <= anio_f:
            for partido in lt.iterator(anio["partidos"]):
                lt.addLast(total_partidos, partido)
            total_local += anio["local"]
            total_visitante += anio["visitante"]
    quk.sort(total_partidos, cmp_fecha_req7)
    antiguo = lt.lastElement(total_partidos)
    fecha_antiguo = antiguo["date"]
    ultimo_partido = lt.firstElement(total_partidos)
    total_partidos = lt.size(total_partidos)
    
    return total_partidos, total_local, total_visitante, fecha_antiguo, ultimo_partido, anios_filtrados
        


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass
# ============================ FUNCIONES DE COMPARACIÓN PARA ORDENAR=====================

# Tres primeras funciones corresponden a los criterios compuestos solicitados para la IMPRECIÓN de la carga de datos.
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
    
def cmp_req4(rs1, rs2):
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
    
def cmp_req7(sr1, sr2):
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
    
def cmp_fecha_req7(rs1,rs2):
    if rs1["date"] > rs2["date"]:
        return True
    else:
        return False
def cmp_bono(yr1, yr2):
    if yr1["year"] == yr2["year"]:
        if yr1["total_points"] == yr2["total_points"]:
            if yr1["goal_difference"] == yr2["goal_difference"]:
                if yr1["penalties"] == yr2["penalties"]:
                    if yr1["matches"] == yr2["matches"]:
                        if yr1["own_goals"] < yr2["own_goals"]:
                            return True
                        else:
                            return False
                    elif yr1["matches"] < yr2["mtches"]:
                        return True
                    else: 
                        return False 
                elif yr1["penalties"] < yr2["penalties"]:
                    return True
                else:
                    return False
            elif yr1["goal_difference"] > yr2["goal_difference"]:
                return True
            else:
                return False
        elif yr1["total_points"] > yr2["total_points"]:
            return True
        else:
            return False
    elif yr1["year"] > yr2["year"]:
        return True
    else:
        return False
    
def cmp_top_scorer(scr1, scr2):
     if scr1["goals"] > scr2["goals"]:
         return True
     else:
         return False
# ---------------------------------------------------------------------------------------------

    
def cmp_fecha(rs1,rs2):
    if rs1["date"] > rs2["date"]:
        return True
    else:
        return False
    
def cmp_fecha_req2(gl1,gl2):
    if gl1["date"] == gl2["date"]:
        if gl1["minute"] < gl2["minute"]:
            return True
        else:
            return False
    elif gl1["date"] < gl2["date"]:
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
    
def cmp_ciudades(cd1, cd2):
    if cd1["num_partidos"] > cd2["num_partidos"]:
        return True
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
    #TODO: Crear función comparadora para ordenar
    pass

# ============================== FUNCIONES PARA ORDENAR =============================
def ordenar_goles(historial_FIFA):
    historial_FIFA["goalscorers"] = sa.sort(historial_FIFA["goalscorers"], sort_crit=cmp_goles_por_fecha_minuto_jugador)
    return historial_FIFA

def ordenar_penales(historial_FIFA):
    historial_FIFA["shootouts"] = sa.sort(historial_FIFA["shootouts"], sort_crit=cmp_penales_por_fecha_equipo)
    return historial_FIFA

def ordenar_partidos(historial_FIFA):
    historial_FIFA["results"] = sa.sort(historial_FIFA["results"], sort_crit=cmp_partidos_por_fecha_puntaje)
    return historial_FIFA

def sort(historial_FIFA):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
