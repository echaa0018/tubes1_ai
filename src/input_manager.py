import json

def load_problem(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    list_items = data.get("barang", [])
    capacity = data.get("kapasitas_kontainer", 0)

    return list_items, capacity