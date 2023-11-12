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
import tabulate as tb
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

def SizeForLoadData(Size):
    if Size==1: 
        filesize='5pct.csv'
    elif Size==2: 
        filesize='10pct.csv'
    elif Size==3: 
        filesize='20pct.csv'
    elif Size==4: 
        filesize='30pct.csv'
    elif Size==5: 
        filesize='50pct.csv'
    elif Size==6: 
        filesize='80pct.csv'
    elif Size==7: 
        filesize='large.csv'
    elif Size==8: 
        filesize='small.csv'
    return filesize

def load_data(control, SizeResults, SizeGoalscorers, SizeShootouts):
    """
    Carga los datos
    """
    results=SizeForLoadData(SizeResults)
    goalscorers=SizeForLoadData(SizeGoalscorers)
    shootouts= SizeForLoadData(SizeShootouts)
    controller.loadData(control, results, goalscorers, shootouts)

#Auxiliar tiempo y memoria carga datos Mapa
def TimeAndMemoryMap(control,SizeGoalscorers):
    memory=controller.MemoryMap(control,SizeGoalscorers)
    time=controller.TimeMap(control,SizeGoalscorers)
    return memory, time
    
    
def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    sizeresults = controller.SizeList(control,"results")
    sizegoalscorers = controller.SizeList(control,"goalscorers")
    sizeshootouts = controller.SizeList(control,'shootouts')
    print('Match result count: ' + str(sizeresults))
    result_list=[]
    r_f_element = lt.subList(control['model']["results"], 1, 3)
    r_l_element = lt.subList(control['model']["results"], sizeresults-2, 3)
    for element in lt.iterator(r_f_element):
        result_list.append(element)
    for element in lt.iterator(r_l_element):
        result_list.append(element)
    print(tb.tabulate(result_list, headers="keys", tablefmt="fancy_grid"))
    print('Goal scorers count: ' + str(sizegoalscorers))
    goalscorers_list=[]
    g_f_element = lt.subList(control['model']["goalscorers"], 1, 3)
    g_l_element = lt.subList(control['model']["goalscorers"], sizegoalscorers-2, 3)
    for element in lt.iterator(g_f_element):
        goalscorers_list.append(element)
    for element in lt.iterator(g_l_element):
        goalscorers_list.append(element)
    print(tb.tabulate(goalscorers_list, headers="keys", tablefmt="fancy_grid"))
    print('Shootout-penalty definition count: ' + str(sizeshootouts))
    shootouts_list=[]
    s_f_element = lt.subList(control['model']["shootouts"], 1, 3)
    s_l_element = lt.subList(control['model']["shootouts"], sizeshootouts-2, 3)
    for element in lt.iterator(s_f_element):
        shootouts_list.append(element)
    for element in lt.iterator(s_l_element):
        shootouts_list.append(element)
    print(tb.tabulate(shootouts_list, headers="keys", tablefmt="fancy_grid"))

def print_req_1(control):
    sizeresults = controller.SizeList(control,"results")
    sizegoalscorers = controller.SizeList(control,"goalscorers")
    sizeshootouts = controller.SizeList(control,'shootouts')
    print('Match result count: ' + str(sizeresults))
    result_list=[]
    r_f_element = lt.subList(control['model']["results"], 1, 3)
    r_l_element = lt.subList(control['model']["results"], sizeresults-2, 3)
    for element in lt.iterator(r_f_element):
        result_list.append(element)
    for element in lt.iterator(r_l_element):
        result_list.append(element)
    print(tb.tabulate(result_list, headers="keys", tablefmt="fancy_grid"))
    print('Goal scorers count: ' + str(sizegoalscorers))
    goalscorers_list=[]
    g_f_element = lt.subList(control['model']["goalscorers"], 1, 3)
    g_l_element = lt.subList(control['model']["goalscorers"], sizegoalscorers-2, 3)
    for element in lt.iterator(g_f_element):
        goalscorers_list.append(element)
    for element in lt.iterator(g_l_element):
        goalscorers_list.append(element)
    print(tb.tabulate(goalscorers_list, headers="keys", tablefmt="fancy_grid"))
    print('Shootout-penalty definition count: ' + str(sizeshootouts))
    shootouts_list=[]
    s_f_element = lt.subList(control['model']["shootouts"], 1, 3)
    s_l_element = lt.subList(control['model']["shootouts"], sizeshootouts-2, 3)
    for element in lt.iterator(s_f_element):
        shootouts_list.append(element)
    for element in lt.iterator(s_l_element):
        shootouts_list.append(element)
    print(tb.tabulate(shootouts_list, headers="keys", tablefmt="fancy_grid"))

def print_req_1(control, n, country, condicion):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    tup = controller.req_1(control, n, country, condicion)
    tiempo = tup[1]
    tupla = tup[0]
    datos = tupla[0]
    equipos_totales = tupla[1]
    juegos_pais = tupla[2]
    juegos_condicion = tupla[3]
    condicion_p=None
    print("\nRealizacion del requerimiento en "+ str(round(tiempo, 3))+ " milisegundos")
    if condicion == "indiferente":
        condicion_p=("Juegos totales de " + country + " como home y away: " + str(juegos_condicion) )
    else:
        condicion_p=("Juegos totales de " + country + " como " + condicion + ": " + str(juegos_condicion))
    size = tupla[4]
    print("\nTotal de equipos con información disponible: " + str(equipos_totales))
    print("Juegos totales de " + country + ": " + str(juegos_pais))
    print(condicion_p)
    print("\nSeleccionando "+str(n)+" partidos...")
    elements=[]
    if size>6: 
        print("\nEl req 1 tiene mas de 6 datos...")
        f_element = lt.subList(datos, 1, 3)
        for element in lt.iterator(f_element):
            elements.append(element)
        l_element = lt.subList(datos, size-2, 3)
        for element in lt.iterator(l_element):
            elements.append(element)
    else: 
        print("\nEl req 1 tiene menos de 6 datos...")
        for element in lt.iterator(datos):
            elements.append(element)
    print(tb.tabulate(elements, headers="keys", tablefmt="fancy_grid"))

def print_req_2(control,n,jugador):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    tup=controller.req_2(control, n, jugador)
    tupla=tup[0]
    tiempo_total=tup[1]
    datos=tupla[0]
    total_jugadores = tupla[1]
    goles_totales = tupla[2]
    penales = tupla[3]
    size=tupla[4]
    print("Realizacion del requerimiento en "+ str(round(tiempo_total, 3))+ " milisegundos")
    print("Jugadores totales: "+ str(total_jugadores))
    print("Goles realizados por "+ jugador+ ": " + str(goles_totales))
    print("Penales realizados por "+ jugador+ ": " + str(penales))
    print("Seleccionando "+str(n)+" goles...")
    elements=[]
    if size>6: 
        print("\nEl req 2 tiene mas de 6 datos...")
        f_element = lt.subList(datos, 1, 3)
        for element in lt.iterator(f_element):
            elements.append(element)
        l_element = lt.subList(datos, size-2, 3)
        for element in lt.iterator(l_element):
            elements.append(element)
    else: 
        print("\nEl req 1 tiene menos de 6 datos...")
        for element in lt.iterator(datos):
            elements.append(element)
    print(tb.tabulate(elements, headers="keys", tablefmt="fancy_grid"))


def print_req_3(control, nombre, fecha_1, fecha_2):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    tup=controller.req_3(control, nombre, fecha_1, fecha_2)
    tupla=tup[0]
    tiempo_total=tup[1]
    lista=tupla[0]
    paises_totales= tupla[1]
    juegos_totales = tupla[2]
    home_games =tupla[3]
    away_games =tupla[4]
    print("\nRealizacion del requerimiento en "+ str(round(tiempo_total, 3))+ " milisegundos")
    print("\nTotal de equipos con información disponible: " + str(paises_totales))
    print("Juegos totales de "+ nombre + ": "+ str(juegos_totales))
    print("Juegos totales como local: "+str(home_games))
    print("Juegos totales como visitante: "+str(away_games))
    elements=[]
    if juegos_totales>6: 
        print("\nEl req 3 tiene mas de 6 datos...")
        f_element = lt.subList(lista, 1, 3)
        for element in lt.iterator(f_element):
            elements.append(element)
        l_element = lt.subList(lista, juegos_totales-2, 3)
        for element in lt.iterator(l_element):
            elements.append(element)
    else: 
        print("\nEl req 3 tiene menos de 6 datos...")
        for element in lt.iterator(lista):
            elements.append(element)
    print(tb.tabulate(elements, headers="keys", tablefmt="fancy_grid"))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control, nombre, fecha_1, fecha_2):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    tup=controller.req_5(control, nombre, fecha_1, fecha_2)
    tupla=tup[0]
    tiempo_total=tup[1]
    lista=tupla[0]
    jugadores_totales=tupla[1]
    torneos=tupla[2]
    penales=tupla[3]
    autogoles=tupla[4]
    anotaciones=tupla[5]
    print("\nRealizacion del requerimiento en "+ str(round(tiempo_total, 3))+ " milisegundos")
    print("\nTotal de jugadores con anotaciones: " + str(jugadores_totales))
    print("\nTotal de goles marcados por "+ nombre + ":"+str(anotaciones))
    print("\nCantidad de torneos donde el jugador "+ nombre + " hizo anotacion: "+ str(torneos))
    print("\nPenales totales: "+str(penales))
    print("\nAutogoles totales: "+str(autogoles))
    elements=[]
    if torneos>6: 
        print("\nEl req 5 tiene mas de 6 datos...")
        f_element = lt.subList(lista, 1, 3)
        for element in lt.iterator(f_element):
            elements.append(element)
        l_element = lt.subList(lista, torneos-2, 3)
        for element in lt.iterator(l_element):
            elements.append(element)
    else: 
        print("\nEl req 5 tiene menos de 6 datos...")
        for element in lt.iterator(lista):
            elements.append(element)
    print(tb.tabulate(elements, headers="keys", tablefmt="fancy_grid"))


def print_req_6(control, torneo, fecha,n_equipos):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    tup=controller.req_6(control, torneo, fecha,n_equipos)
    tupla=tup[0]
    tiempo_total=tup[1]
    answer=tupla[0]
    fecha_inicio=tupla[1]
    fecha_final=tupla[2]
    t_torneos=tupla[3]
    t_equipos=tupla[4]
    t_encuentros=tupla[5]
    t_paises=tupla[6]
    t_ciudades=tupla[7]
    ciudad_r=tupla[8]
    size=tupla[9]
    print("\nStar date: "+ fecha_inicio)
    print("\nEnd date: "+ fecha_final)
    print("\nRealizacion del requerimiento en "+ str(round(tiempo_total, 3))+ " milisegundos")
    print("\nTorneos totales con información disponible: " + str(t_torneos))
    print("Equipos totales participando en "+ torneo + ": "+ str(t_equipos))
    print("Encuentros totales del torneo "+ torneo + ": " + str(t_encuentros))
    print("Paises involucrados en el torneo "+ torneo + ": " + str(t_paises))
    print("Ciudades involucrados en el torneo "+ torneo + ": " + str(t_ciudades))
    #print("La ciudad que mas encuentros presencio en el torneo " + torneo + " Fue: "+ ciudad_r)
    elements=[]
    if size>6: 
        print("\nEl req 6 tiene mas de 6 datos...")
        f_element = lt.subList(answer, 1, 3)
        l_element = lt.subList(answer, size-2, 3)
        for element in lt.iterator(f_element):
            list_goal=[element["top_scorer"]]
            element["top_scorer"]=tb.tabulate(list_goal, headers="keys", tablefmt="fancy_grid")
            elements.append(element)
        for element in lt.iterator(l_element):
            list_goal=[element["top_scorer"]]
            element["top_scorer"]=tb.tabulate(list_goal, headers="keys", tablefmt="fancy_grid")
            elements.append(element)
   
    else: 
        print("\nEl req 6 tiene menos de 6 datos...")
        for element in lt.iterator(answer):
            list_goal=[element["top_scorer"]]
            element["top_scorer"]=tb.tabulate(list_goal, headers="keys", tablefmt="fancy_grid")
            elements.append(element)
    print(tb.tabulate(elements, headers="keys", tablefmt="fancy_grid"))


def print_req_7(control, torneo, n):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    tup=controller.req_7(control, torneo, n)
    tupla=tup[0]
    tiempo_total=tup[1]
    answer=tupla[0]
    n_torneos=tupla[1]
    n_juegadores=tupla[2]
    juegos=tupla[3]
    goles=tupla[4] 
    penales=tupla[5] 
    autogoles=tupla[6]
    size=tupla[7]
    print("\nRealizacion del requerimiento en "+ str(round(tiempo_total, 3))+ " milisegundos")
    print("\nNumero de torneos: "+ str(n_torneos))
    print("Jugadores del torneo : "+ str(n_juegadores))
    print("Juegos en el torneo: "+ str(juegos))
    print("Goles totales: "+ str(goles))
    print("Penales totales: "+ str(penales))
    print("Autogoles totales: "+ str(autogoles))
    print("Jugadores con " + str(n) + " puntos: " + str(size))
    elements=[]
    if size>6: 
        print("\nEl req 7 tiene mas de 6 datos...")
        f_element = lt.subList(answer, 1, 3)
        l_element = lt.subList(answer, size-2, 3)
        for element in lt.iterator(f_element):
            list_goal=[element["last_goal"]]
            element["last_goal"]=tb.tabulate(list_goal, headers="keys", tablefmt="fancy_grid")
            elements.append(element)
        for element in lt.iterator(l_element):
            list_goal=[element["last_goal"]]
            element["last_goal"]=tb.tabulate(list_goal, headers="keys", tablefmt="fancy_grid")
            elements.append(element)
   
    else: 
        print("\nEl req 7 tiene menos de 6 datos...")
        for element in lt.iterator(answer):
            list_goal=[element["last_goal"]]
            element["last_goal"]=tb.tabulate(list_goal, headers="keys", tablefmt="fancy_grid")
            elements.append(element)
    print(tb.tabulate(elements, headers="keys", tablefmt="fancy_grid"))


def print_req_8(control, nombre, fecha_1, fecha_2):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    tup=controller.req_8(control, nombre, fecha_1, fecha_2)
    tupla=tup[0]
    tiempo_total=tup[1]
    answer=tupla[0]
    anios=tupla[1]
    juegos_totales=tupla[2]
    juegos_home=tupla[3]
    juegos_away=tupla[4] 
    menor=tupla[5] 
    mayor_tabla=tupla[6]
    size=tupla[7]
    print("\nRealizacion del requerimiento en "+ str(round(tiempo_total, 3))+ " milisegundos")
    print("Estadisticas de "+ nombre + ": ")
    print("\nAños: "+ str(anios))
    print("Juegos totales : "+ str(juegos_totales))
    print("Juegos como local: "+ str(juegos_home))
    print("Juegos como visitante: "+ str(juegos_away))
    print("Juego mas antiguo: "+ str(menor))
    print("Informacion del ultimo juego: ")
    print(tb.tabulate(mayor_tabla, headers="keys", tablefmt="fancy_grid"))
    print("Estadisticas anuales: ")
    elements=[]
    if size>6: 
        print("\nEl req 8 tiene mas de 6 datos...")
        f_element = lt.subList(answer, 1, 3)
        l_element = lt.subList(answer, size-2, 3)
        for element in lt.iterator(f_element):
            element["top scorer"]=tb.tabulate([element["top scorer"]], headers="keys", tablefmt="fancy_grid")
            elements.append(element)
        for element in lt.iterator(l_element):
            element["top scorer"]=tb.tabulate([element["top scorer"]], headers="keys", tablefmt="fancy_grid")
            elements.append(element)
   
    else: 
        print("\nEl req 8 tiene menos de 6 datos...")
        for element in lt.iterator(answer):
            element["top scorer"]=tb.tabulate([element["top scorer"]], headers="keys", tablefmt="fancy_grid")
            elements.append(element)
    print(tb.tabulate(elements, headers="keys", tablefmt="fancy_grid"))

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
            print("Loading Data ....")
            print("\nTamaño de los archivos:\n")
            print("1. 5pct    -   4. 30pct    -   7. large")
            print("2. 10pct   -   5. 50pct    -   8. small")
            print("3. 20pct   -   6. 80pct\n")
            SizeResutls=int(input("Ingrese 1-2-3-4-5-6-7-8 dependiendo del tamaño de archivo Results: "))
            SizeGoalscorers=int(input("Ingrese 1-2-3-4-5-6-7-8 dependiendo del tamaño de archivo Goalscorers: "))
            SizeShootouts=int(input("Ingrese 1-2-3-4-5-6-7-8 dependiendo del tamaño de archivo Shootouts: "))
            data = load_data(control,SizeResutls,SizeGoalscorers,SizeShootouts)
            print_data(control)

        elif int(inputs) == 2:
            print("Req No. 1")
            n=int(input("\nNumero de juegos: "))
            country=(input("\nNombre del equipo: ")).capitalize()
            c=True
            condicion=None
            while c==True:
                print("\nCondicion del equipo: ")
                print("\n1. Local    2. Visitante     3. Indiferente")
                opc=int(input("Seleccione una opcion: "))
                if opc!=1 and opc!=2 and opc!=3:
                    print("\nOpcion no valida...")
                else:
                    if opc==1:
                        condicion="home_team"
                    elif opc==2:
                        condicion="away_team"
                    else:
                        condicion="indiferente"
                    c=False
            print_req_1(control, n, country, condicion)

        elif int(inputs) == 3:
            print("Req No. 2")
            jugador=input("\nNombre del jugador:")
            n=int(input("\nNumero de goles que desea consultar del jugador:"))
            print_req_2(control,n,jugador)

        elif int(inputs) == 4:
            print("Req No. 3")
            nombre=(input("\nNombre del equipo: ")).capitalize()
            fecha_1=input("\nFecha inicial en formato Y-m-d: ")
            fecha_2=input("\nFecha final en formato Y-m-d: ")
            print_req_3(control, nombre, fecha_1, fecha_2)

        elif int(inputs) == 5:
            print("El requerimiento no fue realizado")

        elif int(inputs) == 6:
            print("Req No. 5")
            nombre=(input("\nNombre del jugador: ")).title()
            fecha_1=input("\nFecha inicial en formato Y-m-d: ")
            fecha_2=input("\nFecha final en formato Y-m-d: ")
            print_req_5(control, nombre, fecha_1, fecha_2)

        elif int(inputs) == 7:
            print("Req No. 6")
            torneo=input("\nNombre del torneo: ")
            fecha=input("\nAno deseado: ")
            n_equipos=int(input("\nTop deseado: "))
            print_req_6(control, torneo, fecha,n_equipos)

        elif int(inputs) == 8:
            torneo=input("\nNombre del torneo: ")
            n=int(input("\nNumero de puntos: "))
            print_req_7(control, torneo, n)

        elif int(inputs) == 9:
            print("Req No. 8")
            nombre=(input("\nNombre del equipo: ")).capitalize()
            fecha_1=int(input("\nFecha inicial: "))
            fecha_2=int(input("\nFecha final: "))
            print_req_8(control, nombre, fecha_1, fecha_2)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)