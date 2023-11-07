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

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller(type_scorers, loadfactor_scorers):
    """
        Se crea una instancia del controlador
    """
    control = controller.new_controller(type_scorers, loadfactor_scorers)
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Listar los ultimos N partidos de un equipo segun su condición")
    print("3- Listar los primeros N goles anotados por un jugador")
    print("4- Consultar los partidos que diputó un equipo durante un periodo especifico")
    print("5- Consultar los partidos relacionados con un torneo durante un periodo especifico")
    print("6- Consultar las anotaciones de un jugador durante un periodo especifico")
    print("7- Clasificar los N mejores equipos del año dentro de un periodo especifico")
    print("8- Clasificar los N mejores anotadores en partidos oficiales dentro de un periodo especifico")
    print("9- Consultar el desempeño historico de ua selección en torneos oficiales")
    print("10- Medir memoria de los requerimientos")
    print("0- Salir")
    
def tamanio_archivo():
    working = True
    while working:
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
            working = False
        elif opcion == 2:
            tamanio_archivo = "10pct"
            working = False
        elif opcion == 3:
            tamanio_archivo = "20pct"
            working = False
        elif opcion == 4:
            tamanio_archivo = '30pct'
            working = False
        elif opcion == 5:
            tamanio_archivo = '50pct'
            working = False
        elif opcion == 6:
            tamanio_archivo = '80pct'
            working = False
        elif opcion == 7:
            tamanio_archivo = 'large'
            working = False
        elif opcion == 8:
            tamanio_archivo = 'small'
            working = False
        else:
            print("ingrese una opción valida")
    return tamanio_archivo

def type_loadfactor_scorers():
    working = True
    while working:
        print("------------------------Tipos de mapa--------------------")
        print("1- CHAINING")
        print('2- PROBING')
        working = True
        type_map = int(input('Seleccione el tipo de mapa en el que desea cargar el indice "scorers": \n'))
        if type_map == 1:
            type_map = "CHAINING"
            working = False
        elif type_map == 2:
            type_map = "PROBING"
            working = False
        else:
            print("opción invalida")
    load_factor = float(input('ingrese el factor de carga con el que desea cargar el indice "scorers":\n'))
    return type_map, load_factor
        

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

def print_carga_inicial(data):
    print("---------------------------------------")
    print("Numero de partidos: " + str( lt.size(data[0])))
    print("Numero de goles: " + str(lt.size(data[1])) )
    print("Numero de penales: " + str(lt.size(data[2])))
    print("Numero de jugadores cargados (lab 7): " + str(mp.size(data[3])))
    print("---------------------------------------")
    print()
    print('====================================================')
    print('=============== HISTORIAL DE LA FIFA ===============')
    print('====================================================')
    print()
    print('imprimiendo los primeros 3 y últimos 3 registros de los archivos ')
    print()
    print('--- RESULTADOS DE PARTIDOS ---')
    print('         Total de partidos: ' + str( lt.size(data[0])))
    print_tabla(data[0])
    print()
    print( '--- GOLES ---')
    print('         Total de goles anotados: ' + str(lt.size(data[1])) )
    print_tabla(data[1])
    print()
    print('--- PENALES ---')
    print('         Total de penales: ' + str(lt.size(data[2])))
    print_tabla(data[2])
    print()
    if len(data) == 6:
        print("Tiempo total de carga [ms]: " + str(round(data[4],3)) + " || Memoria utilizada [kB]: " + str(round(data[5], 3)))
    else:
        print("Tiempo total de carga: " + str(round(data[4],3)) )
    print()

    

def load_data(control, tamanio, memory=False):
    """
    Carga los datos
    """
    data = controller.load_data(control, tamanio, memory)
    #TODO: Realizar la carga de datos}
    return data


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(num_equipos_total , num_partidos_equipo , num_partidos_condicion , lista_final,  d_time, d_memory, equipo, condicion):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1


    print("=============== REQUERIMIENTO No. 1 Resultados ===============")
    print("No. total de equipos con información disponible: " + str(num_equipos_total))
    print("No. total de partidos de " + str(equipo) + " :" + str(num_partidos_equipo))
    print("No. total de partidos de " + str(equipo ) + " , cómo " + str(condicion) + " : " + str(num_partidos_condicion))
    print()
    print_tabla(lista_final)
    print()
    if d_memory != False:
        print("Tiempo de ejecución: " + str(d_time) + "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else:
        print("Tiempo de ejecució: " + str(round(d_time, 3)))
    print()


def print_req_2(n_jugadores_total , n_anotaciones_jugador, n_anotaciones_penalty , anotaciones_jugador,  d_time, d_memory , n_goles , nombre_jugador):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("=============== REQUERIMIENTO No. 2 Resultados ===============")
    print("No. total de jugadores con anotaciones: " + str(n_jugadores_total))
    print("No. total de goles de " + str(nombre_jugador) + " :" + str(n_anotaciones_jugador))
    print("No. total de goles  de " + str(nombre_jugador ) + " , desde el punto penal : " + str(n_anotaciones_penalty))
    print()
    print_tabla(anotaciones_jugador)
    print()
    if d_memory != False:
        print("Tiempo de ejecución: " + str(d_time) + "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else:
        print("Tiempo de ejecució: " + str(round(d_time, 3)))
    print()

    


def print_req_3(num_equipos_total , total_partidos_equipo,num_partidos_local , num_partidos_visitante  , lista_final_req3, d_time, d_memory , equipo ):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3

    print("=============== REQUERIMIENTO No. 3 Resultados ===============")
    print("No. total de equipos con partidos registrados: " + str(num_equipos_total))
    print("No. total de partidos de " + str(equipo) + " :" + str(total_partidos_equipo))
    print("No. total de partidos  de " + str(equipo ) + " ,  cómo Local: " + str(num_partidos_local))
    print("No. total de partidos  de " + str(equipo ) + " ,  cómo Visitante: " + str(num_partidos_visitante))
    print()
    print_tabla(lista_final_req3)
    print()
    if d_memory != False:
        print("Tiempo de ejecución: " + str(d_time) + "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else:
        print("Tiempo de ejecució: " + str(round(d_time, 3)))

    print()


def print_req_4(torneo, total_torneos, total_paises, total_ciudades, penales, partidos_en_fecha, d_time, d_memory):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    print("================== Partidos de un torneo en periodo ===================")
    print("Total de torneos con información disponibel : " + str(total_torneos))
    print("Total de partidos para" + str(torneo) + ": " +str(lt.size(partidos_en_fecha)) )
    print("Total de paises para " + str(torneo) + ": " + str(total_paises))
    print("Total de ciudades para " + str(torneo) + ": " + str(total_ciudades))
    print("Total de penales para:" + str(torneo) + ": " + str(penales))
    print()
    print_tabla(partidos_en_fecha)
    print()
    if d_memory != False:
        print("Tiempo de ejecución: " + str(d_time) + "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else:
        print("Tiempo de ejecució: " + str(round(d_time, 3)))
    print()


def print_req_5(jugador, t_jugadores_anot, num_anot, num_torn, num_penal, num_auto, listado, d_memoria, d_tiempo):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print ("============================ Anotaciones de un jugador en un periodo==================================")
    print("Total de jugadores con anotaciones registradas es: "+ str(t_jugadores_anot))
    print ("Total de anotaciones por " + str(jugador) + " fueron: " + str(num_anot))
    print ("Total numero de torneos en los que anoto " + str(jugador) + " fueron:" + str(num_torn) )
    print("Total de penaltis anotados por " + str(jugador) + " fueron: " + str(num_penal))
    print("Total numero de autogoles anotados por " + str(jugador) + " fueron: " + str(num_auto))
    print()
    print("----------------------------------------------------------------------------")
    print_tabla(listado)
    print()
    if d_memoria != False:
        print("tiempo de ejecución: " + str(round(d_tiempo,3))+ "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else: 
        print("tiempo de ejecución: " + str(round(d_tiempo,3)))
    
    # TODO: Imprimir el resultado del requerimiento 5


def print_req_6(torneo, anio, n, t_anios, t_torneos, t_eq_torn, t_match_anio, t_match_torneo,  t_paises, t_ciudades, max_ciudad, top_equipos, d_tiempo, d_memoria):
    
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    print("====================N mejores equipos de un torneo en el año " + str(anio) + "===========================")
    print("Total de años disponibles: " + str(t_anios))
    print("Total de torneos en el año: " + str(t_torneos))
    print("Total de equipos en el torneo: " + str(t_eq_torn))
    print("Total de encuentros en el año: " + str(t_match_anio))
    print("Totla de encuentros en el torneo: " +str(t_match_torneo))
    print("Total de paises involucados en el torneo: " + str(t_paises))
    print("Total de ciudades envolucradas en el torneo: " + str(t_ciudades))
    print("La ciudad en donde se disputaron mas partidos fue: "+ str(max_ciudad))
    print()
    print("Los mejores " + str(n) + " equipos del torneo " + str(torneo) + " en el año "+ str(anio) + " fueron: ")
    print_tabla(top_equipos)
    print()
    if d_memoria != False:
        print("tiempo de ejecución: " + str(round(d_tiempo,3))+ "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else: 
        print("tiempo de ejecución: " + str(round(d_tiempo,3)))


def print_req_7(torneo, puntos, total_torneos, total_anotadores, total_encuentros, total_anotaciones, total_penales, total_autogoles, goleadores_filtrados, d_tiempo, d_memory):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    print("=================== Anotadores con N puntos en un torneo ==================")
    print("Total de torneos con información disponible: " + str(total_torneos))
    print("Total de jugadores para " + torneo + ": " + str(total_anotadores))
    print("Total de partidos para " + str(torneo) + ": " +str(total_encuentros))
    print("Total de goles para " + torneo + ": " + str(total_anotaciones))
    print("Total de penales para " + torneo + ": " + str(total_penales))
    print("Total de autogoles para " + torneo + ": " + str(total_autogoles))
    print("Total de jugadores con " + str(puntos) + " puntos : " + str(mp.size(goleadores_filtrados)))
    print()
    print_tabla(goleadores_filtrados)
    print()
    if d_memory != False:
        print("Tiempo de ejecución: " + str(round(d_tiempo,3)) + "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else:
        print("Tiempo de ejecución: " + str(round(d_tiempo, 3)))


def print_req_8(anios, equipo, total_partidos, total_local, total_visitante, fecha_antiguo, ultimo_partido, anios_filtrados, d_tiempo, d_memory):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    print()
    print("=============================== BONO ==================================")
    print()
    print("  ++++++++++++ Estadisticas de " + str(equipo) + " ++++++++++++" )
    print("               Años: ",anios)
    print("               Años: con información disponible ", lt.size(anios_filtrados))
    print("               Total de partidos: ", total_partidos)
    print("               Total de partidos como local: ", total_local)
    print("               Total de partidos como visitante: ", total_visitante)
    print("               Fecha del partido más antiguo: ", fecha_antiguo)
    print()
    print("               ++++ Partido más reciente ++++")
    print()
    print(tabulate([ultimo_partido], headers="keys", tablefmt="grid", showindex=False))
    print()
    print("               ++++++++++++ Estadisticas anuales ++++++++++++")
    print()
    print_tabla(anios_filtrados)
    print()
    if d_memory != False:
        print("Tiempo de ejecución: " + str(round(d_tiempo,3)) + "|| Memoria utilizada [kB]: " + str(round(memoria, 2)))
    else:
        print("Tiempo de ejecución: " + str(round(d_tiempo, 3)))

        


# Se crea el controlador asociado a la vista
control = new_controller("PROBING", 0.5)

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    memoria = False
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            tamanio = tamanio_archivo()
            type_scorers, loadfactor_scorers = type_loadfactor_scorers()
            new_controller(type_scorers, loadfactor_scorers)
            opcion = input("¿Desea medir la memoria? Ingrese True/False:")
            if opcion.lower() == "true":
                data = load_data(control, tamanio, True)
                print("Cargando información de los archivos ....\n")
            elif opcion.lower() == "false":
                data = load_data(control, tamanio, False)
                print("Cargando información de los archivos ....\n")
            else:
                print("opción invalida, no se medirá la memoria")
                print()
                print("Cargando información de los archivos ....\n")
                data = load_data(control, tamanio)
            print()
            print_carga_inicial(data)
            
        elif int(inputs) == 2:
            
            equipo= input("Ingrese el nombre del equipo de su interés: \n")
            num_partidos = int(input("Ingrese el número de los últimos N partidos de su interés: \n"))
            condicion= input("Ingrese la condición del equipo; local, visitante o indiferente : \n")
            num_equipos_total , num_partidos_equipo , num_partidos_condicion , lista_final,  d_time, d_memory =  controller.req_1(control, equipo , condicion , num_partidos, memoria)
            print_req_1(num_equipos_total , num_partidos_equipo , num_partidos_condicion , lista_final,  d_time, d_memory, equipo, condicion) 



        elif int(inputs) == 3:
            
            n_goles=int(input("Ingrese el número de N goles de su interés: \n"))
            nombre_jugador= input("Ingrese el nombre del jugador de su interés: \n")

            n_jugadores_total , n_anotaciones_jugador, n_anotaciones_penalty , anotaciones_jugador,  d_time, d_memory= controller.req_2(control,n_goles , nombre_jugador, memoria )

            print_req_2(n_jugadores_total , n_anotaciones_jugador, n_anotaciones_penalty , anotaciones_jugador,  d_time, d_memory , n_goles , nombre_jugador)

        elif int(inputs) == 4:
            

            equipo= input("Ingrese el nombre del equipo de su interés: \n")
            f_inicial=input("Ingrese la fecha incial de su interés: \n")
            f_final= input("Ingrese la fecha final de su interés: \n")
            num_equipos_total , total_partidos_equipo,num_partidos_local , num_partidos_visitante  , lista_final_req3, d_time, d_memory = controller.req_3(control,equipo, f_inicial, f_final , memoria)

            print_req_3(num_equipos_total , total_partidos_equipo,num_partidos_local , num_partidos_visitante  , lista_final_req3, d_time, d_memory , equipo )

        elif int(inputs) == 5:
            nombre_torneo = input("Ingrese el nombre del torneo de interes: \n")
            fecha_inicio = input('Ingrese la fecha de inicio del periodo a consultar: \n')
            fecha_fin = input('La fecha final del periodo a consultar: \n')
            total_torneos,total_paises, total_ciudades, penales, partidos_en_fecha, d_time, d_memory = controller.req_4(control, nombre_torneo , fecha_inicio, fecha_fin, memoria)
            print_req_4(nombre_torneo, total_torneos,total_paises, total_ciudades, penales, partidos_en_fecha, d_time, d_memory)
            

        elif int(inputs) == 6:
            jugador= input("Ingrese el nombre del jugador que desea consultar:\n")
            fecha_i= input("Ingrese la fecha inicial desde la desea consultar:\n")
            fecha_f= input("Ingrese la fecha final hasta la que desea consultar:\n")
            t_jugadores_anot, num_anot, num_torn, num_penal, num_auto, listado, d_memoria, d_tiempo= controller.req_5(control, jugador, fecha_i, fecha_f, memoria)
            print_req_5(jugador,t_jugadores_anot, num_anot, num_torn, num_penal, num_auto, listado, d_memoria, d_tiempo)
            
        elif int(inputs) == 7:
            torneo= input("Ingrese el nombre del torneo que desea consultar: \n")
            anio= input("Ingrese el nombre del año que desea consultar: \n")
            n= input("Ingrese los top n partidos que desea consultar: \n")
            t_anios, t_torneos, t_eq_torn, t_match_anio, t_match_torneo, t_paises, t_ciudades, max_ciudad, top_equipos, d_tiempo, d_memoria= controller.req_6(control,torneo, n, anio, memoria)
            print_req_6(torneo, anio, n, t_anios, t_torneos, t_eq_torn, t_match_anio, t_match_torneo, t_paises, t_ciudades, max_ciudad, top_equipos, d_tiempo, d_memoria)

        elif int(inputs) == 8:
            torneo = input("Ingrese el nombre del torneo de interes:\n" )
            puntos = int(input("Ingrese el puntaje buscado: \n"))
            total_torneos, total_anotadores, total_encuentros, total_anotaciones, total_penales, total_autogoles, goleadores_filtrados, d_tiempo, d_memory = controller.req_7(control, torneo, puntos, memoria)
            print_req_7(torneo, puntos, total_torneos, total_anotadores, total_encuentros, total_anotaciones, total_penales, total_autogoles, goleadores_filtrados, d_tiempo, d_memory)

        elif int(inputs) == 9:
            equipo = input("Ingrese el nombre del equipo de interes: \n")
            anio_i = input("Ingrese el año de inicio: \n")
            anio_f = input("Ingrese el año de termino: \n")
            anios = int(anio_f) - int(anio_i)
            total_partidos, total_local, total_visitante, fecha_antiguo, ultimo_partido, anios_filtrados, d_time, d_memory = controller.req_8(control, equipo, anio_i, anio_f, memoria)
            print_req_8(anios, equipo, total_partidos, total_local, total_visitante, fecha_antiguo, ultimo_partido, anios_filtrados, d_time, d_memory)
        
        elif int(inputs) == 10:
            memory = input("Desea medir la memoria de cada opción del menú?: True/False: \n")
            if memory.lower() == "true":
                memoria = True
                print("Se medirá la memoria, tenga en cuenta que cada opción tomará más tiempo")
            else:
                memoria = False
                print("No se medirá la memoria")
        
        elif int(inputs) == 11:
            goles = control["model"]["goalscorers"]
            partidos = control["model"]["results_map"]
            working = True
            i = 1
            num = 1
            while i <= lt.size(goles):
                gol = lt.getElement(goles, i)
                key = str(gol["date"]) + str(gol["home_team"])
                partido_del_gol = mp.get(partidos, key)
                if partido_del_gol:
                    partido_del_gol = me.getValue(partido_del_gol)
                    if partido_del_gol["tournament"] == "UEFA Euro qualification":
                        print(str(num) )  
                        print(partido_del_gol, "es el prido relacionado con el gol: ", gol)
                        num += 1     
                else:
                    print("No hay partido relacionado para el gol:")
                    print(gol)
                i += 1

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)