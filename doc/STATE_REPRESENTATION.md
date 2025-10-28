# Representasi State untuk Bin Packing Problem

## Struktur Data

### 1. `Barang` (Dataclass)
Representasi sebuah barang yang akan ditempatkan ke dalam kontainer.

**Atribut:**
- `id`: String - ID unik barang (contoh: "BRG001")
- `ukuran`: Integer - Ukuran/berat barang dalam unit yang sama

### 2. `Kontainer` (Dataclass)
Representasi sebuah kontainer yang menampung barang-barang.

**Atribut:**
- `kapasitas`: Integer - Kapasitas maksimum kontainer
- `barang_list`: List[Barang] - Daftar barang yang ada di kontainer

**Properties:**
- `total_ukuran`: Menghitung total ukuran barang dalam kontainer
- `sisa_kapasitas`: Menghitung sisa kapasitas kontainer

**Methods:**
- `bisa_muat(barang)`: Mengecek apakah barang bisa muat
- `tambah_barang(barang)`: Menambahkan barang ke kontainer

### 3. `State` (Dataclass)
Representasi state untuk masalah bin packing. State merepresentasikan alokasi barang ke kontainer yang sudah lengkap.

**Atribut:**
- `kapasitas_kontainer`: Integer - Kapasitas setiap kontainer
- `kontainer_list`: List[Kontainer] - Daftar kontainer yang digunakan

**Properties:**
- `jumlah_kontainer`: Menghitung jumlah kontainer yang digunakan

**Methods:**
- `print_detail()`: Mencetak detail state dalam format yang rapi

## Algoritma Inisialisasi

### First Fit
Fungsi `first_fit(data)` digunakan untuk menginisialisasi state dari input JSON.

**Cara Kerja:**
1. Untuk setiap barang (sesuai urutan dalam input)
2. Coba masukkan ke kontainer pertama yang bisa menampung
3. Jika tidak ada kontainer yang bisa menampung, buat kontainer baru
4. Kontainer ditambahkan secara dinamis sesuai kebutuhan

## Format Input (JSON)

```json
{
  "kapasitas_kontainer": 100,
  "barang": [
    { "id": "BRG001", "ukuran": 40 },
    { "id": "BRG002", "ukuran": 55 },
    ...
  ]
}
```

## Cara Penggunaan

### Inisialisasi State dengan First Fit

```python
import json
from state import first_fit

# Load input
with open('data/input.json', 'r') as f:
    data = json.load(f)

# Buat state menggunakan First Fit
state = first_fit(data)

# Tampilkan hasil
state.print_detail()
print(f"Total kontainer: {state.jumlah_kontainer}")
```

### Akses Data State

```python
# Akses kontainer
for i, kontainer in enumerate(state.kontainer_list, 1):
    print(f"Kontainer {i}:")
    print(f"  Total: {kontainer.total_ukuran}/{kontainer.kapasitas}")
    print(f"  Sisa: {kontainer.sisa_kapasitas}")
    
    # Akses barang dalam kontainer
    for barang in kontainer.barang_list:
        print(f"  - {barang.id}: {barang.ukuran}")
```

## Contoh Output

```
Total Kontainer Digunakan: 4
1. Kontainer 1 (Total: 95/100):
   • BRG001 (40)
   • BRG002 (55)
2. Kontainer 2 (Total: 85/100):
   • BRG003 (25)
   • BRG004 (60)
3. Kontainer 3 (Total: 75/100):
   • BRG005 (30)
   • BRG006 (45)
4. Kontainer 4 (Total: 50/100):
   • BRG007 (50)

Total kontainer yang dibutuhkan: 4
```

## Keuntungan Struktur Ini

1. **Sederhana**: Fokus pada satu algoritma inisialisasi (First Fit)
2. **Dinamis**: Kontainer ditambahkan sesuai kebutuhan
3. **Clean Code**: Menggunakan dataclass dan type hints
4. **Easy to Use**: API yang intuitif
5. **Deterministik**: Hasil konsisten untuk input yang sama
