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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

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
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
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
    print("10- Ejecutar carga de datos lab 7 (EJECUTAR 1 ANTES)")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    message = """
Ingrese 1 si quiere cargar una muestra pequeña de los datos. 
Ingrese 2 si quiere cargar el 5 porciento de los datos.
Ingrese 3 si quiere cargar el 10 porciento de los datos.
Ingrese 4 si quiere cargar el 20 porciento de los datos
Ingrese 5 si quiere cargar el 30 porciento de los datos.
Ingrese 6 si quiere cargar el 50 porciento de los datos
Ingrese 7 si quiere cargar el 80 porciento de los datos
Ingrese 8 si quiere cargar TODOS los datos."""
    data_size = int(input(message))
    scorers, results, shootouts, n_results, n_shootouts, n_scores= controller.load_data(control, data_size)
    return scorers, results, shootouts, n_results, n_shootouts, n_scores

def print_loaded_data(control):
    scores, results, shootouts, n_results, n_shootouts, n_scores = load_data(control)
    print(f'{"-"*10}\n'
            f'Numero de partidos: {n_results}\n'
            f'Numero de penalties: {n_shootouts}\n'
        f'{"-"*10}\n')
    print(f'Goles encontrados: {n_scores}')
    print(f'{tabulate(scores,headers="keys",tablefmt="grid")}')
    print(f'\nResultados de partidos cargados: {n_results}')
    print(f'{tabulate(results,headers="keys",tablefmt="grid")}')
    print(f'\nResultados de penalties cargados: {n_shootouts}')
    print(f'{tabulate(shootouts,headers="keys",tablefmt="grid")}')
    #print(f'Espacio usado en la carga de datos: {delta_m}[kB]')
def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    

def print_req_1(control,team, condition,numero):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    resultados, total_teams, total_partidos ,total_condition,delta= controller.req_1(control,team,condition,numero)
    print("Total teams with avalaible information: " + str(total_teams))
    print("Total matches for "+ str(team) + ": "+ str(total_partidos))
    print("Total matches for "+ str(team) + " as "+str(condition)+" : "+ str(total_condition))
    lista = [x for x in lt.iterator(resultados)]
    print(f'{tabulate(lista,headers="keys",tablefmt="grid")}')
    print(delta)
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control, nombre,cant_goles):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    elems, n_goles, n_penalties, total_scorers = controller.req_2(control, nombre, cant_goles)
    print(f'Number of scorers with available entries: {total_scorers}')
    print(f'Total scores for {nombre}: {n_goles}')
    print(f'Total penalties for {nombre}: {n_penalties}')
    results = [x for x in lt.iterator(elems)]
    print(f'{tabulate(results,headers="keys",tablefmt="grid")}')



def print_req_3(control,date_inicial,data_final,team):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    lista,away,home,ambos,todos,delta=controller.req_3(control,date_inicial,data_final,team)
    print("total teams with information: "+ str(todos))
    print("Total games for: "+str(team)+": " + str(ambos))
    print("Total home games: "+ str(home))
    print("total away games: " + str(away))
    elems = [x for x in lt.iterator(lista)]
    print(f'{tabulate(elems,headers="keys",tablefmt="grid")}')
    print(delta)
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    tournament = input('Ingrese el torneo: ')
    start_d = input('Ingrese la fecha de inicio: ')
    end_d = input('Ingrese la fecha final: ') 
    elems, n_tournaments, n_matches, n_countries, n_cities, n_shootouts,delta = controller.req_4(control,tournament, start_d, end_d)
    print(f'Total tournaments with available information: {n_tournaments}')
    print(f'Total matches for {tournament}: {n_matches}')
    print(f'Total countries for {tournament}: {n_countries}')
    print(f'Total cities for {tournament}:{n_cities}')
    print(f'Total shootouts for {tournament}: {n_shootouts}')
    print(f'\n')
    print(f'{tabulate(elems,headers="keys",tablefmt="grid")}')
    print(delta)

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    nombre = input("Ingrese el nombre del jugador: ")
    fecha_inicial = input("Ingrese la fecha inicial del periodo: ")
    fecha_final = input("Ingrese la fecha final del periodo: ")
    elems,total_scorers,total_anotaciones_jugador,total_torneos,total_penalty,total_autogol = controller.req_5(control, nombre,fecha_inicial, fecha_final)
    lista = [x for x in lt.iterator(elems)]
    print(f"Total players with avaiable information: {total_scorers}")
    print(f"Total tournaments: {total_torneos}")
    print(f"Total goals for {nombre}: {total_anotaciones_jugador}")
    print(f"Total penalties for {nombre}: {total_penalty}")
    print(f"Total autogoal for {nombre}: {total_autogol}")
    print(f'{tabulate(lista,headers="keys",tablefmt="grid")}')
    

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    """ tournament = "FIFA World Cup qualification"
    n_teams = 11
    year=2021 """

    n_teams= input('Ingrese el número de equipos: ')
    tournament = input("Ingrese el torneo: ")
    year= input("Ingrese el año: ") 

    teams,total_years, total_tournaments, n_teams_y, total_matches, n_countries, n_cities, pop_city,delta = controller.req_6(control,n_teams, tournament, year)

    print(f'Total number of years with available information: {total_years}')
    print(f'Total tournaments with available information: {total_tournaments}')
    print(f'Total teams for {tournament}: {n_teams_y}')
    print(f'Total matches for {tournament}: {total_matches}')
    print(f'Total countries for {tournament}: {n_countries}')
    print(f'Total cities for  {tournament}: {n_cities}')
    print(f'Most popular city in {tournament}: {pop_city}')
    print(f'\n')
    print(f'{tabulate(teams,headers="keys",tablefmt="grid")}')
    print(delta)


def print_req_7(control,torneo,numero):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    resultado,total_tourn,total_scorers,total_matches,goals,penalties,autogoles,total_player,delta=controller.req_7(control,torneo,numero)
    print("Total tournaments with available information: "+ str(total_tourn))
    print("Total players for "+ str(torneo)+ " : " +str(total_scorers))
    print("Total matches for "+ str(torneo)+ " : " +str(total_matches))
    print("Total goals for "+ str(torneo)+ " : " +str(goals))
    print("Total penalties for "+ str(torneo)+ " : " +str(penalties))
    print("Total own goals for "+ str(torneo)+ " : " +str(autogoles))
    print("Total players with "+ str(numero)+ " points : " +str(total_player))
    lista = []
    for x in lt.iterator(resultado):
        info = dict(x)
        info['last_goal'] = tabulate([info['last_goal']],headers="keys",tablefmt="grid")
        lista.append(info)
    print(f'{tabulate(lista,headers="keys",tablefmt="grid")}')
    print(delta)


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    team = input("Ingrese el equipo: ")
    start_y = input("Ingrese el año de inicio: ")
    end_y = input("Ingrese el año final: ") 
    elems, n_years, total_matches, home_matches, away_matches, oldest_date, newest_match, delta= controller.req_8(control, team, start_y, end_y)
    for elem in elems:
        elem.pop('dates')
        elem.pop('home_matches')
        elem.pop('away_matches')
    print(f'\n')
    print(f'{team} Statistics')
    print(f'Total years with available information: {n_years}')
    print(f'Total matches: {total_matches}')
    print(f'Total home matches: {home_matches}')
    print(f'Total away matches: {away_matches}')
    print(f'Oldest match date: {oldest_date}')
    print(f'Newest match data: ')
    print(f'\n')
    print(f'{tabulate([newest_match],headers="keys",tablefmt="grid")}')
    print(f'\n')
    print(f'Yearly statistics: ')
    print(f'\n')
    print(f'{tabulate(elems,headers="keys",tablefmt="grid")}')
    print(delta)

def print_lab_7(control):
    maptype=input("Ingrese si quiere un mapa PROBING o CHAINING (P/C): ")
    if maptype=="P":
        maptype="PROBING"
    elif maptype=="C":
        maptype="CHAINING"
    load_factor= float(input("Ingrese el factor de carga: "))
    memflag = input("¿Desea que se devuelva registro de la memoria? (T/F): ")
    if "T" in memflag:
        memflag=True
    else:
        memflag = False
    scorers, delta_time, delta_memory = controller.load_data_lab7(control, maptype, load_factor, memflag)
    if scorers:
        print(f'Tiempo de ejecución[ms]: {delta_time:.3f}')
        if delta_memory:
            print(f'Memoria empleada en la ejecución[kB]: {delta_memory:.3f}')
        print(f'Jugadores encontrados:')
        print(f'{tabulate(scorers,headers="keys",tablefmt="grid")}')


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            print_loaded_data(control)
        elif int(inputs) == 2:
            numero= int(input("Top N matches: \n"))
            team= input("Team name: \n")
            condition= input ("Team condition: \n")
            print_req_1(control,team,condition,numero)

        elif int(inputs) == 3:
            nombre = input("Ingrese el nombre del jugador: ")
            cant_goles = int(input("Ingrese la cantidad de goles que desea consultar: "))
            print_req_2(control, nombre, cant_goles)
            

        elif int(inputs) == 4:
            data_inicial= input("Inicio: ")
            data_final= input("Final: ")
            team= input("Equipo: ")
            print_req_3(control,data_inicial,data_final,team)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            torneo= input("ingrese el torneo: ")
            numero=int(input("Ingrese el numero: "))
            print_req_7(control,torneo,numero)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs)==10:
            print_lab_7(control)
        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)