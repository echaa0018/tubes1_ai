import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from input_manager import load_problem
from state import State
from algorithm.genetic_algorithm import GeneticAlgorithm
from algorithm.hill_climbing import HillClimbing


def hill_climbing_menu(file_path):
    print(f"\n{'='*80}")
    print("PILIH TIPE HILL CLIMBING:")
    print("1. Steepest Ascent Hill Climbing")
    print("2. Hill Climbing with Sideways Move")
    print("3. Stochastic Hill Climbing")
    print("4. Random Restart Hill Climbing")
    print("5. Compare All Hill Climbing Types")
    print("6. Back to Main Menu")
    
    choice = input("Masukkan pilihan: ").strip()
    
    if choice == "1":
        HillClimbing.run_hill_climbing_experiments(file_path, "normal")
    elif choice == "2":
        HillClimbing.run_hill_climbing_experiments(file_path, "sideways")
    elif choice == "3":
        HillClimbing.run_hill_climbing_experiments(file_path, "stochastic")
    elif choice == "4":
        HillClimbing.run_hill_climbing_experiments(file_path, "random_restart")
    elif choice == "5":
        HillClimbing.compare_algorithms(file_path)
    elif choice == "6":
        return
    else:
        print("Pilihan tidak valid!")


def compare_all_algorithms(file_path):
    print(f"\n{'='*80}")
    print("COMPARING ALL ALGORITHMS")
    print("This will run all algorithms and compare their performance...")
    
    print("\n1. Running Hill Climbing Algorithms...")
    hill_results = HillClimbing.compare_algorithms(file_path)
    
    print("\n2. Genetic Algorithm comparison can be run separately from the main menu.")


def main():
    print("=== PROGRAM LOCAL SEARCH ===")
    print()    
    print("Pilih file problem:")
    print("1. problem.json")
    print("2. problem1.json")
    print("3. Custom file path")
    
    file_choice = input("Masukkan pilihan (1/2/3): ").strip()
    
    if file_choice == "1":
        file_path = "problem"
    elif file_choice == "2":
        file_path = "problem1"
    elif file_choice == "3":
        file_path = input("Masukkan path file (tanpa .json): ").strip()
    else:
        print("Pilihan tidak valid!")
        return
    print()
    
    while True:
        print(f"\n{'='*80}")
        print("Pilih algoritma local search:")
        print("1. Genetic Algorithm")
        print("2. Hill Climbing")
        print("3. Exit Program")
        
        algorithm_choice = input("Masukkan pilihan: ").strip()
        
        print()
        if algorithm_choice == "1":
            GeneticAlgorithm.run_genetic_algorithm_experiments(file_path)
        elif algorithm_choice == "2":
            hill_climbing_menu(file_path)
        elif algorithm_choice == "3":
            print("bye")
            return
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
