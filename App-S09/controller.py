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
 """

import tracemalloc
import config as cf
import datetime
import time
import model
import time
import csv
csv.field_size_limit(2147483647)
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None,
    }

    control['model'] = model.new_data_structs()

    return control

# Funciones para la carga de datos


def load_data(control, tamaño,memflag):
    """
    Carga los datos del reto

    retorna: cantidad de datos cargados y el catalogo de datos por cada archivo

    """
    catalog = control['model']


    # TODO: Añadir shootouts (Controller)

    start_time = get_time()
    # inicializa el proceso para medir memoria
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()

    def load_results(catalog, tamaño):
        """
        Carga y por cada resultado toma: date,home_team,away_team,home_score,away_score,tournament,city,country,neutral.
        """
        fsort = "results"

        resultsfile = cf.data_dir + 'Challenge-1/football/results-utf8-'+tamaño+'.csv'
        inputfile = csv.DictReader(
            open(resultsfile, encoding='utf-8'), restval="Desconocido")

        i = 1
        for result in inputfile:

            result["id"] = i
            result= clear_data(result,RESULT_DTYPE)

            model.add_data(catalog['results'], result)

            i += 1
        sort(catalog, fsort)

        return model.data_size(catalog['results']), catalog['results']


    def load_goalscorers(catalog, tamaño):
        """
        Carga y por cada resultado toma: date, Home_team, Away_team,Team, Scorer, Minute, Own_goal, Penalty
        """
        fsort = "goalscorers"

        resultsfile = cf.data_dir + 'Challenge-1/football/goalscorers-utf8-'+tamaño+'.csv'
        inputfile = csv.DictReader(
            open(resultsfile, encoding='utf-8'), restval="Desconocido")
        i = 1
        for scorer in inputfile:

            scorer["id"] = i
            scorer = clear_data(scorer,SCO_DTYPE)
            model.add_data(catalog['goalscorers'], scorer)
            i += 1
        sort(catalog, fsort)

        return model.data_size(catalog['goalscorers']), catalog['goalscorers']


    def load_shootouts(catalog, tamaño):

        """
        Carga y por cada resultado toma: date,home_team,away_team,winner
        """
        fsort = "shootouts"
        resultsfile = cf.data_dir + 'Challenge-1/football/shootouts-utf8-'+tamaño+'.csv'
        inputfile = csv.DictReader(
            open(resultsfile, encoding='utf-8'), restval="Desconocido")
        i = 1
        for shootout in inputfile:

            shootout["id"] = i
            shootout = clear_data(shootout,SHOOTOUT_DTYPE)
            model.add_data(catalog['shootouts'], shootout)
            i += 1
        sort(catalog, fsort)

        return model.data_size(catalog['shootouts']), catalog['shootouts']

    n_results, results = load_results(catalog, tamaño)
    n_goalscorers, goalscorers = load_goalscorers(catalog, tamaño)
    n_shootouts, shootouts = load_shootouts(catalog, tamaño)

    #Carga de mapas
    for result in lt.iterator(catalog["results"]):
        winner=model.decidir_ganador(result,catalog)
        model.add_result(catalog["mapResults"],result,winner)
        equipo=result["home_team"]
        model.add_equipo(catalog["equipos"],equipo,result,winner)
        equipo=result["away_team"]
        model.add_equipo(catalog["equipos"],equipo,result,winner)
        anio=result["date"].year
        model.add_anio_torneo(catalog["anio_torneo"],anio,result,winner)
        model.add_result_torneo(catalog,result)

        for scorer in lt.iterator(catalog["goalscorers"]):
            if scorer["date"] == result["date"] and scorer["home_team"] == result["home_team"] and scorer["away_team"] == result["away_team"]:
                model.add_scorer(catalog['scorer'], scorer, result)
                equipo=scorer["home_team"]
                model.add_goals(catalog['goals'], result, scorer,equipo)
                model.add_scorer_equipo(catalog["equipo_scorer"],scorer, result ,equipo)
                equipo=scorer["away_team"]
                model.add_goals(catalog['goals'], result, scorer,equipo)
                model.add_scorer_equipo(catalog["equipo_scorer"],scorer, result, equipo)
                model.add_scorer_torneo(catalog,scorer)

    stop_time = get_time()
    deltatime = delta_time(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()

        delta_memory = deltaMemory(start_memory, stop_memory)

        return deltatime, delta_memory,n_results, results, n_goalscorers, goalscorers, n_shootouts, shootouts
    else:

        return deltatime,n_results, results, n_goalscorers, goalscorers, n_shootouts, shootouts


#Añade la llave winner a results
def anadir_ganador (control):
    catalog = control['model']
    return model.anadir_ganador(catalog)

# Funciones de ordenamiento


def prepare_date(catalog):

    return model.prepare_date(catalog)


def sort(data_struct, fsort):
    """
    Ordena los datos del modelo
    """
    # TODO: Llamar la función del modelo para ordenar los datos
    model.sort(data_struct, fsort)


# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    # TODO: Llamar la función del modelo para obtener un dato
    return model.get_data(catalog, id)


def get_fl_three(data_structs):
    """
    Retorna los primeros y últimos 3 items de una lista
    """

    return model.first_three(data_structs), model.last_three(data_structs)


def req_1(control, numero, equipo, condicion):
    """
    Retorna el resultado del requerimiento 1
    """

    start_time = get_time()
    totalequipos,totalpartidos,totalcondicion,respuesta = model.req_1(
        control["model"], numero, equipo, condicion)
    end_time = get_time()
    deltaTime = delta_time(end_time, start_time)
    return totalequipos,totalpartidos,totalcondicion,respuesta, deltaTime


def req_2(control, name, cantidad):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = get_time()
    respuesta , num_partidos , total__scorers, penalty = model.req_2(control['model'], name, cantidad)
    end_time = get_time()
    deltaTime = delta_time(end_time, start_time)
    return respuesta , num_partidos , total__scorers, penalty, deltaTime


def req_3(equipo,fecha_inicial,fecha_final,control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3

    start_time = get_time()
    total,local,visitante,partidos = model.req_3(equipo,fecha_inicial,fecha_final,control["model"])
    end_time = get_time()
    deltaTime = delta_time(end_time, start_time)

    return total,local,visitante,partidos,deltaTime

def req_4(tournament, fecha_inicial, fecha_final, control):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = get_time()
    partidos, num_paises, num_ciudades, penalties, num_partidos, num_torneos = model.req_4(tournament, fecha_inicial, fecha_final, control["model"])
    end_time = get_time()
    deltaTime = delta_time(end_time, start_time)

    return partidos, num_paises, num_ciudades, penalties, num_partidos, num_torneos, deltaTime


def req_5(jugador, fecha_inicial, fecha_final, control):
    """
    Retorna el resultado del requerimiento 5
    """

    start_time = get_time()
    numero_jugadores,numero_goles, numero_torneos, penaltis, autogoles, goles = model.req_5(
        jugador, fecha_inicial, fecha_final, control["model"])
    end_time = get_time()
    deltaTime = delta_time(end_time,start_time)

    return numero_jugadores,numero_goles, numero_torneos, penaltis, autogoles, goles, deltaTime


def req_6(cantidad, torneo, anio, control):
    """
    Retorna el resultado del requerimiento 6
    """
    start_time = get_time()
    c_anios,c_torneos,c_equipos,c_partidos,total_paises,total_ciudades,max_ciudad, estadisticas = model.req_6(
        cantidad, torneo,anio, control["model"])
    end_time = get_time()
    deltaTime = delta_time(end_time,start_time)
    return c_anios,c_torneos,c_equipos,c_partidos,total_paises,total_ciudades,max_ciudad, estadisticas, deltaTime


def req_7(n_puntos, torneo, data_structs):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    num_torneos, num_scorers, num_partidos, num_goals, num_penalties, num_own_goals, jugadores = model.req_7(n_puntos, torneo, data_structs["model"])
    end_time = get_time()
    deltaTime = delta_time(end_time, start_time)

    return num_torneos, num_scorers, num_partidos, num_goals, num_penalties, num_own_goals, jugadores,deltaTime


def req_8(equipo1, equipo2, fecha_inicial, fecha_final,control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    start_time = get_time()
    datos_equipo1, datos_equipo2, ambos, estadisticas1, estadisticas2 = model.req_8(equipo1, equipo2, fecha_inicial, fecha_final,control["model"])
    #anios,estadisticas1,estadisticas2,home1,away1,home2,away2,ambos = model.req_8(equipo1, equipo2, fecha_inicial, fecha_final,control["model"])
    end_time = get_time()
    deltaTime = delta_time(start_time, end_time)

    return datos_equipo1, datos_equipo2, ambos, estadisticas1, estadisticas2, deltaTime

# Funciones para medir tiempos de ejecucion y memoria

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en kBytes (ej.: 2100.0 kB)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory


def sort_criteria(control, sort):
    """
    Ordena los libros por average_rating y toma el los tiempos en los
    que se inició la ejecución del requerimiento y cuando finalizó
    con getTime(). Finalmente calcula el tiempo que demoró la ejecución
    de la función con deltaTime()
    """
    # TODO completar los cambios del return en el sort para el lab 4 (Parte 2).
    start_time = get_time()
    sorted_list = model.sort_criteria(control["model"], sort)
    end_time = get_time()
    deltaTime = delta_time(start_time, end_time)

    return deltaTime, sorted_list

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


RESULT_DTYPE = {
    "id": int,
    "date": datetime,
    "home_team": str,
    "away_team": str,
    "home_score": int,
    "away_score": int,
    "tournament": str,
    "city": str,
    "country": str,
    "neutral": bool
}
SCO_DTYPE = {
    "date": datetime,
    "home_team": str,
    "away_team": str,
    "team": str,
    "scorer": str,
    "minute": float,
    "own_goal": bool,
    "penalty": bool
}
SHOOTOUT_DTYPE = {
    "date": datetime,
    "home_team": str,
    "away_team": str,
    "winner": str
}

def clear_data(data,dtype):
    for key , value in data.items():
        if key in dtype.keys():
            if key=="id":
                continue
            try:
                if value==None or value.strip()=="":
                    if  key == "date" :
                        format_data = datetime.datetime.strptime("1900-01-01", "%Y-%m-%d")
                    elif key in ("home_team","away_team","tournament","city","country","team","scorer","winner"):
                        format_data = "unknown"
                    elif key in ("home_score","away_score"):
                        format_data = -1
                    elif key in ("minute"):
                        format_data = -1.0
                    elif key in ("own_goal","penalty","neutral"):
                        format_data = False
                    else:
                        print("No se pudo convertir el valor de la llave",key,"con el valor",value)
                else:
                    if dtype [key] == str:
                        format_data = dtype[key](value)
                        format_data = format_data.strip().title()
                    elif dtype[key] == datetime and isinstance(value,str):
                        format_data = datetime.datetime.strptime(data[key], "%Y-%m-%d")
                    elif dtype[key] == int and isinstance(value,str):
                        format_data = dtype[key](value)
                    elif dtype[key] == float and isinstance(value,str):
                        format_data = dtype[key](value)
                    elif dtype[key] == bool and isinstance(value,str):
                        if value.lower()=="true":
                            format_data = "True"
                        else:
                            format_data = "False"
                    else:
                        print("No se pudo convertir el valor de la llave",key,"con el valor",value)
                data[key]=format_data
            except Exception as e:
                print(e)
                print("No se pudo convertir el valor de la llave",key,"con el valor",value)
                print("El tipo de dato esperado es",dtype[key])
                print(data)
    return data
