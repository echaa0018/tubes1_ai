import random
import math
import time
import os
import matplotlib.pyplot as plt
from copy import deepcopy
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import State, Container
from input_manager import load_problem


def cool_down(current_temp: float, cooling_rate: float) -> float:
    """Menurunkan suhu berdasarkan cooling rate"""
    return current_temp * cooling_rate


def generate_neighbor(state: State) -> State:
    """Menghasilkan tetangga dari state saat ini"""
    new_state = state.copy()
    
    if not new_state.list_container:
        return new_state
    
    non_empty = [c for c in new_state.list_container if c.item_list]
    
    if not non_empty:
        return new_state
    
    move_type = random.choice(['move', 'swap']) if len(non_empty) >= 2 else 'move'
    
    if move_type == 'move':
        container_from = random.choice(non_empty)
        item_to_move = random.choice(container_from.item_list)
        
        try:
            container_from.item_list.remove(item_to_move)
        except ValueError:
            return new_state
        
        if random.random() < 0.12:
            target_container = Container(new_state.list_container[0].capacity)
            new_state.list_container.append(target_container)
        else:
            target_container = random.choice(new_state.list_container)
        
        target_container.item_list.append(item_to_move)
        new_state.list_container = [c for c in new_state.list_container if c.item_list]
    
    else:  # swap
        c1, c2 = random.sample(non_empty, 2)
        i1 = random.choice(c1.item_list)
        i2 = random.choice(c2.item_list)
        
        try:
            idx1 = c1.item_list.index(i1)
            idx2 = c2.item_list.index(i2)
            c1.item_list[idx1], c2.item_list[idx2] = c2.item_list[idx2], c1.item_list[idx1]
        except ValueError:
            pass
    
    return new_state


def simulated_annealing(file_path: str, initial_temp: float, cooling_rate: float):
    """Menjalankan algoritma Simulated Annealing"""
    result = {
        'algorithm': 'Simulated Annealing',
        'initial_score': None,
        'final_score': None,
        'duration': 0.0,
        'iterations': 0,
        'stuck_iterations': 0,
        'objective_history': [],
        'temperature_history': [],
        'acceptance_prob_history': []
    }
    
    # Inisialisasi state awal
    initial_state = State()
    initial_state.generate_random_state(file_path)
    
    current_state = initial_state
    current_score = current_state.count_penalty()
    result['initial_score'] = current_score
    
    best_state = current_state.copy()
    best_score = current_score
    
    temperature = initial_temp
    stuck_count = 0
    iteration = 0
    
    print(f"Memulai SA. Skor Awal: {current_score:.2f}, Suhu Awal: {temperature:.2f}")
    
    start_time = time.time()
    
    # Loop utama SA
    while temperature > 1e-3:
        iteration += 1
        
        # Generate neighbor
        neighbor_state = generate_neighbor(current_state)
        neighbor_score = neighbor_state.count_penalty()
        
        delta_score = neighbor_score - current_score
        acceptance_prob = 0.0
        
        # Evaluasi penerimaan neighbor
        if delta_score < 0:
            # Neighbor lebih baik, terima
            current_state = neighbor_state
            current_score = neighbor_score
            acceptance_prob = 1.0
            stuck_count = 0
        else:
            # Neighbor lebih buruk, terima dengan probabilitas tertentu
            acceptance_prob = math.exp(-delta_score / temperature)
            if random.random() < acceptance_prob:
                current_state = neighbor_state
                current_score = neighbor_score
                stuck_count = 0
            else:
                stuck_count += 1
        
        # Update best state
        if current_score < best_score:
            best_state = current_state.copy()
            best_score = current_score
        
        # Simpan history
        result['objective_history'].append(best_score)
        result['temperature_history'].append(temperature)
        result['acceptance_prob_history'].append(acceptance_prob)
        
        # Turunkan suhu
        temperature = cool_down(temperature, cooling_rate)
        
        # Print progress
        if iteration % 1000 == 0:
            print(f"Iter: {iteration:5d} | Suhu: {temperature:8.4f} | "
                  f"Current: {current_score:7.2f} | Best: {best_score:7.2f} | "
                  f"AccProb: {acceptance_prob:.4f}")
    
    result['stuck_iterations'] = stuck_count
    result['duration'] = time.time() - start_time
    result['final_score'] = best_score
    result['iterations'] = iteration
    
    print(f"\nPencarian Selesai. Suhu terlalu rendah.")
    print(f"Skor terbaik: {best_score:.2f} setelah {iteration} iterasi.")
    print(f"Durasi: {result['duration']:.4f} detik")
    
    return best_state, result


class SimulatedAnnealing:
    @staticmethod
    def print_solution(state: State, title: str):
        """Mencetak detail solusi"""
        print(f"\n--- {title} ---")
        print(f"Total Kontainer Digunakan: {len(state.list_container)}")
        print(f"Nilai Objektif (Penalti): {state.count_penalty()}")
        print("-" * 20)
        for i, container in enumerate(state.list_container):
            total_size = container.total_size()
            capacity = container.capacity
            print(f"Kontainer {i + 1} (Total: {total_size}/{capacity}):")
            if total_size > capacity:
                print(f"  !!! OVER CAPACITY sebanyak {total_size - capacity} !!!")
            for item in container.item_list:
                print(f"  {item['id']} ({item['ukuran']})")

                
    
    @staticmethod
    def run_simulated_annealing_experiments(file_path: str):
        """Menjalankan multiple experiments SA"""
        print("=== MULTIPLE EXPERIMENTS - SIMULATED ANNEALING ===")
        print("Anda akan menjalankan 3 eksperimen dengan parameter berbeda.\n")
        
        experiments_results = []
        
        for i in range(3):
            print(f"\n{'='*80}")
            print(f"EKSPERIMEN {i + 1} dari 3")
            print(f"{'='*80}")
            
            while True:
                try:
                    T0 = float(input(f"Eksperimen {i + 1} - Masukkan suhu awal (T0): "))
                    if T0 <= 0:
                        print("T0 harus lebih dari 0!")
                        continue
                    break
                except ValueError:
                    print("Input tidak valid! Masukkan angka.")
            
            while True:
                try:
                    cooling_rate = float(input(f"Eksperimen {i + 1} - Masukkan cooling rate (0-1): "))
                    if not (0 < cooling_rate < 1):
                        print("Cooling rate harus di antara 0 dan 1!")
                        continue
                    break
                except ValueError:
                    print("Input tidak valid! Masukkan angka.")
            
            # Jalankan SA
            final_state, result = simulated_annealing(file_path, T0, cooling_rate)
            
            experiment_label = f"Exp{i+1}: T0={T0}, α={cooling_rate}"
            experiments_results.append({
                'label': experiment_label,
                'final_state': final_state,
                'result': result
            })
            
            print(f"\n--- HASIL EKSPERIMEN {i + 1} ---")
            print(f"Skor Awal: {result['initial_score']:.2f}")
            print(f"Skor Akhir: {result['final_score']:.2f}")
            print(f"Durasi: {result['duration']:.4f} detik")
            print(f"Iterasi: {result['iterations']}")
            print(f"Jumlah Stuck: {result['stuck_iterations']}")
            SimulatedAnnealing.print_solution(final_state, f"Solusi Akhir Eksperimen {i + 1}")
        
        # Ringkasan
        print(f"\n{'='*80}")
        print("RINGKASAN SEMUA EKSPERIMEN")
        print(f"{'='*80}")
        print(f"Problem File: {file_path}.json\n")
        
        for i, exp in enumerate(experiments_results):
            print(f"\nEksperimen {i + 1}: {exp['label']}")
            print(f"  Durasi: {exp['result']['duration']:.4f} detik")
            print(f"  Skor Akhir: {exp['result']['final_score']:.2f}")
            print(f"  Iterasi: {exp['result']['iterations']}")
        
        # Tentukan eksperimen terbaik
        best_idx = min(range(len(experiments_results)),
                       key=lambda i: experiments_results[i]['result']['final_score'])
        best_exp = experiments_results[best_idx]
        
        print(f"\n{'='*80}")
        print(f"EKSPERIMEN TERBAIK: Eksperimen {best_idx + 1}")
        print(f"{'='*80}")
        SimulatedAnnealing.print_solution(best_exp['final_state'], 
                                         f"Solusi Terbaik (Eksperimen {best_idx + 1})")
        
        # Plot hasil
        print(f"\n{'='*80}")
        print("VISUALISASI PERBANDINGAN EKSPERIMEN")
        print(f"{'='*80}")
        SimulatedAnnealing.plot_experiments(experiments_results, file_path)
        SimulatedAnnealing.save_results(experiments_results, file_path)
    
    @staticmethod
    def plot_experiments(experiments_results: list, file_path: str):
        """Plot hasil multiple experiments"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        project_root = os.path.dirname(parent_dir)
        plot_dir = os.path.join(project_root, 'result', 'plot')
        
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        # Plot 1: Objective Function
        plt.figure(figsize=(10, 6))
        for exp in experiments_results:
            result = exp['result']
            plt.plot(range(len(result['objective_history'])), 
                    result['objective_history'], 
                    label=exp['label'], 
                    linewidth=2)
        
        plt.title("Perbandingan Nilai Objektif vs Iterasi - Simulated Annealing", 
                 fontsize=14, fontweight="bold")
        plt.xlabel("Iterasi")
        plt.ylabel("Nilai Objektif (Penalti)")
        plt.legend(loc="best")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename_obj = f"sa_objective_{timestamp}.png"
        filepath_obj = os.path.join(plot_dir, filename_obj)
        plt.savefig(filepath_obj, dpi=300, bbox_inches="tight")
        print(f"\nPlot Nilai Objektif disimpan ke: {filepath_obj}")
        plt.show()
        plt.close()
        
        
        # Plot 2: Acceptance Probability (Moving Average)
        plt.figure(figsize=(10, 6))
        window_size = 50
        
        for exp in experiments_results:
            result = exp['result']
            acceptance_history = result['acceptance_prob_history']
            
            # Calculate moving average
            smoothed = []
            for i in range(len(acceptance_history)):
                start_idx = max(0, i - window_size + 1)
                window = acceptance_history[start_idx:i+1]
                smoothed.append(sum(window) / len(window))
            
            plt.plot(range(len(smoothed)), smoothed, label=exp['label'], linewidth=2)
        
        plt.title("Perbandingan e^(ΔE/T) vs Iterasi - Simulated Annealing", 
                 fontsize=14, fontweight="bold")
        plt.xlabel("Iterasi")
        plt.ylabel("e^(ΔE/T) (Moving Average)")
        plt.legend(loc="best")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename_acc = f"sa_acceptance_{timestamp}.png"
        filepath_acc = os.path.join(plot_dir, filename_acc)
        plt.savefig(filepath_acc, dpi=300, bbox_inches="tight")
        print(f"Plot Acceptance Probability disimpan ke: {filepath_acc}")
        plt.show()
        plt.close()
    
    @staticmethod
    def save_results(experiments_results: list, file_path: str):
        """Menyimpan hasil eksperimen ke file"""
        print(f"\n{'='*80}")
        print("SIMPAN HASIL EKSPERIMEN SIMULATED ANNEALING")
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
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("="*80 + "\n")
                f.write("HASIL MULTIPLE EXPERIMENTS - SIMULATED ANNEALING\n")
                f.write("="*80 + "\n")
                f.write(f"Problem File: {file_path}.json\n")
                f.write(f"Jumlah Eksperimen: {len(experiments_results)}\n")
                f.write("="*80 + "\n\n")
                
                for i, exp in enumerate(experiments_results):
                    result = exp['result']
                    state = exp['final_state']
                    
                    f.write(f"\n{'='*80}\n")
                    f.write(f"EKSPERIMEN {i + 1}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(f"Label: {exp['label']}\n")
                    f.write(f"Skor Awal: {result['initial_score']:.2f}\n")
                    f.write(f"Skor Akhir: {result['final_score']:.2f}\n")
                    f.write(f"Durasi: {result['duration']:.4f} detik\n")
                    f.write(f"Iterasi: {result['iterations']}\n")
                    f.write(f"Stuck Iterations: {result['stuck_iterations']}\n\n")
                    
                    f.write(f"--- STATE AKHIR ---\n")
                    f.write(f"Total Kontainer: {len(state.list_container)}\n")
                    for j, container in enumerate(state.list_container):
                        total_size = container.total_size()
                        f.write(f"\nKontainer {j + 1} (Total: {total_size}/{container.capacity}):\n")
                        for item in container.item_list:
                            f.write(f"  {item['id']} ({item['ukuran']})\n")
            
            print(f"\nHasil berhasil disimpan ke: {filepath}")
        
        except Exception as e:
            print(f"Terjadi kesalahan saat menyimpan file: {e}")
