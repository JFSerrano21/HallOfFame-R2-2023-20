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
import threading as thr
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller(list):
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller(list)
    return control



def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Listar lo úlrimos N partidos según su condición")
    print("3- Listar los primeros N goles anotados por un jugador ")
    print("4- Consultar los partidos que disputó un equipo durante un periodo especifico")
    print("5- Consultar los partidos relacionados con un torneo durante un periodo específico")
    print("6- Consultar las anotaciones de un jugador durante un periodo espeífico")
    print("7- Clasificar los N mejores equipos de un torneo en un periodo específico")
    print("8- Clasificar los N mejores anotadores en partidos oficiales dentro de un periodo especifico")
    print("9- Seleccionar tipo de ordenamiento iterativo")
    print("0- Salir")
    
    
def tamanio_archivo():
    print ('----------Tamaños disponibles de archivo---------------')
    print("1- 5pct")
    print("2- 10pct")
    print('3- 20pct')
    print('4- 30pct')
    print('5- 50pct')
    print('6- 80pct')
    print('7- large')
    print('8- small')
    opcion = int(input("Seleccione el tamaño de los archivos que desea cargar: \n"))
    tamanio_archivo = "large"
    if opcion == 1:
        tamanio_archivo = "5pct"
    elif opcion == 2:
        tamanio_archivo = "10pct"
    elif opcion == 3:
        tamanio_archivo = "20pct"
    elif opcion == 4:
        tamanio_archivo = '30pct'
    elif opcion == 5:
        tamanio_archivo = '50pct'
    elif opcion == 6:
        tamanio_archivo = '80pct'
    elif opcion == 7:
        tamanio_archivo = 'large'
    elif opcion == 8:
        tamanio_archivo = 'small'
    else:
        print("ingrese una opción valida")
    return tamanio_archivo

def tipo_lista():
    print("-------------------Tipos de lista ---------------------")
    print( '1- ARRAY_LIST')
    print('2- SINGLE_LINKED')
    opcion = int(input("Seleccione la estructura de datos en la que quiere cargar la información: \n"))
    if opcion == 1:
        list = "ARRAY_LIST"
    elif opcion == 2:
        list = "SINGLE_LINKED"
    else:
        print('Ingrese una opción valida')
    return list

def tipo_de_ordenamiento_iterativo (control):
    print("---------------Tipos de ordenamiento iterativo--------------")
    print ("1- SELECTION SORT")
    print("2- INSERTION SORT")
    print("3- SHELL SORT")
    print("4- QUICK SORT")
    print("5- MERGE SORT")
    respuesta= int(input("Seleccione el tipo de ordenamiento con el que desea organizar los datos \n:"))
    if respuesta == 1: 
        print("Ordenando datos con selection sort...")
        deltatime, tipo=controller.ordenamiento_selection(control)
    elif respuesta == 2: 
        print("Ordenando datos con insertion sort...")
        deltatime, tipo= controller.ordenamiento_insertion(control)
    elif respuesta == 3:
        print("Ordenando datos con shell sort...")
        deltatime, tipo = controller.ordenamiento_shell(control)
    elif respuesta == 4:
        print("ordenando datos con quik sort...")
        deltatime, tipo = controller.ordenamiento_quick(control)
    elif respuesta == 5:
        print("ordenando datos con merge sort...")
        deltatime, tipo = controller.ordenamiento_merg(control)
    else:
        print("opcion erronea vuelca a elegir")
    print()
    print_tabla(tipo)
    print()
    print ("Tiempo de ejecución: " + str(deltatime))
    print()

def print_tabla_req6(list, top, sample=3):
    size = lt.size(list)
    if size <= sample*3:
        print("TOP " + str(top) + " tiene menos de 6 registros...")
        print(tabulate(lt.iterator(list),headers="keys", tablefmt = "grid", showindex=False, maxcolwidths=None))
    else:
        print("TOP " + str(top) + " tiene más de 6 registros...")
        list_sample = lt.subList(list,1,3)
        list_ultimos = lt.subList(list,size-2,3)
        for dato in lt.iterator(list_ultimos):
            lt.addLast(list_sample, dato)
        print(tabulate(lt.iterator(list_sample),headers="keys", tablefmt = "grid", showindex=False, maxcolwidths=None))

def print_tabla(list, sample=3):
    size = lt.size(list)
    if size <= sample:
        print("Hay menos de 6 registros...")
        print(tabulate(lt.iterator(list),headers="keys", tablefmt = "grid", showindex=False))
    else:
        print("Hay más de 6 registros...")
        list_sample = lt.subList(list,1,3)
        list_ultimos = lt.subList(list,size-2,3)
        for dato in lt.iterator(list_ultimos):
            lt.addLast(list_sample, dato)
        print(tabulate(lt.iterator(list_sample),headers="keys", tablefmt = "grid", showindex=False))
        
def print_carga_inicial(rs,gl,sh, dt):
    print("---------------------------------------")
    print("Numero de partidos: " + str( lt.size(rs)) )
    print("Numero de goles: " + str(lt.size(gl)) )
    print("Numero de penales: " + str(lt.size(sh)))
    print("---------------------------------------")
    print()
    print('====================================================')
    print('=============== HISTORIAL DE LA FIFA ===============')
    print('====================================================')
    print()
    print('imprimiendo los primeros 3 y últimos 3 registros de los archivos ')
    print()
    print('--- RESULTADOS DE PARTIDOS ---')
    print('         Total de partidos: ' + str(lt.size(rs)))
    print_tabla(rs)
    print()
    print( '--- GOLES ---')
    print('         Total de goles anotados: ' + str(lt.size(gl)) )
    print_tabla(gl)
    print()
    print('--- PENALES ---')
    print('         Total de penales: ' + str(lt.size(sh)))
    print_tabla(sh)
    print()
    print("Tiempo total de carga: " + str(round(dt,3)) )
    print()


def load_data(control, tamanio):
    """
    Carga los datos
    
    """
    results, goalscorers, shootouts, torneos, paises, delta_time = controller.load_data(control, tamanio)
    #Torneos es una estructura para el requerimiento 4.
    
    return results, goalscorers, shootouts, delta_time

def print_listar_partidos_pais(partidos, sz , dt, n):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    print("================= Listar los últimos N partidos de un equipo según su condición ===================")
    print("         Total de partidos encontrados: " + str(sz))
    print("         Seleccionando " + str(n) + " partidos...")
    print()
    print_tabla(partidos)
    print()
    print("Tiempo de ejecución: " + str(dt))
    print()


def print_req_2(player_goals , total_goals , player):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print()
    print ("=============== Primeros N goles de un jugador ===============")
    print ("Total goles anotados por "+  str(player)+ " : " +  str(total_goals))
    print("Cargando los primeros " + str(goals) + " goles anotados por " + str(player))
    print()
    print_tabla(player_goals)
    print()


def print_req_3(list_team , total_partidos , total_local , total_visitante, team_name):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    print()
    print ("=============== Partidos de un equipo en periodo determinado ===============")
    print (str(team_name) + " total partidos disputados: "+ str(total_partidos))
    print (str(team_name) +" total partidos disputados como local: " + str(total_local))
    print (str(team_name) +" total partidos disputados como visitante:  "+ str(total_visitante))
    print()
    print_tabla(list_team)
    print()



def print_get_torneo(torneo, partidos_torneo, cd, ps, np, dt):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    print("================== Partidos de un torneo en periodo ===================")
    print("Total de partidos " + str(torneo) + ": " + str(lt.size(partidos_torneo) ))
    print("Total de paise " + str(torneo) + ": " +str(ps) )
    print("Total de ciudades " + str(torneo) + ": " + str(cd))
    print("Total de penales " + str(torneo) + ": " + str(np))
    print()
    print_tabla(partidos_torneo)
    print()
    print("Tiempo de ejecució: " + str(round(dt, 3)))
    print()


def print_anotaciones_jugador(nombre, num_anot, num_torn, num_penal, num_auto, listado_anots ):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print ("============================ Anotaciones de un jugador en un periodo==================================")
    print ("Total de anotaciones por " + str(nombre) + " fueron: " + str(num_anot))
    print ("Total numero de torneos en los que anoto " + str(nombre) + " fueron:" + str(num_torn) )
    print("Total de penaltis anotados por " + str(nombre) + " fueron: " + str(num_penal))
    print("Total numero de autogoles anotados por " + str(nombre) + "fueron: " + str(num_auto))
    print()
    print("----------------------------------------------------------------------------")
    print_tabla(listado_anots)
    print()
    

def print_req_6(torneo, n, eq, en, ps, cd, cdm, eq_list, dt):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    print("================= Mejores equipos de un torneo en periodo =================")
    print("Total de equipos " + str(torneo) + ": " + str(eq) )
    print("Total de encuentros " + str(torneo) + ": " +str(en) )
    print("Total de paises " + str(torneo) + ": " + str(ps) )
    print("Total de ciudades " + str(torneo) + ": " + str(cd))
    print("Ciudad con mas encuentros " + str(torneo) + ": " + str(cdm))
    print()
    print("Seleccionando TOP " + str(n) + " ..." )
    print_tabla_req6(eq_list, n)
    print()
    print("Tiempo de ejecució: " + str(round(dt, 3)))
    print()

def print_n_mejores_jugadores(t_anotadores, t_partidos, t_torneos, t_goles, t_penales,t_autogoles, listado):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    print("======================= Mejores jugadores en partidos oficiales durante un periodo=======================")
    print( "Total de anotadores que se encontraron en consulta: " + str(t_anotadores) )
    print("Total de partidos en lo que participaron los anotadores: " + str(t_partidos))
    print("Total de goles anotados: " + str(t_goles))
    print("Total de torneos donde participaron los anotadores: " + str(t_torneos))
    print("Total de penaltis conseguidos: " +  str(t_penales))
    print("Total de autogoles obtenidos: " + str(t_autogoles))
    print()
    ("-------------------------------------------------------------------------------------------------------------")
    print_tabla(listado)
    print()
    

#Se pone el limite
default_limit = 1000
# Se crea el controlador asociado a la vista
control = new_controller('ARRAY_LIST')

# main del reto
if __name__ == "__main__":
    thr.stack_size(67108864*2)
    sys.setrecursionlimit(default_limit*1000000)
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            list = tipo_lista()
            control = new_controller(list)
            tamanio = tamanio_archivo()
            print()
            print("Cargando datos ....\n")
            rs, gl, sh, dt = load_data(control, tamanio)
            print_carga_inicial(rs,gl,sh, dt)
            
        elif int(inputs) == 2:
            pais = input("ingrese el nombre del pais de interes: \n")
            condicion = input("ingrese la condición de interes. \n")
            n = int(input("ingrese el numero de partidos: \n"))
            partidos,sz, dt = controller.listar_partidos_pais(control, n, pais, condicion)
            print_listar_partidos_pais(partidos,sz, dt, n)
            
            

        elif int(inputs) == 3:
            player = input("Nombre del jugador: \n ")
            goals = int(input("Igrese el numero de los primeros N goles a buscar: \n "))
            player_goals , total_goals , player , dt = controller.req_2(control , player , goals)
            print_req_2(player_goals , total_goals , player )
            print()
            print("Tiempo de ejecució: " + str(round(dt, 3)))
            print()

        elif int(inputs) == 4:
            #REQ 3 INPUTS
            team_name = input("Ingrese el nombre del equipo de interes: \n")
            start_date =  input('Ingrese la fecha de inicio del periodo a consultar: \n')
            end_date= input('La fecha final del periodo a consultar: \n')
            list_team , total_partidos , total_local , total_visitante, dt = controller.req_3(control, team_name, start_date , end_date)
            print_req_3(list_team , total_partidos , total_local , total_visitante, team_name)
            print()
            print("Tiempo de ejecució: " + str(round(dt, 3)))
            print()

            

        elif int(inputs) == 5:
            nombre_torneo = input("Ingrese el nombre del torneo de interes: \n")
            fecha_inicio = input('Ingrese la fecha de inicio del periodo a consultar: \n')
            fecha_fin = input('La fecha final del periodo a consultar: \n')
            partidos_torneo, cd, ps, np, dt = controller.get_torneo(control, nombre_torneo , fecha_inicio, fecha_fin)
            print_get_torneo(nombre_torneo, partidos_torneo, cd, ps, np, dt)

        elif int(inputs) == 6:
            nombre_jugador= input("Ingrese el nombre del jugador que desea consultar:\n")
            fecha_i= input("Ingrese la fecha inicial desde la desea consultar:\n")
            fecha_f= input("Ingrese la fecha final hasta la que desea consultar:\n")
            num_anot, num_torn, num_penal, num_auto, jugador, tiempo= controller.anotaciones_jugador(control, nombre_jugador, fecha_i, fecha_f)
            print_anotaciones_jugador(nombre_jugador, num_anot, num_torn, num_penal, num_auto, jugador)
            print("----------------------------------------------------------------------------------------------------")
            print ("Tiempo de ejecución: " + str(round(tiempo,3)))
            
        elif int(inputs) == 7:
            torneo = input("Ingrese el nombre del torneo de interes: \n")
            fecha_i = input('Ingrese la fecha de inicio del periodo a consultar: \n')
            fecha_f = input('La fecha final del periodo a consultar: \n')
            n = int(input("TOP? ... \n"))
            eq, en, ps, cd, cdm, eq_list, dt = controller.req_6(control, n, torneo, fecha_i, fecha_f)
            print_req_6(torneo, n, eq, en, ps, cd, cdm, eq_list, dt)

        elif int(inputs) == 8:
            numero_jugadores= input("Ingrese el numero de jugadores TOP en competencias oficiales que desea consultar: \n")
            fecha_i= input("Ingrese la fecha inicial desde la que desea consultar: \n")
            fecha_f= input("ingrese la fecha final hasta la que desea consultar: \n")
            t_anotadores, t_partidos, t_torneos, t_goles, t_penales,t_autogoles, listado, tiempo= controller.n_mejores_anotadores(control, numero_jugadores, fecha_i, fecha_f)
            print_n_mejores_jugadores(t_anotadores, t_partidos, t_torneos, t_goles, t_penales,t_autogoles, listado)
            print ("---------------------------------------------------------------------------------------------------")
            print()
            print ("Tiempo de ejecución: " + str(round(tiempo,3)))
            print()
        
        elif int(inputs) == 9:
            tipo_de_ordenamiento_iterativo(control)
        
        #opcion fantasma, no sale en el menu, es para comprobar una cosita.
        elif int(inputs) == 10:
            torneo = input("Ingrese el nombre del torneo de interes: \n")
            fecha_i = input('Ingrese la fecha de inicio del periodo a consultar: \n')
            fecha_f = input('La fecha final del periodo a consultar: \n')
            hola = controller.contar_equipos(control, fecha_i, fecha_f, torneo)
            print(hola)
            
        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)