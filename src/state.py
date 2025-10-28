from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import copy


@dataclass
class Barang:
    id: str
    ukuran: int
    
    def __repr__(self):
        return f"{self.id} ({self.ukuran})"
    
    def copy(self) -> 'Barang':
        """Membuat salinan barang"""
        return Barang(id=self.id, ukuran=self.ukuran)


@dataclass
class Kontainer:
    kapasitas: int
    barang_list: List[Barang] = field(default_factory=list)
    
    @property
    def total_ukuran(self) -> int:
        return sum(barang.ukuran for barang in self.barang_list)
    
    @property
    def sisa_kapasitas(self) -> int:
        return self.kapasitas - self.total_ukuran
    
    def bisa_muat(self, barang: Barang) -> bool:
        return barang.ukuran <= self.sisa_kapasitas
    
    def tambah_barang(self, barang: Barang) -> bool:
        if self.bisa_muat(barang):
            self.barang_list.append(barang)
            return True
        return False
    
    def hapus_barang(self, barang_id: str) -> Optional[Barang]:
        """Hapus barang berdasarkan ID dan return barang yang dihapus"""
        for i, barang in enumerate(self.barang_list):
            if barang.id == barang_id:
                return self.barang_list.pop(i)
        return None
    
    def copy(self) -> 'Kontainer':
        """Membuat deep copy dari kontainer"""
        new_kontainer = Kontainer(kapasitas=self.kapasitas)
        new_kontainer.barang_list = [barang.copy() for barang in self.barang_list]
        return new_kontainer
    
    def __repr__(self):
        return f"Kontainer(Total: {self.total_ukuran}/{self.kapasitas}): {self.barang_list}"


@dataclass
class State:
    kapasitas_kontainer: int
    kontainer_list: List[Kontainer] = field(default_factory=list)  # List kontainer yang digunakan
    
    @property
    def jumlah_kontainer(self) -> int:
        return len(self.kontainer_list)
    
    def is_valid(self) -> bool:
        """Cek apakah semua kontainer dalam batas kapasitas"""
        return all(k.total_ukuran <= k.kapasitas for k in self.kontainer_list)
    
    def copy(self) -> 'State':
        """Membuat deep copy dari state"""
        new_state = State(kapasitas_kontainer=self.kapasitas_kontainer)
        new_state.kontainer_list = [kontainer.copy() for kontainer in self.kontainer_list]
        return new_state
    
    def remove_empty_containers(self) -> None:
        """Hapus kontainer yang kosong"""
        self.kontainer_list = [k for k in self.kontainer_list if len(k.barang_list) > 0]
    
    def find_barang(self, barang_id: str) -> Optional[Tuple[int, Barang]]:
        """Cari barang berdasarkan ID, return (index_kontainer, barang) atau None"""
        for idx, kontainer in enumerate(self.kontainer_list):
            for barang in kontainer.barang_list:
                if barang.id == barang_id:
                    return (idx, barang)
        return None
    
    def get_all_barang_ids(self) -> List[str]:
        """Return semua ID barang yang ada di state"""
        ids = []
        for kontainer in self.kontainer_list:
            for barang in kontainer.barang_list:
                ids.append(barang.id)
        return ids
    
    def __repr__(self):
        result = [f"Total Kontainer Digunakan: {self.jumlah_kontainer}"]
        for i, kontainer in enumerate(self.kontainer_list, 1):
            result.append(f"{i}. {kontainer}")
        return "\n".join(result)
    
    def print_detail(self):
        print(f"Total Kontainer Digunakan: {self.jumlah_kontainer}")
        for i, kontainer in enumerate(self.kontainer_list, 1):
            print(f"{i}. Kontainer {i} (Total: {kontainer.total_ukuran}/{kontainer.kapasitas}):")
            for barang in kontainer.barang_list:
                print(f"   • {barang.id} ({barang.ukuran})")


def first_fit(data: Dict) -> State:
    # Inisialisasi state menggunakan algoritma First Fit
    kapasitas = data["kapasitas_kontainer"]
    barang_list = [Barang(id=b["id"], ukuran=b["ukuran"]) for b in data["barang"]]
    
    state = State(kapasitas_kontainer=kapasitas)
    
    for barang in barang_list:
        ditempatkan = False
        for kontainer in state.kontainer_list:
            if kontainer.tambah_barang(barang):
                ditempatkan = True
                break
        if not ditempatkan:
            kontainer_baru = Kontainer(kapasitas=kapasitas)
            kontainer_baru.tambah_barang(barang)
            state.kontainer_list.append(kontainer_baru)
    
    return state