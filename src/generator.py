from state import Item, Container, State
import random

def generate_random_state(num_containers: int, max_capacity: int, num_items: int, max_item_size: int) -> State:
    containers = []
    for _ in range(num_containers):
        capacity = random.randint(1, max_capacity)
        containers.append(Container(capacity=capacity, item_list=[]))

    items = []
    for i in range(num_items):
        size = random.randint(1, max_item_size)
        items.append(Item(id=f"item_{i}", size=size))

    for item in items:
        placed = False
        while not placed:
            container = random.choice(containers)
            if sum(it.size for it in container.item_list) + item.size <= container.capacity:
                container.item_list.append(item)
                placed = True

    return State(list_container=containers)