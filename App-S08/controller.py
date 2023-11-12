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

# =================================# =================================
# Funciones para la carga de datos
# =================================
# =================================
def loadData(control, SizeResults, SizeGoalscorers, SizeShootouts):
    """
    Carga los datos del reto
    """
    #se llaman las funciones de carga de los 3 archivos
    loadResults(control, SizeResults)
    loadGoalscorers(control, SizeGoalscorers)
    loadShootouts(control, SizeShootouts)
    model.sort(control['model'])
    return control
    
def loadResults(control, SizeResults):
    """
    Carga los datos del archivo Results
    """
    resultsfile = cf.data_dir + 'results-utf8-' + SizeResults
    input_file = csv.DictReader(open(resultsfile, encoding='utf-8'))
    for result in input_file:
        model.addResult(control['model'], result)

def loadGoalscorers(control,SizeGoalscorers):
    """
    Carga los datos del archivo Goalscorers
    """
    goalscorersfile = cf.data_dir + 'goalscorers-utf8-' + SizeGoalscorers
    input_file = csv.DictReader(open(goalscorersfile, encoding='utf-8'))
    for goalscorer in input_file:
        model.addGoalscorer(control['model'], goalscorer)

def loadShootouts(control, SizeShootouts):
    """
    Carga los datos del archivo Shootouts
    """
    shootoutsfile = cf.data_dir + 'shootouts-utf8-' + SizeShootouts
    input_file = csv.DictReader(open(shootoutsfile, encoding='utf-8'))
    for shootout in input_file:
        model.addShootout(control['model'], shootout)
    
# =========================
# Funciones tamaños listas 
# =========================
def SizeList(control,key):
    return model.SizeList(control['model'],key)


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


def req_1(control, n, country, condicion):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = get_time()
    rta=model.req_1(control['model'], n, country, condicion)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)
    return rta, deltatime


def req_2(control, n, jugador):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = get_time()
    rta=model.req_2(control["model"],n,jugador)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)
    return rta, deltatime


def req_3(control, nombre, fecha_1, fecha_2):
    """
    Retorna el resultado del requerimiento 3
    """
    lista_1=fecha_1.split("-")
    date_1=int((lista_1[0]+lista_1[1]+lista_1[2]))

    lista_2=fecha_2.split("-")
    date_2=int((lista_2[0]+lista_2[1]+lista_2[2]))

    start_time = get_time()
    rta=model.req_3(control['model'], nombre, date_1, date_2)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)

    return rta, deltatime


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(control, nombre, fecha_1, fecha_2):
    """
    Retorna el resultado del requerimiento 5
    """
    lista_1=fecha_1.split("-")
    date_1=int((lista_1[0]+lista_1[1]+lista_1[2]))

    lista_2=fecha_2.split("-")
    date_2=int((lista_2[0]+lista_2[1]+lista_2[2]))

    start_time = get_time()
    rta=model.req_5(control['model'], nombre, date_1, date_2)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)

    return rta, deltatime

def req_6(control, torneo, fecha, n_equipos):
    """
    Retorna el resultado del requerimiento 6
    """

    start_time = get_time()
    rta=model.req_6(control['model'], torneo, fecha,n_equipos)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)

    return rta, deltatime


def req_7(control, torneo, n):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    rta=model.req_7(control['model'], torneo, n)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)

    return rta, deltatime


def req_8(control, nombre, fecha_1, fecha_2):
    """
    Retorna el resultado del requeriemiento 8
    """
    start_time = get_time()
    rta=model.req_8(control['model'],nombre, fecha_1, fecha_2)
    end_time = get_time()
    deltatime = delta_time(start_time, end_time)

    return rta, deltatime

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

# ===============================================
# Funcion tiempo de ejecucion carga datos al mapa
# ===============================================

def MemoryMap(control,SizeGoalscorers):
    tracemalloc.start()
    initial=get_memory()
    #LoadDataScorers(control,SizeGoalscorers)
    final=get_memory()
    tracemalloc.stop()
    deltamemory=delta_memory(final,initial)
    return deltamemory

def TimeMap(control,SizeGoalscorers):
    start=get_time()
    #LoadDataScorers(control,SizeGoalscorers)
    end=get_time()
    deltatime=delta_time(start, end)
    return deltatime