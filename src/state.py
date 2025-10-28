from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Barang:
    """Representasi sebuah barang"""
    id: str
    ukuran: int
    
    def __repr__(self):
        return f"{self.id} ({self.ukuran})"


@dataclass
class Kontainer:
    """Representasi sebuah kontainer"""
    kapasitas: int
    barang_list: List[Barang] = field(default_factory=list)
    
    @property
    def total_ukuran(self) -> int:
        """Menghitung total ukuran barang dalam kontainer"""
        return sum(barang.ukuran for barang in self.barang_list)
    
    @property
    def sisa_kapasitas(self) -> int:
        """Menghitung sisa kapasitas kontainer"""
        return self.kapasitas - self.total_ukuran
    
    def bisa_muat(self, barang: Barang) -> bool:
        """Mengecek apakah barang bisa muat di kontainer"""
        return barang.ukuran <= self.sisa_kapasitas
    
    def tambah_barang(self, barang: Barang) -> bool:
        """Menambahkan barang ke kontainer jika muat"""
        if self.bisa_muat(barang):
            self.barang_list.append(barang)
            return True
        return False
    
    def __repr__(self):
        return f"Kontainer(Total: {self.total_ukuran}/{self.kapasitas}): {self.barang_list}"


@dataclass
class State:
    """
    Representasi state untuk masalah bin packing
    
    State adalah alokasi barang ke kontainer menggunakan algoritma First Fit.
    Kontainer akan ditambahkan secara dinamis sesuai kebutuhan.
    """
    kapasitas_kontainer: int
    kontainer_list: List[Kontainer] = field(default_factory=list)  # List kontainer yang digunakan
    
    @property
    def jumlah_kontainer(self) -> int:
        """Menghitung jumlah kontainer yang digunakan"""
        return len(self.kontainer_list)
    
    def __repr__(self):
        result = [f"Total Kontainer Digunakan: {self.jumlah_kontainer}"]
        for i, kontainer in enumerate(self.kontainer_list, 1):
            result.append(f"{i}. {kontainer}")
        return "\n".join(result)
    
    def print_detail(self):
        """Mencetak detail state dalam format yang lebih rapi"""
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