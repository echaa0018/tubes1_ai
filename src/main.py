import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from input_manager import load_problem
from state import State
from algorithm.genetic_algorithm import GeneticAlgorithm


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
        print("2. Simulated Annealing (coming soon)")
        print("3. Hill Climbing (coming soon)")
        print("4. Exit Program")
        
        algorithm_choice = input("Masukkan pilihan: ").strip()
        
        print()
        if algorithm_choice == "1":
            GeneticAlgorithm.run_genetic_algorithm_experiments(file_path)
        elif algorithm_choice == "2":
            print("Simulated Annealing belum tersedia!")
        elif algorithm_choice == "3":
            print("Hill Climbing belum tersedia!")
        elif algorithm_choice == "4":
            print("bye")
            return
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
