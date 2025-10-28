"""
Contoh penggunaan State untuk masalah bin packing dengan First Fit
"""
import json
import sys
import os

# Tambahkan src ke path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from state import first_fit


def main():
    # Load input dari JSON
    with open('data/input.json', 'r') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("INISIALISASI STATE MENGGUNAKAN FIRST FIT")
    print("=" * 60)
    print()
    
    # Buat state menggunakan First Fit
    state = first_fit(data)
    
    # Tampilkan hasil
    state.print_detail()
    print()
    print(f"Total kontainer yang dibutuhkan: {state.jumlah_kontainer}")


if __name__ == "__main__":
    main()
