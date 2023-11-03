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


default_limit = 1000 
sys.setrecursionlimit(default_limit*10)

def new_controller(struc_list,struc_map,load_factor):
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller(struc_list,struc_map,load_factor)
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


def load_data(control, memflag):
    """
    Carga los datos
    """
    print('\nCuántos datos desea cargar?')
    print('1: Pocos datos')
    print('2: 5% de los datos')
    print('3: 10% de los datos')
    print('4: 20% de los datos')
    print('5: 30% de los datos')
    print('6: 50% de los datos')
    print('7: 80% de los datos')
    print('8: 100% de los datos')
    llave = True
    while llave == True:
        size = input("Ingrese la opcion que desea:\n")
        size = int(size)
        if size in range(0,9):
            llave = False
            if size == 1:
                size = "small"
            elif size == 2:
                size = "5pct"
            elif size == 3:
                size = "10pct"
            elif size == 4:
                size = "20pct"
            elif size == 5:
                size = "30pct"
            elif size == 6:
                size = "50pct"
            elif size == 7:
                size = "80pct"
            elif size == 8:
                size = "large"
            if memflag:
                match_results, goal_scorers, shootouts, delta_time_value, delta_memory_value = controller.load_data(control, size, memflag)
            else:
                match_results, goal_scorers, shootouts, delta_time_value = controller.load_data(control, size, memflag)
        else:
            print("ingrese una opción valida")
    print("Ahora ingrese el metodo con el cual desea ordenar los datos:")
    print('Opción 1: Selection sort')
    print('Opción 2: Insertion sort')
    print('Opción 3: Shell sort')
    print('Opcion 4: Quick sort')
    print('Opcion 5: Merge sort\n')
    metodo = input()
    metodo = int(metodo)
    controller.sort(control, metodo)
    print_tabulated_data(control)
    if memflag:
        return match_results, goal_scorers, shootouts, delta_time_value, delta_memory_value 
    else:
        return match_results, goal_scorers, shootouts, delta_time_value

def print_tabulated_data(control):
    headers1=["Fecha",
             "local",
             "visitante",
             "puntuacion local",
             "puntuacion visitante",
             "Torneo",
             "Ciudad",
             "Pais"]
    headers2=["Fecha",
             "local",
             "visitante",
             "equipo",
             "anotador",
             "minuto"]
    headers3=["Fecha",
             "local",
             "visitante",
             "ganador"]
    datos = controller.get_firts_and_last_3(control["model"],"match_results")
    print(tabulate(datos, headers= headers1, tablefmt="grid"))
    datos = controller.get_firts_and_last_3(control["model"],'goal_scorers')
    print(tabulate(datos, headers= headers2, tablefmt="grid"))
    datos = controller.get_firts_and_last_3(control["model"],'shootouts')
    print(tabulate(datos, headers= headers3, tablefmt="grid"))  

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    num = input("Ingrese numero de partidos a consultar: ")
    equipo = input("Ingrese el nombre del equipo: ")
    condicion = input("Ingrese la condicion del equipo: ").lower()
    resultados, total_equipos, total_partidos, total_condicion, time= controller.req_1(control["model"],int(num),equipo,condicion)
    
    print('\n ========== Req No. 1 Results ==========')
    print("Total teams with available information: "+str(total_equipos))
    print("Total matches for "+equipo+": "+str(total_partidos))
    print("Total matches for "+equipo+" as "+condicion+": "+str(total_condicion)+"\n")
    
    print(tabulate(resultados['elements'] , headers= 'keys', tablefmt = 'grid'))
    print('El tiempo de ejecución es: '  +str(time ) + ' [m/s] \n')
        

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    num = input("Ingrese cuantos goles desea consultar: ")
    jugador = input("Ingrese el nombre completo del jugador: ")
    resultados, time = controller.req_2(control["model"],int(num),jugador)
    print('\n ========== Req No. 2 Results ==========')
    print("Total scorers with available information: "+str(resultados[0]))
    print("Total goals for "+jugador+": "+str(resultados[1]))
    print("Total penalties for "+jugador+": "+str(resultados[2])+"\n")

    print(resultados[4])

    print(tabulate(resultados[3]['elements'] , headers= 'keys', tablefmt = 'grid'))
    print('El tiempo de ejecución es: '  +str(time ) + ' [m/s] \n')


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    try:
        Equipo = input("Ingrese el nombre del quipo que desea consultar: ")
        Inicio = input("Ingrese la fecha inicial con el formato (año-mes-dia): ")
        Final = input("Ingrese la fecha final con el formato(año-mes-dia): ")
        respuesta = controller.req_3(control["model"], Equipo, Inicio, Final)
    except ValueError:
        print("Ingrese una opcion valida")
    print("El tiempo que duro en realizar este requerimiento en ms fueron " +  str(round(respuesta[3],2)))
    print("El total partidos encontrados: " +  str(respuesta[1]+respuesta[2]))
    print("El total de partidos jugados como local: " +  str(respuesta[1]))
    print("El total de partidos jugados como visitante: " +  str(respuesta[2]))
    headers=["Fecha",
             "local",
             "visitante",
             "Puntaje local",
             "Puntaje visitante",
             "Torneo",
             "Ciudad",
             "Pais",
             "AutoGol",
             "Penalty"]
    print(tabulate(respuesta[0], headers= headers, tablefmt="grid"))
    
def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    torneo = input("Ingrese el torneo que desea consultas: ")
    inicio = input("Ingrese desde que fecha desea buscar: ")
    final = input("Ingrese hasta que fecha desea buscar: ")
    resultados = controller.req_4(control['model'],torneo,inicio,final)
    tabla= tabulate(resultados[0]['elements'] , headers= 'keys', tablefmt = 'grid')
    print('\n ========== Req No. 4 Results ==========')
    print('Total tournaments with available information : '  + str(resultados[1]))
    print('Total matches for '+torneo+" : '"  + str(resultados[2]))
    print('Total countries for '+torneo+" : '"  + str(resultados[3]))
    print('Total cities for '+torneo+" : '"  + str(resultados[4]))
    print('Total shootout for '+torneo+" : '"  + str(resultados[5]) +  '\n')
    print(resultados[6])
    print(tabla)



def print_req_5(control, player, Inicio, Final):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    returns = controller.req_5(control['model'], player, Inicio, Final)
    sol = returns[0]
    elements = sol['elements'] 
    print('\n ========== Req No. 5 Results ==========')
    print('Total players with available information : '  + str(returns[1]))
    print('Total goals for ' + str(player) + ': ' + str(returns[2]) )
    print('Total tournaments for ' + str(player) + ': ' + str(returns[3]))
    print('Total penalties for ' + str(player) + ': ' + str(returns[4]))
    print('Total autogoals for ' + str(player) + ': ' + str(returns[5])  + '\n')
    
    print(tabulate(elements, headers= 'keys', tablefmt = 'grid'))



def print_req_6(control, torneo, año, n ):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    data, años, torneos, equipos, partidos, countries, citiesUniqueN, mostPopCity = controller.req_6(control['model'], torneo, año, n )
    newRank =lt.newList('ARRAY_LIST')
     
    elements = data['elements']
    for i in elements:
        top_scorer = [i['top_scorer']]
        f = tabulate(top_scorer, headers = 'keys', tablefmt='grid' )
        i['top_scorer'] = f
        
    for team in elements:
        newFormat ={}
        
        newFormat['team'] = team['team']
        newFormat['total_points'] = team['total_points']
        newFormat['goal_difference'] = team['goal_difference']
        newFormat['penalty_points'] = team['penalty_points']
        newFormat['matches'] = team['matches']
        newFormat['own_goal_points'] = team['own_goal_points']
        newFormat['wins'] = team['wins']
        newFormat['draws'] = team['draws']
        newFormat['losses'] = team['losses']
        newFormat['goals_for'] = team['goals_for']
        newFormat['goals_against'] = team['goals_against']
        newFormat['top_scorer'] = team['top_scorer']

        lt.addLast(newRank, newFormat)
    
    rankElements = newRank['elements']
    print('\n ========== Req No. 6 Results ==========')
    print('Total years with available information : '  + str(años))
    print('Total tournaments with available information :  ' + str(torneos))
    print('Total teams for ' + str(torneo) + ': ' + str(equipos))
    print('Total matches for ' + str(torneo) + ': ' + str(partidos))
    print('Total countries for ' + str(torneo) + ': ' + str(countries))
    print('Total cities for ' + str(torneo) + ': ' + str(citiesUniqueN))
    print('City with most matches for ' + str(torneo) + ': ' + str(mostPopCity) + '\n')
    
    print(tabulate(rankElements, headers = 'keys', tablefmt = 'grid'))
    

    
def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    torneo = input("Ingrese que torneo desea buscar: ")
    puntos = input("Con que puntaje desea buscar a los jugadores: ")
    resultados= controller.req_7(control["model"],torneo,int(puntos))
    print('\n ========== Req No. 7 Results ==========')
    print('Total tournaments with available information : '  + str(resultados[1]))
    print('Total players for ' + str(torneo) + ': ' + str(resultados[2]))
    print('Total matches for ' + str(torneo) + ': ' + str(resultados[3]))
    print('Total goals for ' + str(torneo) + ': ' + str(resultados[4]))
    print('Total penalties for ' + str(torneo) + ': ' + str(resultados[5]))
    print('Total own goals for ' + str(torneo) + ': ' + str(resultados[6]))
    print ('Total of players with ' + str(puntos) + ': ' + str(resultados[7]) + '\n')
    print(resultados[8])
    print(tabulate(resultados[0]['elements'] , headers= 'keys', tablefmt = 'grid'))

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    try:
        Equipo = input("Ingrese el nombre del quipo que desea consultar: ")
        Inicio = input("Ingrese la fecha inicial con el formato (año-mes-dia): ")
        Final = input("Ingrese la fecha final con el formato(año-mes-dia): ")
        respuesta = controller.req_8(control["model"], Equipo, Inicio, Final)
    except ValueError:
        print("Ingrese una opcion valida")
    print('Años: '+ str(respuesta[4]))
    print('Total Partidos:'+ str(respuesta[2]+respuesta[3]))
    print('Partidos locales: '+ str(respuesta[2]))
    print('Partidos visitante: '+ str(respuesta[3]))
    headers=["Fecha",
             "local",
             "visitante",
             "Puntaje local",
             "Puntaje visitante",
             "Torneo",
             "Ciudad",
             "Pais"]
    print(tabulate(respuesta[1], headers=headers, tablefmt="grid"))
    headers_externa=["Año",
             "Matches",
             "TotalP",
             "GD",
             "Penalties",
             "Own",
             "Wins",
             "Draws",
             "Losses",
             "GF",
             "GA",
             "Top Scorer"]
    headers_interna=["sc","G","M","AvgT"]
    for fila in respuesta[0]:
        fila[11] = tabulate(fila[11], headers=headers_interna, tablefmt="grid")

    tabla = tabulate(respuesta[0], headers=headers_externa, tablefmt="grid")
    print(tabla)
    print('El tiempo que duro el programa fue de: '+ str(round(respuesta[5],2)) + ' segundos')
    
def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False
    
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
        try:
            if int(inputs) == 1:
                tipo_list = input("Ingrese que tipo de lista quiere utilizar. \n1 Para ARRAY LIST\n2 Para SINGLE LINKED\n")
                tipo_map = input("\nIngrese que mecanismo de colisiones quiere utilizar. \n1 Para CHAINING \n2 Para PROBING\n")
                if tipo_list in ["1","2"]:
                    if tipo_list == "1":
                        struc_list = 'ARRAY_LIST'
                    elif tipo_list == "2":
                        struc_list = 'SINGLE_LINKED'
                if tipo_map in ["1","2"]:
                    if tipo_map == "1":
                        struc_map = "CHAINING"
                    elif tipo_map == "2":
                        struc_map = 'PROBING'
                    load_factor=float(input("Seleccione el factor de carga que desea utilizar: "))
                    control = new_controller(struc_list,struc_map,load_factor)
                    memflag=castBoolean(input("Desea medir la memoria utilizada? (True/False): "))
                    print("Cargando información de los archivos ....\n")
                    partidos = load_data(control, memflag)                    
                    print('Partidos cargados: ' + str(partidos[0]) + ' goles cargados: '+ str(partidos[1]) + " shootous cargados: " + str(partidos[2]))
                    print('El tiempo de carga es de '+ str(round(partidos[3],2)) + ' segundos')
                    if memflag:
                        print('El espacio usado de carga es de '+ str(round(partidos[4],2)) + 'KB')
                else:
                    print("Ingrese una opcion valida")            
            elif int(inputs) == 2:
                print_req_1(control)

            elif int(inputs) == 3:
                print_req_2(control)

            elif int(inputs) == 4:
                print_req_3(control)

            elif int(inputs) == 5:
                print_req_4(control)

            elif int(inputs) == 6:
                player = str(input('Ingrese el jugador a consultar: '))
                Inicio = str(input('Ingrese la fecha inicial (año-mes-dia): '))
                Final = str(input('Ingrese la fecha final (año-mes-dia): '))
                print_req_5(control, player, Inicio, Final)

            elif int(inputs) == 7:
                torneo = str(input('ingrese el torneo a revisar: '))
                año = str(input('ingrese el año a consultar: '))    
                n = int(input( 'ingrese el tamaño de top que desea: '))
 
                print_req_6(control, torneo, año, n)

            elif int(inputs) == 8:
                print_req_7(control)

            elif int(inputs) == 9:
                print_req_8(control)

            elif int(inputs) == 0:
                working = False
                print("\nGracias por utilizar el programa") 
            else:
                print("Opción errónea, vuelva a elegir.\n")
        except ValueError:
            print("Ingrese un opción valida.\n")
    sys.exit(0)
