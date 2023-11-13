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


def new_controller(tipo_mapa,lf):
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    data_structs=controller.new_controller(tipo_mapa,lf)
    return data_structs
 

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

def load_data(data_structs,archivo,prueba):
    """
    Carga los datos
    """
    datos= controller.load_data(data_structs,archivo,prueba)
    return datos

def cantidad_datos(control):
    archivo=""
    print("\n ¿Cuantos datos desea cargar?")
    print("1: 0.5% de los datos")
    print("2: 5% de los datos")
    print("3: 10% de los datos")
    print("4: 20% de los datos")
    print("5: 30% de los datos")
    print("6: 50% de los datos")
    print("7: 80% de los datos")
    print("8: 100% de los datos")
    opcion=int(input("\n Ingrese cuantos datos desea cargar: "))
    if opcion==1:
        archivo="small.csv"
    elif opcion==2:
        archivo="5pct.csv"
    elif opcion==3:
        archivo="10pct.csv"
    elif opcion==4:
        archivo="20pct.csv"
    elif opcion==5:
        archivo="30pct.csv"
    elif opcion==6:
        archivo="50pct.csv" 
    elif opcion==7:
        archivo="80pct.csv"
    elif opcion==8:
        archivo="large.csv"
    rpta=int(input("\nIngrese 1 si desea medir el tiempo o 2 si desea medir la memoria: "))
    prueba=True
    if rpta==1:
        prueba=False
    resultados, goleadores, penales = load_data(control, archivo,prueba)
    respuesta=controller.sort(control)
    print(respuesta)
    print("\n------------ Carga Completa ---------------")
    print("\n Se cargaron ",resultados, " partidos")
    print("\n Se cargaron ",goleadores, " goleadores")
    print("\n Se cargaron ",penales, " definiciones de partidos por penal")
    print("\n -----------------------------------------------------------\n")
    nombres_documentos=["results","goalscorers","shootouts"]
    for i in range(3):
        print((nombres_documentos[i]).title(), "tiene mas de 6 datos")
        l_results=controller.resumir_lista(control["model"][nombres_documentos[i]])
        print(controller.creartabla(l_results),"\n")
    


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
    
    cantidad = int(input("\nIngrese el número de partidos de consulta:"))
    team = input("\nIngrese el equipo que desea consultar: ")
    condicion = input("\nIngrese la condición del equipo en los partidos: ")
    prueba=analisis()
    respuesta= controller.req_1(control,condicion, cantidad, team,prueba)
    lista_final, total_partidos,total_equipos,total_equipo,tamaño=respuesta
    print("\n====================== Req No. 1 Inputs ======================")
    print("Number of matches: ",cantidad)
    print("Team name: ",team)
    print("Team condition: ",condicion)
    print("\n====================== Req No. 1 Results ======================")
    print("Total teams with available information: ", total_equipos)
    print("Total matches for " + team + ":", total_equipo)
    print("Total matches for " + team + " as " + condicion + " : ", total_partidos)
    print(f"\nSelecting {cantidad} matches. . .")

    if tamaño==0:
        print("No results")
    elif tamaño<=6:
        print("\nResults structs has 6 records or less...")
        tabla=controller.creartabla(lista_final)
        print(tabla)
    elif tamaño>6:
        print("\nResults structs has more than 6 records...")
        tabla=controller.creartabla(lista_final)
        print(tabla)


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    n = int(input("\nIngrese el número de goles de consulta:"))
    jugador = input("\nIngrese el jugador que desea consultar: ")
    prueba=analisis()
    respuesta= controller.req_2(control,n, jugador,prueba)
    size, size_jugadores, subtotal_penales, lista_goles_final, tamaño=respuesta
    print("\n====================== Req No. 2 Inputs ======================")
    print("TOP N Goals: ",n)
    print("Player name: ",jugador)
    print("Only ", size_jugadores, "goals found, selecting all..." )
    print("\n====================== Req No. 2 Results ======================")
    print("Total scorers with available information: ", size)
    print("Total goals for " + jugador + ": ", size_jugadores)
    print("Total penalties for " + jugador + ": ", subtotal_penales )


    if tamaño==0:
        print("No results")
    elif tamaño<=6:
        print("\nResults structs has 6 records or less...")
        tabla=controller.creartabla(lista_goles_final)
        print(tabla)
    elif tamaño>6:
        print("\nResults structs has more than 6 records...")
        tabla=controller.creartabla(lista_goles_final)
        print(tabla)


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    equipo = input("\nIngrese el equipo de consulta:")
    fecha_inicial = input("\nIngrese la fecha inicial del periodo que desea consultar(con formato \"Y-m-d\"): ")
    fecha_final = input("\nIngrese la fecha final del periodo que desea consultar(con formato \"Y-m-d\"): ")
    prueba=analisis()
    respuesta= controller.req_3(control, equipo, fecha_inicial, fecha_final,prueba)
    total_equipos, size_total_partidos, size_subtotal_local, size_subtotal_visitante, total_partidos=respuesta
    print("\n====================== Req No. 3 Inputs ======================")
    print("Team name: ", equipo)
    print("Start date: ",fecha_inicial)
    print("End date: ",fecha_final)
    print("\n====================== Req No. 3 Results ======================")
    print("Total teams with available information: ", total_equipos)
    print("Total games for " + equipo + ": ", size_total_partidos)
    print("Total home games for " + equipo + ": ", size_subtotal_local)
    print("Total away games for " + equipo + ": ", size_subtotal_visitante)

    if size_total_partidos==0:
        print("No results")
    elif size_total_partidos<=6:
        print("\nResults structs has 6 records or less...")
        tabla=controller.creartabla(total_partidos)
        print(tabla)
    elif size_total_partidos>6:
        print("\nResults structs has more than 6 records...")
        tabla=controller.creartabla(total_partidos)
        print(tabla)


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
  
    torneo= input("\nIngrese el nombre del torneo: ")
    fecha_inicial= input("\nIngrese la fecha inicial del periodo que desea consultar(con formato \"Y-m-d\"): ")
    fecha_final= input("\nIngrese la fecha final del periodo que desea consultar(con formato \"Y-m-d\"): ")
    prueba=analisis()
    final= controller.req_4(control,torneo,fecha_inicial,fecha_final,prueba)
    total_tournament,lista_final, total_partidos, shootout,countries, cities = final
    print("\n====================== Req No. 4 Inputs ======================")
    print("Player name: ",torneo)
    print("Start Date: ",fecha_inicial)
    print("End Date: ",fecha_final)
    print("\n====================== Req No. 4 Results ======================")
    print("Total Tournament with available information: ", total_tournament)
    print("Total matches: ", total_partidos)
    print("Total countries: ", countries)
    print("Total cities: ", cities)
    print("Total shootouts: ", shootout,"\n")
    if total_partidos==0:
        print("No goals from", torneo,"were found in the given time period")
    elif total_partidos<=6:
        print("Scorers results has 6 records or less...")
        tabla=controller.creartabla(lista_final)
        print(tabla)
    elif total_partidos>6:
        print("Scorers results has more than 6 records...")
        tabla=controller.creartabla(lista_final)
        print(tabla)


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    nombre= input("\nIngrese el nombre del jugador, del que desea encontrar las anotaciones: ")
    fecha_inicial= input("\nIngrese la fecha inicial del periodo que desea consultar(con formato \"Y-m-d\"): ")
    fecha_final= input("\nIngrese la fecha final del periodo que desea consultar(con formato \"Y-m-d\"): ")
    prueba=analisis()
    respuesta= controller.req_5(control,nombre,fecha_inicial,fecha_final,prueba)
    total_goleadores,total_goles,torneos,penal,autogol,lista_imprimir=respuesta
    print("\n====================== Req No. 5 Inputs ======================")
    print("Player name: ",nombre)
    print("Start Date: ",fecha_inicial)
    print("End Date: ",fecha_final)
    print("\n====================== Req No. 5 Results ======================")
    print("Total players with available information:",total_goleadores)
    print("Total goals for", nombre, ":", total_goles)
    print("Total tournaments for", nombre, ":", torneos)
    print("Total penalties for", nombre, ": ", penal)
    print("Total autogoals for", nombre, " : ", autogol,"\n")

    if total_goles==0:
        print("No goals from", nombre,"were found in the given time period")
    elif total_goles<=6:
        print("Scorers results has 6 records or less...")
        tabla=controller.creartabla(lista_imprimir)
        print(tabla)
    elif total_goles>6:
        print("Scorers results has more than 6 records...")
        lresumida=controller.resumir_lista(lista_imprimir)
        tabla=controller.creartabla(lresumida)
        print(tabla)
    print("\n")



def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    torneo=input("\nIngrese el nombre del torneo que desea buscar: ")
    numero_equipos = int(input("Ingrese el número de equipos de consulta: "))
    anio= input("\nIngrese el año que desea consultar(con formato %Y): ")
    prueba=analisis()
    total_anios,total_torneos, total_equipos, partidos_totales, total_paises,total_ciudades,ciudad_max,lista_final=controller.req_6(control,torneo,anio,numero_equipos,prueba)
    print("\n====================== Req No. 6 Inputs ======================")
    print("Tournament name: ",torneo)
    print("Top N",numero_equipos, "team ranking")
    print("Consult year",anio)
    print("Start Date: ",anio,"- 01 - 01 in consult year")
    print("End Date: ",anio,"- 12 - 31 in consult year")
    print("\n====================== Req No. 6 Results ======================")
    print("Total years with available information:", total_anios)
    print("Total tournaments with available information:", total_torneos)
    print("Total teams for", torneo, ":", total_equipos)
    print("Total matches for", torneo, ":", partidos_totales)
    print("Total countries for", torneo, ":", total_paises)
    print("Total cities for", torneo, ":", total_ciudades)
    print("City with most matches for", torneo, ":", ciudad_max,"\n")

    if total_equipos==0:
        print("No teams from",torneo,"were found in the given time period")
    elif numero_equipos<=6 or total_equipos<=6:
        print("Top",numero_equipos,"teams results has 6 records or less...")
        tabla=controller.creartabla(lista_final)
        print(tabla)
    elif total_equipos>6 or numero_equipos>6:
        print("Top",numero_equipos,"teams results has more than 6 records...")
        tabla=controller.creartabla(lista_final)
        print(tabla)


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    torneo = input("Ingrese el torneo de consulta: ")
    points= int(input("\nIngrese la cantidad de puntos para la consulta: "))
    prueba=analisis()
    total_partidos,lista_resumida,Total_torneos,total_jugadores,clas_jug,total_anotaciones,total_penales,total_owngoal=controller.req_7(control,torneo,points,prueba)
    print("\n====================== Req No. 7 Inputs ======================")
    print("Tournament name: ",torneo)
    print("players with",points, "points in the scorer ranking")
    print("\n====================== Req No. 7 Results ======================")
    print("Total tournaments with availabe information: ", Total_torneos)
    print("Total players for ",torneo,": ", total_jugadores)
    print("Total matches for ",torneo,": ", total_partidos)
    print("Total goals for ",torneo,": ", total_anotaciones)
    print("Total penalties for ",torneo,": ", total_penales)
    print("Total own goals for ",torneo,": ", total_owngoal)
    print("Total of players with",points,"points: ",clas_jug,"\n")

    if clas_jug==0:
        print("No scorers were found in the given time period")
    elif clas_jug<=6:
        print("Players with",points,"points results has 6 records or less...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    elif clas_jug>6 :
        print("Players with",points,"points results has more than 6 records...")
        tabla=controller.creartabla(lista_resumida)
        print(tabla)
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    nom_equipo=input("\nIngrese el nombre del equipo que desea buscar: ")
    anio_inicial= input("\nIngrese el año inicial que desea consultar(con formato %Y): ")
    anio_final= input("\nIngrese el año final que desea consultar(con formato %Y): ")
    prueba=analisis()
    total_anios,total_partidos,partidos_local,partidos_visitante,partidos_mas_antiguo,lis_part_reciente,lista_final=controller.req_8(control,nom_equipo,anio_inicial,anio_final,prueba)
    print("\n====================== Req No. 8 Inputs (BONUS) ======================")
    print("Team name: ",nom_equipo)
    print("Start year",anio_inicial)
    print("End year",anio_final)
    fecha1=anio_inicial+"01-01"
    print("Start Date: ",fecha1,"- 01 - 01 in year",anio_inicial)
    fecha2=anio_final+"12-31"
    print("End Date: ",fecha2,"- 12 - 31 in year",anio_final)
    print("\nConsulting data range...")
    print("\nExcluding friendly matches...")
    print("\n====================== Req No. 8 Results (BONUS) ======================\n")
    if total_anios==0:
        print("No games from",nom_equipo,"were found in the given time period")
    else:
        print("\t\t ------------",nom_equipo,"Statistics ------------")
        print("\t\t\tYears:", total_anios)
        print("\t\t\tTotal matches:", total_partidos)
        print("\t\t\tTotal home matches:", partidos_local)
        print("\t\t\tTotal away matches:", partidos_visitante)
        print("\t\t\tOldest match date:", partidos_mas_antiguo)
        print("\n \t\t\t+++ Newest match data +++")
        tab_partido_reciente=controller.creartabla(lis_part_reciente)
        print(tab_partido_reciente)

        if total_anios<=6:
            print("There are",total_anios,"in years on record for the",nom_equipo,"team, 6 records or less than the allowed...")
            tabla=controller.creartabla(lista_final)
            print(tabla)
        else:
            print("There are",total_anios,"in years on record for the",nom_equipo,"team, more than the 6 allowed...")
            tabla=controller.creartabla(lista_final)
            print(tabla)

def analisis():
    rpta=int(input("\nIngrese 1 si desea medir el tiempo o 2 si desea medir la memoria: "))
    prueba=True
    if rpta==1:
        prueba=False
    return prueba

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
            rpta=int(input("\nIngrese 1 si desea separate chaining o 2 si desea linear probing: "))
            tipo_mapa=""
            if rpta==1:
                tipo_mapa="CHAINING"
            elif rpta==2:
                tipo_mapa="PROBING"    
            lf=float(input("Ingrese el Factor de Carga que desea utilizar: "))
            control = new_controller(tipo_mapa,lf)
            print("Cargando información de los archivos ....\n")
            data = cantidad_datos(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
