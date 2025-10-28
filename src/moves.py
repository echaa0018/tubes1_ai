"""
Module untuk generate neighbor states untuk local search algorithms.

Terdapat 2 jenis move sesuai spesifikasi:
1. Move 1 Barang: Pindahkan 1 barang dari kontainer ke kontainer lain
2. Swap 2 Barang: Tukar 2 barang dari 2 kontainer berbeda
"""

from typing import List, Optional
import random
from state import State, Barang, Kontainer


class MoveGenerator:

    @staticmethod
    def move_barang(state: State, barang_id: str, from_idx: int, to_idx: int) -> Optional[State]:
        # Validasi input
        if from_idx == to_idx:
            return None
        if from_idx < 0 or from_idx >= len(state.kontainer_list):
            return None
        if to_idx < 0 or to_idx >= len(state.kontainer_list):
            return None
        
        # Copy state
        new_state = state.copy()
        
        # Hapus barang dari kontainer asal
        barang = new_state.kontainer_list[from_idx].hapus_barang(barang_id)
        if barang is None:
            return None
        
        # Tambahkan ke kontainer tujuan
        new_state.kontainer_list[to_idx].tambah_barang(barang)
        
        # Hapus kontainer kosong
        new_state.remove_empty_containers()
        
        return new_state
    
    
    @staticmethod
    def swap_barang(state: State, barang1_id: str, kontainer1_idx: int, barang2_id: str, kontainer2_idx: int) -> Optional[State]:
        # Validasi input
        if kontainer1_idx == kontainer2_idx:
            return None
        if kontainer1_idx < 0 or kontainer1_idx >= len(state.kontainer_list):
            return None
        if kontainer2_idx < 0 or kontainer2_idx >= len(state.kontainer_list):
            return None
        
        # Copy state
        new_state = state.copy()
        
        # Hapus kedua barang
        barang1 = new_state.kontainer_list[kontainer1_idx].hapus_barang(barang1_id)
        barang2 = new_state.kontainer_list[kontainer2_idx].hapus_barang(barang2_id)
        
        if barang1 is None or barang2 is None:
            return None
        
        # Tukar posisi
        new_state.kontainer_list[kontainer1_idx].tambah_barang(barang2)
        new_state.kontainer_list[kontainer2_idx].tambah_barang(barang1)
        
        return new_state
    
    
    @staticmethod
    def create_new_container_move(state: State, barang_id: str, from_idx: int) -> Optional[State]:
        # Validasi input
        if from_idx < 0 or from_idx >= len(state.kontainer_list):
            return None
        
        # Copy state
        new_state = state.copy()
        
        # Hapus barang dari kontainer asal
        barang = new_state.kontainer_list[from_idx].hapus_barang(barang_id)
        if barang is None:
            return None
        
        # Buat kontainer baru dan masukkan barang
        kontainer_baru = Kontainer(kapasitas=state.kapasitas_kontainer)
        kontainer_baru.tambah_barang(barang)
        new_state.kontainer_list.append(kontainer_baru)
        
        # Hapus kontainer kosong (dari kontainer asal jika kosong)
        new_state.remove_empty_containers()
        
        return new_state
    
    
    @staticmethod
    def get_all_move_neighbors(state: State) -> List[State]:
        neighbors = []
        
        # Untuk setiap kontainer
        for from_idx, from_kontainer in enumerate(state.kontainer_list):
            # Untuk setiap barang di kontainer
            for barang in from_kontainer.barang_list:
                # Coba pindahkan ke kontainer lain
                for to_idx in range(len(state.kontainer_list)):
                    if from_idx != to_idx:
                        new_state = MoveGenerator.move_barang(
                            state, barang.id, from_idx, to_idx
                        )
                        if new_state is not None:
                            neighbors.append(new_state)
                
                # Coba pindahkan ke kontainer baru (opsional, bisa di-comment jika terlalu banyak)
                new_state = MoveGenerator.create_new_container_move(state, barang.id, from_idx)
                if new_state is not None:
                    neighbors.append(new_state)
        
        return neighbors
    
    
    @staticmethod
    def get_all_swap_neighbors(state: State) -> List[State]:
        neighbors = []
        
        # Untuk setiap pasangan kontainer
        for idx1 in range(len(state.kontainer_list)):
            for idx2 in range(idx1 + 1, len(state.kontainer_list)):
                kontainer1 = state.kontainer_list[idx1]
                kontainer2 = state.kontainer_list[idx2]
                
                # Untuk setiap pasangan barang
                for barang1 in kontainer1.barang_list:
                    for barang2 in kontainer2.barang_list:
                        new_state = MoveGenerator.swap_barang(
                            state, barang1.id, idx1, barang2.id, idx2
                        )
                        if new_state is not None:
                            neighbors.append(new_state)
        
        return neighbors
    
    
    @staticmethod
    def get_all_neighbors(state: State, include_swap: bool = True) -> List[State]:
        neighbors = []
        
        neighbors.extend(MoveGenerator.get_all_move_neighbors(state))
        
        if include_swap:
            neighbors.extend(MoveGenerator.get_all_swap_neighbors(state))
        
        return neighbors
    
    
    @staticmethod
    def get_random_neighbor(state: State, max_attempts: int = 100) -> Optional[State]:
        if len(state.kontainer_list) == 0:
            return None
        
        for _ in range(max_attempts):
            # Random pilih jenis move
            if random.random() < 0.5:
                # Random Move
                neighbor = MoveGenerator._random_move_neighbor(state)
            else:
                # Random Swap
                neighbor = MoveGenerator._random_swap_neighbor(state)
            
            if neighbor is not None:
                return neighbor
        
        return None
    
    
    @staticmethod
    def _random_move_neighbor(state: State) -> Optional[State]:
        if len(state.kontainer_list) < 2:
            return None
        
        # Random pilih kontainer asal
        from_idx = random.randint(0, len(state.kontainer_list) - 1)
        from_kontainer = state.kontainer_list[from_idx]
        
        if len(from_kontainer.barang_list) == 0:
            return None
        
        # Random pilih barang
        barang = random.choice(from_kontainer.barang_list)
        
        # Random pilih kontainer tujuan (berbeda dari asal)
        to_idx = random.randint(0, len(state.kontainer_list) - 1)
        while to_idx == from_idx:
            to_idx = random.randint(0, len(state.kontainer_list) - 1)
        
        return MoveGenerator.move_barang(state, barang.id, from_idx, to_idx)
    
    
    @staticmethod
    def _random_swap_neighbor(state: State) -> Optional[State]:
        if len(state.kontainer_list) < 2:
            return None
        
        # Random pilih 2 kontainer berbeda
        idx1 = random.randint(0, len(state.kontainer_list) - 1)
        idx2 = random.randint(0, len(state.kontainer_list) - 1)
        while idx2 == idx1:
            idx2 = random.randint(0, len(state.kontainer_list) - 1)
        
        kontainer1 = state.kontainer_list[idx1]
        kontainer2 = state.kontainer_list[idx2]
        
        if len(kontainer1.barang_list) == 0 or len(kontainer2.barang_list) == 0:
            return None
        
        # Random pilih barang dari masing-masing kontainer
        barang1 = random.choice(kontainer1.barang_list)
        barang2 = random.choice(kontainer2.barang_list)
        
        return MoveGenerator.swap_barang(state, barang1.id, idx1, barang2.id, idx2)


# Helper functions untuk kemudahan penggunaan
def get_neighbors(state: State, include_swap: bool = True) -> List[State]:
    return MoveGenerator.get_all_neighbors(state, include_swap)


def random_neighbor(state: State) -> Optional[State]:
    return MoveGenerator.get_random_neighbor(state)