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
import threading
import model as md

default_limit = 1000
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

### Controlador

def new_controller():
    """
        Se crea una instancia del controlador
    """
    # Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


### Menu

def print_menu():
    print("\nWelcome")
    print("1- Load data")
    print("2- Consult the N most recent matches of a country")
    print("3- Consult the first N goals scored by a player")
    print("4- Consult all team matches in a specific time period")
    print("5- Consult all tournament matches in a specific time period")
    print("6- Consult all player goals in a specific time period")
    print("7- Consult the top N teams in a tournament in a specific year")
    print("8- Consult the scorers with N points in a specific tournament")
    print("9- Compare performance between 2 teams in a specific time period (not implemented)")
    print("10- Change memory configuration")
    print("0- Exit")


### Carga de datos

def load_data(control, size, memflag):
    """
    Carga los datos
    """
    # Realizar la carga de datos
    sizes, columns, time, delta_time, delta_memory = controller.load_data(control, size, memflag)
    return sizes, columns, time, delta_time, delta_memory

def ask_load_info():
    #Choose size
    print('\nAvailable sizes:')
    print('1- Smallest')
    print('2- 5 % de los datos')
    print('3- 10 % of all data')
    print('4- 20 % of all data')
    print('5- 30 % of all data')
    print('6- 50 % of all data')
    print('7- 80 % of all data')
    print('8- 100 % of all data')
    #Choose sorting algorithm
    size_input = int(input('Choose the size:\n'))

    print("\nDo you wish to monitor memory usage?")
    print('1- Yes')
    print('2- No')

    meminput = int(input("Choose: "))

    
    if size_input == 1:
        size='small'
    elif size_input == 2:
        size='5pct'
    elif size_input == 3:
        size='10pct'
    elif size_input == 4:
        size='20pct'
    elif size_input == 5:
        size='30pct'
    elif size_input == 6:
        size='50pct'
    elif size_input == 7:
        size='80pct'
    elif size_input == 8:
        size='large'
        
    if meminput == 1:
        memflag = True
    else:
        memflag = False
        
    return size, memflag

def change_memory_usage(memflag):
    print('\nCurrent memory usage: ' + str(memflag))
    print('Do you wish to monitor memory?: ')
    print('1- Yes')
    print('2- No')
    meminput = int(input('Choose an option: '))
    
    if meminput == 1:
        memflag = True
    else:
        memflag = False
    
    return memflag

### Impresión de datos

def print_results_table(control, delta_t_r, r_size, r_columns):
    data_structs = control['model']
    sorted_r = data_structs['results']
    print('\n'+'---- MATCH RESULTS ----')
    print(' '*8 + 'Total match results in '+str(round(delta_t_r, 3))+' [ms]: '+str(r_size))
    sorted_r_sublist = controller.create_data_list(sorted_r)
    create_table(sorted_r, sorted_r_sublist, r_columns)
    
def print_goalscorers_table(control, delta_t_g, g_size, g_columns):
    data_structs = control['model']
    sorted_g = data_structs['goalscorers']
    print('\n'+'---- GOAL SCORERS ----')
    print(' '*8 +' Total match results in '+str(round(delta_t_g, 3))+' [ms]: '+str(g_size))
    sorted_g_sublist = controller.create_data_list(sorted_g)
    create_table(sorted_g, sorted_g_sublist, g_columns)
    
def print_shootouts_table(control, delta_t_s, s_size, s_columns):
    data_structs = control['model']
    sorted_s = data_structs['shootouts']
    print('\n'+'---- SHOOTOUTS ----')
    print(' '*8 + 'Total match results in '+str(round(delta_t_s, 3))+' [ms]: '+str(s_size))
    sorted_s_sublist = controller.create_data_list(sorted_s)
    create_table(sorted_s, sorted_s_sublist, s_columns)

def create_table(list, sublist, columns):
    """creates and prints a table based on an original list and its sublist

    Args:
        list (list): original list
        sublist (list): sub list containing first and last 3 elements. can be None
        columns (list): list containing the headers of the table's columns
    """
    if sublist == None:
        table = list
        print('Results struct has less than 6 records...')
    else:
        table = sublist
        print('Results struct has more than 6 records...')
    print(tabulate(lt.iterator(table), tablefmt="grid", headers=columns)+'\n')

def create_req5_table(list, sublist):
    
    if sublist == None:
        table = list
        print('Goals struct has less than 6 records...')
    else:
        table = sublist
        print('Goals struct has more than 6 records...')
    print(tabulate(lt.iterator(table), tablefmt="grid", headers='keys')+'\n')


def create_req6_table(list, sublist, columns):
    """creates and prints a table based on an original list and its sublist

    Args:
        list (list): original list
        sublist (list): sub list containing first and last 3 elements. can be None
        columns (list): list containing the headers of the table's columns
    """
    if sublist == None:
        table = list
        print('Results struct has less than 6 records...')
    else:
        table = sublist
        print('Results struct has more than 6 records...')
    print(tabulate(lt.iterator(table), tablefmt="grid", headers=columns, maxcolwidths=[None,5,5,5,5,5,5,5,5,5,5,None])+'\n')
    
def create_req7_table(list, sublist, columns):
    """creates and prints a table based on an original list and its sublist

    Args:
        list (list): original list
        sublist (list): sub list containing first and last 3 elements. can be None
        columns (list): list containing the headers of the table's columns
    """
    if sublist == None:
        table = list
        print('Results struct has less than 6 records...')
    else:
        table = sublist
        print('Results struct has more than 6 records...')
    print(tabulate(lt.iterator(table), tablefmt="grid", headers=columns)+'\n')


# impresión de tiempo y memoria

def delta_time_and_memory(delta_time, delta_memory):
    if delta_memory is not None:
        print("\nTime [ms]: "+ str(round(delta_time, 3)))
        print("Memory [kb]: "+ str(round(delta_memory, 3)) + '\n')
    else:
        print("\nTime [ms]: "+ str(round(delta_time, 3)) + '\n')


### Requerimientos

# REQ 1

def print_games_played(control,memflag):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    games = int(input("Ingrese el numero de partidos que desea cosultar: "))
    #games = 15
    team = input("Ingrese el nombre del equipo que desea cosultar: ")
    #team = "Italy"
    condition = input("Ingrese la condicion del equipo: ")
    #condition = "home"
    print("=================== Req No. 1 Inputs ===================")
    print("TOP N matches: "+"'"+str(games)+"'" )
    print("Team name: "+"'"+ team+"'")
    print("Condition: "+"'"+ condition+"'")
    file  = controller.print_games_played(control,memflag,games,team,condition)
    print("\n      Only"+"'"+str(file[3])+"'"+"matches found, selecting all... ")
    print("\n=================== Req No. 1 Results ===================")
    print("Total teams with available information: "+"'"+str(file[1])+"'")
    print("Total matches for "+"'"+ team +"'"+" : "+"'"+str(file[2])+"'")
    print("Total matches for "+"'"+ team +"'"+" as "+"'"+condition+"'"+" : "+"'"+str(file[3])+"'")
    print("\n the Team results have more than 6 records...")
    print(tabulate(lt.iterator(file[0]),headers= "keys" ,tablefmt='grid'))

# REQ2

def Goals_for_player(control,memflag):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("Listar los primeros N goles anotados por un jugador (G).")
    n_goals = int(input("Ingrese el numero de goles que desea consultar: "))
    #n_goals= 7
    player = input("Ingrese el nombre del jugador:  ") 
    #player = "Michael Ballack"
    print("\n =================== Req No. 2 Inputs ===================")
    print ("Number of goals: "+"'"+str(n_goals)+"'")
    print ("Player name: "+"'"+player+"'")
    file = controller.Goals_for_player(control,memflag,n_goals,player)
    print("\n      Only"+"'"+str(file[2])+"'"+"goals found, selecting all... ")
    print("\n=================== Req No. 2 Results ===================")
    print("Scorers with available information: "+"'"+str(file[1])+"'")
    print("Total goals for "+"'"+player+"'"+ ":" +"'"+str(file[2])+"'")
    print("Total penalties for "+"'"+player+"'"+": "+"'"+str(file[3])+"'")
    print("\n")
    print ("The result has more than 6 records...")
    return print((tabulate(lt.iterator(file[0]),headers= "keys" ,tablefmt='grid')))


# REQ. 3

def Consult_Period_Matches(control, memflag):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    team = input("Ingrese el nombre del equipo: ")
    #team = "Italy"
    print( "NOTA: Para ingresar la fechas dijitelas en formato: AÑO-MES-DIA")
    start_date = input("Fecha inicial que desea consultar: ")
    #start_date = "1939-01-01"
    end_date = input("Fecha Final que desea consultar: ")
    #end_date = "2018-12-31"
    print("=================== Req No. 3 Inputs ===================")
    print("Team Name: "+"'"+team+"'" )
    print("start date: "+"'"+ start_date+"'")
    print("end date: "+"'"+ end_date+"'")
    file = controller.Consult_Period_Matches(control,memflag,team,start_date,end_date)
    print("\n=================== Req No. 3 Results ===================")
    print("Total teams with available information: "+"'"+str(file[1])+"'")
    print("Total games for "+"'"+ team +"'"+" : "+"'"+str(file[2])+"'")
    print("Total home games for "+"'"+ team +"'"+" : "+"'"+str(file[3])+"'")
    print("Total away games for "+"'"+ team +"'"+" : "+"'"+str(file[4])+"'")
    print("\n the Team results have more than 6 records...")
    
    return print(tabulate(lt.iterator(file[0]),headers= "keys" ,tablefmt='grid'))
    


# REQ 4

def print_tournament_matches(control, memflag):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # Imprimir el resultado del requerimiento 4
    tournament = input('\nWhat tournament would you like to evaluate?:\n')
    start_date = input('\nStarting what date (earliest) would you like to evaluate? (%Y-%M-%D):\n')
    end_date = input('\nUntil what date (latest) would you like to evaluate? (%Y-%M-%D):\n')

    print('\n' + '='*15 + ' Showing results for all matches from ' + tournament +' between '+ start_date + ' and ' + end_date + ' ' + '='*15 + '\n')
    
    matches_list, matches_sublist, count, time, memory = controller.tournament_matches(control, tournament, start_date, end_date, memflag)
    
    total_tournaments = count['total_tournaments']
    total_tournament_matches = count['total_tournament_matches']
    total_matches_in_range = count['total_matches_in_range']
    total_involved_countries = count['total_involved_countries']
    total_involved_cities = count['total_involved_cities']
    total_penalty_matches = count['total_penalty_matches']
    
    delta_time_and_memory(time, memory)
    
    print("Total tournaments: " + str(total_tournaments))
    print(tournament + " total matches: " + str(total_tournament_matches))
    print(tournament + " total matches in range: " + str(total_matches_in_range))
    print(tournament + " total countries involved: " + str(total_involved_countries))
    print(tournament + " total cities involved: " + str(total_involved_cities))
    print(tournament + " total penalty-defined matches in range: " + str(total_penalty_matches) +'\n')
    
    columns = ['date', 'home_team', 'away_team','home_score', 'away_score', 'tournament',
                   'city','country', 'penalty_win', 'penalty_winner']
    
    create_table(matches_list, matches_sublist, columns)


# REQ 5

def print_req_5(control, memflag):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    '''data_structs = control['model']
    lista = controller.req_5(control,'Ali Daei','1999-03-25', '2021-11-23', memflag)
    lista_goles = lista[0]
    print(tabulate(lt.iterator(lista_goles),headers= 'keys' , tablefmt='grid'))'''
    scorer = input('\nWhich player would you like to evaluate?:\n')
    start_date = input('\nStarting what date (earliest) would you like to evaluate? (%Y-%M-%D):\n')
    end_date = input('\nUntil what date (latest) would you like to evaluate? (%Y-%M-%D):\n')
    
    print('\n' + '='*15 + ' Showing goals of ' + scorer +' between '+ start_date + ' and ' + end_date + ' ' + '='*15 + '\n')
    
    goals_list, goals_sublist, contadores, time, memory = controller.req_5(control, scorer, start_date, end_date, memflag)
    
    total_players = contadores['total_jugadores_disponibles']
    total_scorer_goals = contadores['anotaciones_jugador']
    total_tournaments_scored = contadores['numero_torneos_marcados']
    total_penalty_goals = contadores['total_goles_penales']
    total_own_goals = contadores['total_autogoles']
    
    delta_time_and_memory(time, memory)
    
    print("Total scorers: " + str(total_players))
    print(scorer + " total goals: " + str(total_scorer_goals))
    print(scorer + " total tournaments scored: " + str(total_tournaments_scored))
    print(scorer + " total penalty goals: " + str(total_penalty_goals))
    print(scorer + " total own goals: " + str(total_own_goals) + '\n')
    
    create_req5_table(goals_list, goals_sublist)


# REQ 6

def print_classified_teams(control, memflag):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # Imprimir el resultado del requerimiento 6
    tournament = input('\nWhat tournament would you like to evaluate?:\n')
    n = int(input('\nHow many teams would you like to evaluate?:\n'))
    year = input('\nWhat year would you like to evaluate?:\n')
    
    print('\n' + '='*15 + ' Showing results for the top '+ str(n) + ' teams from ' + tournament +' in '+ year + ' ' + '='*15 + '\n')
    
    classified_teams, classified_teams_sublist, count, popular_city, time, memory = controller.classify_teams(control, n, tournament, year, memflag)
    
    total_tournaments = count['total_tournaments']
    total_teams = count['total_teams']
    matches_in_range = int(count['matches_in_range']/2)
    countries = len(count['countries'])
    cities = len(count['cities'])
    
    delta_time_and_memory(time, memory)
    
    print("Tournaments with available information: " + str(total_tournaments))
    print(tournament + " total teams: " + str(total_teams))
    print(tournament + " total matches in range: " + str(matches_in_range))
    print(tournament + " total countries involved: " + str(countries))
    print(tournament + " total cities involved: " + str(cities))
    print(tournament + " most popular city: " + str(popular_city) +'\n')
    
    columns = ['team', 'total_points', 'matches','goal_difference', 'penalty_points', 'own_goal_points',
                   'wins','draws', 'losses', 'goals_for', 'goals_against', 'top_scorer']
    
    create_req6_table(classified_teams, classified_teams_sublist, columns)


# REQ 7

def print_top_scorers(control, memflag):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    tournament = input('\nWhat tournament would you like to evaluate?:\n')
    n = int(input('\nWhat score would you like to evaluate?:\n'))
    
    top_n_scorers, top_n_scorers_sublist, count, time, memory = controller.top_scorers(control, tournament, n, memflag)
    
    print('\n' + '='*15 + ' Showing results for the top '+ str(n) + ' from '+ tournament + ' ' + '='*15 + '\n')
    
    total_tournaments = count['total_tournaments']
    total_matches = count['total_matches']
    total_scorers = len(count['total_scorers'])
    total_scorers_in_range = count['total_scorers_in_range']
    total_goals = count['total_goals_in_range']
    total_penalties = count['total_penalty_points']
    total_own_goals= count['total_own_goals']
    
    delta_time_and_memory(time, memory)
    
    print("Total official tournaments: " + str(total_tournaments))
    print(tournament + " total scorers: " + str(total_matches))
    print(tournament + " total scorers: " + str(total_scorers))
    print(tournament + " total scorers_in_range: " + str(total_scorers_in_range))
    print(tournament + " total goals: " + str(total_goals))
    print(tournament + " total penalties: " + str(total_penalties))
    print(tournament + " total own goals: " + str(total_own_goals) +'\n')
    
    columns = ['scorer', 'total_points', 'total_goals', 'penalty_goals', 'own_goals', 'avg_time [min]',
               'total_tournaments', 'scored_in_wins', 'scored_in_losses', 'scored_in_draws', 'last_goal']
    
    create_req7_table(top_n_scorers, top_n_scorers_sublist, columns)


# REQ 8

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


### Controlador

# Se crea el controlador asociado a la vista
control = new_controller()

#### main cycle
def menu_cycle():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Select an option to continue\n')
        if int(inputs) == 1:
            print("Loading data...\n")
            control = new_controller()
            size, memflag = ask_load_info()
            print("\nLoading data...")
            sizes, columns, times, delta_time, delta_memory = load_data(control, size, memflag)
            print('-'*38)
            print ('Match result count: ' + str(sizes[0]))
            print ('Goal scorers count: ' + str(sizes[1]))
            print ('Shootout-penalty definition count: ' + str(sizes[2]))
            print('-'*38 + '\n')
            print('='*51)
            print('='*15 + ' FIFA RECORDS REPORT ' + '='*15)
            print('='*51 + '\n')
            print('Printing results for the first 3 and last 3 records on file.')
            delta_time_and_memory(delta_time, delta_memory)
            print_results_table(control, times[0], sizes[0], columns[0])
            print_goalscorers_table(control, times[1], sizes[1], columns[1])
            print_shootouts_table(control, times[2], sizes[2], columns[2])
        elif int(inputs) == 2:
            print_games_played(control,memflag)

        elif int(inputs) == 3:
            Goals_for_player(control, memflag)

        elif int(inputs) == 4:
            Consult_Period_Matches(control, memflag)

        elif int(inputs) == 5:
            print_tournament_matches(control, memflag)

        elif int(inputs) == 6:
            print_req_5(control,memflag)

        elif int(inputs) == 7:
            print_classified_teams(control, memflag)

        elif int(inputs) == 8:
            print_top_scorers(control, memflag)

        elif int(inputs) == 9:
            print_req_8(control)
        
        elif int(inputs) == 10:
            memflag = change_memory_usage(memflag)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)


# main del reto
if __name__ == "__main__":
    
    threading.stack_size(67108864*2) # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    thread = threading.Thread(target=menu_cycle())
    thread.start()