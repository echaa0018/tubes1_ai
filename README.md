
# Tugas Besar 1 IF3070 Pencarian Solusi Pengepakan Barang (Bin Packing Problem) dengan Local Search
## Deskripsi
Tujuan dari program ini adalah untuk menggunakan algoritma Local Search untuk menempatkan sekumpulan barang dengan ukuran yang berbeda-beda ke dalam sejumlah kontainer dengan kapasitas yang sama, dengan tujuan menggunakan jumlah kontainer sesedikit mungkin.

### Algoritma yang Digunakan
- Genetic Algorithm
- Steepest Ascent Hill Climbing
- Stochastic Ascent Hill Climbing
- Sideways Move Hill Climbing
- Random Restart Hill Climbing
- Simulated Annealing

## Cara Menjalankan Program
### Pre-Requirements
- __`matplotlib`__
Download matplotlib dengan cara:
```markdown
pip install matplotlib
```
### Run Program
Clone github ini,
```markdown
git clone https://github.com/echaa0018/tubes1_ai.git
```
Pergi ke directory hasil clone repo,
```markdown
cd ../tubes1_ai
```
Run main.py,
```markdown
py src/main.py
```
Setelah run main, anda akan disuruh untuk input nama file .json sebagai input (sudah ada beberapa template yang tersedia, bisa buat baru juga), kemudian pilih antara 6 algoritma local search. Setelah memilih, program akan menjalankan local search sebanyak 3 kali, akan ditampilkan juga ringkasan dan hasil terbaik dari 3 search tersebut. Hasil ketiga instance local search tersebut akan disimpan di folder __`../result`__, dan plot dapat disimpan di __`../result/plot`__.
## Pembagian Tugas Kelompok
| Anggota | NIM | Pembagian Tugas |
| --- | --- | --- |
| Valereo Jibril Al Buchori | 18223030 | Hill Climbing, Laporan |
| Mahesa Satria Prayata | 18223082 | Genetic Algorithm, Laporan |
| Jason Samuel | 18223091 | Simulated Annealing, Laporan |