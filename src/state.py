from input_manager import load_problem
import random

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
        return sum(item.size for item in self.item_list)

class State:
    list_container: list[Container]

    def __init__(self):
        self.list_container = []

    def count_penalty(self):
        penalty = 0
        for container in self.list_container:
            total_size = sum(item.size for item in container.item_list)
            if total_size > container.capacity:
                penalty += (total_size - container.capacity)*10
            else :
                penalty += (container.capacity - total_size)
        return penalty
    
    def first_fit(self, filepath):
        list_items, capacity = load_problem(f'data/{filepath}.json')
        temp_container = Container(capacity=capacity)
        for item in list_items:
            if temp_container.total_size() + item['ukuran'] <= capacity:
                temp_container.item_list.append(item)
            else:
                self.list_container.append(temp_container)
                temp_container = Container(capacity=capacity)
                temp_container.item_list.append(item)

    def generate_random_state(self, filepath):
        list_items, capacity = load_problem(f'data/{filepath}.json')
        temp_container = Container(capacity=capacity)
        
        while list_items:
            a = random.choice(list_items)
            if temp_container.total_size() + a['ukuran'] <= capacity:
                temp_container.item_list.append(a)
                list_items.remove(a)
            else:
                self.list_container.append(temp_container)
                temp_container = Container(capacity=capacity)
                temp_container.item_list.append(a)
                list_items.remove(a)
        
        # Append the last container if it has items
        if temp_container.item_list:
            self.list_container.append(temp_container)