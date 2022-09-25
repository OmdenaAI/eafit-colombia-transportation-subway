''' IMPORTANT. It is necessary to install PANDAS, NETWORKX, and FOLIUM from CMD with PIP '''
#      Example: [Using CMD] "C:\Users\username> pip install pandas"
import pandas as pd     # [DATAFRAME]. transforms the .csv to a pandas [DATAFRAME]
import networkx as nx   #  [DIJKSTRA]. transforms the dataframe to a GRAPH, to apply a [DIJKSTRA] pathfinder algorithm on it
import folium           #      [PLOT]. converts dijkstra's path into to something [PLOTTABLE], and returns an HTML
import os               #      [SAVE]. to [SAVE] that html
import webbrowser as wb #      [OPEN]. to [OPEN] that html in a browser
import time             #      [WAIT]. the execution [WAITS] for a bit so it's comfortable to see the important info
from math import dist   #  [DISTANCE]. quick calculation of [DISTANCE] between points



# Reads the database and saves it into a pandas dataframe for its use
# name | origin | destination | length | oneway | geometry
dataframe = pd.read_csv("streets_database.csv", sep=';') 
# Transforms the pandas dataframe into a graph. The streets are now nodes with  between coordinates
graph = nx.from_pandas_edgelist(dataframe,source='origin',target='destination',edge_attr= 'length')
# A list with all the streets origin nodes in tuple type, we will iterate on it in the custom coords functions
origins = list(map(eval,set(list(dataframe['origin']))))



# Graphicates the shortest path between two points in a web map
def PATHFINDING(selected_origin : tuple,selected_destination : tuple) -> list :

    print(f'\n--> ORIGIN:  {selected_origin}')
    print(f'--> DESTINY: {selected_destination}\n')
    time.sleep(3)

    # Dijkstra's pathfinder alghorithm. Searchs the shortest route between two nodes of our graph
    djk= nx.dijkstra_path(graph, source= str(selected_origin), target= str(selected_destination), weight= 'length')
    length = nx.dijkstra_path_length(graph,str(selected_origin),str(selected_destination),'length\n')

    print(f'--> ROUTE:\n{djk}\n')
    print(f'--> LENGTH: {int(length*100)} meters since {selected_origin} to {selected_destination}\n')

    # Folium uses the (lat, long) format, not our (long, lat) format, so...
    for i in range(len(djk)):   djk[i] = eval(djk[i])[::-1]

    # Map's initial zoom and center
    map = folium.Map([(selected_origin[1]+selected_destination[1])/2 , (selected_origin[0]+selected_destination[0])/2], zoom_start = "14")
    # Line config
    route = folium.PolyLine(djk,color = 'red' ,weight = 5,opacity = 0.8).add_to(map)

    # Saves the map and the render config in a html 
    map.save (os.path.join('Route.html'))

    # Opens the html in your default browser
    wb.open_new_tab('Route.html')
    # Now you can see the map!

    # Returns the coordinates list for future uses
    return djk



# Numeric menu to select the points for your route. Redirects you to other sub-menus
def ubication_selection_menu() -> tuple :
    print("1. LINE A (Niquia - La Estrella)")
    print("2. LINE B (San Javier - San Antonio)")
    print("3. LINE T (San Antonio - Oriente)")
    print("0. CHOOSE A CUSTOM COORDINATE")

    # Selected number option
    while True:
        option = input('>> ').lower()
        if option.isnumeric():
            option = int(option)
        # We have numeric options, but we can use char options for the lines too
        if option in list(range(0,4))+['a','b','t']:
            break    
        else:
            print('Please select a valid option')

    if option == '0': return custom_coord_menu()
    if option in [1,'a']: return coords_selection_line_A()
    if option in [2,'b']: return coords_selection_line_B()
    if option in [3,'t']: return coords_selection_line_T()



# Sub-menu
def coords_selection_line_A():
    print("\n-> LINE A:")
    print("1. Niquia             8. Hospital            15. Poblado   ")
    print("2. Bello              9. Prado               16. Aguacatala  ")
    print("3. Madera            10. Parque Berrío       17. Ayurá       ")
    print("4. Acevedo           11. San Antonio         18. Envigado    ")
    print("5. Tricentenario     12. Alpujarra           19. Itagui      ")
    print("6. Caribe            13. Exposiciones        20. Sabaneta    ")
    print("7. Universidad       14. Industriales        21. La Estrella ")

    coords_line_A = {1: (-75.5571114, 6.3115868), 2: (-75.5571114, 6.3115868), 3: (-75.5571114, 6.3115868), 4: (-75.5589453, 6.2990036), 5: (-75.5642928, 6.2908133), 6: (-75.5696692, 6.2773731), 7: (-75.565927, 6.2695386), 8: (-75.5636321, 6.2639618), 9: (-75.5661495, 6.2567282), 10: (-75.5682139, 6.2503631), 11: (-75.569809, 6.2473028), 12: (-75.5721487, 6.2432105), 13: (-75.5732653, 6.2383899), 14: (-75.575271, 6.2301564), 15: (-75.578089, 6.2125688), 16: (-75.5814861, 6.19359), 17: (-75.5828842, 6.1884255), 18: (-75.5931765, 6.1931561), 19: (-75.5948746, 6.1935344), 20: (-75.6355661, 6.1751822), 21: (-75.6454255, 6.1654827)}

    while True:
        option = input('>> ')
        if option in map(str,range(1,22)):
            option = int(option)
            break    
        else:
            print('Please select a valid option')

    return coords_line_A[option]
    


# Sub-menu
def coords_selection_line_B():
    print("\n-> LINE B:")
    print("1. San Javier        4. Estadio              7. San Antonio  ")
    print("2. Santa Lucía       5. Suramericana         -               ")
    print("3. Floresta          6. Cisneros             -               ")

    coords_line_B = {1: (-75.6136328, 6.2567588), 2: (-75.6037893, 6.2581547), 3: (-75.5978493, 6.2585128), 4: (-75.5884782, 6.2533936), 5: (-75.5827968, 6.2528555), 6: (-75.574962, 6.2506914), 7: (-75.569809, 6.2473028)}

    while True:
        option = input('>> ')
        if option in map(str,range(1,8)):
            option = int(option)
            break    
        else:
            print('Please select a valid option')

    return coords_line_B[option]



# Sub-menu
def coords_selection_line_T():
    print("\n-> LINE T (Trainway):")
    print("1. San Antonio       4. Bicentenario         7. Loyola               ")
    print("2. San José          5. Buenos Aires         8. Alejandro Echavarria ")
    print("3. Pabellón EPM      6. Miraflores           9. Oriente              ")

    coords_line_T = {1: (-75.569809, 6.2473028), 2: (-75.5656191, 6.2474828), 3: (-75.5617771, 6.2454194), 4: (-75.5589926, 6.2440992), 5: (-75.5535271, 6.2412797), 6: (-75.548963, 6.2416769), 7: (-75.5451867, 6.2392961), 8: (-75.5418453, 6.2358023), 9: (-75.5405103, 6.2334242)}

    while True:
        option = input('>> ')
        if option in map(str,range(1,8)):
            option = int(option)
            break    
        else:
            print('Please select a valid option')

    return coords_line_T[option]



# You also can use a different coordinate for your route, a custom one, you just need to write them
def custom_coord_menu():
    while True:
        print('Write your own coords!')
        original_coords = input('>> ')

        original_coords = original_coords.replace('(','').replace(')','').replace(',',' ').replace('/',' ').split()
        original_coords = tuple(sorted(map(eval,original_coords)))

        # If the distance between the custom coord and the Medellin's center is too high,
        # the custom point is so far from medellín that it is better to choose a different one.
        if dist(original_coords,(-75.574236, 6.259676)) > 2.5:
            print('The specified coordinates are not in Medellín.\n--> Try again')
            continue
        else:
            break

    final_coords = approximator(original_coords)

    print(f'{original_coords} was approximated to {final_coords}')
    time.sleep(3)

    return final_coords



# Approximates the custom coords to one of the coords we already have in the dataframe, now we can use it.
def approximator(original_coords):
    
    aprox_coords = None     #coord
    distance = None         #distance to compare    
    
    for i in origins.copy():
        distance_temp = dist(original_coords,i)

        if aprox_coords != None:
            if distance_temp < distance:
                aprox_coords = i
                distance =  distance_temp
        else:
            aprox_coords = i
            distance = distance_temp

    return aprox_coords



# MAIN (yup, looks weird but python have a 'main' format)
if __name__ == '__main__':

    #You can select if you want to execute the path research for multiple locations or not
    repeat_pathfinding = True  # while aux
    while repeat_pathfinding == True:

        print('\n-> Select an ORIGIN to your route\n')
        selected_origin = ubication_selection_menu()

        print('\n-> Select the DESTINY of your route\n')
        selected_destination = ubication_selection_menu()

        # Graphicates the route with the selected ubications,
        # the shortest path between that two coordinates.
        PATHFINDING(selected_origin, selected_destination)

        # You can search routes multiple times if you want to
        print('Do you want to search another route?\nY/N: ', end = '')
        while True:
    
            repeat_input = input()

            if repeat_input.lower() in ['n','no','0']:
                repeat_pathfinding = False
                break # The pathfinding ends.

            elif repeat_input.lower() in ['y','yes','s','si','1']:
                break # The pathfinding cicle continues.

            # [Invalid input case]
            else:
                print("Please select Yes or No")
                continue # The input cicle continues until a valid option is reached.

    print('\nGoodbye!') # And that's all c:



#               INDEX:    PATHFINDING                  22
#                         ubication_selection_menu     56
#                         coords_selection_line_A      81
#                         coords_selection_line_B     106
#                         coords_selection_line_T     127
#                         custom_coord_menu           148 
#                         approximator                174
#                         main                        196
#


'''
    _                ___       _.--.    
    \`.|\..----...-'`   `-._.-'_.-'`   
    /  ' `         ,       _.-'       
    )/' _/     \   `-_,   /           
    `-'" `"\_  ,_.-;_.-\_ ',     
        _.-'_./   E_.'   ; /       
       {_.-``-'         C_/     

'''
