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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import csv
from tabulate import tabulate 
import time
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs(tipo_mapa,lf):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {"results": None,
                    "goalscorers" : None,
                    "shootouts" : None,
                    "team" : None,
                    "scorers" : None,
                    "tournament" : None,
                    "anios_torneo":None,
                    "home_away_team_results" : None,
                    "home_away_team_goalscorers": None}
    
    data_structs["results"] =lt.newList("ARRAY_LIST",cmpfunction=cmpCargaDatos)
    
    data_structs["goalscorers"] =lt.newList("ARRAY_LIST",cmpfunction=cmpCargaDatos)
    
    data_structs["shootouts"] =  lt.newList("ARRAY_LIST",cmpfunction=cmpCargaDatos)

    #Ordena partidos de results por equipos
    data_structs["team"] = mp.newMap(350,
                                     maptype=tipo_mapa,
                                     loadfactor=lf)
    
    #Ordena partidos de goalscorers por jugados
    data_structs["scorers"] = mp.newMap(13500,
                                        maptype=tipo_mapa,
                                        loadfactor=lf)
    
    #Ordena partidos de results por torneo
    data_structs["tournament"] = mp.newMap(145,
                                           maptype="CHAINING",
                                           loadfactor=4)
    
    #Ordena partidos de results por año y luego por torneo
    data_structs["anios_torneo"]=mp.newMap(160,
                                           maptype="CHAINING",
                                           loadfactor=4)
    
    #Ordena partidos de results por fecha-equipo local-equipo visitante
    data_structs["home_away_team_results"] = mp.newMap(44800,
                                                        maptype=tipo_mapa,
                                                        loadfactor=lf)
    
    #Ordena partidos de goalscorers por fecha-equipo local-equipo visitante
    data_structs["home_away_team_goalscorers"] = mp.newMap(44800,
                                                            maptype=tipo_mapa,
                                                            loadfactor=lf)
    
    #Ordena partidos de shootouts por fecha-equipo local-equipo visitante
    data_structs["home_away_team_shootouts"] = mp.newMap(560,
                                                            maptype=tipo_mapa,
                                                            loadfactor=lf)

    return data_structs


#Funciones de cargar Datos
def carga_resultados(data_structs,archivo):
    """
    Función para cargar los datos del archivo de "results"
    """

    nombre_archivo=cf.data_dir+"football/results-utf8-"+archivo
    archivo_leido= csv.DictReader(open(nombre_archivo, encoding="utf-8"))   
    for cada_linea in archivo_leido:
        add_data_lists(data_structs,cada_linea,"results")
        add_data_map(data_structs,cada_linea,"tournament","tournament")
        add_data_mapTeam(data_structs,cada_linea)
        add_data_mapAnio_torneo(data_structs["anios_torneo"],cada_linea)
        add_data_partido(data_structs,"home_away_team_results",cada_linea)
    return data_size(data_structs, "results")

def carga_goleadores(data_structs,archivo):
    """
    Función para cargar los datos del archivo de "goalscorers"
    """
    nombre_archivo=cf.data_dir+"football/goalscorers-utf8-"+archivo
    archivo_leido= csv.DictReader(open(nombre_archivo, encoding="utf-8"))
    for cada_linea in archivo_leido:
        add_data_lists(data_structs,cada_linea,"goalscorers")
        add_data_map(data_structs,cada_linea,"scorers","scorer")
        add_data_map_simplificado_llave(data_structs["home_away_team_goalscorers"],cada_linea, (cada_linea["date"]+ "-" + cada_linea["home_team"] + "-" + cada_linea["away_team"]))
    return data_size(data_structs, "goalscorers")

def carga_penales(data_structs,archivo):
    """
    Función para cargar los datos del archivo de "shootouts"
    """
    nombre_archivo=cf.data_dir+"football/shootouts-utf8-"+archivo
    archivo_leido= csv.DictReader(open(nombre_archivo, encoding="utf-8"))
    for cada_linea in archivo_leido:
        add_data_lists(data_structs,cada_linea,"shootouts")
        add_data_partido(data_structs,"home_away_team_shootouts",cada_linea)
    return data_size(data_structs, "shootouts")

# Funciones para agregar informacion al modelo

def add_data_lists(data_structs, data, archivo):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs[archivo],data)
    return data_structs

def add_data_map(data_structs, data, archivo, llave):
    """
    Función para agregar nuevos elementos a un mapa
    """
    titl=mp.contains(data_structs[archivo], data[llave])
    if titl:
        ind=mp.get(data_structs[archivo], data[llave])
        partidos=me.getValue(ind)
        lt.addLast(partidos, data)
        mp.put(data_structs[archivo], data[llave], partidos)
    else:
        partidos=lt.newList("ARRAY_LIST")
        lt.addLast(partidos, data)
        mp.put(data_structs[archivo], data[llave], partidos)

def add_data_map_simplificado(mapa, data, val):
    """
    Función para agregar nuevos elementos a un mapa
    """
    llave=data[val]
    titl=mp.contains(mapa, llave)
    if titl:
        ind=mp.get(mapa, llave)
        partidos=me.getValue(ind)
        lt.addLast(partidos, data)
        mp.put(mapa, llave, partidos)
    else:
        partidos=lt.newList("ARRAY_LIST")
        lt.addLast(partidos, data)
        mp.put(mapa, llave, partidos)

def add_data_map_simplificado_llave(mapa, data, llave):
    """
    Función para agregar nuevos elementos a un mapa
    """
    titl=mp.contains(mapa, llave)
    if titl:
        ind=mp.get(mapa, llave)
        partidos=me.getValue(ind)
        lt.addLast(partidos, data)
        mp.put(mapa, llave, partidos)
    else:
        partidos=lt.newList("ARRAY_LIST")
        lt.addLast(partidos, data)
        mp.put(mapa, llave, partidos)

def add_data_mapAnio_torneo(mapa, data):
    """
    Función para agregar nuevos elementos a un mapa segun el año
    """
    anio=data["date"]
    llave=anio[0:4]
    an=mp.contains(mapa, llave)
    if an:
        ind=mp.get(mapa, llave)
        torneos=me.getValue(ind)
        add_data_map_simplificado(torneos,data,"tournament")
    else:
        torn=mp.newMap(145,
                       maptype="CHAINING",
                       loadfactor=4)
        partidos=lt.newList("ARRAY_LIST")
        lt.addLast(partidos, data)
        mp.put(torn,data["tournament"],partidos)
        mp.put(mapa, llave, torn)

def add_data_partido(data_structs, nom_mapa, data):
    #Agrega partido, por llave local-visitante
    mp.put(data_structs[nom_mapa], (data["date"]+ "-" + data["home_team"] + "-" + data["away_team"]), data)

def add_data_mapTeam(data_structs,data):
    """
    Función para agregar nuevos elementos a los mapas, de team y home_away_team
    """
    #Agrega equipo local a mapa
    local=mp.contains(data_structs["team"], data["home_team"])
    if local:
        ind=mp.get(data_structs["team"], data["home_team"] )
        partidos=me.getValue(ind)
        lt.addLast(partidos, data)
        mp.put(data_structs["team"], data["home_team"], partidos)
    else:
        partidos=lt.newList("ARRAY_LIST")
        lt.addLast(partidos, data)
        mp.put(data_structs["team"], data["home_team"], partidos)
    
    #Agrega equipo visitante a mapa
    visitante=mp.contains(data_structs["team"], data["away_team"])
    if visitante:
        ind=mp.get(data_structs["team"], data["away_team"])
        partidos=me.getValue(ind)
        lt.addLast(partidos, data)
        mp.put(data_structs["team"], data["away_team"], partidos)
    else:
        partidos=lt.newList("ARRAY_LIST")
        lt.addLast(partidos, data)
        mp.put(data_structs["team"], data["away_team"], partidos)
    


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def creartabla (lista,primer_valor): 
    titulos = primer_valor.keys()
    filas =[]
    for partido in lt.iterator(lista):
        fila=[]
        valores=partido.values()
        fila.extend(valores)
        filas.append(fila)
    tabla = tabulate(filas, headers = titulos, tablefmt = "grid" )
    return tabla

# Funciones de consulta
def resumir_lista(lista_final):
    """
    Crea una tabala en donde se encuentran los primeros 3 valores y los ultimos 3 valores de la lista que ingresa
    """
    nueva_lista=lt.newList("ARRAY_LIST")
    n = lt.size(lista_final)
    posiciones = [1,2,3,n-2,n-1,n]
    for i in posiciones:
        elemento = lt.getElement(lista_final,i)
        lt.addLast(nueva_lista,elemento)
    return nueva_lista

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs,nom_archivo):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    return lt.size(data_structs[nom_archivo])

def req_1(data_structs,condicion, n, team):
    """
    Función que soluciona el requerimiento 1
    """
   
    equipos = data_structs["model"]["team"]
    lista_seleccionados = lt.newList("ARRAY_LIST")
    pareja = mp.get(equipos,team)
    lista = me.getValue(pareja)
    total_equipo = lt.size(lista)
    if condicion == "home" or condicion == "away":
        for equipo in lt.iterator(lista):
            if condicion == "home":
                if  team == equipo["home_team"]:
                    lt.addLast(lista_seleccionados,equipo)
            elif condicion == "away":
                if  team == equipo["away_team"]:
                    lt.addLast(lista_seleccionados,equipo)
    else:
        lista_seleccionados = lista
    sub_total = lt.size(lista_seleccionados)
    quk.sort(lista_seleccionados,cmp_partidos_results)
    total_equipos = mp.size(equipos) 
    
    
    if sub_total > n:
        lista_final = lt.subList(lista_seleccionados,1,n)
        tamaño = lt.size(lista_final)
    else:
        lista_final = lista_seleccionados
        tamaño = lt.size(lista_seleccionados)
    return lista_final, sub_total, total_equipos,total_equipo,tamaño

def req_2(data_structs, n, jugador):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    
    #Se llama al mapa correspondiente a los anotadores y se obtiene su tamaño
    jugadores = data_structs["model"]["scorers"]
    size = mp.size(jugadores)
    
    #Se crea una lista vacía, y se inicia un contador para contar los goles por penales
    lista_final = lt.newList("ARRAY_LIST")
    subtotal_penales = 0

    #Se obtiene el valor a partir de la llave correspondiente al jugador que entra por parámetro
    pareja = mp.get(jugadores, jugador)
    lista_jugadores = me.getValue(pareja)

    #Se obtiene la cantidad de goles realizados por el jugador que entra por parámetro
    size_jugadores = lt.size(lista_jugadores)

    #Se itera sobre la lista con la información de cada jugador, se suma uno si el gol fue realizado por penal, y se agrega a la lista
    for jugador in lt.iterator(lista_jugadores):
        if jugador["penalty"] == "True":
            subtotal_penales += 1
        lt.addLast(lista_final,jugador)
    
    #Se ordena
    quk.sort(lista_final,cmpreq2)   

    #Verificar si el numero total es mayor al ingresado, y se crea la sublista con el numero exacto 
    if size_jugadores > n:
        lista_goles_final= lt.subList(lista_final,1,n)
        tamaño = lt.size(lista_goles_final)
    else:
        lista_goles_final = lista_final
        tamaño = lt.size(lista_goles_final)
   
    return size, size_jugadores, subtotal_penales, lista_goles_final, tamaño


def req_3(data_structs, equipo, fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 3
    """
   #Se llama al mapa de los partidos en goalscorers identificados por fecha- equipo local- equipo viaitante
    goalscorers_map = data_structs["model"]["home_away_team_goalscorers"]

    #Se llama al mapa correspondiente a todos los equipos
    equipos = data_structs["model"]["team"]

    #Se crea la lista donde se almacenarán los partidos filtrados, y se inician contadores para subtotales
    total_partidos = lt.newList("ARRAY_LIST")
    size_subtotal_local = 0
    size_subtotal_visitante = 0

    #Se obtiene el valor a partir de la llave correspondiente al equipo que entra por parámetro
    por_equipo = mp.get(equipos, equipo)
    partidos=me.getValue(por_equipo)

    #Se itera sobre la lista de partidos por cada equipo, y se filtra por fecha 
    for partido in lt.iterator(partidos):
        if partido["date"] >= fecha_inicial and partido["date"] <= fecha_final:
    
    #Se filtra según la condición del equipo y se suma al contador
            if partido["home_team"] == equipo:
                size_subtotal_local += 1

            if partido["away_team"] == equipo:
                size_subtotal_visitante += 1

    #Se trae la información de penalty y own goal del mapa de goalscorers, y se añaden estos partidos a la lista vacía
            x = mp.contains(goalscorers_map, (partido["date"]+ "-"+partido["home_team"]+"-"+partido["away_team"]))
            if x:

                goal = me.getValue(mp.get(goalscorers_map, partido["date"]+ "-"+partido["home_team"]+"-"+partido["away_team"]))

                for g in lt.iterator(goal):
                    partido["penalty"] = g["penalty"]
                    partido["own_goal"] = g["own_goal"]
            else:
                partido["penalty"] = "Unknown"
                partido["own_goal"] = "Unknown"

            lt.addLast(total_partidos, partido)
            
    #Se halla el tamaño del total de equipos y el total de partido filtrado    
    total_equipos = mp.size(equipos)
    size_total_partidos = lt.size(total_partidos)

    #Se ordena  
    quk.sort(total_partidos,cmpreq3)        
    return total_equipos, size_total_partidos, size_subtotal_local, size_subtotal_visitante, total_partidos
    


def req_4(data_structs, torneo,fecha_inicial, fecha_final):
    """
    Función que soluciona el requerimiento 4
    """
    
    
    shootout_map =data_structs["model"]["home_away_team_shootouts"]
    torneos = data_structs["model"]["tournament"]
    shootout = 0 
    paises = lt.newList("ARRAY_LIST")
    ciudades = lt.newList("ARRAY_LIST")
    lista_final=lt.newList("ARRAY_LIST")
    #al recorrer results filtrar cada partido por fecha y torneo para agregarlo a otra lista,agregar cada pais y ciudad a sus respectivas listas
    tournament = mp.get(torneos, torneo)
    partidos=me.getValue(tournament)
    for partido in lt.iterator(partidos):
        if partido["date"] >= fecha_inicial and partido["date"] <= fecha_final:
                x=mp.contains(shootout_map,(partido["date"]+ "-"+partido["home_team"]+"-"+partido["away_team"]))
                if x:
                    shoot=me.getValue(mp.get(shootout_map,partido["date"]+ "-"+partido["home_team"]+"-"+partido["away_team"]))
                    partido["winner"] = shoot["winner"]
                    shootout += 1
                
                else:
                    partido["winner"] = "Unknown"
                lt.addLast(lista_final,partido)
                if lt.isPresent(paises,partido["country"]) == 0:
                    lt.addLast(paises,partido["country"])
                if lt.isPresent(ciudades,partido["city"]) == 0:
                    lt.addLast(ciudades,partido["city"])
    #Ver el tamaño de estas lista para encontrar los totales pedidos
    countries = lt.size(paises)
    cities = lt.size(ciudades)        
    total_partidos = lt.size(lista_final)
    total_tournament = mp.size(torneos)
    quk.sort(lista_final,cmp_partidos_results)
    return total_tournament,lista_final,total_partidos, shootout,countries,cities


def req_5(data_structs,nombre,fecha_inicio,fecha_final):
    """
    Función que soluciona el requerimiento 5
    """
    # Sacar lista del mapa y extraer por el periodo de tiempo
    jug=mp.contains(data_structs["scorers"],nombre)
    if jug is False:
        return 0, 0, 0, 0, 0, 0
    ind=mp.get(data_structs["scorers"], nombre)
    partidos=me.getValue(ind)

    penal=0
    autogol=0
    torneos=lt.newList("ARRAY_LIST")

    finales=lt.newList("ARRAY_LIST")
    for gol in lt.iterator(partidos):
        if fecha_inicio<=gol["date"] and gol["date"]<=fecha_final:
            info_extra=me.getValue(mp.get(data_structs["home_away_team_results"],(gol["date"]+ "-" + gol["home_team"] + "-" + gol["away_team"])))
            if gol["penalty"] =="True":
                penal+=1
            if gol["own_goal"] == "True":
                autogol+=1

            #Formar diccionario para imprimir
            partido={
                "date":gol["date"], 
                "minute":gol["minute"],
                "home_team":gol["home_team"],
                "away_team":gol["away_team"], 
                "team":gol["team"], 
                "home_score":info_extra["home_score"],
                "away_score":info_extra["away_score"],
                "tournament":info_extra["tournament"],
                "penalty":gol["penalty"],
                "own_goal":gol["own_goal"]}
            lt.addLast(finales,partido)

            torneo=info_extra["tournament"]
            if lt.isPresent(torneos,torneo) == 0:
                lt.addLast(torneos, torneo)
    
    merg.sort(finales,cmp_goals_scorers)
    tot_goleadores=mp.size(data_structs["scorers"])

    return tot_goleadores, lt.size(finales), lt.size(torneos), penal, autogol, finales




def req_6(data_structs,n,torneo,anio):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    #Extraer todos los torneos de ese año
    an_io=mp.contains(data_structs["anios_torneo"],anio)
    if an_io: 
        ind=mp.get(data_structs["anios_torneo"],anio)
        torneos=me.getValue(ind)
    else:
        return(0,0,0,0,0,0,0,0)
    
    #Extraer el torneo especifico 
    tor=mp.contains(torneos,torneo)
    if tor: 
        ind=mp.get(torneos,torneo)
        partidos=me.getValue(ind)
    else:
        return(0,0,0,0,0,0,0,0)
    
    #Trabajar con los datos
    cant_p=lt.size(partidos)
    equipo=mp.newMap(cant_p*3,
                     maptype="PROBING",
                     loadfactor=0.7)
    
    paises=lt.newList("ARRAY_LIST")
    ciudades=mp.newMap(cant_p,
                       maptype="PROBING",
                       loadfactor=0.7)

    #Divide por equipos
    for partido in lt.iterator(partidos):
        add_data_map_simplificado(equipo,partido,"home_team")
        add_data_map_simplificado(equipo,partido,"away_team")
        add_data_map_simplificado(ciudades,partido,"city")
        if lt.isPresent(paises,partido["country"])==0:
            lt.addLast(paises,partido["country"])

    lista_final=lt.newList("ARRAY_LIST")
    partidos_totales=lt.size(partidos)
    #Saca informacion completa por equipos
    llaves=mp.keySet(equipo)
    tam=lt.size(llaves)
    for equip in lt.iterator(llaves):
        team=mp.get(equipo,equip)
        team=me.getValue(team)
        partidos=lt.size(team)
        goles_favor=0
        goles_contra=0
        puntos=0
        wins=0
        draws=0
        losses=0
        penal=0
        autogol=0
        goleador=lt.newList("ARRAY_LIST")
        for partido in lt.iterator(team):
            if partido["home_team"]==equip:
                goles_favor+=int(partido["home_score"])
                goles_contra+=int(partido["away_score"])
                if partido["home_score"]>partido["away_score"]:
                    wins+=1
                    puntos+=3
                elif partido["home_score"]<partido["away_score"]:
                    losses+=1
                else:
                    draws+=1
                    puntos+=1
            else: 
                goles_favor+=int(partido["away_score"])
                goles_contra+=int(partido["home_score"])
                if partido["home_score"]<partido["away_score"]:
                    wins+=1
                    puntos+=3
                elif partido["home_score"]>partido["away_score"]:
                    losses+=1
                else:
                    draws+=1
                    puntos+=1
            
            gol=mp.contains(data_structs["home_away_team_goalscorers"],(partido["date"]+ "-" + partido["home_team"] + "-" + partido["away_team"]))
            if gol: 
                gol=me.getValue(mp.get(data_structs["home_away_team_goalscorers"],(partido["date"]+ "-" + partido["home_team"] + "-" + partido["away_team"])))
                for g in lt.iterator(gol):
                    if g["team"]==equip:
                        if g["penalty"] =="True":
                            penal+=1
                        if g["own_goal"] == "True":
                            autogol+=1
                        lt.addLast(goleador,g)

        goleadores=mp.newMap(partidos,
                     maptype="PROBING",
                     loadfactor=0.7)
        for gol in lt.iterator(goleador):
            add_data_map_simplificado(goleadores,gol,"scorer")
        
        prom_min,scorer,matches,goals=encontrar_goleador(goleadores)

        datos_jugador=lt.newList("ARRAY_LIST")
        dt={"scorer":scorer,
            "goals": goals,
            "matches":matches,
            "avg_time [min]":prom_min}
        lt.addLast(datos_jugador,dt)
        gols=creartabla(datos_jugador,datos_jugador["elements"][0])


        #Formar diccionario para imprimir
        equip_final={"team":equip,
                     "total_points":puntos,
                     "goal_difference":(goles_favor-goles_contra),
                     "penalty_points":penal,
                     "matches":partidos,
                     "own_goals_points":autogol,
                     "wins":wins,
                     "draws":draws,
                     "losses":losses,
                     "goals_for":goles_favor,
                     "goals_against":goles_contra,
                     "top_scorer":gols}
        
        lt.addLast(lista_final,equip_final)

    #Encontrar ciudad mas repetida
    ciudad_max=""
    num_rep=0
    llaves_ciud=mp.keySet(ciudades)
    for ciudad in lt.iterator(llaves_ciud):
        ciud=me.getValue(mp.get(ciudades,ciudad))
        if lt.size(ciud)>=num_rep:
            num_rep=lt.size(ciud)
            ciudad_max=ciudad
    
    #Ordenar lista y sacar numero de equipos
    merg.sort(lista_final,cmpx_estadisticas_equipo)
    if lt.size(lista_final)>n:
        lista_final=lt.subList(lista_final,1,n)

    return (mp.size(data_structs["anios_torneo"]),mp.size(torneos), lt.size(llaves), partidos_totales, lt.size(paises),mp.size(ciudades),ciudad_max,lista_final)

def encontrar_goleador(goleadores):
        goles_max=0
        goleador=0
        llaves=mp.keySet(goleadores)
        for jugador in lt.iterator(llaves):
            jug=me.getValue(mp.get(goleadores,jugador))
            if lt.size(jug) > goles_max:
                goles_max=lt.size(jug)
                goleador=jug
        
        #Sacar datos de jugador para imprimir
        
        prom_min=0.0
        scorer="Unavailable"
        matches=0
        goals=0
        if mp.size(goleadores)>0:
            total_partidos=lt.newList("ARRAY_LIST")
            for gol in lt.iterator(goleador):
                prom_min+=float(gol["minute"])
                if lt.isPresent(total_partidos,gol["date"]) ==0:
                    lt.addLast(total_partidos,gol["date"])
            p=prom_min/goles_max
            prom_min=round(p,2)
            scorer=goleador["elements"][0]["scorer"]
            matches=lt.size(total_partidos)
            goals=lt.size(jug)
        return (prom_min,scorer,matches,goals)

def req_7(data_structs,torneo,n):
    """
    Función que soluciona el requerimiento 7
    """
    torneos_map = data_structs["model"]["tournament"]
    goals_map = data_structs["model"]["home_away_team_goalscorers"]
    Total_torneos = mp.size(torneos_map) 
    total_anotaciones = 0
    total_penales = 0 
    total_owngoal = 0 
    partidos = me.getValue(mp.get(torneos_map,torneo)) 
    total_partidos = lt.size(partidos)
    jugadores = mp.newMap(total_partidos,
                       maptype="PROBING",
                       loadfactor=0.7)
    for partido in lt.iterator(partidos):
        anotaciones = int(partido["home_score"]) + int(partido["away_score"])
        total_anotaciones += anotaciones
        x=mp.contains(goals_map,(partido["date"]+ "-"+partido["home_team"]+"-"+partido["away_team"]))
        if x:
            gol=me.getValue(mp.get(goals_map,partido["date"]+ "-"+partido["home_team"]+"-"+partido["away_team"]))
            for g in lt.iterator(gol):
                if g["penalty"] == "True":
                    total_penales +=1 
                if g["own_goal"] == "True":
                    total_owngoal +=1
                g["tournament"] = partido["tournament"]    
                g["home_score"] = partido["home_score"]
                g["away_score"] = partido["away_score"]
                
                add_data_map_simplificado(jugadores, g, "scorer")
    total_jugadores = mp.size(jugadores)
    nom_jug=mp.keySet(jugadores)
    lista_jugadores = lt.newList("ARRAY_LIST")

    for jugador in lt.iterator(nom_jug):
        pareja_j = mp.get(jugadores,jugador)
        goles_jug = me.getValue(pareja_j)
        quk.sort(goles_jug,cmp_partidos_results)
        total_goles =float(lt.size(goles_jug))
        avg = 0
        penalties = 0
        autogol = 0 
        wins = 0
        losses = 0
        draws = 0
        for gol in lt.iterator(goles_jug):
            scorer = gol["scorer"]
            avg += float(gol["minute"])
            if gol["penalty"] == "True":
                penalties += 1
            if gol["own_goal"] == "True":
                autogol += 1

            if gol["team"] == gol["home_team"]:
                if gol["home_score"] > gol["away_score"]:
                    wins += 1
                elif gol["home_score"] <  gol["away_score"]:
                    losses += 1
                else: 
                    draws += 1 
                
            elif gol["team"] == gol["away_team"]:
                if gol["away_score"] > gol["home_score"]:
                    wins += 1
                elif gol["away_score"] <  gol["home_score"]:
                    losses += 1
                else:
                    draws += 1 
        total_goals = wins + draws + losses
        total_points = total_goals + penalties - autogol
        if total_points == n:
            list_gol=lt.newList("ARRAY_LIST")
            ultimo={"date":goles_jug["elements"][0]["date"],"tournament":goles_jug["elements"][0]["tournament"],"home_team":goles_jug["elements"][0]["home_team"], 
                             "away_team":goles_jug["elements"][0]["away_team"], "home_score":goles_jug["elements"][0]["home_score"],"away_home":goles_jug["elements"][0]["away_score"],
                             "minute":goles_jug["elements"][0]["minute"],"penalty":goles_jug["elements"][0]["penalty"],"own_goal":goles_jug["elements"][0]["own_goal"]}
            lt.addLast(list_gol,ultimo)
            last_goal=creartabla(list_gol,list_gol["elements"][0])
                #Diccionario con valores :nombre,suma,goles, penalty,own goal, average, torneos del jugador, v,e,d, lista de dict de goles]
            dic_goleador = {"scorer":scorer,
               "total_points":total_points, 
               "total_goals":total_goals,
               "penalty_goals":penalties,
                "own_goals":autogol,
                "avg_time [min]":avg/total_goles,
                "scored_in_wins":wins,
                "scored_in_losses":losses,
                "scored_in_draws":draws,
                "last_goal":last_goal}
        
            lt.addLast(lista_jugadores,dic_goleador)
    clas_jug = lt.size(lista_jugadores)
    merg.sort(lista_jugadores,cmpx_estadisticas_jugador)

    return total_partidos,lista_jugadores,Total_torneos,total_jugadores,clas_jug,total_anotaciones,total_penales,total_owngoal

def req_8(data_structs,nom_equipo,fecha_inicial,fecha_final):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    eq=mp.contains(data_structs["team"], nom_equipo)
    if eq:
        ind=mp.get(data_structs["team"],nom_equipo)
        partidos_equipo=me.getValue(ind)
    else:
        return 0,0,0,0,0,0,0
    
    #Mapa para guardar partidos por año
    cant_p=lt.size(partidos_equipo)
    partido_anio=mp.newMap(cant_p,
                     maptype="PROBING",
                     loadfactor=0.7)

    #Asignar partidos en mapa, filtracion por años y torneo, contadores
    partidos_local=0
    partidos_visitante=0
    partidos_mas_antiguo="2025-01-01"
    partidos_mas_reciente="1800-01-01"
    for partido in lt.iterator(partidos_equipo):
        if partido["date"]>=fecha_inicial and partido["date"]<=fecha_final and partido["tournament"] != "Friendly":
            llave=partido["date"][0:4]
            add_data_map_simplificado_llave(partido_anio,partido,llave)
            if partido["home_team"]==nom_equipo:
                partidos_local+=1
            elif partido["away_team"]==nom_equipo:
                partidos_visitante+=1
            
            if partido["date"]<partidos_mas_antiguo:
                partidos_mas_antiguo=partido["date"]
            if partido["date"]>partidos_mas_reciente:
                partidos_mas_reciente=partido["date"]
                part_reciente=partido

    if mp.size(partido_anio)==0:
        return(0,0,0,0,0,0,0)
    
    lista_final=lt.newList("ARRAY_LIST")
    #Diccionario imprimir para partido mas reciente
    lis_part_reciente=lt.newList("ARRAY_LIST")
    dic_partid_reciente={
                         "date":part_reciente["date"],
                         "home_team":part_reciente["home_team"],
                         "away_team":part_reciente["away_team"],
                         "home_score":part_reciente["home_score"],
                         "away_score":part_reciente["away_score"],
                         "country":part_reciente["country"],
                         "city":part_reciente["city"],
                         "tournament":part_reciente["tournament"]
                         }
    lt.addLast(lis_part_reciente,dic_partid_reciente)

    #Extraer estadisticas
    llaves= mp.keySet(partido_anio)
    for anio in lt.iterator(llaves):
        ani=me.getValue(mp.get(partido_anio,anio))
        partidos_total=lt.size(ani)
        goles_favor=0
        goles_contra=0
        puntos=0
        wins=0
        draws=0
        losses=0
        penal=0
        autogol=0
        goleador=lt.newList("ARRAY_LIST")
        for partido in lt.iterator(ani):
            if partido["home_team"]==nom_equipo:
                goles_favor+=int(partido["home_score"])
                goles_contra+=int(partido["away_score"])
                if partido["home_score"]>partido["away_score"]:
                    wins+=1
                    puntos+=3
                elif partido["home_score"]<partido["away_score"]:
                    losses+=1
                else:
                    draws+=1
                    puntos+=1
            else: 
                goles_favor+=int(partido["away_score"])
                goles_contra+=int(partido["home_score"])
                if partido["home_score"]<partido["away_score"]:
                    wins+=1
                    puntos+=3
                elif partido["home_score"]>partido["away_score"]:
                    losses+=1
                else:
                    draws+=1
                    puntos+=1
            
            gol=mp.contains(data_structs["home_away_team_goalscorers"],(partido["date"]+ "-" + partido["home_team"] + "-" + partido["away_team"]))
            if gol: 
                gol=me.getValue(mp.get(data_structs["home_away_team_goalscorers"],(partido["date"]+ "-" + partido["home_team"] + "-" + partido["away_team"])))
                for g in lt.iterator(gol):
                    if g["team"]==nom_equipo:
                        if g["penalty"] =="True":
                            penal+=1
                        if g["own_goal"] == "True":
                            autogol+=1
                        lt.addLast(goleador,g)

        goleadores=mp.newMap(partidos_total,
                     maptype="PROBING",
                     loadfactor=0.7)
        for gol in lt.iterator(goleador):
            add_data_map_simplificado(goleadores,gol,"scorer")
        
        prom_min,scorer,matches,goals=encontrar_goleador(goleadores)

        datos_jugador=lt.newList("ARRAY_LIST")
        dt={"scorer":scorer,
            "goals": goals,
            "matches":matches,
            "avg_time [min]":prom_min}
        lt.addLast(datos_jugador,dt)
        gols=creartabla(datos_jugador,datos_jugador["elements"][0])


        #Hacer dic para imprimir
        equip_final={"year":anio,
                     "matches":partidos_total,
                     "total_points":puntos,
                     "goal_difference":(goles_favor-goles_contra),
                     "penalties":penal,
                     "own_goals":autogol,
                     "wins":wins,
                     "draws":draws,
                     "losses":losses,
                     "goals_for":goles_favor,
                     "goals_against":goles_contra,
                     "top_scorer":gols}
        
        lt.addLast(lista_final,equip_final)
    
    #Ordenar lista
    quk.sort(lista_final,cmp_rq8) 


    return mp.size(partido_anio),(partidos_local+partidos_visitante),partidos_local,partidos_visitante,partidos_mas_antiguo,lis_part_reciente,lista_final


# Funciones de ordenamiento

def cmpCargaDatos(partido1,partido2):
    if partido1["date"]==partido2["date"]:
        if partido1["home_team"]== partido2["home_team"]:
           if partido1["away_team"]==partido2["away_team"]:
                return 0
           elif partido1["away_team"]<partido2["away_team"]:
                return -1
           else:
               return 1
        elif partido1["home_team"] < partido2["home_team"]:
            return -1
        else:
            return 1
    elif partido1["date"] < partido2["date"]:
        return -1
    else:
        return 1
    
def cmpreq2(resultado_1, resultado_2):
    if resultado_1["date"] < resultado_2["date"]:
        return True
    elif resultado_1["date"] == resultado_2["date"]:
        if resultado_1["minute"] < resultado_2["minute"]:
            return True
        elif resultado_1["minute"] == resultado_2["minute"]:
            if resultado_1["scorer"] < resultado_2["scorer"]:
                return True
            else:
                return False
        else:
            return False

    return False

def cmpreq3(resultado_1, resultado_2):
    if resultado_1["date"]>resultado_2["date"]:
        return True
    else:
        return False

def cmpreq4(resultado_1, resultado_2):
    if resultado_1["date"] > resultado_2["date"]:
        return True
    elif resultado_1["date"] == resultado_2["date"]:
        if resultado_1["country"] < resultado_2["country"]:
            return True
        elif resultado_1["country"] == resultado_2["country"]:
            if resultado_1["city"] > resultado_2["city"]:
                return True
            else:
                return False
        else:
            return False
    return False
def cmp_partidos_results(resultado_1, resultado_2):
    if resultado_1["date"] > resultado_2["date"]:
        return True
    elif resultado_1["date"] == resultado_2["date"]:
        if resultado_1["home_score"] > resultado_2["home_score"]:
            return True
        elif resultado_1["home_score"] == resultado_2["home_score"]:
            if resultado_1["away_score"] > resultado_2["away_score"]:
                return True
            else:
                return False
        else:
            return False
    return False

def cmp_goals_scorers(resultado_1, resultado_2):
    if resultado_1["date"] > resultado_2["date"]:
        return True
    elif resultado_1["date"] == resultado_2["date"]:
        if resultado_1["minute"] > resultado_2["minute"]:
            return True
        elif resultado_1["minute"] == resultado_2["minute"]:
            if resultado_1["scorer"] < resultado_2["scorer"]:
                return True
            else:
                return False
        else:
            return False

    return False

def cmp_shootouts(resultado_1, resultado_2):
    if resultado_1["date"] > resultado_2["date"]:
        return True
    elif resultado_1["date"] == resultado_2["date"]:
        if resultado_1["home_team"] < resultado_2["home_team"]:
            return True
        elif resultado_1["home_team"] == resultado_2["home_team"]:
            if resultado_1["away_team"] < resultado_2["away_team"]:
                return True
            else:
                return False
        else:
            return False
    return False

def cmpx_estadisticas_equipo(equipo1,equipo2):
    if equipo1["total_points"] > equipo2["total_points"]:
        return True
    elif equipo1["total_points"] == equipo2["total_points"]:
        if equipo1["goal_difference"] > equipo2["goal_difference"]:
            return True
        elif equipo1["goal_difference"] == equipo2["goal_difference"]:
            if equipo1["penalty_points"] > equipo2["penalty_points"]:
                return True
            elif equipo1["penalty_points"] == equipo2["penalty_points"]:
                if equipo1["matches"] < equipo2["matches"]:
                    return True
                elif equipo1["matches"] == equipo2["matches"]:
                    if equipo1["own_goals_points"] < equipo2["own_goals_points"]:
                        return True
    return False

def cmpx_estadisticas_jugador(jugador1, jugador2):
    if jugador1["total_points"] > jugador2["total_points"]:
        return True
    elif jugador1["total_points"] == jugador2["total_points"]:
        if jugador1["total_goals"] > jugador2["total_goals"]:
            return True
        elif jugador1["total_goals"] == jugador2["total_goals"]:
            if jugador1["penalty_goals"] > jugador2["penalty_goals"]:
                return True
            elif jugador1["penalty_goals"] == jugador2["penalty_goals"]:
                if jugador1["own_goals"] < jugador2["own_goals"]:
                    return True
                elif jugador1["own_goals"] == jugador2["own_goals"]:
                    if jugador1["avg_time [min]"] < jugador2["avg_time [min]"]:
                        return True
    return False

def cmp_rq8(anio1,anio2):
    if anio1["year"]>anio2["year"]:
        return True
    else:
        return False

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    sa.sort(data_structs["results"],cmp_partidos_results)
    sa.sort(data_structs["goalscorers"],cmp_goals_scorers)
    sa.sort(data_structs["shootouts"],cmp_shootouts)
    resp= "\nLos datos fueron ordenados"
    return resp

