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
import datetime

from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
import datetime, time

assert cf


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
    catalog = {
        'goalscorers': None,
        'results': None,
        'shootouts': None,
        "scorer": None,
        'mapResults':None,
        'equipos':None,
        "anio_torneo":None,
        'goals':None,
        'torneos_goles': None,
        "equipo_scorer":None
    }

    catalog['goalscorers'] = lt.newList("ARRAY_LIST")
    catalog['results'] = lt.newList("ARRAY_LIST")
    catalog['shootouts'] = lt.newList("ARRAY_LIST")
    catalog["scorer"] = mp.newMap(13000, prime=109345121, loadfactor=4, maptype="CHAINING")
    catalog['mapResults'] = mp.newMap(40000, prime=109345121, loadfactor=4, maptype="CHAINING")
    catalog['equipos'] = mp.newMap(300, prime=109345121, loadfactor=0.5, maptype="PROBING")
    catalog["anio_torneo"] = mp.newMap(160, prime=109345121, loadfactor=0.5, maptype="PROBING")
    catalog["goals"] = mp.newMap(10000, prime=109345121, loadfactor=4, maptype="CHAINING")
    catalog["torneos_goles"] = mp.newMap(10000, prime=109345121, loadfactor=4, maptype="CHAINING")
    catalog["equipo_scorer"] = mp.newMap(300, prime=109345121, loadfactor=0.5, maptype="PROBING")

    return catalog

def prepare_date(catalog):

    new_list = lt.newList("ARRAY_LIST")

    for dic in lt.iterator(catalog):

        lt.addLast(new_list, dic.copy())

    for dic in lt.iterator(new_list):

        if "date" in dic:

            dic['date'] = datetime.datetime.strftime(dic['date'], "%Y-%m-%d")

    return new_list

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    lt.addLast(data_structs, data)

def add_scorer_equipo(data_structs,scorer,result,equipo):
    """
    Función para agregar nuevos elementos a la lista
    """
    equipos=data_structs
    equipo_info={
        "date": result["date"],
        "home_team": result["home_team"],
        "away_team": result["away_team"],
        "home_score": result["home_score"],
        "away_score": result["away_score"],
        "tournament": result["tournament"],
        "city": result["city"],
        "country": result["country"],
        "neutral": result["neutral"],
        "own_goal": scorer["own_goal"],
        "penalty": scorer["penalty"]

    }
    entry = mp.get(equipos, equipo)

    if not entry:

        mp.put(equipos, equipo, lt.newList("ARRAY_LIST"))

    output = me.getValue((mp.get(equipos, equipo)))
    lt.addLast(output, equipo_info)

def add_scorer(data_structs,scorer,result):
    """
    Función para agregar nuevos elementos a la lista
    """

    scorers = data_structs
    goal_info = {
        "date": scorer["date"],
        "minute": scorer["minute"],
        "home_team": scorer["home_team"],
        "away_team": scorer["away_team"],
        "team": scorer["team"],
        "home_score": result["home_score"],
        "away_score": result["away_score"],
        "tournament": result["tournament"],
        "own_goal": scorer["own_goal"],
        "penalty": scorer["penalty"]
    }

    entry = mp.get(scorers, scorer["scorer"])

    if not entry:

        mp.put(scorers, scorer["scorer"], lt.newList("ARRAY_LIST"))

    output = (mp.get(scorers, scorer["scorer"]))["value"]
    lt.addLast(output, goal_info)


def add_result (data_structs, partido,winner):
    results=data_structs
    result=partido.copy()

    result_info={
        "date": result["date"],
        "home_team": result["home_team"],
        "away_team": result["away_team"],
        "home_score": result["home_score"],
        "away_score": result["away_score"],
        "tournament": result["tournament"],
        "city": result["city"],
        "country": result["country"],
        "neutral": result["neutral"],
        "winner":winner
    }
    date=datetime.datetime.strftime(result['date'], "%Y-%m-%d")

    r=str(date+result["home_team"]+result["away_team"])
    mp.put(results, r, result_info)


def add_equipo (data_structs,equipo,result,winner):
    equipos=data_structs
    equipo_info={
        "date": result["date"],
        "home_team": result["home_team"],
        "away_team": result["away_team"],
        "home_score": result["home_score"],
        "away_score": result["away_score"],
        "tournament": result["tournament"],
        "city": result["city"],
        "country": result["country"],
        "neutral": result["neutral"],
        "winner":winner
    }
    entry = mp.get(equipos, equipo)

    if not entry:

        mp.put(equipos, equipo, lt.newList("ARRAY_LIST"))

    output = (mp.get(equipos, equipo))["value"]
    lt.addLast(output, equipo_info)


def add_anio_torneo (data_structs,anio,result,winner):
    anios_torneos=data_structs

    entry = mp.get(anios_torneos, anio)
    if not entry:
        mp.put(anios_torneos, anio, mp.newMap(100))
    torneo = me.getValue(mp.get(anios_torneos, anio))
    e=mp.get(torneo, "encuentros_anio")
    if not e:
        mp.put(torneo,"encuentros_anio",lt.newList("ARRAY_LIST"))
    o= me.getValue(mp.get(torneo, "encuentros_anio"))
    lt.addLast(o,"1")
    add_torneo(torneo,result,winner)


def add_torneo(data_structs,result,winner):
    torneo_info={
        "date": result["date"],
        "home_team": result["home_team"],
        "away_team": result["away_team"],
        "home_score": result["home_score"],
        "away_score": result["away_score"],
        "tournament": result["tournament"],
        "city": result["city"],
        "country": result["country"],
        "neutral": result["neutral"],
        "winner":winner
    }

    entry = mp.get(data_structs, result["tournament"])
    if not entry:
        mp.put(data_structs, result["tournament"], mp.newMap(100))
    equipos = me.getValue(mp.get(data_structs, result["tournament"]))
    e=mp.get(equipos, "encuentros_torneo")
    if not e:
        mp.put(equipos,"encuentros_torneo",lt.newList("ARRAY_LIST"))
    o= me.getValue(mp.get(equipos, "encuentros_torneo"))
    lt.addLast(o,torneo_info)

    equipo=result["home_team"]
    add_equipo(equipos,equipo,result,winner)
    equipo=result["away_team"]
    add_equipo(equipos,equipo,result,winner)

def add_result_torneo(data_structs,result):

    entry_tournament = mp.get(data_structs["torneos_goles"], result["tournament"].title())
    if not entry_tournament:
        torneo_info = mp.newMap(200)
        mp.put(torneo_info, "results", 0)
        mp.put(torneo_info, "results_map", mp.newMap(1000))
        mp.put(torneo_info, "goals", 0)
        mp.put(torneo_info, "penalties", 0)
        mp.put(torneo_info, "own_goals", 0)
        mp.put(torneo_info, "scorers", mp.newMap(1000))
        mp.put(data_structs["torneos_goles"], result["tournament"].title(), torneo_info)

def add_scorer_torneo(data_struct, scorer):

    date=datetime.datetime.strftime(scorer['date'], "%Y-%m-%d")
    key_on_map = date + scorer["home_team"] + scorer["away_team"]
    entry = mp.get(data_struct["mapResults"], key_on_map)
    result = me.getValue(entry)
    tournament = me.getValue(entry)["tournament"].title()

    entry_tournament = mp.get(data_struct["torneos_goles"], tournament)

    if not entry_tournament:
        torneo_info = mp.newMap(1000)
        mp.put(torneo_info, "results", 0)
        mp.put(torneo_info, "results_map", mp.newMap(1000))
        mp.put(torneo_info, "goals", 0)
        mp.put(torneo_info, "penalties", 0)
        mp.put(torneo_info, "own_goals", 0)
        mp.put(torneo_info, "scorers", mp.newMap(1000))
        mp.put(data_struct["torneos_goles"], tournament, torneo_info)

    entry_tournament_map = me.getValue(mp.get(data_struct["torneos_goles"], tournament))
    entry_result_map = mp.get(me.getValue(mp.get(entry_tournament_map, "results_map")), key_on_map)
    if not entry_result_map:
        mp.put(me.getValue(mp.get(entry_tournament_map, "results_map")), key_on_map, 1)
        mp.put(entry_tournament_map, "results", me.getValue(mp.get(entry_tournament_map, "results")) + 1)

    torneo_info = me.getValue(mp.get(data_struct["torneos_goles"], tournament))

    entry_scorer = mp.get(me.getValue(mp.get(torneo_info, "scorers")), scorer["scorer"])
    scorers_key = me.getValue(mp.get(torneo_info, "scorers"))

    if not entry_scorer:
        scorer_info = mp.newMap(50)
        mp.put(scorer_info, "total_points", 0)
        mp.put(scorer_info, "name", scorer["scorer"])
        mp.put(scorer_info, "total_goals", 0)
        mp.put(scorer_info, "scored_in_wins", 0)
        mp.put(scorer_info, "scored_in_draws", 0)
        mp.put(scorer_info, "scored_in_losses", 0)
        mp.put(scorer_info, "penalty_goals", 0)
        mp.put(scorer_info, "own_goals", 0)
        mp.put(scorer_info, "avg_times", lt.newList("ARRAY_LIST"))
        mp.put(scorer_info, "last_goal", {})
        mp.put(scorers_key, scorer["scorer"], scorer_info)

    scorer_info = me.getValue(mp.get(scorers_key, scorer["scorer"]))

    mp.put(torneo_info, "goals", me.getValue(mp.get(torneo_info, "goals")) + result["home_score"] + result["away_score"])

    if scorer["team"] == result["winner"]:
        mp.put(scorer_info, "scored_in_wins", me.getValue(mp.get(scorer_info, "scored_in_wins")) + 1)
    elif scorer["team"] == "empate":
        mp.put(scorer_info, "scored_in_draws", me.getValue(mp.get(scorer_info, "scored_in_draws")) + 1)
    else:
        mp.put(scorer_info, "scored_in_losses", me.getValue(mp.get(scorer_info, "scored_in_losses")) + 1)

    if scorer["own_goal"].title().strip() == "True":
        mp.put(scorer_info, "own_goals", me.getValue(mp.get(scorer_info, "own_goals")) + 1)
        mp.put(torneo_info, "own_goals", me.getValue(mp.get(torneo_info, "own_goals")) + 1)

    mp.put(scorer_info, "total_goals", me.getValue(mp.get(scorer_info, "total_goals")) + 1)

    if scorer["penalty"].title().strip() == "True":
        mp.put(torneo_info, "penalties", me.getValue(mp.get(torneo_info, "penalties")) + 1)
        mp.put(scorer_info, "penalty_goals", me.getValue(mp.get(scorer_info, "penalty_goals")) + 1)

    # Calcular el total de puntos. Este calculo se calcula sumando los goles anotados, mas los penalties menos los autogoles
    mp.put(scorer_info, "total_points", me.getValue(mp.get(scorer_info, "total_goals")) + me.getValue(mp.get(scorer_info, "penalty_goals")) - me.getValue(mp.get(scorer_info, "own_goals")))

    date_exists = me.getValue(mp.get(scorer_info, "last_goal"))

    if date_exists:
        if scorer["date"] > me.getValue(mp.get(scorer_info, "last_goal"))["date"]:
            mp.put(scorer_info, "last_goal", {
                "date": scorer["date"],
                "tournament": tournament,
                "home_team": scorer["home_team"],
                "away_team": scorer["away_team"],
                "home_score": result["home_score"],
                "away_score": result["away_score"],
                "minute": scorer["minute"],
                "penalty": scorer["penalty"],
                "own_goal": scorer["own_goal"]
            })
    else:
        mp.put(scorer_info, "last_goal", {
            "date": scorer["date"],
            "tournament": tournament,
            "home_team": scorer["home_team"],
            "away_team": scorer["away_team"],
            "home_score": result["home_score"],
            "away_score": result["away_score"],
            "minute": scorer["minute"],
            "penalty": scorer["penalty"],
            "own_goal": scorer["own_goal"]
        })

    lt.addLast(me.getValue(mp.get(scorer_info, "avg_times")), scorer["minute"])

def add_goals(data_structs,result,scorer,equipo):
    goals = data_structs
    goal_info = {
        "date": scorer["date"],
        "scorer": scorer["scorer"],
        "minute": scorer["minute"],
        "home_team": scorer["home_team"],
        "away_team": scorer["away_team"],
        "team": scorer["team"],
        "home_score": result["home_score"],
        "away_score": result["away_score"],
        "tournament": result["tournament"],
        "own_goal": scorer["own_goal"],
        "penalty": scorer["penalty"]
    }
    r=str(equipo+str(scorer["date"].year)+result["tournament"])
    entry = mp.get(goals, r)

    if not entry:

        mp.put(goals, r, lt.newList("ARRAY_LIST"))

    output = me.getValue(mp.get(goals, r))
    lt.addLast(output, goal_info)

# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    # TODO: Crear la función para obtener un dato de una lista
    return lt.getElement(data_structs, id)


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    # TODO: Crear la función para obtener el tamaño de una lista

    return lt.size(data_structs)


def first_three(data_structs):
    """Retorna los primeros 3 items de una lista

    Recibe una lista y devuelve los primeros 3 items
    Importan! Ejemplo de como recibe la lista -> catalog['results']

    """
    return lt.subList(data_structs, 1, 3)


def last_three(data_structs):
    minus_three = lt.size(data_structs) - 2
    return lt.subList(data_structs, minus_three, 3)

#Funcion que define el ganador
def anadir_ganador (data_structs):
    ganador=""
    for partido in lt.iterator(data_structs["results"]):
        if partido["home_score"]>partido["away_score"]:
            ganador=partido["home_team"]
        elif partido["home_score"]<partido["away_score"]:
            ganador=partido["away_team"]
        elif partido["home_score"]==partido["away_score"]:
            for shootout in lt.iterator(data_structs["shootouts"]):
                if partido["date"] == shootout["date"] and partido["home_team"] == shootout["home_team"] and partido["away_team"] == shootout["away_team"]:
                    ganador= shootout["winner"]
                else:
                    ganador="empate"
        partido["winner"]=ganador

    return data_structs
def decidir_ganador (partido, data_structs):
    ganador=""

    if partido["home_score"]>partido["away_score"]:
        ganador=partido["home_team"]

    elif partido["home_score"]<partido["away_score"]:
        ganador=partido["away_team"]

    elif partido["home_score"]==partido["away_score"]:
        for shootout in lt.iterator(data_structs["shootouts"]):
            if partido["date"] == shootout["date"] and partido["home_team"] == shootout["home_team"] and partido["away_team"] == shootout["away_team"]:
                ganador= shootout["winner"]
    if ganador=="":
        ganador="empate"
    return ganador


def req_1(data_structs, cantidad, nombre, condicion):
    """
    Función que soluciona el requerimiento 1: Listar los ultimos n partidos de un equipo segun condición.
    Inputs:
        data_structs = estructuras de datos
        nombre = nombre del jugador
        cantidad = cantidad de partidos que queremos que nos devuelva

    Devuelve:
        respuesta = lista con los partidos con la cantidad (n) que nos interesa.
        totalpartidos = lleva el conteo del total de partidos que cumplen las condiciones.
    """
    c = int(cantidad)
    totalcondicion=0
    totalequipos=mp.size(data_structs['equipos'])
    respuesta = lt.newList("ARRAY_LIST")
    nombre=nombre.title()
    condicion=condicion.lower()

    entry=mp.get(data_structs['equipos'],nombre)
    partidos=me.getValue(entry)
    totalpartidos=lt.size(partidos)

    for dic in lt.iterator(partidos):

        if condicion== "local":
            if dic["home_team"] == nombre and dic["neutral"] != "True":
                totalcondicion+=1
                if totalcondicion <= c:
                    lt.addLast(respuesta, dic.copy())
        elif condicion == "visitante":
            if dic["away_team"] == nombre and dic["neutral"] != "True":
                totalcondicion+=1
                if totalcondicion <= c:
                    lt.addLast(respuesta, dic.copy())

        else:
            if dic["away_team"] == nombre or dic["home_team"] == nombre:
                totalcondicion+=1
                if totalcondicion <= c:
                    lt.addLast(respuesta, dic.copy())


    return totalequipos,totalpartidos,totalcondicion,respuesta


def req_2(data_structs, name, cantidad):
    """
    Función que soluciona el requerimiento 2: Listar los primeros N goles anotados por un jugador (G).

    Inputs:
        data_structs = estructuras de datos
        name = nombre del jugador
        cantidad = cantidad de goles que queremos que nos devuelva

    Devuelve:
        respuesta = lista con los goles anotados por el la cantidad (n) que nos interesa
        num_partidos = lleva el conteo de goles que ha anotado el jugador (deberia ser num_goles pero aja)
    """
    c = int(cantidad)
    respuesta = lt.newList("ARRAY_LIST")
    name=name.title()
    entry=mp.get(data_structs['scorer'],name)
    goles=me.getValue(entry)
    num_goles=lt.size(goles)
    total__scorers=  lt.size(data_structs['scorer'])
    penalty=0

    for dic in lt.iterator(goles):
        if dic["penalty"] == "True":
            penalty+=1

    if c<num_goles:
        respuesta=lt.subList(goles,lt.size(goles)-c+1,c)
    else:
        respuesta=goles

    return respuesta , num_goles , total__scorers, penalty


def req_3(equipo,fecha_inicial,fecha_final,data_structs):
    """
    Función que soluciona el requerimiento 3

    Consultar los partidos que disputó un equipo durante un periodo especifico. (I)

    Parametros:

        equipo: Nombre del equipo
        fecha_inicial: Fecha inicial del periodo
        fecha_final: Fecha final del periodo

    Devuelve:

        Número total de partidos disputados.
        Número total de partidos disputados como local.
        Número total de partidos disputados como visitante.
        El listado de los partidos disputados ordenados cronologicamente.
        obtener si el partido tuvo autogol o penal a partir de goalscorer


    """

    equipo=equipo.title()
    fecha_inicial = datetime.datetime.strptime(fecha_inicial, "%Y-%m-%d")
    fecha_final = datetime.datetime.strptime(fecha_final, "%Y-%m-%d")

    partidos_finales = lt.newList("ARRAY_LIST")

    mapa = data_structs["equipo_scorer"]
    partidos = me.getValue(mp.get(mapa, equipo))
    local=0
    visitante=0

    for partido in lt.iterator(partidos):
        if fecha_inicial <= partido["date"] and partido["date"] <= fecha_final:
            if partido["home_team"] == equipo:
                local+=1
            elif partido["away_team"] == equipo:
                visitante+=1

            lt.addLast(partidos_finales, partido)


    return lt.size(data_structs["equipo_scorer"]), local, visitante, partidos_finales


def req_4(tournament, fecha_inicial, fecha_final, data_structs):
    """
    Función que soluciona el requerimiento 4

    Consultar los partidos de un torneo durante un periodo especifico.

    Parámetros:

            tournament: Nombre del torneo
            fecha_inicial: Fecha inicial del periodo
            fecha_final: Fecha final del periodo
            data_structs: Estructuras de datos

    Devuelve:

            partidos_lista: Lista con los partidos del torneo
            num_paises: Número de paises diferentes que se jugo el torneo
            num_ciudades: Número de ciudades diferentes donde se jugaron los partidos del torneo
            penalties: Número de penalties que hubo
            num_partidos: Número de partidos que se jugaron en el torneo
            num_torneos: Número de torneos diferentes que se jugaron en el periodo

    """
    tournament=tournament.title()

    fecha_inicial = datetime.datetime.strptime(fecha_inicial, "%Y-%m-%d")
    fecha_final = datetime.datetime.strptime(fecha_final, "%Y-%m-%d")

    paises = mp.newMap(210)
    ciudades = mp.newMap(1000)
    penalties = 0
    torneos = mp.newMap(30)
    partidos = mp.newMap(1000)
    partidos_lista = lt.newList("ARRAY_LIST")

    rango_binaria = crear_rango_busqueda_binaria(data_structs["results"], fecha_inicial, fecha_final)

    for partido in lt.iterator(rango_binaria):
        # Obtengo la key del torneo que me interesa
        torneo = mp.get(torneos, partido["tournament"].strip().title())
        # Si no encuentra el torneo entonces añade el torneo al mapa
        if not torneo:
            mp.put(torneos, partido["tournament"].strip().title(), 1)
        # Si el torneo es el que me interesa entonces añade los datos a los mapas
        if partido["tournament"].title() == tournament:

            pais = mp.get(paises, partido["country"].title().strip())
            if not pais:
                mp.put(paises, partido["country"].title().strip(), 1)

            ciudad = mp.get(ciudades, partido["city"].title().strip())
            if not ciudad:
                mp.put(ciudades, partido["city"].title().strip(), 1)

            penalty, winner = penalty_check(data_structs, partido)
            penalties += penalty

            date=datetime.datetime.strftime(partido['date'], "%Y-%m-%d")

            partido_get = mp.get(partidos, date + partido["home_team"].title() + partido["away_team"].title())
            if not partido_get:
                mp.put(partidos, date + partido["home_team"].title() + partido["away_team"].title(),1)
                lt.addLast(partidos_lista, {
                           "date": partido["date"],
                           "tournament": partido["tournament"],
                           "country": partido["country"],
                            "city": partido["city"],
                            "home_team": partido["home_team"],
                            "away_team": partido["away_team"],
                            "home_score": partido["home_score"],
                            "away_score": partido["away_score"],
                            "winner": winner,
                       })

    num_paises = mp.size(paises)
    num_ciudades = mp.size(ciudades)
    num_partidos = mp.size(partidos)
    num_torneos = mp.size(torneos)

    return partidos_lista, num_paises, num_ciudades, penalties, num_partidos, num_torneos

def penalty_check(data_structs,partido):
    """
    Esta funcion recibe un partido y revisa si este termino en penalties.
    Esto lo hace viendo el score del partido y si queda en empate revisa
    si el winner fue diferente a empate. Si el winner fue diferente a
    empate entonces significara que TUVIERON que haber ido a penalties.

    Retorna 1 si hubo penalties o 0 sí no.
    """
    date=datetime.datetime.strftime(partido['date'], "%Y-%m-%d")
    key_on_map = date + partido["home_team"] + partido["away_team"]
    entry = mp.get(data_structs["mapResults"], key_on_map)

    if entry:
        result = me.getValue(entry)
        if result["home_score"] == result["away_score"]:
            if result["winner"] != "empate" and result["winner"] != "":
                return 1, result["winner"]
        else:
            return 0, result["winner"]
    return 0, "Unavailable"


def check_who_won(data_structs, partido):
    """
    Esta función con base al partido, revisa en los datos de shootouts quien ganó el partido (si termino siendo empato
    termino en penalties)
    """

    for shootout in lt.iterator(data_structs["shootouts"]):
            if partido["date"] == shootout["date"] and partido["home_team"] == shootout["home_team"] and partido["away_team"] == shootout["away_team"]:
                return shootout["winner"]

    return None

def req_5(jugador, fecha_inicial, fecha_final, data_structs):

    """
    Función que soluciona el requerimiento 5

    Consultar los goles de un jugador durante un periodo especifico.

    Parámetros:

        jugador: Nombre del jugador
        fecha_inicial: Fecha inicial del periodo
        fecha_final: Fecha final del periodo
        data_structs = estructura de datos

    Devuelve:

        numero_jugadores: Numero de jugadores con info disponible
        numero_goles: Número total de goles marcados por el jugador en el periodo específico.
        numero_torneos: Número total de torneos en los que marcó el jugador en el periodo específico.
        penaltis: Número total de penaltis que marcó el jugador en el periodo específico.
        autogoles: Número total de autogoles que marcó el jugador en el periodo específico.
        resultado: El listado con los goles anotados por el jugador ordenado cronológicamente
    """

    jugador=jugador.title()
    fecha_inicial = datetime.datetime.strptime(fecha_inicial, "%Y-%m-%d")
    fecha_final = datetime.datetime.strptime(fecha_final, "%Y-%m-%d")
    penaltis = 0
    autogoles = 0
    tournaments = mp.newMap(60)
    resultado=lt.newList("ARRAY_LIST")

    scorers=data_structs['scorer']

    #Se obtiene la pareja llave valor que corresponde con el jugador ingresado por parámetro
    entry=mp.get(scorers,jugador)
    goles=me.getValue(entry)

    #Se hace busqueda binaria para definir los goles que se encuentran dentro del rango que entra por parámetro
    resultado=crear_rango_busqueda_binaria(goles,fecha_inicial,fecha_final)

    #Se recorre la lista de los goles que cumplen todas las condiciones para encontrar el numero de penaltis, autogoles y torneos
    for dic in lt.iterator(resultado):
        if dic["own_goal"] == "True":
            autogoles += 1
        if dic["penalty"] == "True":
            penaltis += 1
        entry=mp.get(tournaments,dic["tournament"])
        if not entry:
            mp.put(tournaments,dic["tournament"],1)

    numero_jugadores=mp.size(scorers)
    numero_goles = lt.size(resultado)
    numero_torneos = mp.size(tournaments)


    return numero_jugadores,numero_goles, numero_torneos, penaltis, autogoles, resultado

def max_dic(dic):
    """ Función que recorre un dicionario de valores enteros y busca el mayor valor entre los resultados, retornando el valor de la llave"""
    max=-1
    respuesta=""
    for llave in dic:
        if dic[llave]>max:
            max=dic[llave]
            respuesta=llave
    return respuesta

def req_6(cantidad, torneo,anio,data_structs):
    """
    Función que soluciona el requerimiento 6

    Consultar a los n mejores equipos de un torneo durante un año especifico.

    Parámetros:

        cantidad: cantidad de equipos que queremos que nos devuelva
        torneo: Nombre del torneo a consultar
        anio: Año de consulta
        data_structs = estructura de datos

    Devuelve:

        c_anios: Total de años con info disponible.
        c_torneos: Total de torneos disputados en el año.
        c_equipos: Total de equipos involucrados en el torneo.
        c_partidos: Total de partido disputados en el torneo.
        total_paises: Total de países en los que se disputo el torneo durante el año.
        total_ciudades: Total de ciudades en las que se disputo el torneo durante el año.
        max_ciudad : Nombre de la ciudad en la que más partidos se disputaron.
        estadisticas: Listado de las estadisticas ordenadas de mejor a peor equipo.

    """
    torneo=torneo.title()
    c=int(cantidad)
    anio=int(anio)
    anios=data_structs['anio_torneo']
    c_anios=mp.size(anios)-1

    #Se obtiene el valor(otra mapa de torneos) que corresponde con el año ingresado por parámetro
    torneos=me.getValue(mp.get(anios,anio))
    c_torneos=mp.size(torneos)-1

    #Se obtiene el valor(otra mapa de equipos) que corresponde con el torneo ingresado por parámetro
    equipos=me.getValue(mp.get(torneos,torneo))
    partidos_torneo=me.getValue(mp.get(equipos, "encuentros_torneo"))

    c_partidos=lt.size(partidos_torneo)
    mp.remove(equipos,"encuentros_torneo")
    lista_equipos=mp.keySet(equipos)
    mp.put(equipos,"encuentros_torneo",partidos_torneo)
    c_equipos=mp.size(lista_equipos)
    paises=lt.newList("ARRAY_LIST")
    ciudades={}

    #Se recorre la lista de los partidos en el año y torneo específicos
    for dic in lt.iterator(partidos_torneo):
            if lt.isPresent(paises, dic["country"]) == 0:
                lt.addLast(paises, dic["country"])
            if dic["city"] not in ciudades:
                ciudades[dic["city"]]=1
            else:
                ciudades[dic["city"]]+=1

    total_paises=lt.size(paises)
    total_ciudades=len(ciudades)
    max_ciudad=max_dic(ciudades)
    estadisticas=lt.newList("ARRAY_LIST")

    #Se recorre la lista de todos los equipos que participaron en el torneo para ir llenar sus estadisticas uno a uno
    for equipo in lt.iterator(lista_equipos):
        team={"team":equipo,
                "total_points":0,
                "goal_difference":0,
                "penalty_points":0,
                "matches":0,
                "own_goal_points":0,
                "wins":0,
                "draws":0,
                "loses":0,
                "goals_for":0,
                "goals_against":0,
                "top_scorer":"No hay"}

        partidos_equipo=me.getValue(mp.get(equipos,equipo))
        for partido in lt.iterator(partidos_equipo):

            team["matches"]=lt.size(partidos_equipo)
            if partido["home_team"]==equipo:
                team["goals_for"]+=int(partido["home_score"])
                team["goals_against"]+=int(partido["away_score"])
            elif partido["away_team"]==equipo:
                team["goals_for"]+=int(partido["away_score"])
                team["goals_against"]+=int(partido["home_score"])

            if partido["winner"]==equipo:
                team["total_points"]+=3
                team["wins"]+=1
            elif partido["winner"]=="empate":
                team["total_points"]+=1
                team["draws"]+=1
            else:
                team["loses"]+=1
        team["goal_difference"]=team["goals_for"]-team["goals_against"]

        #Se busca si existen goles que tengan que ver con el equipo (anotados y recibidos) en el año y torneo, si encuentra añade la información de "top_socer", si no lo deja como "No hay"
        r=equipo+str(anio)+torneo
        entry=mp.get(data_structs["goals"],r)
        if entry:
            goles_equipo=me.getValue(entry)
            jugadores={}
            for gol in lt.iterator(goles_equipo):
                if gol["penalty"]=="True":
                        team["penalty_points"]+=1
                if gol["own_goal"]=="True":
                    team["own_goal_points"]+=1
                if gol["team"]==equipo:
                    if gol["scorer"] not in jugadores:
                        jugadores[gol["scorer"]]=1
                    elif gol["scorer"] in jugadores:
                        jugadores[gol["scorer"]]+=1

            if jugadores:
                goleador=max_dic(jugadores)
                estadisticas_goleador={"scorer":goleador, "goals":0, "matches":0, "avg_time":0}
                dates=mp.newMap(100)
                minutos=0
                for gol in lt.iterator(goles_equipo):
                    if gol["scorer"]==goleador:
                        estadisticas_goleador["goals"]+=1
                        minutos+=float(gol["minute"])
                        en=mp.get(dates,gol["date"])
                        if not en:
                            mp.put(dates,gol["date"],1)

                estadisticas_goleador["matches"]=mp.size(dates)
                estadisticas_goleador["avg_time"]=minutos/estadisticas_goleador["goals"]
                goleado=lt.newList("ARRAY_LIST")
                lt.addLast(goleado,estadisticas_goleador)
                team["top_scorer"]=goleado
            else:
                estadisticas_goleador={"scorer":"No hay", "goals":0, "matches":0, "avg_time":0}
                goleado=lt.newList("ARRAY_LIST")
                lt.addLast(goleado,estadisticas_goleador)
                team["top_scorer"]=goleado
        else:
            estadisticas_goleador={"scorer":"No hay", "goals":0, "matches":0, "avg_time":0}
            goleado=lt.newList("ARRAY_LIST")
            lt.addLast(goleado,estadisticas_goleador)
            team["top_scorer"]=goleado

        lt.addLast(estadisticas, team)

    #Se ordena estadisticas del mejor al peor equipo, y se recorta la lista tenienco en cuenta la cantidad entrada por parámetro
    merg.sort(estadisticas, cmpReq6)
    if lt.size(estadisticas)>c:
        estadisticas=lt.subList(estadisticas,1,c)

    return c_anios,c_torneos,c_equipos,c_partidos,total_paises,total_ciudades,max_ciudad, estadisticas


def req_7(n_puntos, torneo, data_structs):
    """
    Encontrar los anotadores con N puntos en un torneo especifico

    Parametros:
        n_puntos: Número de puntos que se quiere buscar
        torneo: Nombre del torneo
        data_structs: Estructuras de datos
    Devuelve:
        num_torneos: Número de torneos diferentes que se jugaron en el periodo
        num_scorers: Número de jugadores diferentes que anotaron en el torneo
        num_partidos: Número de partidos que se jugaron en el torneo
        num_goals: Número de goles que se anotaron en el torneo
        num_penalties: Número de goles que se anotaron en el torneo
        num_own_goals: Número de goles que se anotaron en el torneo
        jugadores: Lista de jugadores con N puntos en el torneo


    """

    jugadores = lt.newList("ARRAY_LIST")
    tournament_key = me.getValue(mp.get(data_structs["torneos_goles"], torneo))
    tournament_scorers = mp.keySet(me.getValue(mp.get(tournament_key, "scorers")))

    num_torneos = mp.size(data_structs["torneos_goles"])
    num_scorers = lt.size(tournament_scorers)
    num_partidos = me.getValue(mp.get(tournament_key, "results"))
    num_goals = me.getValue(mp.get(tournament_key, "goals"))
    num_penalties = me.getValue(mp.get(tournament_key, "penalties"))
    num_own_goals = me.getValue(mp.get(tournament_key, "own_goals"))


    scorers_map = me.getValue(mp.get(tournament_key, "scorers"))

    for scorer in lt.iterator(tournament_scorers):
        scorer_info = me.getValue(mp.get(scorers_map, scorer))
        points = me.getValue(mp.get(scorer_info, "total_points"))

        if points == int(n_puntos):
            lt.addLast(jugadores, scorer_info)

    merg.sort(jugadores, cmpReq7)

    return num_torneos, num_scorers, num_partidos, num_goals, num_penalties, num_own_goals, jugadores

def clean_data(results, dtypes):
    """
    Vuelve el datetime un str
    """

    for result in lt.iterator(results):

        result['date'] = datetime.datetime.strptime(result['date'], "%Y-%m-%d")

    return results

# Funciones de ordenamiento

def cmpReq6(partido1, partido2):
    """Cmp function que permite el ordenamiento de la respuesta del requerimiento 6 """

    if partido1['total_points'] == partido2['total_points']:
        if partido1['goal_difference'] == partido2['goal_difference']:
            if partido1['penalty_points'] > partido2['penalty_points']:
                return 1
        elif partido1['goal_difference'] > partido2['goal_difference']:
            return 1
        else:
            return 0
    elif partido1['total_points'] > partido2['total_points']:
        return 1
    else:
        return 0

def cmpReq7(jugador1, jugador2):
    """Cmp function que permite el ordenamiento de la respuesta del requerimiento 7
    El listado de equipos obtenido en la respuesta debe estar ordenado por el criterio compuesto de
evaluación de sus estadísticas. Es decir, ordenar por la mayor cantidad de puntos obtenidos por el
jugador, mayor total de goles anotados y más goles obtenidos por penales. En conjunto con la menor
cantidad de autogoles y el menor tiempo promedio de anotación (en minutos).
    """

    jugador1_points = me.getValue(mp.get(jugador1, "total_points"))
    jugador2_points = me.getValue(mp.get(jugador2, "total_points"))
    jugador1_goals = me.getValue(mp.get(jugador1, "total_goals"))
    jugador2_goals = me.getValue(mp.get(jugador2, "total_goals"))
    jugador1_penalties = me.getValue(mp.get(jugador1, "penalty_goals"))
    jugador2_penalties = me.getValue(mp.get(jugador2, "penalty_goals"))
    jugador1_avg_time = me.getValue(mp.get(jugador1, "avg_times"))
    jugador2_avg_time = me.getValue(mp.get(jugador2, "avg_times"))

    if jugador1_points == jugador2_points:
        if jugador1_goals == jugador2_goals:
            if jugador1_penalties == jugador2_penalties:
                if calculate_avg_time(jugador1_avg_time) < calculate_avg_time(jugador2_avg_time):
                    return 1
            elif jugador1_penalties > jugador2_penalties:
                return 1
        elif jugador1_goals > jugador2_goals:
            return 1
        else:
            return 0

def calculate_avg_time(times):
    """
    Recibe una lista con la lista de los tiempos de los goles de un jugador
    y retorna el promedio de estos
    """

    time = 0

    for i in lt.iterator(times):
        time += i

    return time/lt.size(times)

def cmpResults(partido1, partido2):
    """Cmp function que permite el ordenamiento de Results en la carga de datos"""

    if partido1['date'] == partido2['date']:
        if partido1['home_score'] == partido2['home_score']:
            if partido1['away_score'] > partido2['away_score']:
                return 1
        elif partido1['home_score'] > partido2['home_score']:
            return 1
        else:
            return 0
    elif partido1['date'] > partido2['date']:
        return 1
    else:
        return 0


def cmpGoalscorers(partido1, partido2):
    """Cmp function que permite el ordenamiento de Goalscorers en la carga de datos"""

    if partido1['date'] == partido2['date']:
        if partido1['minute'] == partido2['minute']:
            if partido1['scorer'] > partido2['scorer']:
                return 1
        elif partido1['minute'] > partido2['minute']:
            return 1
        else:
            return 0
    elif partido1['date'] > partido2['date']:
        return 1
    else:
        return 0


def cmpShootouts(partido1, partido2):
    """Cmp function que permite el ordenamiento de Shootouts en la carga de datos"""

    if partido1['date'] == partido2['date']:
        if partido1['home_team'] == partido2['home_team']:
            if partido1['away_team'] > partido2['away_team']:
                return 1
        elif partido1['home_team'] > partido2['home_team']:
            return 1
        else:
            return 0
    elif partido1['date'] > partido2['date']:
        return 1
    else:
        return 0

def sort(data_structs, fsort):
    """
    Función encargada de ordenar el catalogo en la carga de datos
    """
    if fsort == "results":
        sa.sort(data_structs[fsort], cmpResults)
    elif fsort == "goalscorers":
        sa.sort(data_structs[fsort], cmpGoalscorers)
    else:
        sa.sort(data_structs[fsort], cmpShootouts)

def busqueda_binaria(lista,elemento, cmpFunction):
    """
    Función encargada de realizar la busqueda binaria optimizada

    cmpFunction:
     si a<b, retorna 1
     si a==b, retorna 0
     si a>b, retorna -1

    Si no encuentra el elemento, retorna el inmediamante anterior
    Ejemplo:
    lista=[2021, 2019], valor = 2020
    retorna 0, porque es el indice anterior a donde estaria 2020.
    """

    izq = 1
    der = lt.size(lista)
    while izq<der:
        medio = (izq + der) // 2
        if medio==izq:
            izq+=1
        elif cmpFunction(lt.getElement(lista,medio), elemento) == 0:
            return medio
        elif cmpFunction(lt.getElement(lista,medio), elemento) == -1:
            izq = medio
        else:
            der = medio
    return medio

def crear_rango_busqueda_binaria(lista, fecha_inicial, fecha_final):
    def cmpFechaBinaria(a,b):
            if a["date"]<b["date"]:
                return 1
            elif a["date"]==b["date"]:
                return 0
            else:
                return -1

    der = 1+busqueda_binaria(lista, {"date": fecha_inicial}, cmpFechaBinaria)
    if lt.getElement(lista, der)["date"]< fecha_inicial:
       der -= 1
    # rango final: der tiene el elemento correcto
    # (Encuentra el indice si el elemento esta, y si no, encuentra el primero mayor)

    izq = busqueda_binaria(lista, {"date": fecha_final}, cmpFechaBinaria)
    if lt.getElement(lista, izq)["date"]> fecha_final:
       izq += 1
    # (Encuentra el indice si el elemento esta, y si no, encuentra el primero mayor,
    # por lo que se le suma 1 para que quede el indice del elemento menor)

    return lt.subList(lista, izq, der-izq+1)
