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
csv.field_size_limit(2147483647)



def new_controller(tipo_mapa,load_factor):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs(tipo_mapa,load_factor)
    return control


# Funciones para la carga de datos

def load_results(control, prefijo):
    filename = cf.data_dir + f'football/results-utf8-{prefijo}.csv'
    input_file = csv.DictReader(open(filename, encoding='utf-8'))
    for result in input_file:
        model.add_result(control['model'], result)
        model.add_home_team(control['model'], result)
        model.add_away_team(control["model"], result)
        model.add_team(control["model"], result)
        model.add_result2(control["model"], result)
        model.add_year1(control["model"], result)
        model.add_year(control["model"], result)
        model.add_t_req_4(control["model"],result)
        model.add_num_tournaments_req7(control["model"], result)
        model.add_loqfalta(control["model"], result)
        model.add_loqfalta_total_goals(control["model"], result)
    return control["model"]

def load_goalscoers(control, prefijo):
    filename = cf.data_dir + f'football/goalscorers-utf8-{prefijo}.csv'
    input_file = csv.DictReader(open(filename, encoding='utf-8'))
    for goalscorer in input_file:
        model.add_goalscorer(control['model'], goalscorer)
        model.add_home_team(control["model"], goalscorer)
        model.add_away_team(control["model"], goalscorer)
        model.add_year(control["model"], goalscorer)
        model.add_scorer2(control["model"], goalscorer)
        model.add_year1(control["model"], goalscorer)
        #model.add_scorer(control['model'], goalscorer)
    segundo_recorrido(control, prefijo)
    return control["model"]

def segundo_recorrido(control, prefijo):
    filename = cf.data_dir + f'football/goalscorers-utf8-{prefijo}.csv'
    input_file = csv.DictReader(open(filename, encoding='utf-8'))
    for goalscorer in input_file:
        model.add_scorer(control['model'], goalscorer)
        model.add_tournament_req7(control['model'], goalscorer)
        
    return control["model"]

def load_shootouts(control, prefijo):
    filename = cf.data_dir + f'football/shootouts-utf8-{prefijo}.csv'
    input_file = csv.DictReader(open(filename, encoding='utf-8'))
    for shootout in input_file:
        model.add_shootout(control['model'], shootout)
    return control["model"]

def load_data(control, prefijo):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    return (load_results(control, prefijo), load_goalscoers(control, prefijo), load_shootouts(control, prefijo))


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

def resultsSize(control):
    """
    Numero de libros cargados al catalogo
    """
    return model.results_size(control['model'])

def goalscorersSize(control):
    """
    Numero de libros cargados al catalogo
    """
    return model.goalscorers_size(control['model'])

def shootoutsSize(control):
    """
    Numero de libros cargados al catalogo
    """
    return model.shootouts_size(control['model'])

def map_a_lista_results(control):
    return model.map_a_lista_results(control["model"])

def map_a_lista_goalscorers(control):
    sublist = model.sublist(control["model"]["goalscorers"])
    return model.map_a_lista_goalscorers(sublist)

def map_a_lista_shootouts(control):
    return model.map_a_lista_shootouts(control["model"])

def req_1(control, num_equipos, nombre_equipo, condicion_equipo):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    return model.req_1(control, num_equipos, nombre_equipo, condicion_equipo)


def req_2(control,jugador, ngoles):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    return model.req_2(control["model"],jugador,ngoles)


def req_3(control, equipo, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    return model.req_3(control["model"], equipo, fecha_inicial, fecha_final)


def req_4(control,torneo,f1,f2):
    """
    Retorna el resultado del requerimiento 4
    """
    return model.req_4(control["model"],torneo,f1,f2)


def req_5(control, anotador, fecha_inicial, fecha_final):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    return model.req_5(control, anotador, fecha_inicial, fecha_final)

def req_6(control, n, tournament, year):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    return model.req_6(control["model"], n, tournament, year)


def req_7(control, numero_jugadores, torneo):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    return model.req_7(control, numero_jugadores, torneo)


def req_8(control,pais,f1,f2):
    """
    Retorna el resultado del requerimiento 8
    """
    return model.req_8(control["model"],pais,f1,f2)


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
