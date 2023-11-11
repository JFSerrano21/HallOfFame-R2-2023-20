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

import config as cf
import model
import time
import tracemalloc
import csv
csv.field_size_limit(2147483647)
import tracemalloc
import sys

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {'model': None}
    control['model'] = model.new_data_structs()
    return control


### Funciones para la carga de datos

def load_data(control, size, memflag):
    """
    Carga los datos del reto
    """
    data_structs = control['model']
    
    start_time = get_time()
    
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    
    
    r_size, r_columns = load_results_data(data_structs, size)
    g_size, g_columns = load_goalscorers_data(data_structs, size)
    s_size, s_columns = load_shootouts_data(data_structs, size)
    
    ti_r = get_time()
    model.sort(data_structs, 'results')
    tf_r = get_time()
    delta_t_r = delta_time(ti_r,tf_r)
    
    ti_g = get_time()
    model.sort(data_structs, 'goalscorers')
    tf_g = get_time()
    delta_t_g = delta_time(ti_g,tf_g)
    
    ti_s = get_time()
    model.sort(data_structs, 'shootouts')
    tf_s = get_time()
    delta_t_s = delta_time(ti_s,tf_s)
    
    # Ordenamiento de las estructuras de los requerimientos
    sizes = r_size, g_size, s_size
    columns =  r_columns, g_columns, s_columns
    time = delta_t_r, delta_t_g, delta_t_s
    
    # toma el tiempo al final del proceso
    stop_time = get_time()
    # calculando la diferencia en tiempo
    d_time = delta_time(start_time, stop_time)
    
    model.sort(data_structs, 'g_req7')
    
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        d_memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
        return sizes, columns, time, d_time, d_memory
    else:
        return sizes, columns, time, d_time, None

def load_results_data(data_structs, size):
    resultsfile = cf.data_dir + 'football/results-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(resultsfile, encoding='utf-8'))
    for result in input_file:
        model.add_data(data_structs, result, 'results')
        r_column = model.new_column_data(result)
    return model.data_size(data_structs, 'results'), r_column
    
def load_goalscorers_data(data_structs, size):
    goalscorersfile = cf.data_dir + 'football/goalscorers-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(goalscorersfile, encoding='utf-8'))
    for goalscorer in input_file:
        model.add_data(data_structs, goalscorer, 'goalscorers')
        g_column = model.new_column_data(goalscorer)
    return model.data_size(data_structs, 'goalscorers'), g_column
    
def load_shootouts_data(data_structs, size):
    shootoutsfile = cf.data_dir + 'football/shootouts-utf8-'+size+'.csv'
    input_file = csv.DictReader(open(shootoutsfile, encoding='utf-8'))
    for shootout in input_file:
        model.add_data(data_structs, shootout, 'shootouts')
        s_column = model.new_column_data(shootout)
    return model.data_size(data_structs, 'shootouts'), s_column

def create_data_list(sorted_list):
    new_list = model.new_top3bot3_sublist(sorted_list)
    return new_list


### Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


### Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


### Requerimientos

# REQ 1

def print_games_played(control,memflag,games,team,condition):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    data_structs = control['model']
    time = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    file = model.print_games_played(data_structs,games,team,condition)
    time_final = get_time()
    time_total = delta_time(time, time_final)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
    #print("TIME: ",time_total)
    #print("MEMORY: ",memory)     
    return file
    
    #return(file)


# REQ 2

def Goals_for_player(control,memflag,n_goals,player):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    data_structs = control['model']
    time = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    file = model.Goals_for_player(data_structs,n_goals,player)
    time_final = get_time()
    time_total = delta_time(time, time_final)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
    #print("TIME: ",time_total)
    #print("MEMORY: ",memory)   
    return file


# REQ 3

def Consult_Period_Matches(control,memflag,team,start_date,end_date):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    data_structs = control['model']
    time = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    file = model.Consult_Period_Matches(data_structs,team,start_date,end_date)
    time_final = get_time()
    time_total = delta_time(time, time_final)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
    #print("TIME: ",time_total)
    #print("MEMORY: ",memory)    
    return file

# REQ 4

def tournament_matches(control, tournament, start_date, end_date, memflag):
    """
    Retorna el resultado del requerimiento 4
    """
    # Modificar el requerimiento 4
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    matches_list, count = model.tournament_matches(data_structs, tournament, start_date, end_date)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    if model.data_size(matches_list) <= 6:
        return matches_list, None, count, time, memory
    else:
        return matches_list, model.new_top3bot3_sublist(matches_list), count, time, memory
    

# REQ 5

def req_5(control, scorer, start_date, end_date, memflag):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
        
    goals_list, contadores = model.req_5(data_structs, scorer, start_date, end_date)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
        
    if model.data_size(goals_list) <= 6:
        return goals_list, None, contadores, time, memory
    else:
        return goals_list, model.new_top3bot3_sublist(goals_list), contadores, time, memory


# REQ 6

def classify_teams(control, n, tournament, year, memflag):
    """
    Retorna el resultado del requerimiento 6
    """
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    
    top_n_classified_teams, count, popular_city = model.classify_teams(data_structs, n, tournament, year)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
    
    if model.data_size(top_n_classified_teams) <= 6:
        return top_n_classified_teams, None, count, popular_city, time, memory
    else:
        return top_n_classified_teams, model.new_top3bot3_sublist(top_n_classified_teams), count, popular_city, time, memory


# REQ 7

def top_scorers(control, tournament, n, memflag):
    """
    Retorna el resultado del requerimiento 7
    """
    data_structs = control['model']
    
    ti = get_time()
    if memflag == True:
        tracemalloc.start()
        start_memory = get_memory()
    
    top_n_scorers, count = model.top_scorers(data_structs, tournament, n)
    
    tf = get_time()
    time = delta_time(ti, tf)
    if memflag == True:
        stop_memory = get_memory()
        tracemalloc.stop()
        # calcula la diferencia de memoria
        memory = delta_memory(stop_memory, start_memory)
        # respuesta con los datos de tiempo y memoria
    else:
        memory = None
    
    
    if model.data_size(top_n_scorers) <= 6:
        return top_n_scorers, None, count, time, memory
    else:
        return top_n_scorers, model.new_top3bot3_sublist(top_n_scorers), count, time, memory


# REQ 8

def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


### Funciones para medir tiempos de ejecucion

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