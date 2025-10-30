import random
import time
import os
import sys
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import State, Container
from input_manager import load_problem

class GeneticAlgorithm:
    def __init__(self, problem_file, population_size, mutation_rate, crossover_rate, generations):
        self.problem_file = problem_file
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations

        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        project_root = os.path.dirname(parent_dir)
        self.problem_path = os.path.join(project_root, 'data', f'{self.problem_file}.json')
        self.all_items, self.capacity = load_problem(self.problem_path)
        self.population = []
        self.history = {
            'best_objective': [],
            'max_objective': [],
            'avg_objective': []
        }

    def initialize_population(self):
        self.population = []
        for _ in range(self.population_size):
            state = State()
            state.generate_random_state(self.problem_file)
            self.population.append(state)

    def _selection(self, k=3):
        tournament_contenders = random.sample(self.population_with_penalty, k)
        tournament_contenders.sort(key=lambda x: x[1])
        return tournament_contenders[0][0]

    def crossover(self, parent1, parent2):
        child = State()
        p1_containers = parent1.list_container
        p2_containers = parent2.list_container
        cut1 = random.randint(0, len(p1_containers))
        cut2 = random.randint(0, len(p2_containers))
        
        child_containers = []
        for c in p1_containers[:cut1]:
            new_c = Container(c.capacity)
            new_c.item_list = c.item_list.copy()
            child_containers.append(new_c)
            
        for c in p2_containers[cut2:]:
            new_c = Container(c.capacity)
            new_c.item_list = c.item_list.copy()
            child_containers.append(new_c)

        child.list_container = child_containers
        self.repair(child)
        return child

    def repair(self, state):
        items_in_state = set()

        for container in state.list_container:
            for item in container.item_list[:]:
                if item['id'] in items_in_state:
                    container.item_list.remove(item)
                else:
                    items_in_state.add(item['id'])

        all_item_ids = set(item['id'] for item in self.all_items)
        missing_item_ids = all_item_ids - items_in_state
        
        if missing_item_ids:
            for item_id in missing_item_ids:
                item_to_add = next(item for item in self.all_items if item['id'] == item_id)
                placed = False
                for container in state.list_container:
                    if container.total_size() + item_to_add['ukuran'] <= container.capacity:
                        container.item_list.append(item_to_add)
                        placed = True
                        break
                if not placed:
                    new_container = Container(self.capacity)
                    new_container.item_list.append(item_to_add)
                    state.list_container.append(new_container)
        
        state.list_container = [c for c in state.list_container if c.item_list]

    def mutate(self, state):
        if random.random() > self.mutation_rate:
            return
        
        move_type = random.randint(1, 2)
        
        if not state.list_container:
            return

        if move_type == 1 or len(state.list_container) < 2:
            container_from = random.choice([c for c in state.list_container if c.item_list] or state.list_container)
            if not container_from.item_list:
                return
            
            item_to_move = random.choice(container_from.item_list)
            container_from.item_list.remove(item_to_move)

            if random.random() < 0.1:
                target_container = Container(self.capacity)
                state.list_container.append(target_container)
            else:
                target_container = random.choice(state.list_container)
            target_container.item_list.append(item_to_move)

            if not container_from.item_list:
                state.list_container.remove(container_from)
        else:
            non_empty_containers = [c for c in state.list_container if c.item_list]
            if len(non_empty_containers) < 2:
                return
            c1, c2 = random.sample(non_empty_containers, 2)
            item1 = random.choice(c1.item_list)
            item2 = random.choice(c2.item_list)
            c1.item_list.remove(item1)
            c2.item_list.remove(item2)
            c1.item_list.append(item2)
            c2.item_list.append(item1)

    def run(self):
        start_time = time.time()
        self.initialize_population()
        initial_best_state = min(self.population, key=lambda s: s.count_penalty()).copy()
        best_state_overall = initial_best_state
        best_penalty_overall = best_state_overall.count_penalty()
        max_penalty_overall = best_penalty_overall

        for gen in range(self.generations):
            self.population_with_penalty = []
            penalties = []
            for state in self.population:
                penalty = state.count_penalty()
                self.population_with_penalty.append((state, penalty))
                penalties.append(penalty)
                if penalty < best_penalty_overall:
                    best_penalty_overall = penalty
                    best_state_overall = state.copy()

            best_objective = min(penalties)
            max_objective = max(penalties)
            avg_objective = sum(penalties) / len(penalties)
            
            if max_objective > max_penalty_overall:
                max_penalty_overall = max_objective
            
            self.history['best_objective'].append(best_objective)
            self.history['max_objective'].append(max_objective)
            self.history['avg_objective'].append(avg_objective)
            
            new_population = []
            new_population.append(best_state_overall.copy())

            while len(new_population) < self.population_size:
                parent1 = self._selection()
                parent2 = self._selection()
                if random.random() < self.crossover_rate:
                    child = self.crossover(parent1, parent2)
                else:
                    child = parent1.copy()
                self.mutate(child)
                new_population.append(child)
            self.population = new_population
        self.history['max_objective_overall'] = max_penalty_overall

        end_time = time.time()
        duration = end_time - start_time
        return initial_best_state, best_state_overall, self.history, duration

    @staticmethod
    def print_solution(state, title):
        print(f"\n--- {title} ---")
        print(f"Total Kontainer Digunakan: {len(state.list_container)}")
        print(f"Nilai Objektif (Penalti): {state.count_penalty()}")
        print("-" * 20)
        for i, container in enumerate(state.list_container):
            total_size = container.total_size()
            capacity = container.capacity
            print(f"Kontainer {i + 1} (Total: {total_size}/{capacity}):")
            if total_size > capacity:
                print(f"  !!! OVER CAPACITY by {total_size - capacity} !!!")
            for item in container.item_list:
                print(f"  {item['id']} ({item['ukuran']})")

    @staticmethod
    def plot_multiple_experiments(experiments_data):
        if not experiments_data:
            print("Tidak ada data eksperimen untuk di-plot.")
            return
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        project_root = os.path.dirname(parent_dir)
        plot_dir = os.path.join(project_root, 'result', 'plot')
        
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)

        plt.figure(figsize=(10, 6))
        
        for label, history in experiments_data:
            plt.plot(history['best_objective'], label=f"{label} (Best)", linewidth=2)
            plt.plot(history['avg_objective'], label=f"{label} (Avg)", linewidth=2, linestyle='--', alpha=0.7)
        
        plt.title('Perbandingan Nilai Objektif (Best & Average) vs. Generasi', fontsize=14, fontweight='bold')
        plt.xlabel('Generasi')
        plt.ylabel('Nilai Objektif (Penalti)')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"ga_plot_{timestamp}.png"
        filepath = os.path.join(plot_dir, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"\nPlot perbandingan disimpan ke: {filepath}")
        
        plt.show()
        plt.close()
        
        print("\n" + "="*80)
        print("RINGKASAN PERBANDINGAN EKSPERIMEN")
        print("="*80)
        for label, history in experiments_data:
            best_pen = history['best_objective'][-1]
            max_pen = history.get('max_objective_overall', max(history['max_objective']))
            avg_pen = history['avg_objective'][-1]
            initial_pen = history['best_objective'][0]
            
            print(f"\n{label}:")
            print(f"  Nilai Objektif Awal: {initial_pen:.2f}")
            print(f"  Nilai Objektif Akhir: {best_pen:.2f}")
            print(f"  Nilai Objektif Maximum: {max_pen:.2f}")
            print(f"  Rata-Rata Nilai Objektif: {avg_pen:.2f}")

    @staticmethod
    def save_ga(experiments_results, file_path, mutation_rate):
        print(f"\n{'='*80}")
        print("SIMPAN HASIL EKSPERIMEN")
        print(f"{'='*80}")
        filename = input("Masukkan nama file untuk menyimpan hasil (tanpa .txt): ").strip()
        
        if not filename:
            print("Nama file tidak valid. Hasil tidak disimpan.")
            return
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        project_root = os.path.dirname(parent_dir)
        result_dir = os.path.join(project_root, 'result')
        filepath = os.path.join(result_dir, f"{filename}.txt")

        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("="*80 + "\n")
                f.write("HASIL MULTIPLE EXPERIMENTS - GENETIC ALGORITHM\n")
                f.write("="*80 + "\n")
                f.write(f"Problem File: {file_path}.json\n")
                f.write(f"Probabilitas Mutasi: {mutation_rate}\n")
                f.write(f"Jumlah Eksperimen: {len(experiments_results)}\n")
                f.write("="*80 + "\n\n")
                
                for i, result in enumerate(experiments_results):
                    f.write(f"\n{'='*80}\n")
                    f.write(f"EKSPERIMEN {i + 1}\n")
                    f.write(f"{'='*80}\n\n")
                    
                    # parameter
                    f.write(f"Jumlah Populasi: {result['population_size']}\n")
                    f.write(f"Jumlah Generation: {result['generations']}\n")
                    f.write(f"Probabilitas Mutasi: {mutation_rate}\n")
                    f.write(f"Durasi Proses Pencarian: {result['duration']:.4f} detik\n\n")
                    
                    # objective function
                    initial_obj = result['initial_state'].count_penalty()
                    final_obj = result['final_state'].count_penalty()
                    history = result['history']
                    max_obj = history.get('max_objective_overall', max(history['max_objective']))
                    avg_obj = history['avg_objective'][-1]
                    f.write(f"Nilai Objective Function Awal: {initial_obj}\n")
                    f.write(f"Nilai Objective Function Akhir: {final_obj}\n")
                    f.write(f"Nilai Objective Function Maximum: {max_obj:.2f}\n")
                    f.write(f"Rata-Rata Nilai Objective Function: {avg_obj:.2f}\n\n")
                    
                    # state awal
                    f.write(f"\n--- STATE AWAL ---\n")
                    f.write(f"Total Kontainer: {len(result['initial_state'].list_container)}\n")
                    for j, container in enumerate(result['initial_state'].list_container):
                        total_size = container.total_size()
                        capacity = container.capacity
                        f.write(f"\nKontainer {j + 1} (Total: {total_size}/{capacity}):\n")
                        if total_size > capacity:
                            f.write(f"  !!! OVER CAPACITY by {total_size - capacity} !!!\n")
                        for item in container.item_list:
                            f.write(f"  {item['id']} ({item['ukuran']})\n")
                    
                    # state akhir
                    f.write(f"\n--- STATE AKHIR ---\n")
                    f.write(f"Total Kontainer: {len(result['final_state'].list_container)}\n")
                    for j, container in enumerate(result['final_state'].list_container):
                        total_size = container.total_size()
                        capacity = container.capacity
                        f.write(f"\nKontainer {j + 1} (Total: {total_size}/{capacity}):\n")
                        if total_size > capacity:
                            f.write(f"  !!! OVER CAPACITY by {total_size - capacity} !!!\n")
                        for item in container.item_list:
                            f.write(f"  {item['id']} ({item['ukuran']})\n")
                    f.write("\n")
        
            print(f"\nHasil berhasil disimpan ke: {filepath}")
            
        except Exception as e:
            print(f"Error saat menyimpan file: {e}")


    @staticmethod
    def run_genetic_algorithm_experiments(file_path):
        print("=== MULTIPLE EXPERIMENTS - GENETIC ALGORITHM ===")
        print("Anda akan menjalankan 3 eksperimen dengan parameter berbeda.")
        print()

        MUTATION_RATE = 0.1
        CROSSOVER_RATE = 0.8
        experiments_results = []

        for i in range(3):
            print(f"\n{'='*80}")
            print(f"EKSPERIMEN {i + 1} dari 3")
            print(f"{'='*80}")
            
            while True:
                try:
                    population_size = int(input(f"Eksperimen {i + 1} - Masukkan population size: "))
                    if population_size <= 0:
                        print("Population size harus lebih dari 0!")
                        continue
                    break
                except ValueError:
                    print("Input tidak valid! Masukkan angka.")
            
            while True:
                try:
                    generations = int(input(f"Eksperimen {i + 1} - Masukkan jumlah generations: "))
                    if generations <= 0:
                        print("Generations harus lebih dari 0!")
                        continue
                    break
                except ValueError:
                    print("Input tidak valid! Masukkan angka.")
            
            ga = GeneticAlgorithm(
                problem_file=file_path,
                population_size=population_size,
                mutation_rate=MUTATION_RATE,
                crossover_rate=CROSSOVER_RATE,
                generations=generations
            )
            
            initial_state, final_state, history, duration = ga.run()
            
            experiment_label = f"Exp{i+1}: Pop={population_size}, Gen={generations}"
            experiments_results.append({
                'label': experiment_label,
                'population_size': population_size,
                'generations': generations,
                'initial_state': initial_state,
                'final_state': final_state,
                'history': history,
                'duration': duration
            })
            
            print(f"\n--- HASIL EKSPERIMEN {i + 1} ---")
            print(f"Durasi Proses Pencarian: {duration:.4f} detik")
            print(f"Nilai Objektif Awal: {initial_state.count_penalty()}")
            print(f"Nilai Objektif Akhir: {final_state.count_penalty()}")
            print(f"Total Kontainer Digunakan: {len(final_state.list_container)}")
            
        print(f"\n{'='*80}")
        print("RINGKASAN SEMUA EKSPERIMEN")
        print(f"{'='*80}")
        print(f"Problem File: {file_path}.json")
        print()
        
        for i, result in enumerate(experiments_results):
            print(f"\nEksperimen {i + 1}:")
            print(f"  Parameter: Pop={result['population_size']}, Gen={result['generations']}")
            print(f"  Durasi: {result['duration']:.4f} detik")
            print(f"  Nilai Objektif Awal: {result['initial_state'].count_penalty()}")
            print(f"  Nilai Objektif Akhir: {result['final_state'].count_penalty()}")
            print(f"  Total Kontainer: {len(result['final_state'].list_container)}")
        
        best_experiment_idx = min(range(len(experiments_results)), 
                                 key=lambda i: experiments_results[i]['final_state'].count_penalty())
        
        print(f"\n{'='*80}")
        print(f"EKSPERIMEN TERBAIK: Eksperimen {best_experiment_idx + 1}")
        print(f"{'='*80}")
        best_result = experiments_results[best_experiment_idx]
        GeneticAlgorithm.print_solution(best_result['final_state'], f"Solusi Terbaik (Eksperimen {best_experiment_idx + 1})")
        print(f"\n{'='*80}")
        print("VISUALISASI PERBANDINGAN EKSPERIMEN")
        print(f"{'='*80}")
        
        experiments_data = [(result['label'], result['history']) for result in experiments_results]
        GeneticAlgorithm.plot_multiple_experiments(experiments_data)
        GeneticAlgorithm.save_ga(experiments_results, file_path, MUTATION_RATE)