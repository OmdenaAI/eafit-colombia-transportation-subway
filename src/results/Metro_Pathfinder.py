import time, pandas as pd, os, networkx as nx, folium, webbrowser as wb

dataframe = pd.read_csv("streets_database.csv", sep=';')
dataframe.head()
graph = nx.from_pandas_edgelist(dataframe,source='origin',target='destination',edge_attr= 'length')

def pathfinding(graph , selected_origin : tuple,selected_destination : tuple) -> list :
    djk= nx.dijkstra_path(graph, source= str(selected_origin), target= str(selected_destination), weight= 'length')
    length = nx.dijkstra_path_length(graph,str(selected_origin),str(selected_destination),'length\n')

    print(f'--> ROUTE:\n{djk}\n')
    print(f'--> LENGTH: {int(length)} meters since {selected_origin} to {selected_destination}\n')

    #folium uses the (lat, long) format, not our (long, lat) format, so...
    for i in range(len(djk)):   djk[i] = eval(djk[i])[::-1]

    #map's zoom and center
    map = folium.Map([(selected_origin[1]+selected_destination[1])/2 , (selected_origin[0]+selected_destination[0])/2], zoom_start = "14")
    route = folium.PolyLine(djk,color = 'red' ,weight = 10,opacity = 0.8).add_to(map)

    #saves the map and the render config in a html 
    map.save (os.path.join('Route.html'))

    #opens the html in your browser
    wb.open_new_tab('Route.html')
    #now you can see the map!

    #returns this, the coordinates list, for future uses if someone needs it.
    return djk

# ubications menu EXAMPLE. Please use a dict() for the coordinates return in next uses 
def ubication_selection_menu() -> tuple :
    print("1.EAFIT University            6.Coltejer Building          11.Robledo      ")
    print("2.Medellín's  University      7.San Antonio Station        12.Laureles     ")
    print("3.Antioquia's  University     8.Explora Park               13.San Cristóbal")
    print("4.Nacional University         9.St. Atanasio Girardot      14.Santo Domingo")
    print("5.Luis Amigó University      10.Aeropuerto O. Herrera      15.Prado        ")
    print("                     >> 0. UBICACIÓN PERSONALIZADA <<")

    #selected number invalid cases
    try: num = int(input())
    except:
        print('Please select a valid ubication.')
        time.sleep(4)
        return ubication_selection_menu()
    if num not in range(0,16): 
        print('Please select a valid ubication.')
        time.sleep(4)
        return ubication_selection_menu()

    if num == 0:
        coords = input()
        if coords[0] != "(": coords = "("+coords+")"
        return eval(coords) if coords[1]=="-" else eval(coords)[::-1]

    if num == 1: return (-75.578416, 6.2007688)
    if num == 2: return (-75.6101004, 6.2312125)
    if num == 3: return (-75.5694416, 6.2650137)
    if num == 4: return (-75.5762232, 6.266327)
    if num == 5: return (-75.5832559, 6.2601878)

    if num == 6: return (-75.5664549, 6.2500233)
    if num == 7: return (-75.5697559, 6.2472846)
    if num == 8: return (-75.5635812, 6.2703451)
    if num == 9: return (-75.5879543, 6.2568545)
    if num == 10: return (-75.5887149, 6.216229)

    if num == 11: return (-75.583682, 6.2892842)
    if num == 12: return (-75.6123571, 6.2440634)
    if num == 13: return (-75.6371302, 6.2793696)
    if num == 14: return (-75.5387441, 6.2986144)
    if num == 15: return (-75.5575788, 6.2596423)

# python main (yup, looks rare but python have a 'main' format)
if __name__ == '__main__':
    repeat_pathfinding = True
    while repeat_pathfinding == True:
        selected_origin = ubication_selection_menu()
        selected_destination = ubication_selection_menu()
        pathfinding(graph, selected_origin, selected_destination)
        print('Do you want to search another route?\nY/N: ', end = '')
        repeat_input = input()
        if repeat_input.lower() in ['n','no',0]:
            repeat_pathfinding = False
    print('\nGoodbye!')