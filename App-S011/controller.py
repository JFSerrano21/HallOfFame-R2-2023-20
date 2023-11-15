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
import csv
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from tabulate import tabulate
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model':None
    }
    control['model']=model.new_data_structs()
    return control


# Funciones para la carga de datos
def load_data(control, data_size):
    #Indica la ruta de los archivos
    """ tracemalloc.start()
    start_memory = get_memory()
 """
    filegoalscorers = load_goal_scorers(data_size)
    fileresults = load_results(data_size)
    fileshootouts = load_shootouts(data_size)

    #Carga los datos y los ordena
    load_data_mask(control['model'], filegoalscorers, fileresults, fileshootouts)
    model.sort(control['model'])

    results = control['model']['results']
    scores = control['model']['goal_scorers']
    shootouts= control['model']['shootouts']
    

    #Listas donde se guardarán los años presentes en el archivo de partidos y penalties.
    r_dates= model.keys_to_array(results)
    s_dates = model.keys_to_array(shootouts)
    sc_dates = model.keys_to_array(scores)

    #Ordena los años de más reciente a más antiguo
    model.sort_dates_new_first(r_dates)
    model.sort_dates_new_first(s_dates)
    model.sort_dates_new_first(sc_dates)
    
    #Mira el número de partidos y penalties
    n_results= model.n_elements(results, r_dates)
    n_shootouts=model.n_elements(shootouts, s_dates)
    n_scores=model.n_elements(scores, sc_dates)
    
    #Retorna 3 primeros y 3 últimos elementos
    return_results=model.first_last_three_elems(results, r_dates, n_results)
    return_shootouts=model.first_last_three_elems(shootouts, s_dates, n_shootouts)
    return_scores = model.first_last_three_elems(scores, sc_dates, n_scores)

    """ stop_memory = get_memory()
    tracemalloc.stop()
    delta_m = delta_memory(stop_memory, start_memory) """

    return return_scores, return_results, return_shootouts, n_results, n_shootouts, n_scores
    
def load_data_lab7(control, maptype, loadfactor, memflag):
        try: 
            start_time = get_time()
            if memflag:
                tracemalloc.start()
                start_memory = get_memory() 
                
            data_structs = model.scorers_lab7(control['model'], maptype, loadfactor)
            model.add_scorer(data_structs)
            scorers_size = mp.size(data_structs["scorers_lab"])
            scorers_values = mp.valueSet(data_structs["scorers_lab"])
            #Devuelve 6 elementos en caso de que haya más de ello
            return_scorers= model.elements_lab7(scorers_values, scorers_size)

            stop_time = get_time()
            delta_t = delta_time(start_time, stop_time)

            if memflag:
                stop_memory = get_memory()
                tracemalloc.stop()
                delta_m = delta_memory(stop_memory, start_memory)
                return return_scorers, delta_t, delta_m
            return return_scorers, delta_t, []
        except:
            print("Antes de ejecutar la carga de datos del laboratorio 7, asegúrate de primero ejecutar la función 1 (carga de datos)")
            

def load_data_mask(control, filegoalscorers, fileresults, fileshootouts):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    archivos =lt.newList()
    lt.addLast(archivos,fileresults)
    lt.addLast(archivos,filegoalscorers)
    lt.addLast(archivos,fileshootouts)
    for archivo in lt.iterator(archivos):
        file = cf.data_dir  + archivo
        input_file = csv.DictReader(open(file, encoding='utf-8'))
        if "goalscorers" in archivo:
            llave = "goal_scorers"
        elif "results" in archivo: 
            llave = "results"
        else: 
            llave = "shootouts"
        for dato in input_file:
            
            model.addData(control, dato, llave)
            
def load_goal_scorers(data_size):
    if data_size==1:
     scores_file =  'goalscorers-utf8-small.csv'
    elif data_size==2:
        scores_file =  'goalscorers-utf8-5pct.csv'
    elif data_size==3:
        scores_file =  'goalscorers-utf8-10pct.csv'
    elif data_size==4:
        scores_file =  'goalscorers-utf8-20pct.csv'
    elif data_size==5:
        scores_file =   'goalscorers-utf8-30pct.csv'
    elif data_size==6:
        scores_file =   'goalscorers-utf8-50pct.csv'
    elif data_size==7:
        scores_file =  'goalscorers-utf8-80pct.csv'
    elif data_size==8:
        scores_file =  'goalscorers-utf8-large.csv'
    return scores_file

def load_shootouts(data_size):
    if data_size==1:
     file =  'shootouts-utf8-small.csv'
    elif data_size==2:
        file =  'shootouts-utf8-5pct.csv'
    elif data_size==3:
        file =  'shootouts-utf8-10pct.csv'
    elif data_size==4:
        file =  'shootouts-utf8-20pct.csv'
    elif data_size==5:
        file =  'shootouts-utf8-30pct.csv'
    elif data_size==6:
        file =  'shootouts-utf8-50pct.csv'
    elif data_size==7:
        file =  'shootouts-utf8-80pct.csv'
    elif data_size==8:
        file =  'shootouts-utf8-large.csv'
    return file

def load_results(data_size):
    
    if data_size==1:
        match_file =  'results-utf8-small.csv'
    elif data_size==2:
        match_file = 'results-utf8-5pct.csv'
    elif data_size==3:
        match_file = 'results-utf8-10pct.csv'
    elif data_size==4:
        match_file =  'results-utf8-20pct.csv'
    elif data_size==5:
        match_file = 'results-utf8-30pct.csv'
    elif data_size==6:
        match_file = 'results-utf8-50pct.csv'
    elif data_size==7:
        match_file = 'results-utf8-80pct.csv'
    elif data_size==8:
        match_file = 'results-utf8-large.csv'
    return match_file


""" def load_goal_scorers(n_d, filename):
    goals_file = cf.data_dir  +filename
    input_file = csv.DictReader(open(goals_file, encoding='utf-8'))
    
    for goals in input_file:
        model.addData(n_d, goals)
    
    return model.dataSize(n_d)
def load_results(n_d, filename):
    resultsfile = cf.data_dir + filename
    input_file = csv.DictReader(open(resultsfile, encoding='utf-8'))
    for results in input_file:
        model.addData(n_d, results)
    return model.dataSize(n_d)


def load_shootouts(n_d, filename):
    shootoutsfile = cf.data_dir  + filename
    input_file = csv.DictReader(open(shootoutsfile, encoding='utf-8'))
    for shootout in input_file:
        model.addData(n_d, shootout)
    return model.dataSize(n_d) """


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo




def req_1(control,team, condition, numero):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    if condition =="indiferent":
        condition= "MatchResults"
    resultados,total_teams,total_partidos= model.req_1(control,team,condition)
    if resultados!= "El equipo no tiene partidos en esa condicion":
        Forcondition= lt.size(resultados)
        resultado=resultados
        if Forcondition>=numero:
            resultado= lt.subList(resultados,1,numero)
        tamano=lt.size(resultado)
        if tamano> 6:
            stop_time = get_time()
            delta_times = delta_time(start_time,stop_time)
            return model.get_data_3(resultado,tamano),total_teams,total_partidos,Forcondition,delta_times
        stop_time = get_time()
        delta_times = delta_time(start_time,stop_time)
        return resultado,total_teams,total_partidos,Forcondition,delta_times
    stop_time = get_time()
    delta_times = delta_time(start_time,stop_time)
    return resultados,0,0,0,delta_times

    


def req_2(control, nombre,cant_goles):
    """
    Retorna el resultado del requerimiento 2

    """
    goles, n_goles, n_penalties, total_scorers = model.req_2(control["model"], nombre, cant_goles)
    if goles=="El jugador no existe":
        return goles
    respuesta = lt.newList("ARRAY_LIST")

    if lt.size(goles) > 6:
        primeros_tres = lt.subList(goles, 1 , 3)
        ultimos_tres = lt.subList(goles, lt.size(goles) - 3, 3)
        for cada in lt.iterator(primeros_tres):
            lt.addLast(respuesta, cada)
        for cada in lt.iterator(ultimos_tres):
            lt.addLast(respuesta, cada)
    else:
        respuesta=goles
                
    return respuesta, n_goles, n_penalties, total_scorers


def req_3(control,date_inicial,date_final,team):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    away,home,ambos, todos,lista=model.req_3(control,date_inicial,date_final,team)
    if ambos>6:
        stop_time = get_time()
        delta_times = delta_time(start_time,stop_time)
        return model.get_data_3(lista,ambos),away,home,ambos,todos,delta_times
    stop_time = get_time()
    delta_times = delta_time(start_time,stop_time)
    return lista,away,home,ambos,todos,delta_times

    # TODO: Modificar el requerimiento 3
    pass


def req_4(control, tournament, start_d, end_d):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time = get_time()
    elems, n_tournaments, n_matches, n_countries, n_cities, n_shootouts = model.req_4(control['model'], tournament,start_d, end_d)
    ans_list = lt.newList("ARRAY_LIST")
    if lt.size(elems) > 6:
        first_3 = lt.subList(elems, 1 , 3)
        last_3 = lt.newList("ARRAY_LIST")
        length=lt.size(elems)
        for x in range(length-2,length+1):
            lt.addLast(last_3, lt.getElement(elems, x))
        for each in lt.iterator(first_3):
            lt.addLast(ans_list, each)
        for each in lt.iterator(last_3):
            lt.addLast(ans_list, each)
    else:
        ans_list = elems
    return_list = [x for x in lt.iterator(ans_list)]
    stop_time = get_time()
    delta_times = delta_time(start_time,stop_time)
    return return_list, n_tournaments, n_matches, n_countries, n_cities, n_shootouts,delta_times


def req_5(control, nombre, fecha_inicio, fecha_final):
    """
    Retorna el resultado del requerimiento 5
    """
    respuesta = lt.newList("ARRAY_LIST")
    periodo,total_scorers,total_anotaciones_jugador,total_torneos,total_penalty,total_autogol = model.req_5(control["model"], nombre, fecha_inicio, fecha_final)
    if periodo == "No se encuentran anotaciones realizadas por este jugador en el periodo de tiempo dado.":
        return periodo,total_scorers,total_anotaciones_jugador,total_torneos,total_penalty,total_autogol
    
    elif lt.size(periodo) > 6:
        primeros_tres = lt.subList(periodo, 1 , 3)
        ultimos_tres = lt.subList(periodo, lt.size(periodo) - 3, 3)
        for cada in lt.iterator(primeros_tres):
            lt.addLast(respuesta, cada)
        for cada in lt.iterator(ultimos_tres):
            lt.addLast(respuesta, cada)
    else:
        respuesta=periodo
                
    return respuesta,total_scorers,total_anotaciones_jugador,total_torneos,total_penalty,total_autogol 
    
    # TODO: Modificar el requerimiento 5
    

def req_6(control,n_teams, tournament, year):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = get_time()
    elems,total_years, total_tournaments, n_teams_y, total_matches, n_countries, n_cities, pop_city  = model.req_6(control['model'], int(n_teams), tournament, int(year))
    
    ans_list = lt.newList("ARRAY_LIST")
    if lt.size(elems) > 6:
        first_3 = lt.subList(elems, 1 , 3)
        last_3 = lt.subList(elems, lt.size(elems) - 3, 3)
        for each in lt.iterator(first_3):
            lt.addLast(ans_list, each)
        for each in lt.iterator(last_3):
            lt.addLast(ans_list, each)
    else:
        ans_list = elems
    
    return_list = [dict(x) for x in lt.iterator(ans_list)]
    for x in return_list:
        top_scorer = model.values_to_array(x['top_scorer'])
        model.sort_players_req6(top_scorer)
        first_el = lt.getElement(top_scorer, 1)
        x['top_scorer']= tabulate([first_el],headers="keys",tablefmt="grid")
        x.pop('match_info')
    stop_time = get_time()
    delta_times = delta_time(start_time,stop_time)
    return return_list,total_years, total_tournaments, n_teams_y, total_matches, n_countries, n_cities, pop_city,delta_times

def req_7(control,torneo,numero):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time = get_time()
    total_tourn,total_scorers,total_matches,goals,penalties,autogoles,resultado=model.req_7(control,torneo,numero)
    total_player=lt.size(resultado)
    if total_player>6:
        stop_time = get_time()
        delta_times = delta_time(start_time,stop_time)
        return model.get_data_3(resultado,total_player),total_tourn,total_scorers,total_matches,goals,penalties,autogoles,total_player,delta_times
    stop_time = get_time()
    delta_times = delta_time(start_time,stop_time)
    return resultado,total_tourn,total_scorers,total_matches,goals,penalties,autogoles,total_player,delta_times


def req_8(control, team, start_y, end_y):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    start_time = get_time()
    elems, n_years, total_matches, home_matches, away_matches, oldest_date, newest_match = model.req_8(control['model'],team, start_y, end_y)
    ans_list = lt.newList("ARRAY_LIST")
    if lt.size(elems) > 6:
        first_3 = lt.subList(elems, 1,3)
        last_3 = lt.newList("ARRAY_LIST")
        length=lt.size(elems)
        
        
        for x in range(length-2,length+1):
            lt.addLast(last_3, lt.getElement(elems, x))
        for each in lt.iterator(first_3):
            lt.addLast(ans_list, each)
        for each in lt.iterator(last_3):
            lt.addLast(ans_list, each)
    else:
        ans_list = elems

    return_list = [dict(x) for x in lt.iterator(ans_list)]
    for x in return_list:
        if lt.size(x['top_scorer']):
            top_scorer = model.values_to_array(x['top_scorer'])
            model.sort_players_req6(top_scorer)
            first_el = dict(lt.getElement(top_scorer, 1))
            first_el.pop('match_dates')
            
            x['top_scorer']= tabulate([first_el],headers="keys",tablefmt="grid")
        else:
            x['top_scorer']='No scorer data available'
    stop_time = get_time()
    delta_times = delta_time( start_time,stop_time)
    return return_list, n_years, total_matches, home_matches, away_matches, oldest_date, newest_match,delta_times
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