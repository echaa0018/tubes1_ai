# Objective Function Documentation

## Tujuan Utama
**Meminimalkan jumlah kontainer yang digunakan** untuk menampung semua barang.

## Komponen Objective Function

### 1. Penalti Kapasitas Berlebih
**Bobot: 1,000,000 per unit kelebihan**

- **Tujuan**: Memastikan solusi yang dihasilkan VALID (semua kontainer dalam batas kapasitas)
- **Cara Kerja**: Setiap kontainer yang melebihi kapasitas akan mendapat penalti sangat besar
- **Pengaruh**: SANGAT BESAR - solusi invalid akan langsung ditolak
- **Formula**: 
  ```
  Penalti = Σ(kelebihan_kapasitas × 1,000,000) untuk setiap kontainer overload
  ```

**Contoh**:
- Kontainer kapasitas 100, terisi 110 → Penalti = 10 × 1,000,000 = 10,000,000
- Kontainer kapasitas 100, terisi 90 → Penalti = 0 (valid)

---

### 2. Skor Jumlah Kontainer
**Bobot: 1,000 per kontainer**

- **Tujuan**: Meminimalkan jumlah kontainer (PRIORITAS UTAMA)
- **Cara Kerja**: Setiap kontainer yang digunakan menambah biaya 1,000
- **Pengaruh**: TINGGI - merupakan tujuan utama optimasi
- **Formula**: 
  ```
  Skor = Jumlah_Kontainer × 1,000
  ```

**Contoh**:
- 3 kontainer → Skor = 3,000
- 4 kontainer → Skor = 4,000
- State dengan 3 kontainer LEBIH BAIK daripada 4 kontainer

---

### 3. Skor Kepadatan
**Bobot: 100**

- **Tujuan**: Memaksimalkan utilisasi ruang di setiap kontainer
- **Cara Kerja**: Mendorong algoritma untuk mengisi kontainer sepadat mungkin
- **Pengaruh**: SEDANG - digunakan sebagai tie-breaker ketika jumlah kontainer sama
- **Formula**: 
  ```
  Kepadatan = Total_Ukuran / Kapasitas (untuk setiap kontainer)
  Rata_Kepadatan = Σ(Kepadatan) / Jumlah_Kontainer
  Skor = (1 - Rata_Kepadatan) × 100
  ```

**Contoh**:
- 2 kontainer dengan kepadatan 90% dan 90% → Rata = 90% → Skor = (1 - 0.9) × 100 = 10
- 2 kontainer dengan kepadatan 50% dan 50% → Rata = 50% → Skor = (1 - 0.5) × 100 = 50
- Kepadatan tinggi → Skor RENDAH → LEBIH BAIK

---

## Total Objective Function

```
Objective = Penalti_Kapasitas + Skor_Jumlah_Kontainer + Skor_Kepadatan
```

**Aturan: SEMAKIN RENDAH nilai objective, SEMAKIN BAIK solusinya**

---

## Proporsi Pengaruh

Berdasarkan bobot, pengaruh setiap komponen:

| Komponen | Bobot | Pengaruh Relatif | Prioritas |
|----------|-------|------------------|-----------|
| Penalti Kapasitas | 1,000,000 | 99.9%+ (jika ada overload) | 1 (Mutlak) |
| Jumlah Kontainer | 1,000 | ~99% (untuk solusi valid) | 2 (Utama) |
| Kepadatan | 100 | ~1% | 3 (Tie-breaker) |

---

## Contoh Perhitungan

### State 1: 4 kontainer dengan kepadatan rata-rata 76.25%
```
Penalti Kapasitas    = 0 (semua valid)
Skor Jumlah          = 4 × 1,000 = 4,000
Skor Kepadatan       = (1 - 0.7625) × 100 = 23.75
─────────────────────────────────────────
TOTAL OBJECTIVE      = 4,023.75
```

### State 2: 3 kontainer dengan kepadatan rata-rata 90%
```
Penalti Kapasitas    = 0 (semua valid)
Skor Jumlah          = 3 × 1,000 = 3,000
Skor Kepadatan       = (1 - 0.90) × 100 = 10
─────────────────────────────────────────
TOTAL OBJECTIVE      = 3,010.00
```

**Kesimpulan**: State 2 LEBIH BAIK (3,010 < 4,023.75)

---

## Kalibrasi Bobot

Bobot dipilih dengan pertimbangan:

1. **Penalti Kapasitas (1,000,000)**:
   - Harus jauh lebih besar dari komponen lainnya
   - Bahkan 1 unit overload harus membuat solusi tidak competitive
   - Menjamin solusi akhir selalu valid

2. **Jumlah Kontainer (1,000)**:
   - 10x lebih besar dari bobot kepadatan
   - Memastikan mengurangi 1 kontainer lebih penting daripada meningkatkan kepadatan
   - Sesuai dengan tujuan utama: meminimalkan kontainer

3. **Kepadatan (100)**:
   - Cukup untuk mempengaruhi keputusan ketika jumlah kontainer sama
   - Tidak terlalu besar sehingga mengalahkan tujuan utama
   - Berfungsi sebagai tie-breaker yang efektif

---

## Penggunaan dalam Algoritma

Objective function ini dirancang untuk digunakan dalam berbagai algoritma optimasi:

- **Local Search**: Memilih neighbor dengan objective terendah
- **Simulated Annealing**: Menghitung Δ objective untuk acceptance probability
- **Genetic Algorithm**: Fitness function (invert untuk maximization)
- **Hill Climbing**: Greedy selection berdasarkan objective

---

## Validasi

Objective function menjamin:

1. ✓ Solusi invalid (overload) SELALU lebih buruk dari solusi valid
2. ✓ Solusi dengan lebih sedikit kontainer SELALU lebih baik (jika keduanya valid)
3. ✓ Ketika jumlah kontainer sama, solusi dengan kepadatan lebih tinggi lebih baik
4. ✓ Nilai objective dapat dibandingkan secara konsisten

---

## API Usage

```python
from objective import ObjectiveFunction, evaluate, print_evaluation
from state import State

# Cara 1: Evaluasi sederhana
nilai = evaluate(state)
print(f"Objective: {nilai}")

# Cara 2: Detail lengkap
print_evaluation(state)

# Cara 3: Manual per komponen
penalti = ObjectiveFunction.hitung_penalti_kapasitas_berlebih(state)
skor_jumlah = ObjectiveFunction.hitung_skor_jumlah_kontainer(state)
skor_kepadatan = ObjectiveFunction.hitung_skor_kepadatan(state)
total = ObjectiveFunction.hitung_objective(state)
```
