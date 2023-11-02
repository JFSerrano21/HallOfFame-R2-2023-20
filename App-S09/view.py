"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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


import copy
import traceback
import threading as th
from tabulate import tabulate
import config as cf
import sys
import controller
import datetime
import time
import pandas as pd
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """

    control = controller.new_controller()

    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control,tamaño,memoria):
    """
    Carga los datos
    Donde
        First: Corresponde a los resultados
        Second: Corresponde a los goleadores
        Third: Corresponde a los penaltis
    """
    if memoria:
        delta_time, delta_memory,r_number, results, g_number, goalscorers, s_number, shootouts =controller.load_data(control, tamaño,memoria)
        return delta_time, delta_memory,r_number, results, g_number, goalscorers, s_number, shootouts
    else:
        delta_time,r_number, results, g_number, goalscorers, s_number, shootouts = controller.load_data(control,tamaño,memoria)
        return delta_time,r_number, results, g_number, goalscorers, s_number, shootouts

def tabulate_data(list_to_tabulate):
    """
        Función que imprime todos los datos que se le pasan
    """
    print(tabulate(list_to_tabulate, headers="keys", tablefmt="grid"))


def tabulated_data(catalog):
    """Imprime los datos de forma tabulada.
    """
    first, last = controller.get_fl_three(catalog)

    first = controller.prepare_date(first)
    last = controller.prepare_date(last)

    print("Primeros 3 resultados:")
    tabulate_data(lt.iterator(first))
    print("Ultimos 3 resultados:")
    tabulate_data(lt.iterator(last))


def tabulated_answers(catalog):
    """
    Esta funcion tabula los primero y ultimos 3 resultados de una lista.
    """
    if lt.size(catalog) <= 6:
        print("Hay seis o menos de seis resultados para esta busqueda...")
        data = controller.prepare_date(catalog)
        tabulate_data(lt.iterator(data))
    else:
        first, last = controller.get_fl_three(catalog)
        if "date" in lt.getElement(first, 1):
            first = controller.prepare_date(first)
            last = controller.prepare_date(last)
        print("Hay más de seis resultados para esta busqueda...")
        print("Primeros 3 resultados:")
        tabulate_data(lt.iterator(first))
        print("Ultimos 3 resultados:")
        tabulate_data(lt.iterator(last))


def print_req_1(catalog, numero, equipo, condicion):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    totalequipos,totalpartidos,totalcondicion,npartidos,deltaTime = controller.req_1(
        catalog, numero, equipo, condicion)
    print("\n==== Resultados Requerimieto No.1 ====")
    print("\nNúmero de equipos con info disponible: ", totalequipos, "\n")
    print("\nNúmero de partidos totales encontrados: ", totalpartidos, "\n")
    print("\nNúmero de partidos según condición: ", totalcondicion, "\n")
    print("Partidos seleccionados: ", numero, "\n")

    data_to_show = lt.newList("ARRAY_LIST")
    for partido in lt.iterator(npartidos):
        lt.addLast(data_to_show, {
            "date": partido["date"],
            "home_team": partido["home_team"],
            "away_team": partido["away_team"],
            "home_score": partido["home_score"],
            "away_score": partido["away_score"],
            "country": partido["country"],
            "city": partido["city"],
            "tournament": partido["tournament"], })

    tabulated_answers(data_to_show)
    delta_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución:", str(delta_time), " ms")


def print_req_2(control, name, cantidad):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2

    respuesta , num_partidos , total__scorers, penalty, deltaTime = controller.req_2(
        control, name, cantidad)

    print("\n==== Resultados Requerimieto No.2 ====\n")
    print("Goleadores con información disponible: " + str(total__scorers))
    print("Nombre del jugador: " + name)
    print("Cantidad de goles: " + str(num_partidos)+"\n")
    print("Cantidad de penalties "+ str(penalty) + "\n")

    print("Listando los primeros " + str(cantidad) + " goles de " + name + ":")

    # Necesito mostrar cierta info, por lo que:

    data_to_show = lt.newList("ARRAY_LIST")

    for goal in lt.iterator(respuesta):

        # Hago un add first porque necesito el orden inverso de los datos
        # Es una implementación O(n) pero reorganizarlos tambien seria O(n)
        # Por lo que es mejor hacerlo de esta forma. Es un tradeoff razonable.
        lt.addFirst(data_to_show, {
            "date": goal["date"],
            "home_team": goal["home_team"],
            "away_team": goal["away_team"],
            "team": goal["team"],
            "scorer": name ,
            "minute": goal["minute"],
            "own_goal": goal["own_goal"],
            "penalty": goal["penalty"]
        }
        )

    tabulated_answers(data_to_show)
    delta_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución:", str(delta_time), " ms")


def print_req_3(equipo,fecha_inicial,fecha_final,control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3

    total,local,visitante,partidos,deltaTime = controller.req_3(equipo,fecha_inicial,fecha_final,control)

    print("==== Resultados Requerimieto No.3 ====")
    print( "Equipos con información disponible: "+ str(total))
    print(equipo + "Total de partidos: " + str(lt.size(partidos)))
    print(equipo + "Total de partidos como local: " + str(local))
    print(equipo + "Total de partidos como visitante: " + str(visitante))

    data_to_show = lt.newList("ARRAY_LIST")

    for partido in lt.iterator(partidos):

        lt.addLast(data_to_show, {
        "date": partido["date"],
        "home_score": partido["home_score"],
        "away_score": partido["away_score"],
        "home_team": partido["home_team"],
        "away_team": partido["away_team"],
        "country": partido["country"],
        "city": partido["city"],
        "tournament": partido["tournament"],
        "penalty": partido["penalty"],
        "own_goal": partido["own_goal"]
    })

    tabulated_answers(data_to_show)
    delta_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución: ", str(delta_time), " ms")




def print_req_4(tournament, fecha_inicial, fecha_final, catalog):
    """
        Función que imprime la solución del Requerimiento 4 en consola

        Consultar los partidos relacionados con un torneo durante un periodo especifico. (I)
    """

    partidos, num_paises, num_ciudades, penalties, num_partidos, num_torneos, deltaTime = controller.req_4(
        tournament, fecha_inicial, fecha_final, catalog)
    print("\n==== Inputs Requerimieto No.4 ====\n")
    print("Torneo: " + tournament)
    print("Fecha inicial: " + fecha_inicial)
    print("Fecha final: " + fecha_final)

    print("\n==== Resultados Requerimieto No.4 ====\n")

    print(tournament + " Total de torneos en el rango: " + str(num_torneos))
    print(tournament + " Total de partidos: " + str(num_partidos))
    print(tournament + " Total de paises: " + str(num_paises))
    print(tournament + " Total de ciudades: " + str(num_ciudades))
    print(tournament + " Total de penalties: " + str(penalties)+"\n")

    # Necesito mostrar cierta info, por lo que:

    data_to_show = lt.newList("ARRAY_LIST")

    for partido in lt.iterator(partidos):

        lt.addLast(data_to_show, {
            "date": partido["date"],
            "tournament": partido["tournament"],
            "country": partido["country"],
            "city": partido["city"],
            "home_team": partido["home_team"],
            "away_team": partido["away_team"],
            "home_score": partido["home_score"],
            "away_score": partido["away_score"],
            "winner": partido["winner"],
        })

    tabulated_answers(data_to_show)

    delta_of_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución: ", str(delta_of_time), " ms")


def print_req_5(control, jugador, fecha_inicial, fecha_final):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    numero_jugadores,numero_goles, numero_torneos, penaltis, autogoles, goles, deltaTime = controller.req_5(
        jugador, fecha_inicial, fecha_final, control)
    print("\n==== Resultados Requerimieto No.5 ====")
    print("\nNombre del jugador: ", jugador, "\n")
    print("Número de jugadores con información disponible: ", numero_jugadores)
    print("Total de goles de ", jugador, ": ", numero_goles)
    print("Total de torneos de ", jugador, ": ", numero_torneos)
    print("Total de penaltis de ", jugador, ": ", penaltis)
    print("Total de autogoles de ", jugador, ": ", autogoles, "\n")

    # Necesito mostrar sólo cierta info, por lo que:
    data_to_show = lt.newList("ARRAY_LIST")
    for gol in lt.iterator(goles):
        lt.addLast(data_to_show, {
            "date": gol["date"],
            "minute": gol["minute"],
            "home_team": gol["home_team"],
            "away_team": gol["away_team"],
            "team": gol["team"],
            "home_score": gol["home_score"],
            "away_score": gol["away_score"],
            "tournament": gol["tournament"],
            "penalty": gol["penalty"],
            "own_goal": gol["own_goal"]})

    tabulated_answers(data_to_show)
    delta_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución: ", str(delta_time), " ms")


def print_req_6(cantidad, torneo, anio, control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    c_anios,c_torneos,c_equipos,c_partidos,total_paises,total_ciudades,max_ciudad, estadisticas, deltaTime = controller.req_6(
        cantidad, torneo, anio, control)
    print("\n==== Resultados Requerimieto No.6 ====\n")
    print("Total de años con información disponible: ", c_anios)
    print("Total torneos con información disponible: ", c_torneos)
    print("Equipos totales en ", torneo, ": ", c_equipos)
    print("Partidos totales en ", torneo, ": ", c_partidos)
    print("Países totales en ", torneo, ": ", total_paises)
    print("Ciudades totales en ", torneo, ": ", total_ciudades)
    print("Ciudad con más partidos en ", torneo, ": ", max_ciudad, "\n")

    data_to_show = lt.newList("ARRAY_LIST")
    for equipo in lt.iterator(estadisticas):
        lt.addLast(data_to_show, {"team": equipo["team"],
                                  "total_points": equipo["total_points"],
                                  "goal_difference": equipo["goal_difference"],
                                  "penalty_points": equipo["penalty_points"],
                                  "matches": equipo["matches"],
                                  "own_goal_points": equipo["own_goal_points"],
                                  "wins": equipo["wins"],
                                  "draws": equipo["draws"],
                                  "loses": equipo["loses"],
                                  "goals_for": equipo["goals_for"],
                                  "goals_against": equipo["goals_against"],
                                  "top_scorer": tabulate(lt.iterator(equipo["top_scorer"]), headers="keys", tablefmt="grid", showindex=False, maxcolwidths=22)})

    tabulated_answers_no_date(data_to_show)
    delta_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución: ", str(delta_time), " ms")

def tabulated_answers_no_date(data_to_show):
    """
    Esta funcion tabula los primero y ultimos 3 resultados de una lista.
    Se revisa que no tenga la columna date para no tabularla.
    Se creo esta funcion debido a que habia un error
    cuando usaba la funcion tabulated_answers con listas que no tenian la columna date.
    """


    if lt.size(data_to_show) <= 6:
        print("Hay seis o menos de seis resultados para esta busqueda...")
        print(tabulate(lt.iterator(data_to_show), headers="keys", tablefmt="grid"))
    else:
        first, last = controller.get_fl_three(data_to_show)
        print("Hay más de seis resultados para esta busqueda...")
        print("Primeros 3 resultados:")
        print(tabulate(lt.iterator(first), headers="keys", tablefmt="grid"))
        print("Ultimos 3 resultados:")
        print(tabulate(lt.iterator(last), headers="keys", tablefmt="grid"))

def print_req_7(n_puntos, torneo, control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """

    num_torneos, num_scorers, num_partidos, num_goals, num_penalties, num_own_goals, jugadores,deltaTime = controller.req_7(
        n_puntos, torneo, control
    )

    print("==== Inputs Requerimieto No.7 ====")
    print("Torneo: ", torneo)
    print(f'Número de jugadores con {n_puntos} puntos: {lt.size(jugadores)}')

    print("==== Resultados Requerimieto No.7 ====")
    print("Total de torneos: ", num_torneos)
    print("Total de goleadores: ", num_scorers)
    print("Total de partidos: ", num_partidos)
    print("Total de goles: ", num_goals)
    print("Total de penaltis: ", num_penalties)
    print("Total de autogoles: ", num_own_goals, "\n")

    print(f'Total de jugadores con {n_puntos}: {lt.size(jugadores)}' )

    data_to_show = lt.newList("ARRAY_LIST")

    for jugadorx in lt.iterator(jugadores):

        last_goal_map = me.getValue(mp.get(jugadorx, "last_goal"))

        last_goal =pd.DataFrame( {

            "date": datetime.datetime.strftime(last_goal_map["date"], "%Y-%m-%d"),
            "tournament": last_goal_map["tournament"],
            "home_team": last_goal_map["home_team"],
            "away_team": last_goal_map["away_team"],
            "home_score": last_goal_map["home_score"],
            "away_score": last_goal_map["away_score"],
            "minute": last_goal_map["minute"],
            "penalty": str(last_goal_map["penalty"]),
            "own_goal": str(last_goal_map["own_goal"])
        }, index=[0])



        lt.addLast(data_to_show, {
            "scorer": me.getValue(mp.get(jugadorx, "name")),
            "total_points": me.getValue(mp.get(jugadorx, "total_points")),
            "total_goals": me.getValue(mp.get(jugadorx, "total_goals")),
            "penalty_goals": me.getValue(mp.get(jugadorx, "penalty_goals")),
            "own_goals": me.getValue(mp.get(jugadorx, "own_goals")),
            "avg_time": calculate_avg_time(me.getValue(mp.get(jugadorx, "avg_times"))),
            "scored_in_wins": me.getValue(mp.get(jugadorx, "scored_in_wins")),
            "scored_in_losses": me.getValue(mp.get(jugadorx, "scored_in_losses")),
            "scored_in_draws": me.getValue(mp.get(jugadorx, "scored_in_draws")),
            "last_goal":tabulate(last_goal, headers="keys", tablefmt="grid", showindex=False)
        })


    tabulated_answers_no_date(data_to_show)

    delta_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución: ", str(delta_time), " ms")


def calculate_avg_time(times):
    """
    Recibe una lista con la lista de los tiempos de los goles de un jugador
    y retorna el promedio de estos
    """

    time = 0

    for i in lt.iterator(times):
        time += i

    return time/lt.size(times)


def print_req_8(control, equipo1, equipo2, fecha_inicial, fecha_final):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """

    datos_equipo1, datos_equipo2, ambos, estadisticas1, estadisticas2, deltaTime = controller.req_8(
        equipo1, equipo2, fecha_inicial, fecha_final, control)
    print("\n==== Resultados Requerimieto No.8 ====")
    print("\nNombre del equipo 1: ", equipo1, "\n")
    print("Nombre del equipo 2: ", equipo2, "\n")
    """print("Años en los que se enfrentaron: ", anios, "\n")"""
    """print("Partidos como local del equipo 1: ", home1, "\n")
    print("Partidos como visitante del equipo 1: ", away1, "\n")
    print("Partidos como local del equipo 2: ", home2, "\n")
    print("Partidos como visitante del equipo 2: ", away2, "\n")"""

    print("Estadisticas del equipo 1: ")
    data_to_show = lt.newList("ARRAY_LIST")
    for datos in lt.iterator(estadisticas1):
        lt.addLast(data_to_show, {
            "Año": datos["year"],
            "matches": datos["matches"],
            "total_points": datos["total_points"],
            "goal_difference": datos["goal_difference"],
            "penalties": datos["penalties"],
            "own_goals": datos["own_goals"],
            "wins": datos["wins"],
            "draws": datos["draws"],
            "loses": datos["loses"],
            "goles_for": datos["goles_for"],
            "Mejor Goleador": tabulate(datos["mejor_jugador"], headers="keys", tablefmt="grid")
        })
    tabulated_answers(data_to_show)
    print("Estadisticas del equipo 2: ")
    data_to_show = lt.newList("ARRAY_LIST")
    for datos in lt.iterator(estadisticas2):
        lt.addLast(data_to_show, {
            "Año": datos["year"],
            "matches": datos["matches"],
            "total_points": datos["total_points"],
            "goal_difference": datos["goal_difference"],
            "penalties": datos["penalties"],
            "own_goals": datos["own_goals"],
            "wins": datos["wins"],
            "draws": datos["draws"],
            "loses": datos["loses"],
            "goles_for": datos["goles_for"],
            "Mejor Goleador": tabulate(datos["mejor_jugador"], headers="keys", tablefmt="grid")
        })
    tabulated_answers(data_to_show)
    print("Estadisticas de ambos equipos: ")
    data_to_show = lt.newList("ARRAY_LIST")
    for partido in lt.iterator(ambos):
        continue #TODO
    tabulated_answers(data_to_show)
    delta_time = f"{deltaTime:.3f}"
    print("Tiempo de ejecución: ", str(delta_time), " ms")


# configurando el limite de recursion
default_limit = 1000

# main del reto
if __name__ == "__main__":
    th.stack_size(67108864*2)  # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    thread = th.Thread()
    thread.start()
    """
    Menu principal
    """
    working = True
    # ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n').strip()
        if int(inputs) == 1:
            # Se crea el controlador asociado a la vista
            catalog = new_controller()

            print("¿Qué tamaño de archivo desea cargar")
            print('1: 1%')
            print('2: 5%')
            print('3: 10%')
            print('4: 20%')
            print('5: 30%')
            print('6: 50%')
            print('7: 80%')
            print('8: 100%')

            resp = int(input().strip())
            if resp == 1:
                tamaño = 'small'
            elif resp == 2:
                tamaño = '5pct'
            elif resp == 3:
                tamaño = '10pct'
            elif resp == 4:
                tamaño = '20pct'
            elif resp == 5:
                tamaño = '30pct'
            elif resp == 6:
                tamaño = '50pct'
            elif resp == 7:
                tamaño = '80pct'
            elif resp == 8:
                tamaño = 'large'

            memoria=int(input("Desea medir la memoria: (1-True o 2-False) "))
            if memoria ==1:
                memoria=True
            else:
                memoria=False

            print("Cargando información de los archivos ....\n")
            print("Con medición de memoria",memoria, ",los resultados de la carga de datos son:\n")

            if memoria is True:
                delta_time, delta_memory,r_number, results, g_number, goalscorers, s_number, shootouts =load_data(catalog, tamaño,memoria)
                print("Tiempo [ms]: ", f"{delta_time:.3f}", "||","Memoria [kB]: ", f"{delta_memory:.3f}"+"\n")

            else:
                delta_time,r_number, results, g_number, goalscorers, s_number, shootouts = load_data(catalog,tamaño,memoria)
                print("Tiempo [ms]: ", f"{delta_time:.3f}"+"\n")



            print("RESULTADOS DE PARTIDOS")
            print("Resultados cargados: " + str(r_number) + "\n")
            tabulated_data(results)
            print("\n")
            print("GOLEADORES")
            print("Goleadores cargados: " + str(g_number) + "\n")
            tabulated_data(goalscorers)
            print("\n")
            print("PENALTIS")
            print("Penaltis cargados: " + str(s_number) + "\n")
            tabulated_data(shootouts)
            print("\n")

            # TODO: Añadir shootouts (view)

        elif int(inputs) == 2:
            numero = input("¿Cuántos partidos desea consultar? ").strip()
            equipo = input("¿Qué equipo desea consultar? ").strip()
            condicion = input("¿Qué condición (Local, Visitante o Indiferente) desea consultar? ").strip()

            print_req_1(catalog, numero, equipo, condicion)

        elif int(inputs) == 3:

            name = input("¿Cuál es el nombre del jugador que desea consultar? ").strip()
            cantidad = int(input("¿Cuantos primeros goles desea consultar? ").strip())

            print_req_2(catalog, name, cantidad)

        elif int(inputs) == 4:
            equipo= input("¿Qué equipo desea consultar? ").strip()
            fecha_inicial= input("¿Desde qué fecha desea cosultar? (con formato %Y-%m-%d) ").strip()
            fecha_final= input("¿Hasta qué fecha desea cosultar? (con formato %Y-%m-%d) ").strip()

            print_req_3(equipo, fecha_inicial, fecha_final, catalog)

        elif int(inputs) == 5:
            tournament = input("¿Qué torneo desea consultar? ").strip()
            fecha_inicial = input("¿Desde qué fecha desea cosultar? (con formato %Y-%m-%d) ").strip()
            fecha_final = input("¿Hasta qué fecha desea cosultar? (con formato %Y-%m-%d) ").strip()

            print_req_4(tournament, fecha_inicial, fecha_final, catalog)

        elif int(inputs) == 6:
            jugador = input("¿Cuál es el nombre del jugador?").strip()
            fecha_inicial = input("¿Desde qué fecha desea cosultar?(con formato %Y-%m-%d) ").strip()
            fecha_final = input("¿Hasta qué fecha desea cosultar?(con formato %Y-%m-%d) ").strip()

            print_req_5(catalog, jugador, fecha_inicial, fecha_final)

        elif int(inputs) == 7:
            cantidad = input("¿Desea consultar el top de cuantos equipos? ").strip()
            torneo = input("¿Qué torneo desea consultar? ").strip()
            anio = input("¿Qué anio desea consultar? ").strip()
            print_req_6(cantidad, torneo,anio, catalog)

        elif int(inputs) == 8:

            torneo = input("¿Qué torneo desea consultar? ").strip().title()
            n_puntos = int(
                input("Desea consultar los jugadores con cuantos puntos ").strip())
            print_req_7(n_puntos, torneo, catalog)

        elif int(inputs) == 9:
            equipo1 = input("¿Cuál es el nombre del equipo 1? ").strip()
            equipo2 = input("¿Cuál es el nombre del equipo 2? ").strip()
            fecha_inicial = input("¿Desde qué fecha desea cosultar?(con formato %Y-%m-%d) ").strip()
            fecha_final = input("¿Hasta qué fecha desea cosultar?(con formato %Y-%m-%d) ").strip()

            print_req_8(catalog ,equipo1, equipo2, fecha_inicial, fecha_final)


        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
