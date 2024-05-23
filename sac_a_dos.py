from ortools.linear_solver import pywraplp
import argparse,os
import time
from datetime import datetime

def read_file(file, solver):
    #lire déjà le début pour voir dans quel type de fichier on est et revenir en arrière après ?
    try:
        f = open(file, 'r') 
    except FileNotFoundError:
        print(f"Error: The file '{file}' was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

    tmp_var = f.readline().split(' ') 
    if(tmp_var[0] == 'n:'):
        nb_var = int(tmp_var[1])
        contrainte = int(f.readline().split(' ')[1])
        objective.SetMaximization()    
        #ligne vide
        f.readline()
        
        # Définition de la fonction objectif 
        objective = solver.Objective()

 
    else: 
        nb_var = int(tmp_var[1])
        nb_contraintes = int(f.readline().split(' ')[1])
        maximisation = (f.readline() == "max\n")

        #variables de la fonction objectif 
        variables = f.readline().rstrip().split(' ')
        #ligne vide
        f.readline()
        
        #contraintes 
        contraintes = f.readline().rstrip().split(' ')
        x = []
        # Initialisation des variables 
        for i in range(nb_var): 
            #print(variables[i*3+2])
            # ou numvar ? 
            x.append(solver.IntVar(0, solver.infinity(), (variables[i*3+2])))
        
    
        # Ajout des contraintes 
        ct = solver.Constraint(0, int(contraintes[3*nb_var+1]),"ct")
        for i in range(nb_var):
            #print(contraintes[i*3+2])
            #print(int(contraintes[i*3+1]))
            
            if(contraintes[i*3] == "+"):
                ct.SetCoefficient(x[i], int(contraintes[i*3+1]))
            else:
                ct.SetCoefficient(x[i], -int(contraintes[i*3+1]))
        # Définition de la fonction objectif 
        objective = solver.Objective()
        for i in range(nb_var):
            #print(int(variables[i*3+1]))
            if(contraintes[i*3] == "+"):
                objective.SetCoefficient(x[i], int(variables[i*3+1]))
            else:
                objective.SetCoefficient(x[i], -int(variables[i*3+1]))

        if(maximisation):
            objective.SetMaximization()    
        else:
            objective.SetMinimization()   
    f.close()
        
    return solver,objective,ct,x

def get_parser(h):
    
	parser = argparse.ArgumentParser(add_help=h)
	parser.add_argument("-f", "--file",type=str, help="Path to the file (ex : \"./problems/prob_sac_1.txt\")", required=True)

	return parser.parse_args().file

def main(file):    
    
    #Création du solveur 
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        exit
        
    #Lecture du fichier 
    solver,objective,ct,x = read_file(file,solver)

    # Résolution 
    start_time = time.perf_counter()#plus précis que time.time
    print(f"Solving with {solver.SolverVersion()}")
    solver.Solve()
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    #Affichage de la solution
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    # Create the filename with the timestamp
    output_file = f"..\\resultats\\output_{timestamp}.txt"
    
    # Ensure the directory exists
    os.makedirs("../resultats", exist_ok=True)    
    
    print("Solution:")
    print("Objective value =", objective.Value())
    print(f"Execution time: {execution_time} seconds")
    i = 1
    for x_solution in x:
        print("x" + str(i) + " = " + str(x_solution.solution_value()))
        i = i + 1
        
        
    with open(output_file, 'w') as of:
        of.write("Solution:\n")
        of.write(f"Objective value = {objective.Value()}\n")
        of.write(f"Execution time: {execution_time} seconds\n")
        i = 1
        for x_solution in x:
            of.write(f"x {str(i)} = {str(x_solution.solution_value())}\t")
            i = i + 1
            
        
        

if __name__ == "__main__": 
    #Récupérer les arguments 
    filename = get_parser(h=True)
    main(filename)
