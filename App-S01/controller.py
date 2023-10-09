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


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller(list):
    """
    Crea una instancia del modelo
    """
    control = { "model": None}
    control["model"] = model.new_historial_FIFA(list)
    return control


# =================== CARGA DE DATOS ============================================

def load_data(control, tamanio):
    """
    Carga los datos del reto
    """
    tiempo_i = get_time()
    historial_FIFA = control["model"]
    shootouts = load_shootouts(historial_FIFA, tamanio)
    results, torneos, paises = load_results(historial_FIFA, tamanio)
    goalscorers = load_goals(historial_FIFA, tamanio)
    tiempo_f = get_time()
    dt = delta_time(tiempo_i,tiempo_f)
    return results, goalscorers, shootouts, torneos, paises, dt

def load_results(historial_FIFA, tamanio):
    """
    Carga los resultados del archivo.
    """
    archivo = "football/results-utf8-" + str(tamanio) + ".csv"
    results_file = cf.data_dir + archivo
    input_file = csv.DictReader(open(results_file, encoding="utf8"))
    for result in input_file:
        model.add_result(historial_FIFA, result)
    historial_FIFA = model.ordenar_partidos(historial_FIFA)
    historial_FIFA = model.ordenar_torneos(historial_FIFA)
    
    return historial_FIFA['results'], historial_FIFA["torneos"], historial_FIFA["paises"]

def load_goals(historial_FIFA, tamanio):
    archivo = 'football/goalscorers-utf8-' + str(tamanio) + '.csv'
    goals_file = cf.data_dir + archivo
    input_file = csv.DictReader(open(goals_file, encoding='utf8'))
    for goal in input_file:
        model.add_goal(historial_FIFA, goal)
    historial_FIFA = model.ordenar_goles(historial_FIFA)
    return historial_FIFA['goalscorers']

def load_shootouts(historial_FIFA, tamanio):
    shoots_file = cf.data_dir + 'football/shootouts-utf8-' + str(tamanio) + '.csv'
    input_file = csv.DictReader(open(shoots_file, encoding='utf8'))
    for shoot in input_file:
        model.add_shootout(historial_FIFA, shoot)
    historial_FIFA = model.ordenar_penales(historial_FIFA)
    return historial_FIFA['shootouts']
    

# =================================== REQUERIMINTOS =========================================

def listar_partidos_pais(control, n, pais, condicion):
    """
    Retorna el resultado del requerimiento 1
    """
    tiempo_i = get_time()
    historial_FIFA = control["model"]
    partidos, sz = model.listar_partido_pais(historial_FIFA, n, pais, condicion)
    tiempo_f = get_time()
    dt = delta_time(tiempo_i, tiempo_f)
    return partidos, sz, dt
    


def req_2(control, player , goals):
    """
    Retorna el resultado del requerimiento 2
    """
    tiempo_i = get_time()
    player_goals , total_goals , player = model.req_2(control["model"], player , goals)
    tiempo_f = get_time()
    dt = delta_time(tiempo_i, tiempo_f)

    return player_goals , total_goals , player , dt


def req_3(control, team_name , start_date , end_date):
    """
    Retorna el resultado del requerimiento 3
    """
    tiempo_i = get_time()
    list_team , total_partidos , total_local , total_visitante = model.req_3(control["model"], team_name , start_date , end_date)
    tiempo_f = get_time()
    dt = delta_time(tiempo_i, tiempo_f)

    return list_team , total_partidos , total_local , total_visitante ,dt


#requerimiento 4
def get_torneo(control, nombre_torneo, fecha_inicio, fecha_fin,):
    """
    Retorna el resultado del requerimiento 4
    """
    tiempo_i = get_time()
    partidos_torneo, cd, ps, np = model.get_torneo(control["model"], nombre_torneo, fecha_inicio, fecha_fin )
    tiempo_f = get_time()
    dt = delta_time(tiempo_i, tiempo_f)
    return partidos_torneo, cd, ps, np, dt
    

#requerimiento 5
def anotaciones_jugador(control, nombre, fecha_i, fecha_f):
    """
    Retorna el resultado del requerimiento 5
    """
    tiempo_inicial= get_time()
    num_anot, num_torn, num_penal, num_auto, jugador=model.anotaciones_jugador(control["model"],nombre, fecha_i, fecha_f)
    tiempo_final= get_time()
    tiempo= delta_time(tiempo_inicial, tiempo_final)
    return num_anot, num_torn, num_penal, num_auto, jugador, tiempo
    
def req_6(control, n , torneo, fecha_i, fecha_f):
    """
    Retorna el resultado del requerimiento 6
    """
    tiempo_i = get_time()
    eq, en, ps, cd, cdm, eq_list = model.req_6(control["model"], torneo, n, fecha_i, fecha_f )
    tiempo_f = get_time()
    dt = delta_time(tiempo_i, tiempo_f)
    return eq, en, ps, cd, cdm, eq_list, dt #7 elementos en la tupla.


def n_mejores_anotadores(control, numero_jugadores, fecha_i, fecha_f):
    """
    Retorna el resultado del requerimiento 7
    """
    tiempo_inicial= get_time()
    t_anotadores, t_partidos, t_torneos, t_goles, t_penales,t_autogoles, listado = model.n_mejores_anotadores(control["model"],numero_jugadores, fecha_i, fecha_f)
    tiempo_final= get_time()
    tiempo= delta_time(tiempo_inicial, tiempo_final)
    return t_anotadores, t_partidos, t_torneos, t_goles, t_penales,t_autogoles, listado, tiempo

# FUnción fantasma ----- de verificación
    
def contar_equipos(control, fecha_i, fecha_f, torneo):
    hola = model.contar_equipos(control["model"], fecha_i, fecha_f, torneo)
    return hola


# ------------------------------------Funciones para medir tiempos de ejecucion--------------------------------------------

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

#---------------------------------------Funciones de ordenamiento para lab 4-5----------------------------------------------------

def ordenamiento_shell (control):
    historial_FIFA= control["model"]
    start_time = get_time()
    historial_FIFA= model.ordenamiento_shell(historial_FIFA)
    end_time = get_time()
    dt = delta_time(start_time, end_time)
    return dt, historial_FIFA["results"]
     

def ordenamiento_insertion (control):
    historial_FIFA= control["model"]
    start_time = get_time()
    historial_FIFA= model.ordenamiento_insertion(historial_FIFA)
    end_time = get_time()
    dt = delta_time(start_time, end_time)
    return dt , historial_FIFA["results"]

def ordenamiento_selection (control):
    historial_FIFA= control["model"]
    start_time = get_time()
    historial_FIFA= model.ordenamiento_selection(historial_FIFA)
    end_time = get_time()
    dt = delta_time(start_time, end_time)
    return dt, historial_FIFA["results"]

def ordenamiento_quick(control):
    historial_FIFA= control["model"]
    start_time = get_time()
    historial_FIFA= model.ordenamiento_quick(historial_FIFA)
    end_time = get_time()
    dt = delta_time(start_time, end_time)
    return dt, historial_FIFA["results"]

def ordenamiento_merg(control):
    historial_FIFA= control["model"]
    start_time = get_time()
    historial_FIFA= model.ordenamiento_merg(historial_FIFA)
    end_time = get_time()
    dt = delta_time(start_time, end_time)
    return dt, historial_FIFA["results"]
