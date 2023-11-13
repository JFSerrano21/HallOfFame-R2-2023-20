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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
csv.field_size_limit(2147483647)

def new_controller(tipo_mapa,lf):
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    data_structs = {"model" : None }
    data_structs ["model"] = model.new_data_structs(tipo_mapa,lf)
    return data_structs


# Funciones para la carga de datos

def load_data(control, archivo, prueba):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    
    if prueba is True:
        tracemalloc.start()
        start_memory = get_memory()
    else:
        start_time = get_time()

    data_structs = control["model"]
    resultados= model.carga_resultados(data_structs,archivo)
    goleadores= model.carga_goleadores(data_structs, archivo)
    penales= model.carga_penales(data_structs, archivo)

    if prueba is False:
        stop_time = get_time()
        deltatime = delta_time(start_time,stop_time)
        print("Tiempo transcurrido: ",deltatime)
    else:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltamemory = delta_memory(stop_memory, start_memory)
        print("Memoria usada: ",deltamemory)


    return resultados,goleadores, penales

def creartabla(lista):
    tipo_lista=lista["type"]
    if tipo_lista is "ARRAY_LIST":
        primer_valor=lista["elements"][0]
    else:
        primer_valor=lista["first"]["info"]
    tabla=model.creartabla(lista,primer_valor)
    return tabla

def resumir_lista(lista):
    lista_resumida=model.resumir_lista(lista)
    return lista_resumida


#Funciones Analisis
def inicio_analisis(prueba):
    if prueba is True:
        tracemalloc.start()
        start = get_memory()
    else:
        start = get_time()
    
    return start

def fin_analisis(prueba,start):
    if prueba is False:
        stop_time = get_time()
        deltatime = delta_time(start,stop_time)
        print("Tiempo transcurrido: ",deltatime)
    else:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltamemory = delta_memory(stop_memory, start)
        print("Memoria usada: ",deltamemory)

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    data_structs = control["model"]
    resp=model.sort(data_structs)
    return resp


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, condicion,n, equipo,prueba):
    """
    Retorna el resultado del requerimiento 1
    """
    start=inicio_analisis(prueba)
    partidos=model.req_1(control,condicion,n,equipo)
    fin_analisis(prueba,start)
    lista_final,total_partidos,total_equipos,total_equipo,tamaño=partidos
    if tamaño > 6:
        lista_resumida = model.resumir_lista(lista_final)
    else:
        lista_resumida = lista_final

    return lista_resumida, total_partidos,total_equipos, total_equipo,tamaño
    


def req_2(control, n, jugador,prueba):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start=inicio_analisis(prueba)
    goles = model.req_2(control,n, jugador)
    fin_analisis(prueba,start)
    size, size_jugadores, subtotal_penales, lista_goles_final, tamaño = goles
    if size_jugadores > 6:
        lista_resumida = model.resumir_lista(lista_goles_final)
    else:
        lista_resumida = lista_goles_final

    return size, size_jugadores, subtotal_penales, lista_resumida, tamaño, 


def req_3(control, equipo, fecha_inicial, fecha_final,prueba):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start=inicio_analisis(prueba)
    partidos = model.req_3(control, equipo, fecha_inicial, fecha_final)
    fin_analisis(prueba,start)
    total_equipos, size_total_partidos, size_subtotal_local, size_subtotal_visitante, total_partidos = partidos
    if size_total_partidos > 6:
        lista_resumida = model.resumir_lista(total_partidos)
    else:
        lista_resumida = total_partidos

    return total_equipos, size_total_partidos, size_subtotal_local, size_subtotal_visitante, lista_resumida


def req_4(control,torneo,fecha_inicial,fecha_final,prueba):
    """
    Retorna el resultado del requerimiento 4
    """
    start=inicio_analisis(prueba)
    final= model.req_4(control,torneo,fecha_inicial,fecha_final)
    fin_analisis(prueba,start)
    total_tournament,lista_final, total_partidos, shootout, countries, cities = final 
    if total_partidos > 6:
        lista_resumida = model.resumir_lista(lista_final)
    else:
        lista_resumida = lista_final
    return total_tournament,lista_resumida, total_partidos,shootout,countries,cities


def req_5(control,nombre,fecha_inicio,fecha_final,prueba):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    data_structs=control["model"]
    start=inicio_analisis(prueba)
    tot_goleadores, goles, cant_torneos, penal, autogol, finales= model.req_5(data_structs,nombre,fecha_inicio,fecha_final)
    fin_analisis(prueba,start)
    return tot_goleadores, goles, cant_torneos, penal, autogol, finales

def req_6(control,torneo,anio,numero_equipos,prueba):
    """
    Retorna el resultado del requerimiento 6
    """
    data_structs=control["model"]
    start=inicio_analisis(prueba)
    respuesta=model.req_6(data_structs,numero_equipos,torneo,anio)
    fin_analisis(prueba,start)
    total_anios,total_torneos, total_equipos, partidos_totales, total_paises,total_ciudades,ciudad_max,lista_final=respuesta
    if total_equipos==0:
        return total_anios,total_torneos, total_equipos, partidos_totales, total_paises,total_ciudades,ciudad_max,lista_final
    if lt.size(lista_final)>6:
        lista_a_imprimir=model.resumir_lista(lista_final)
        return total_anios,total_torneos, total_equipos, partidos_totales, total_paises,total_ciudades,ciudad_max,lista_a_imprimir
    return total_anios,total_torneos, total_equipos, partidos_totales, total_paises,total_ciudades,ciudad_max,lista_final


def req_7(control, torneo,n,prueba):
    """
    Retorna el resultado del requerimiento 7
    """
    start=inicio_analisis(prueba)
    respuesta=model.req_7(control,torneo,n)
    fin_analisis(prueba,start)
    total_partidos,lista_jugadores,Total_torneos,total_jugadores,clas_jug,total_anotaciones,total_penales,total_owngoal=respuesta
    if clas_jug >6:
        lista_resumida=model.resumir_lista(lista_jugadores)
    else:
        lista_resumida = lista_jugadores
    return total_partidos,lista_resumida,Total_torneos,total_jugadores,clas_jug,total_anotaciones,total_penales,total_owngoal

def req_8(control,nom_equipo,anio_inicial,anio_final,prueba):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    data_structs=control["model"]
    fecha_inicial=anio_inicial+"-01-01"
    fecha_final=anio_final+"-12-31"
    start=inicio_analisis(prueba)
    respuesta=model.req_8(data_structs,nom_equipo,fecha_inicial,fecha_final)
    fin_analisis(prueba,start)
    total_anios,total_partidos,partidos_local,partidos_visitante,partidos_mas_antiguo,lis_part_reciente,lista_final=respuesta
    if total_anios==0:
        return total_anios,total_partidos,partidos_local,partidos_visitante,partidos_mas_antiguo,lis_part_reciente,lista_final
    if lt.size(lista_final)>6:
        lista_a_imprimir=model.resumir_lista(lista_final)
        return total_anios,total_partidos,partidos_local,partidos_visitante,partidos_mas_antiguo,lis_part_reciente,lista_a_imprimir
    return total_anios,total_partidos,partidos_local,partidos_visitante,partidos_mas_antiguo,lis_part_reciente,lista_final


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
