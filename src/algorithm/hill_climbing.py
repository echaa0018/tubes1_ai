import random
import time
import os
import sys
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state import State, Container
from input_manager import load_problem

class HillClimbing:
    def __init__(self, problem_file, algorithm_type="steepest"):
        self.problem_file = problem_file
        self.algorithm_type = algorithm_type
        self.iterations = 0
        self.sideways_moves = 0
        self.restarts = 0
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        project_root = os.path.dirname(parent_dir)
        self.problem_path = os.path.join(project_root, 'data', f'{self.problem_file}.json')
        _, self.capacity = load_problem(self.problem_path)
        
        self.original_state = State()
        self.original_state.generate_random_state(problem_file)
        self.current_state = self.original_state.copy()
        self.best_state = self.current_state.copy()
        
        self.values = []
        
    def generate_successors(self, state):
        successors = []
        
        for i, container_from in enumerate(state.list_container):
            for item in container_from.item_list:
                for j, _ in enumerate(state.list_container):
                    if i != j:  
                        new_state = state.copy()
                        new_state.list_container[i].item_list.remove(item)
                        new_state.list_container[j].item_list.append(item)
                        new_state.list_container = [c for c in new_state.list_container if c.item_list]
                        successors.append(new_state)
                
                new_state = state.copy()
                new_state.list_container[i].item_list.remove(item)
                new_container = Container(self.capacity)
                new_container.item_list.append(item)
                new_state.list_container.append(new_container)
                new_state.list_container = [c for c in new_state.list_container if c.item_list]
                successors.append(new_state)
        
        for i, container1 in enumerate(state.list_container):
            for j, container2 in enumerate(state.list_container):
                if i < j: 
                    for item1 in container1.item_list:
                        for item2 in container2.item_list:
                            new_state = state.copy()
                            new_state.list_container[i].item_list.remove(item1)
                            new_state.list_container[j].item_list.remove(item2)

                            new_state.list_container[i].item_list.append(item2)
                            new_state.list_container[j].item_list.append(item1)
                            successors.append(new_state)
        return successors
    
    def hcSteepest(self, max_iterations=1000, save_plot=True):
        self.iterations = 0
        self.values = [self.current_state.count_penalty()]
        print(f"Initial Penalty: {self.current_state.count_penalty()}")
        while self.iterations < max_iterations:
            self.iterations += 1
            successors = self.generate_successors(self.current_state)
            if not successors:
                break
            best_successor = min(successors, key=lambda state: state.count_penalty())
            if best_successor.count_penalty() < self.current_state.count_penalty():
                self.current_state = best_successor
                self.values.append(self.current_state.count_penalty())
                if self.current_state.count_penalty() < self.best_state.count_penalty():
                    self.best_state = self.current_state.copy()
            else:
                break
        fig = self.plot_progress("Steepest Ascent Hill Climbing Progress", save=save_plot)
        return self.current_state, fig
    
    def hcSideways(self, max_sideways=10, max_iterations=1000, save_plot=True):
        self.iterations = 0
        self.sideways_moves = 0
        self.values = [self.current_state.count_penalty()]
        print(f"Initial Penalty: {self.current_state.count_penalty()}")
        while self.iterations < max_iterations and self.sideways_moves < max_sideways:
            self.iterations += 1
            successors = self.generate_successors(self.current_state)
            if not successors:
                break
            best_successor = min(successors, key=lambda state: state.count_penalty())
            if best_successor.count_penalty() < self.current_state.count_penalty():
                self.current_state = best_successor
                self.sideways_moves = 0  
                self.values.append(self.current_state.count_penalty())
                if self.current_state.count_penalty() < self.best_state.count_penalty():
                    self.best_state = self.current_state.copy()
            elif best_successor.count_penalty() == self.current_state.count_penalty():
                self.current_state = best_successor
                self.sideways_moves += 1
                self.values.append(self.current_state.count_penalty())
            else:
                break
        fig = self.plot_progress("Sideways Hill Climbing Progress", save=save_plot)
        return self.current_state, fig
    
    def hcStochastic(self, max_iterations=1000, save_plot=True):
        self.iterations = 0
        self.values = [self.current_state.count_penalty()]
        print(f"Initial Penalty: {self.current_state.count_penalty()}")
        for _ in range(max_iterations):
            self.iterations += 1
            successors = self.generate_successors(self.current_state)
            if not successors:
                break
            current_penalty = self.current_state.count_penalty()
            improving = [s for s in successors if s.count_penalty() < current_penalty]
            if not improving:
                break
            chosen = random.choice(improving)
            self.current_state = chosen
            new_penalty = self.current_state.count_penalty()
            self.values.append(new_penalty)
            if new_penalty < self.best_state.count_penalty():
                self.best_state = self.current_state.copy()
        
        fig = self.plot_progress("Stochastic Hill Climbing Progress", save=save_plot)
        return self.current_state, fig
    
    def hcRandomRestart(self, max_restarts=10, max_iterations_per_restart=100, save_plot=True):
        self.restarts = 0
        best_overall_state = None
        best_overall_penalty = float('inf')
        self.iterations_per_restart = []
        per_restart_final_penalties = []

        for _ in range(max_restarts):
            self.restarts += 1
            temp_hc = HillClimbing(self.problem_file, 'steepest')
            _final_state, _ = temp_hc.hcSteepest(max_iterations=max_iterations_per_restart, save_plot=False)
            self.iterations_per_restart.append(temp_hc.iterations)

            final_penalty = _final_state.count_penalty()
            print(f"Final Penalty: {final_penalty}")
            per_restart_final_penalties.append(final_penalty)
            if final_penalty < best_overall_penalty:
                best_overall_penalty = final_penalty
                best_overall_state = _final_state.copy()

        self.current_state = best_overall_state
        self.best_state = best_overall_state.copy()
        self.values = per_restart_final_penalties
        self.iterations = sum(self.iterations_per_restart)

        print(f"Total Restarts: {self.restarts}, Iterations per Restart: {self.iterations_per_restart}")

        fig = self.plot_progress("Random Restart Final Penalty per Restart", save=save_plot)
        return self.current_state, fig
    
    
    def plot_progress(self, title="Hill Climbing Progress", save=True):
        fig, ax = plt.subplots(figsize=(10, 6))
        x_vals = list(range(1, len(self.values) + 1))
        if self.algorithm_type == 'random_restart':
            ax.plot(x_vals, self.values, linestyle='-', marker='o', color='b', linewidth=1.5, markersize=4)
            ax.set_title('Random Restart - Final Penalty per Restart')
            ax.set_xlabel('Restart')
            ax.set_ylabel('Final Penalty')
        else:
            ax.plot(x_vals, self.values, linestyle='-', marker='o', color='b', linewidth=1.5, markersize=4)
            ax.set_title(f'{title} - Objective Function')
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Penalty Value')
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        if save:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(script_dir)
            project_root = os.path.dirname(parent_dir)
            plot_dir = os.path.join(project_root, 'result', 'plot')
            if not os.path.exists(plot_dir):
                os.makedirs(plot_dir)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"hill_{self.algorithm_type}_{timestamp}.png"
            filepath = os.path.join(plot_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {filepath}")
        return fig
    
    def printhasil(self, state, title):
        print(f"\n--- {title} ---")
        print(f"Total Kontainer Digunakan: {len(state.list_container)}")
        print(f"Nilai Objektif (Penalti): {state.count_penalty()}")
        print(f"Jumlah Iterasi: {self.iterations}")
        if hasattr(self, 'sideways_moves'):
            print(f"Jumlah Sideways Moves: {self.sideways_moves}")
        if hasattr(self, 'restarts'):
            print(f"Jumlah Restarts: {self.restarts}")
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
    def plott(results, algorithm_type, save=True):
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['b', 'g', 'r']
        
        for i, result in enumerate(results):
            if algorithm_type == 'random_restart':                
                num_runs = len(results)
                bar_width = 0.8 / num_runs
                
                iterations_per_restart = result['iterations_per_restart']
                num_restarts = len(iterations_per_restart)
                
                base_x = list(range(1, num_restarts + 1))
                bar_positions = [x + i * bar_width for x in base_x]
                
                ax.bar(bar_positions, iterations_per_restart, width=bar_width, color=colors[i % len(colors)], label=f"Run {i+1}")
                
                ax.set_xticks([r + bar_width * (num_runs - 1) / 2 for r in base_x])
                ax.set_xticklabels(base_x)
            else:
                values = result['values']
                x_vals = list(range(1, len(values) + 1))
                ax.plot(x_vals, values, linestyle='-', marker='o', color=colors[i % len(colors)], linewidth=1.5, markersize=4, label=f"Run {i+1}")

        if algorithm_type == 'random_restart':
            ax.set_title(f'Random Restart - Iterations Until Stop per Restart')
            ax.set_xlabel('Restart Number (Grouped by Run)')
            ax.set_ylabel('Iterations Until Stop')
        else:
            ax.set_title(f'{algorithm_type.replace("_", " ").title()} - Objective Function (3 Runs)')
            ax.set_xlabel('Iteration')
            ax.set_ylabel('Penalty Value')
        
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        if save:
            plot_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'result', 'plot')
            if not os.path.exists(plot_dir):
                os.makedirs(plot_dir)
            filename = f"hill_{algorithm_type}.png"
            filepath = os.path.join(plot_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot disimpan ke: {filepath}")
        return fig

    def run_hill_climbing_experiments(problem_file, algorithm_type="steepest"):
        print(f"=== HILL CLIMBING EXPERIMENTS - {algorithm_type.upper()} ===")
        experiments_results = []
        final_state = None 

        num_runs = 3
        for i in range(num_runs):
            print(f"\n--- Running Experiment {i+1}/{num_runs} for {algorithm_type.upper()} ---")
            start_time = time.time()
            hc_run = HillClimbing(problem_file, algorithm_type)
            hc_run.printhasil(hc_run.original_state, f"Initial State - Eksperimen {i+1}")
            if algorithm_type == "steepest": final_state, _ = hc_run.hcSteepest(save_plot=False)
            elif algorithm_type == "sideways": final_state, _ = hc_run.hcSideways(save_plot=False)
            elif algorithm_type == "stochastic": final_state, _ = hc_run.hcStochastic(save_plot=False)
            elif algorithm_type == "random_restart": final_state, _ = hc_run.hcRandomRestart(save_plot=False)
            
            duration = time.time() - start_time
            
            result = {
                'experiment_num': i + 1,
                'algorithm_type': algorithm_type,
                'initial_state': hc_run.original_state.copy(),
                'final_state': final_state,
                'duration': duration,
                'iterations': hc_run.iterations,
                'values': hc_run.values.copy(),
                'iterations_per_restart': hc_run.iterations_per_restart.copy() if hasattr(hc_run, 'iterations_per_restart') else []
            }
            if hasattr(hc_run, 'sideways_moves'): result['sideways_moves'] = hc_run.sideways_moves
            if hasattr(hc_run, 'restarts'): result['restarts'] = hc_run.restarts
            
            experiments_results.append(result)
            hc_run.printhasil(final_state, f"Final State - Eksperimen {i+1}")
            print(f"Durasi: {duration:.4f} detik")

        HillClimbing.plott(experiments_results, algorithm_type, save=True)
        return experiments_results
    
    @staticmethod
    def compare_algorithms(problem_file):
        algorithms = ["steepest", "sideways", "stochastic", "random_restart"]
        all_results = {}
        print("=== COMPARING ALL HILL CLIMBING ALGORITHMS ===")
        for algorithm in algorithms:
            print(f"\nRunning {algorithm}...")
            results = HillClimbing.run_hill_climbing_experiments(problem_file, algorithm)
            all_results[algorithm] = results
        print(f"\n{'='*100}")
        print("COMPARISON SUMMARY")
        print(f"{'='*100}")
        print(f"{'Algorithm':<20} {'Avg Final Penalty':<18} {'Avg Duration':<15} {'Avg Iterations':<15} {'Best Final Penalty':<18}")
        print("-" * 100)
        for algorithm, results in all_results.items():
            avg_final_penalty = sum(r['final_state'].count_penalty() for r in results) / len(results)
            avg_duration = sum(r['duration'] for r in results) / len(results)
            avg_iterations = sum(r['iterations'] for r in results) / len(results)
            best_final_penalty = min(r['final_state'].count_penalty() for r in results)
            print(f"{algorithm:<20} {avg_final_penalty:<18.2f} {avg_duration:<15.4f} {avg_iterations:<15.0f} {best_final_penalty:<18.2f}")
        return all_results
