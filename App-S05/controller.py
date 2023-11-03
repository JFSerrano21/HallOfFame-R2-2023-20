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
from DISClib.ADT import list as lt
import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(struc_list,struc_map,load_factor):
    """
    Crea una instancia del modelo
    """
    control = {
        "model": None
    }
    control["model"] = model.new_data_structs(struc_list,struc_map,load_factor)
    return control


# Funciones para la carga de datos

def load_data(control, size, memflag):
    """
    Carga los datos del reto
    """
    football_data = control["model"]
    match_results = loadResults(football_data, size)
    shootouts = loadShootouts(football_data, size)
    goal_scorers = loadGoalScorers(football_data, size)
    #Medicion inicial de tiempo y memoria
    start_time = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()
    #ejecucion principal
    loadScorers(football_data, size)
    #Medicion final de tiempo y memoria
    stop_time = get_time()
    delta_time_value = delta_time(start_time,stop_time)
    
    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        delta_memory_value = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return match_results, goal_scorers, shootouts, delta_time_value, delta_memory_value
    else:
        # respuesta sin medir memoria
        return match_results, goal_scorers, shootouts, delta_time_value

def loadResults(football_data, size):
    texto = "football/results-utf8-" +str(size)+".csv"
    footballfile = cf.data_dir + texto
    input_file = csv.DictReader(open(footballfile, encoding='utf-8'))
    for result in input_file:
        model.add_result(football_data, result, "match_results")
        #Mapa Jugadores
        model.add_MapResult(football_data, result, result["home_team"], result["away_team"], "Result")
        #Mapa Torneos
        model.add_MapTournament(football_data, result, result["tournament"])
        #Mapa Req 8
        año = result["date"]
        año = año[0:4]
        model.add_MapReq8(football_data, result, result["home_team"], result["away_team"], año)
        
        model.add_idResults(football_data,result)
       #Mapa Dates
        date = result['date']
        model.add_MapYears(football_data, result, date[:4])
        
    return model.data_size(football_data["match_results"])

def loadGoalScorers(football_data, size):
    texto = "football/goalscorers-utf8-" +str(size)+".csv"
    footballfile = cf.data_dir +texto
    input_file = csv.DictReader(open(footballfile, encoding='utf-8'))
    for GoalScorer in input_file:
        model.add_result(football_data, GoalScorer, "goal_scorers")
        #Mapa
        model.add_MapResult(football_data, GoalScorer, GoalScorer["home_team"], GoalScorer["away_team"], "GoalScorer")
        año = GoalScorer["date"]
        año = año[0:4]
        model.add_map_Req8_GoalScorers(football_data, GoalScorer, GoalScorer["home_team"], GoalScorer["away_team"], año)
        
        model.add_idGoalscorers(football_data,GoalScorer)
        #mapa DAtes
        model.add_MapDatesScores(football_data, GoalScorer, GoalScorer['date'])
    return model.data_size(football_data["goal_scorers"])
#
def loadShootouts(football_data, size):
    texto = "football/shootouts-utf8-" +str(size)+".csv"
    footballfile = cf.data_dir + texto
    input_file = csv.DictReader(open(footballfile, encoding='utf-8'))
    for Shootout in input_file:
        model.add_result(football_data, Shootout,"shootouts")
        #Mapa
        model.add_MapResult(football_data, Shootout, Shootout["home_team"], Shootout["away_team"], "Shootout")

    return model.data_size(football_data["shootouts"])

def loadScorers(football_data, size):
    texto = "football/goalscorers-utf8-" +str(size)+".csv"
    footballfile = cf.data_dir +texto
    input_file = csv.DictReader(open(footballfile, encoding='utf-8'))
    for datos in input_file:
        GoalScorer = datos["scorer"]
        model.add_Scorer(football_data, datos, GoalScorer)

# Funciones de ordenamiento

def sort(control, metodo):
    """
    Ordena los datos del modelo
    """
    start_time = get_time()
    model.sort(control["model"], metodo)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return delta_t


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def get_firts_and_last_3(control, type):
    datos = model.get_firts_and_last_3(control,type)
    return datos

def req_1(control,num,equipo,condicion):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    SubListN, total_equipos, total_partidos, total_condicion = model.req_1(control,num,equipo,condicion)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return SubListN, total_equipos, total_partidos, total_condicion, delta_t
   


def req_2(control,num,jugador):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    resultados = model.req_2(control,num,jugador)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return resultados, delta_t

def  req_3(control, Equipo, Inicio, Final):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    respuesta = model.req_3(control, Equipo, Inicio, Final)
    end_time = get_time() 
    delta_t = delta_time(start_time, end_time)
    total_games = lt.size(respuesta[0])
    respuesta_lista = respuesta[0]
    if total_games > 7:
        respuesta_lista = lt.newList("ARRAY_LIST")
        for i in range(1,4):
            lt.addLast(respuesta_lista, lt.getElement(respuesta[0], i))
        for i in range(1,4):
            lt.addLast(respuesta_lista, lt.getElement(respuesta[0], total_games-3+i))
    i = 0
    lista_final = []
    for dict in lt.iterator(respuesta_lista):
        valores = list(dict.values())
        lista_final.append(valores)
        
    return lista_final, respuesta[1], respuesta[2], delta_t


def req_4(control,torneo,inicio,final):
    """
    Retorna el resultado del requerimiento 4
    """
    resultados = model.req_4(control,torneo,inicio,final)
    
    return resultados


def req_5(control, player, Inicio, Final):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time = get_time()
    returns = model.req_5(control, player, Inicio, Final)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return returns
    
def req_6(control, torneo, año, n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = get_time()
    data, años, torneos, equipos, partidos, countries, citiesUniqueN, mostPopCity = model.req_6(control, torneo, año, n)
    end_time = get_time()
    delta_t = delta_time(start_time, end_time)
    return data, años, torneos, equipos, partidos, countries, citiesUniqueN, mostPopCity


def req_7(control,torneo,puntos):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time = get_time()
    resultados = model.req_7(control,torneo,puntos)
    end_time = get_time() 
    delta_t = delta_time(start_time, end_time)
    print('El tiempo que duro el programa fue de: '+ str(round(delta_t,2)) + ' milisegundos')
    return resultados

def req_8(control, Equipo, Inicio, Final):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    respuesta = model.req_8(control, Equipo, Inicio, Final)
    end_time = get_time() 
    delta_t = delta_time(start_time, end_time)
    años = int(Final[0:4]) - int(Inicio[0:4]) + 1
    total_games = lt.size(respuesta[0])
    respuesta_lista = lt.newList("ARRAY_LIST")
    if total_games > 7:
        for i in range(1,4):
            lt.addLast(respuesta_lista, lt.getElement(respuesta[0], i))
        for i in range(1,4):
            lt.addLast(respuesta_lista, lt.getElement(respuesta[0], total_games-3+i))
    i = 0
    lista_final = []
    for dict in lt.iterator(respuesta_lista):
        for goleador in lt.iterator(dict['top_scorer']):
            valores_goleador = list(goleador.values())
            dict['top_scorer'] = [valores_goleador]
        valores = list(dict.values())
        lista_final.append(valores)
    last_game = list(respuesta[1].values())
    last_game = last_game[:-1]
    last_game = [last_game]
    años = int(Final[0:4]) - int(Inicio[0:4]) + 1
    return lista_final, last_game, respuesta[2], respuesta[3], años, delta_t

# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
