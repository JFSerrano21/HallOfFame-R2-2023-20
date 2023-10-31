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

import tracemalloc
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


def new_controller(tipo_mapa,load_factor):
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller(tipo_mapa,load_factor)
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


def load_data(control, prefijo):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    data = controller.load_data(control,prefijo)
    return data

def print_sizes(control, prefijo):
    load_data(control, prefijo)
    results_size = controller.resultsSize(control)
    goalscorers_size = controller.goalscorersSize(control)
    shootouts_size = controller.shootoutsSize(control)
    print(f"Match result count: {results_size}")
    print(f"Goalscorers count: {goalscorers_size}")
    print(f"Shootout-Penalty definition count: {shootouts_size}")

def print_results_table(control, prefijo):
    results_info = controller.map_a_lista_results(control)
    results_size = controller.resultsSize(control)
    print(f"           Total match results: {results_size}")
    size = mp.size(results_info) 
    if size == 6:
        print("Results struct has more than 6 records...")
    elif size < 6:
        print("Results struct has less than 6 records...")
    headers_results=["date","home_team","away_team","home_score","away_score","country","city","tournament"]
    total = []
    for linea in lt.iterator(results_info):
        valores = linea["value"]
        lista1=[valores["date"], valores["home_team"],valores["away_team"],valores["home_score"],valores["away_score"],valores["country"], valores["city"], valores["tournament"]]
        total.append(lista1)
    print(tabulate(total, headers=headers_results))
    
def print_goalscorers_table(control, prefijo):
    total = controller.map_a_lista_goalscorers(control)
    goalscorers_size = controller.goalscorersSize(control)
    print(f"           Total goal scorers: {goalscorers_size}")
    headers_goalscorers=["date","home_team","away_team","scorer","team","minute","penalty", "own_goal"]
    print(tabulate(total, headers=headers_goalscorers))

def print_shootouts_table(control, prefijo):
    shootouts_info = controller.map_a_lista_shootouts(control)
    shootouts_size = controller.shootoutsSize(control)
    print(f"           Total shootouts: {shootouts_size}")
    size = mp.size(shootouts_info) 
    if size == 6:
        print("Shoootouts struct has more than 6 records...")
    elif size < 6:
        print("Shoootouts struct has less than 6 records...")
    headers_shhotouts=["date","home_team","away_team","winner"]
    total = []
    for linea in lt.iterator(shootouts_info):
        valores = linea["value"]
        lista1=[valores["date"], valores["home_team"],valores["away_team"],valores["winner"]]
        total.append(lista1)
    print(tabulate(total, headers=headers_shhotouts))


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control, num_equipos, nombre_equipo, condicion_equipo):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    headers_req1 = ["date", "home_team", "away_team", "home_score", "away_score", "tournament", "city", "country"]
    respuesta = controller.req_1(control, num_equipos, nombre_equipo, condicion_equipo)
    print(f"Total teams with available information: {respuesta[1]}")
    print(f"Total matches for {nombre_equipo}: {respuesta[2]}")
    print(f"Total matches for {nombre_equipo} as {condicion_equipo}: {respuesta[3]}")
    print(tabulate(respuesta[0],headers=headers_req1))
    
def print_req_2(control,jugador,ngoles):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    titulos = ["date","home_team","away_team","team","scorer","minute","own_goal","penalty"]
    resulto2 = controller.req_2(control,jugador,ngoles)
    rfinal = []
    nelem = int(lt.size(resulto2))

    print("Total scorers found: " + str(nelem))
    print("selecting " + str(nelem) + " scorers. . .")

    conti = 0

    if ngoles <= 6 or nelem <= 6:
        for f in lt.iterator(resulto2):
            lct = [f["date"],f["home_team"],f["away_team"],f["team"],jugador,f["minute"],f["own_goal"],f["penalty"]]
            rfinal.append(lct)
        if nelem < 6:
            print("Goal scorers has less than 6 records")
        else: 
            print("Goal scorers has 6 records")
    elif nelem > 6:
        for f in lt.iterator(resulto2):
            if conti<=3 or conti > nelem-3:
                lct = [f["date"],f["home_team"],f["away_team"],f["team"],jugador,f["minute"],f["own_goal"],f["penalty"]]
                rfinal.append(lct)
            conti+=1
        print("Goal scorers more than 6 records")
    return (tabulate(rfinal,headers=titulos))



def print_req_3(control, equipo, fecha_inicial, fecha_final):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    info = controller.req_3(control, equipo, fecha_inicial, fecha_final)
    print(f"Total teams with available information: {info[0]}")
    print(f"Total games for {equipo}: {info[1]}")
    print(f"Total home games for {equipo}: {info[2]}")
    print(f"Total away games for {equipo}: {info[3]}")
    todo = []
    headers_req3 = ["date", "home_team", "away_team", "home_score", "away_score", "tournament", "city", "country", "own_goal", "penalty"]
    for linea in info[4]:
        lista = [linea["date"], linea["home_team"], linea["away_team"], linea["home_score"], linea["away_score"], linea["tournament"], linea["city"], linea["country"], linea["own_goal"], linea["penalty"]]
        todo.append(lista)
    print()
    if info[1] > 6:
        print("The team results has more than 6 records...")
    elif info[1] == 6:
        print("The team results has 6 records...")
    else:
        print("The team results has less than 6 records...")
    print(tabulate(todo, headers=headers_req3))
    print()


def print_req_4(control, torneo, f1,f2):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4

    resulto1 = controller.req_4(control, torneo, f1, f2)
    data = resulto1["data"]
    tt = resulto1["total_tournamens"]
    encabe = ["date", "tournament", "country", "city", "home_team", "away_team","home_score", "away_score", "winner"]
    final = []
    Totp = 0
    Totc = 0 
    Tots = 0
    paises = lt.newList("ARRAY_LIST")
    ult = int(lt.size(resulto1["data"]))
    ciudades = lt.newList("ARRAY_LIST")
    conte = 0

    #conseguir el numero total de equipos, paises, ciudades y shootouts
    for j in lt.iterator(data):
        
        conte += 1
        if conte == 1:
            lt.addLast(ciudades, j["city"])
            Totc += 1
            lt.addLast(paises,j["country"])
            Totp += 1

        
        if int(lt.isPresent(ciudades, j["city"]))==0:
            lt.addLast(ciudades,j["city"])
            Totc += 1
        if int(lt.isPresent(paises, j["country"]))==0:
            lt.addLast(paises,j["country"])
            Totp += 1

        if str(j["winner"]) != "Unknow":
            Tots += 1

        if ult > 6 and conte <= 3 or conte > ult-3:
            lst1 = [j["date"],j["tournament"],j["country"],j["city"],j["home_team"],j["away_team"],j["home_score"],j["away_score"],j["winner"]]
            final.append(lst1)
        
        elif ult <= 6:
            lst1 = [j["date"],j["tournament"],j["country"],j["city"],j["home_team"],j["away_team"],j["home_score"],j["away_score"],j["winner"]]
            final.append(lst1)
        
    #imprimir los resultados  
    print("Total tournaments with aviable information: " + str(tt))
    print(str(torneo)+" Total matches " + str(ult))
    print(str(torneo)+" Total countries " + str(Totp))
    print(str(torneo)+" Total cities " + str(Totc))
    print(str(torneo)+" Total shootouts " + str(Tots))
    print()
    
    if ult >= 6:
        print("The tournament results has 6 or more records")
           
    elif ult < 6:
        print("The tournament results has less than 6 records")


    return (tabulate(final,headers=encabe))


def print_req_5(control, anotador, fecha_inicial, fecha_final):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    respuesta = controller.req_5(control, anotador, fecha_inicial, fecha_final)
    lista_tabulate=respuesta[1]
    lista_final = []
    headers_req5=['date',"minute","home_team","away_team","team","home_score","away_score","tournament","own_goal","penalty"]
    if lista_tabulate[1] == None:
        print("se encontraron menos de 6 datos:")
        for partido in lt.iterator(lista_tabulate[0]):
            valores_partido=list(partido.values())
            lista_final.append(valores_partido)
        
    else:
        for partido in lt.iterator(lista_tabulate[0]):
            valores_partido=list(partido.values())
            lista_final.append(valores_partido)
        for partido in lt.iterator(lista_tabulate[1]):
            valores_partido=list(partido.values())
            lista_final.append(valores_partido)
    print(f"Total players with available information: {respuesta[0]}")
    print(f"Total goals for {anotador}: {respuesta[3]}")
    print(f"Total torunaments for {anotador}: {respuesta[2]}")
    print(f"Total penalties for {anotador}: {respuesta[4]}")
    print(f"Total own goals for {anotador}: {respuesta[5]}")
    print(tabulate(lista_final, headers=headers_req5))
    
    


def print_req_6(control, n, tournament, year):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    info = controller.req_6(control, n, tournament, year)
    print(f"Total tournaments with available information: {info[0]}")
    print(f"Total teams for {tournament}: {info[1]}")
    print(f"Total matches for {tournament}: {info[2]}")
    print(f"Total countries for {tournament}: {info[3]}")
    print(f"Total cities for {tournament}: {info[4]}")
    print(f"City with most matches for {tournament}: {info[5]}")
    print()
    if info[1] > 6:
        print(f"Top {n} teams results has more than 6 records...")
    elif info[1] == 6:
        print(f"Top {n} teams results has 6 records...")
    else:
        print(f"Top {n} teams results has less than 6 records...")
    headers_req6 = ["team","total_points","goal_difference","penalty_points", "matches", "own_goal_points", "wins", "draws", "losses", "goals_for", "goals_against", "top_scorer"]
    total = []
    for linea in info[6]:
        top_scorer_lista = linea["top_scorer"]
        mas_goles = -1
        scorer_headers = ["scorer", "goals", "matches", "avg_time [min]"]
        for jugador in top_scorer_lista:
            if jugador["goals"] > mas_goles:
                mas_goles = jugador["goals"]
                matches = 0
                if jugador["matches"] != None:
                    matches = lt.size(jugador["matches"])
                avg_time = 0.0
                if jugador["avg_time [min]"] != None:
                    for minuto in lt.iterator(jugador["avg_time [min]"]):
                        avg_time += float(minuto)
                    avg_time = avg_time / lt.size(jugador["avg_time [min]"])
                lista_jugador = [[jugador["scorer"], jugador["goals"], matches, avg_time]]
        scorer = tabulate(lista_jugador, headers=scorer_headers)
        lista1=[linea["team"], linea["total_points"], linea["goal_difference"], linea["penalty_points"], lt.size(linea["matches"]), linea["own_goal_points"], linea["wins"], linea["draws"], linea["losses"], linea["goals_for"], linea["goals_against"], scorer]
        total.append(lista1)
    print(tabulate(total, headers=headers_req6))


def print_req_7(control, numero_jugadores, torneo):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    tracemalloc.start()
    respuesta= controller.req_7(control, numero_jugadores, torneo)
    
    tabla_tabulate=respuesta
    headers_tabla_tabulate=["scorer", "total_points", "total_goals", "penalty_goals", "own_goals", "avg_time [min]", "scored_in_wins", "scored_in_losses", "scored_in_draws", "last_goal"]
    print(f"Total tournaments with available information: {respuesta[3]}")
    print(f"Total players for {torneo}: {respuesta[2]}")
    print(f"Total matches for {torneo}: {respuesta[5]}")
    print(f"Total goals for {torneo}: {respuesta[4]}")
    print(f"Total penalties for {torneo}: {respuesta[6]}")
    print(f"Total own goals for {torneo} : {respuesta[7]}")
    print(f"Players with {numero_jugadores} points:{respuesta[8]}")
    print(tabulate(tabla_tabulate[0],headers=headers_tabla_tabulate))
    
    

def print_req_81(control,pais,f1,f2):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    titulos = ["date","home_team","away_team","away_score","country","city","tournament"]
    resultos = controller.req_8(control,pais,f1,f2)
    taw = resultos["away_m"]
    tho = resultos["home_m"]
    ultm = resultos["last_match"]
    primerp = resultos["f_date"]
    tmatches = lt.size(resultos["data"])
    yearos = int(f2) - int(f1)
    print("        --------- "+str(pais)+"Statistics ---------")
    print("                Years: "+ str(yearos))
    print(                "Total matches: " + str(tmatches))
    print("                Total home matches: "+str(tho))
    print("                Total away matches: "+str(taw))
    print("                Oldest match date: " +str(primerp))
    print()
    print("                +++ Newest match data +++")
    return tabulate(ultm,headers=titulos)

def print_req_8(control,pais,f1,f2):
    
    pass

# Se crea el controlador asociado a la vista


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
            print("1. Medir memoria")
            print("2. Medir timepo")
            print("3. No medir ninguna")
            memoria_o_tiempo=input("Seleccione una opción: ")
            medir_memoria=False
            medir_timepo=False
            if memoria_o_tiempo=="1":
                medir_memoria=True
            elif memoria_o_tiempo=="2":
                medir_timepo=True
            tiempo=0
            memoria=0
            
            print("Seleccione qué porcentaje de datos desea cargar...")
            print("1. 5%")
            print("2. 10%")
            print("3. 20%")
            print("4. 30%")
            print("5. 50%")
            print("6. 80%")
            print("7. Large")
            print("8. Small")
            prefijo="nada xd"
            porcentaje=int(input("Seleccione una opción para continuar: "))
            if porcentaje==1:
                prefijo="5pct"
            elif porcentaje==2:
                prefijo="10pct"
            elif porcentaje==3:
                prefijo="20pct"
            elif porcentaje==4:
                prefijo="30pct"
            elif porcentaje==5:
                prefijo="50pct"
            elif porcentaje==6:
                prefijo="80pct"
            elif porcentaje==7:
                prefijo="large"
            elif porcentaje==8:
                prefijo="small"
            print("Elija el tipo de mapa que desea cargar")
            print("1. Chaining")
            print("2. Linear Probing")
            tipo_mapa=input("Seleccione una opción para continuar: ")
            if tipo_mapa=="1":
                tipo_mapa="CHAINING"
            elif tipo_mapa=="2":
                tipo_mapa="PROBING"
            load_factor=float(input("Ingrese load_factor: "))
            control = new_controller(tipo_mapa,load_factor)
            print("Cargando información de los archivos ....\n")
            print("Loading data...")
            print("------------------------------")
            if medir_memoria==True:
                tracemalloc.start()
                memoria_inicial=controller.get_memory()
                print_sizes(control, prefijo)
                memoria_final=controller.get_memory()
                tracemalloc.stop
                memoria = controller.delta_memory(memoria_final,memoria_inicial)
            elif medir_timepo==True:
                tiempo_inicial = controller.get_time()
                print_sizes(control, prefijo)
                tiempo_final = controller.get_time()
                tiempo= abs(controller.delta_time(tiempo_final,tiempo_inicial))
            else:
                print_sizes(control, prefijo)
                
            print("------------------------------")
            print()
            print("=============================================")
            print("============ FIFA RECORDS REPORT ============")
            print("=============================================")
            print()
            print("Printing results for the first 3 and last 3 records on file.")
            print()
            print("--- MATCH RESULTS ---")
            print_results_table(control, prefijo)
            print()
            print("--- GOAL SCORERS ---")
            print_goalscorers_table(control, prefijo)
            print()
            print("--- SHOOTOUTS ---")
            print_shootouts_table(control, prefijo)
            print()
            if medir_memoria==True:
                print(f"Memoria usada: {memoria}")
            elif medir_timepo==True:
                print(f"Tiempo que tomó la carga: {tiempo}ms")
                            
        elif int(inputs) == 2:
            num_equipos = int(input("Seleccione el número de equipos que desea consultar: "))
            nombre_equipo = input("Seleccione el nombre del equipo a consultar: ")
            condicion_equipo = input("Seleccione la condición del equipo: ")
            #num_equipos = 15
            #nombre_equipo = "Italy"
            #condicion_equipo = "away"
            print_req_1(control, num_equipos, nombre_equipo, condicion_equipo)

        elif int(inputs) == 3:
            print("========= Req No. 2 Inputs =========")
            jugador = input("Scorer name: ")
            ng = int(input("Number of scores: "))
            print()
            print("========= Req No. 2 Results =========")
            tracemalloc.start()
            memoria_inicial=controller.get_memory()
            tiempo_i = controller.get_time()
            print(print_req_2(control,jugador,ng))
            tiempo_final = controller.get_time()
            memoria_final=controller.get_memory()
            tracemalloc.stop()
            tiempo= abs(controller.delta_time(tiempo_final,tiempo_i))
            memoria = controller.delta_memory(memoria_final,memoria_inicial)
            print(f"Tiempo que tomó la función: {tiempo}ms")
            print(f"Memoria usada: {memoria}")

        elif int(inputs) == 4:
            print("========= Req No. 3 Inputs =========")
            equipo = input("Team name: ")
            fecha_inicial = input("Start date: ")
            fecha_final = input("End date: ")
            print()
            print("========= Req No. 3 Results =========")
            tracemalloc.start()
            memoria_inicial=controller.get_memory()
            tiempo_inicial = controller.get_time()
            print_req_3(control, equipo, fecha_inicial, fecha_final)
            tiempo_final = controller.get_time()
            memoria_final=controller.get_memory()
            tracemalloc.stop()
            tiempo= abs(controller.delta_time(tiempo_final,tiempo_inicial))
            memoria = controller.delta_memory(memoria_final,memoria_inicial)
            print(f"Tiempo que tomó la carga: {tiempo}ms")
            print(f"Memoria usada: {memoria}")

        elif int(inputs) == 5:
            print("========= Req No. 4 Inputs =========")
            torneo = input("Tournament name: ")
            f1 = input("Start date In YYYY-mm-dd: ")
            f2 = input("End date In YYYY-mm-dd: ")
            print()
            print("========= Req No. 4 Results =========")
            tracemalloc.start()
            memoria_inicial=controller.get_memory()
            tiempo_i = controller.get_time()
            print(print_req_4(control,torneo,f1,f2))
            memoria_final=controller.get_memory()
            tracemalloc.stop()
            tiempo_final = controller.get_time() 
            tiempo= abs(controller.delta_time(tiempo_final,tiempo_i))
            memoria = controller.delta_memory(memoria_final,memoria_inicial)
            print(f"Tiempo que tomó la función: {tiempo}ms")
            print(f"Memoria usada: {memoria}")

        elif int(inputs) == 6:
            
            #anotador = "Ali Daei"
            #fecha_inicial = "1999-03-25"
            #fecha_final = "2021-11-23"
            anotador = input("Scorer: ")
            fecha_inicial = input("Start date: ")
            fecha_final = input("End date: ")
            
            print_req_5(control, anotador, fecha_inicial, fecha_final)

        elif int(inputs) == 7:
            print("========= Req No. 6 Inputs =========")
            n = int(input("Top N: "))
            tournament = input("Tournament name: ")
            year = input("Consult year: ")
            print(f"Start date: {year}-01-01 in consult year")
            print(f"End date: {year}-12-31 in consult year")
            print()
            print("========= Req No. 6 Results =========")
            tracemalloc.start()
            memoria_inicial=controller.get_memory()
            tiempo_inicial = controller.get_time()
            print_req_6(control, n, tournament, year)
            tiempo_final = controller.get_time()
            memoria_final=controller.get_memory()
            tracemalloc.stop()
            tiempo= abs(controller.delta_time(tiempo_final,tiempo_inicial))
            memoria = controller.delta_memory(memoria_final,memoria_inicial)
            print(f"Tiempo que tomó la carga: {tiempo}ms")
            print(f"Memoria usada: {memoria}")

        elif int(inputs) == 8:
            #puntaje_jugador = 2
            #torneo = "UEFA Euro qualification"
            puntaje_jugador = int(input("Ingrese el puntaje de los jugadores que desea conocer: "))
            torneo =  input("Ingrese el torneo del cual desea obtener información: ")
            print_req_7(control, puntaje_jugador, torneo)

        elif int(inputs) == 9:
            print("========= Req No. 8 Inputs =========")
            pais = str(input("Team name: "))
            f1 = int(input("Start year: "))
            f2 =int(input("End year: "))
            print("Start date In " + str(f1) + "-01-01 in year: "+ str(f1))
            print("End date In" + str(f2) + "-12-31 in year: "+ str(f2))
            print("consulting date range")
            print()
            print("        ========= Req No. 8 Results =========")
            tiempo_i = controller.get_time()
            print(print_req_81(control,pais,f1,f2))
            print()
            print()
            print()
            print(print_req_8(control,pais,f1,f2))
            tiempo_f = controller.get_time()
            delta_time = controller.delta_time(tiempo_i, tiempo_f)
            result = f"{delta_time:.3f}"
            print()
            print(f"La función se demora {result} ms.")

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
