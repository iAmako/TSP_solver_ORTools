from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

import argparse
import os

def read_file(file):
    #lire déjà le début pour voir dans quel type de fichier on est et revenir en arrière après ?
    try:
        f = open(file, 'r')
    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        
    if(os.path.splitext(file)[1]=='.tsp'):
        #lecture des gros fichiers 
        data = {}
    else:
        
        n_sommets = int(f.readline().split(' ')[1])
        oriente = ((f.readline().split(' ')[1])==1)
        value = ((f.readline().split(' ')[1])==1)
        
        #DEBUT DES ARETES 
        f.readline()
        
        data = {}
        # float inf peut-être à changer, par une grosse valeur d'entier par exemple 
        data["distance_matrix"] = [[-1 for _ in range(n_sommets)] for _ in range(n_sommets)]
        
        for i in range(n_sommets):
            data["distance_matrix"][i][i] = 0
        
        tmp = f.readline().rstrip().split(' ')
        
        while(tmp != ['FIN_DEF_ARETES']):
            #print(tmp)
            data["distance_matrix"][int(tmp[0])][int(tmp[1])] = int(tmp[2])
            data["distance_matrix"][int(tmp[1])][int(tmp[0])] = int(tmp[2])
            
            tmp = f.readline().rstrip().split(' ')
            
        data["num_vehicles"] = 1
        data["depot"] = 0 
        
        for d in data["distance_matrix"]:
            print(d)
            
    return data,oriente,value

def get_parser(h):
    
	parser = argparse.ArgumentParser(add_help=h)
	parser.add_argument("-f", "--file",type=str, help="Path to the file (ex : \"./problems/prob_sac_1.txt\")", required=True)

	return parser.parse_args().file
    

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Route distance: {route_distance}miles\n"
    
def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes
    
def main(file):
    
    # Lecture du fichier 
    data,oriente,value = read_file(file)
    
    # Création du routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])
    
    # création du modèle
    routing = pywrapcp.RoutingModel(manager)
    
    #Fonction distance
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    
    # Coût de chaque arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Résolution 
    solution = routing.SolveWithParameters(search_parameters)
    
    # Affichage de la solution
    if solution:
        print_solution(manager, routing, solution)
        
if __name__ == "__main__":
    # Récupérer les arguments 
    filename = get_parser(h=True)
    main(filename)
