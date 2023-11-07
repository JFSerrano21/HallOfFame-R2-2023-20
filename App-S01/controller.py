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

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(type_scorers, loadfactor_scorers):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {'model': None}
    control['model'] = model.new_historial_FIFA(type_scorers, loadfactor_scorers)
    return control


# Funciones para la carga de datos

def load_data(control, tamanio, memory=False):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    time_i = get_time()
    if memory:
        tracemalloc.start()
        memory_i = get_memory()
    historial_FIFA = control["model"]
    load_goals_map(historial_FIFA, tamanio)
    shootouts = load_shootouts(historial_FIFA, tamanio)
    results = load_results(historial_FIFA, tamanio)
    goalscorers, scorers = load_goals(historial_FIFA, tamanio)
    time_f = get_time()
    time = delta_time(time_i,time_f)
    if memory:
        memory_f = get_memory()
        tracemalloc.stop()
        memory = delta_memory(memory_f, memory_i)
        return results, goalscorers, shootouts, scorers, time, memory
    return results, goalscorers, shootouts, scorers, time
    
def load_results(historial_FIFA, tamanio):
    """
    Carga los resultados del archivo de results.
    """
    archivo = "football/results-utf8-" + str(tamanio) + ".csv"
    results_file = cf.data_dir + archivo
    input_file = csv.DictReader(open(results_file, encoding="utf8"))
    for result in input_file:
        model.add_result(historial_FIFA, result)
    historial_FIFA = model.ordenar_partidos(historial_FIFA)
    
    return historial_FIFA['results']

def load_goals_map(historial_FIFA, tamanio):
    archivo = 'football/goalscorers-utf8-' + str(tamanio) + '.csv'
    goals_file = cf.data_dir + archivo
    input_file = csv.DictReader(open(goals_file, encoding='utf8'))
    for goal in input_file:
        model.add_goal_map(historial_FIFA, goal)

def load_goals(historial_FIFA, tamanio):
    archivo = 'football/goalscorers-utf8-' + str(tamanio) + '.csv'
    goals_file = cf.data_dir + archivo
    input_file = csv.DictReader(open(goals_file, encoding='utf8'))
    for goal in input_file:
        model.add_goal(historial_FIFA, goal)
    model.ordenar_goles(historial_FIFA)
    return historial_FIFA['goalscorers'], historial_FIFA['scorers']

def load_shootouts(historial_FIFA, tamanio):
    shoots_file = cf.data_dir + 'football/shootouts-utf8-' + str(tamanio) + '.csv'
    input_file = csv.DictReader(open(shoots_file, encoding='utf8'))
    for shoot in input_file:
        model.add_shootout(historial_FIFA, shoot)
    historial_FIFA = model.ordenar_penales(historial_FIFA)
    return historial_FIFA['shootouts']

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, equipo , condicion , num_partidos, memoria):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    

    d_memory = False
   
    if memoria:
        tracemalloc.start()
        memoria_i = get_memory()
    time_i = get_time()
    num_equipos_total , num_partidos_equipo , num_partidos_condicion , lista_final = model.req_1(control["model"], equipo , condicion , num_partidos)
    time_f = get_time()
    d_time = delta_time(time_i, time_f)
    if memoria:
        memoria_f = get_memory()
        tracemalloc.stop()
        d_memory = delta_memory(memoria_f, memoria_i)
    return num_equipos_total , num_partidos_equipo , num_partidos_condicion , lista_final,  d_time, d_memory




def req_2(control, n_goles , jugador, memoria ):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    d_memory = False
   
    if memoria:
        tracemalloc.start()
        memoria_i = get_memory()
    time_i = get_time()
    n_jugadores_total , n_anotaciones_jugador, n_anotaciones_penalty , anotaciones_jugador = model.req_2(control["model"],n_goles , jugador,)
    time_f = get_time()
    d_time = delta_time(time_i, time_f)
    if memoria:
        memoria_f = get_memory()
        tracemalloc.stop()
        d_memory = delta_memory(memoria_f, memoria_i)

    return n_jugadores_total , n_anotaciones_jugador, n_anotaciones_penalty , anotaciones_jugador , d_time, d_memory


def req_3(control, equipo , f_inicial , f_final , memoria):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    
    d_memory = False
   
    if memoria:
        tracemalloc.start()
        memoria_i = get_memory()
    time_i = get_time()
    num_equipos_total , total_partidos_equipo,num_partidos_local , num_partidos_visitante  , lista_final_req3= model.req_3(control["model"],equipo , f_inicial , f_final )
    time_f = get_time()
    d_time = delta_time(time_i, time_f)
    if memoria:
        memoria_f = get_memory()
        tracemalloc.stop()
        d_memory = delta_memory(memoria_f, memoria_i)
    
    return num_equipos_total , total_partidos_equipo,num_partidos_local , num_partidos_visitante  , lista_final_req3, d_time, d_memory


def req_4(control, torneo, fecha_i, fecha_f, memoria):
    """
    Retorna el resultado del requerimiento 4
    """
    d_memory = False
    # TODO: Modificar el requerimiento 4,
    if memoria:
        tracemalloc.start()
        memoria_i = get_memory()
    time_i = get_time()
    total_torneos, total_paises, total_ciudades, penales, partidos_en_fecha = model.req_4(control["model"], torneo, fecha_i, fecha_f)
    time_f = get_time()
    d_time = delta_time(time_i, time_f)
    if memoria:
        memoria_f = get_memory()
        tracemalloc.stop()
        d_memory = delta_memory(memoria_f, memoria_i)
    return total_torneos,  total_paises, total_ciudades, penales, partidos_en_fecha, d_time, d_memory



def req_5(control, jugador, fecha_i, fecha_f, memoria):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    d_memoria= False
    if memoria:
        tracemalloc.start()
        memory_i= get_memory()
    tiempo_i= get_time()
    t_jugadores_anot, num_anot, num_torn, num_penal, num_auto, listado= model.req_5(control["model"], jugador, fecha_i, fecha_f)
    tiempo_f= get_time()
    d_tiempo= delta_time(tiempo_i, tiempo_f)
    if memoria:
        memory_f= get_memory()
        tracemalloc.stop()
        d_memoria= delta_memory(memory_f, memory_i)
        
    return t_jugadores_anot, num_anot, num_torn, num_penal, num_auto, listado, d_memoria, d_tiempo


def req_6(control, torneo, n, anio, memory):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    d_memoria= False
    if memory:
        tracemalloc.start()
        memory_i= get_memory()
    tiempo_i= get_time()
    t_anios, t_torneos, t_eq_torn, t_match_anio, t_match_torneo, t_paises, t_ciudades, max_ciudad, top_equipos = model.req_6(control["model"], torneo, n, anio)
    tiempo_f= get_time()
    d_tiempo= delta_time(tiempo_i, tiempo_f)
    if memory:
        memory_f= get_memory()
        tracemalloc.stop()
        d_memoria= delta_memory(memory_f, memory_i)
        
    return t_anios, t_torneos, t_eq_torn, t_match_anio, t_match_torneo, t_paises, t_ciudades, max_ciudad, top_equipos, d_tiempo, d_memoria


def req_7(control, torneo, puntos, memoria):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    d_memory = False
    if memoria:
        tracemalloc.start()
        memoria_i = get_memory()
    time_i = get_time()
    total_torneos, total_anotadores, total_encuentros, total_anotaciones, total_penales, total_autogoles, goleadores_filtrados = model.req_7(control["model"], torneo, puntos)
    time_f = get_time()
    d_time = delta_time(time_i, time_f)
    if memoria:
        memoria_f = get_memory()
        tracemalloc.stop()
        d_memory = delta_memory(memoria_f, memoria_i)
    return total_torneos, total_anotadores, total_encuentros, total_anotaciones, total_penales, total_autogoles, goleadores_filtrados, d_time, d_memory


def req_8(control, equipo, anio_i, anio_f, memoria):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    d_memory = False
    if memoria:
        tracemalloc.start()
        memoria_i = get_memory()
    time_i = get_time()
    total_partidos, total_local, total_visitante, fecha_antiguo, ultimo_partido, anios_filtrados = model.req_8(control["model"], equipo, anio_i, anio_f)
    time_f = get_time()
    d_time = delta_time(time_i, time_f)
    if memoria:
        memoria_f = get_memory()
        tracemalloc.stop()
        d_memory = delta_memory(memoria_f, memoria_i)
    return total_partidos, total_local, total_visitante, fecha_antiguo, ultimo_partido, anios_filtrados, d_time, d_memory


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

