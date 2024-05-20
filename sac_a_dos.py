from ortools.linear_solver import pywraplp
import argparse,os

def read_file(file, solver):
    #lire déjà le début pour voir dans quel type de fichier on est et revenir en arrière après ?
    f = open(file,"r")
    nb_var = int(f.readline().split(' ')[1])
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
    return solver,objective,ct,x

def get_parser(h):
    
	parser = argparse.ArgumentParser(add_help=h)
	parser.add_argument("-f", "--file",type=str, help="Path to the file (ex : \"./problems/prob_sac_1.txt\")", required=True)

	return parser.parse_args().file
    

def main():
    
    #Récupérer les arguments 
    file = get_parser(h=True)

    #Création du solveur 
    solver = pywraplp.Solver.CreateSolver("SAT")
    if not solver:
        exit
        
        
    #Lecture du fichier 
    solver,objective,ct,x = read_file(file,solver)
    

    # Résolution 
    print(f"Solving with {solver.SolverVersion()}")
    solver.Solve()
    
    
    #Affichage de la solution
    print("Solution:")
    print("Objective value =", objective.Value())
    i = 1
    for x_solution in x:
        print("x" + str(i) + " = " + str(x_solution.solution_value()))
        i = i + 1


if __name__ == "__main__":
    main()
