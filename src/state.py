from input_manager import load_problem
import random
import os

class Item:
    id: str
    size: int

class Container:
    capacity: int
    item_list: list[Item]

    def __init__(self, capacity : int):
        self.capacity = capacity
        self.item_list = []

    def total_size(self):
        return sum(item['ukuran'] for item in self.item_list)

class State:
    list_container: list[Container]

    def __init__(self):
        self.list_container = []

    def count_penalty(self):
        penalty = 0
        count = 0
        for container in self.list_container:
            count += 1
            total_size = sum(item['ukuran'] for item in container.item_list)
            if total_size > container.capacity:
                penalty += (total_size - container.capacity)*50
            else :
                penalty += (container.capacity - total_size)*0.5
        penalty += count * 100
        return penalty
    
    def first_fit(self, filepath):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        problem_path = os.path.join(parent_dir, 'data', f'{filepath}.json')
        list_items, capacity = load_problem(problem_path)
        self.list_container = [] 

        for item in list_items:
            item_placed = False
            for container in self.list_container:
                if container.total_size() + item['ukuran'] <= capacity:
                    container.item_list.append(item)
                    item_placed = True
                    break
            if not item_placed:
                new_container = Container(capacity=capacity)
                new_container.item_list.append(item)
                self.list_container.append(new_container)
    
    def copy(self):
        new_state = State()
        for container in self.list_container:
            new_container = Container(capacity=container.capacity)
            new_container.item_list = container.item_list.copy()
            new_state.list_container.append(new_container)
        return new_state
    
    def generate_random_state(self, filepath):
        import random
        import os
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        problem_path = os.path.join(parent_dir, 'data', f'{filepath}.json')
        list_items, capacity = load_problem(problem_path)
        random.shuffle(list_items)
        num_containers = random.randint(1, len(list_items))
        
        self.list_container = [Container(capacity=capacity) for _ in range(num_containers)]
        
        for item in list_items:
            random.choice(self.list_container).item_list.append(item)
        if random.random() < 0.2:
            extra_empty = random.randint(1, 3)
            for _ in range(extra_empty):
                self.list_container.append(Container(capacity=capacity))