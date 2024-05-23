import sac_a_dos
import tsp

def main():
    choice = -1
    while(choice != '0'):
        print("\nProgrammes:")
        print("1. Sac à dos (KP)")
        print("2. Voyageur de Commerce (TSP)")
        print("0. Fermer le programme")

        choice = input("\nEntrer un nombre: ")

        if choice in ['1', '2']:
            filename = input("Entrer le chemin vers le fichier à charger: ")
            if choice == '1':
                sac_a_dos.main(filename)
            elif choice == '2':
                tsp.main(filename)
        elif choice == '0':
            pass
        else:
            print("Choix invalide. Merci d'entrer 1 ou 2.")

if __name__ == "__main__":
    main()