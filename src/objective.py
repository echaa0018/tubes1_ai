from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from state import State


class ObjectiveFunction:
    # Semakin RENDAH nilai objective, semakin BAIK solusinya.
    PENALTI_KAPASITAS_BERLEBIH = 1000000
    
    BOBOT_JUMLAH_KONTAINER = 1000
    BOBOT_KEPADATAN = 100
    
    
    @staticmethod
    def hitung_penalti_kapasitas_berlebih(state: 'State') -> float:
        total_penalti = 0
        for kontainer in state.kontainer_list:
            if kontainer.total_ukuran > kontainer.kapasitas:
                kelebihan = kontainer.total_ukuran - kontainer.kapasitas
                total_penalti += kelebihan * ObjectiveFunction.PENALTI_KAPASITAS_BERLEBIH
        
        return total_penalti
    
    
    @staticmethod
    def hitung_skor_jumlah_kontainer(state: 'State') -> float:
        return state.jumlah_kontainer * ObjectiveFunction.BOBOT_JUMLAH_KONTAINER
    
    
    @staticmethod
    def hitung_skor_kepadatan(state: 'State') -> float:
        """
        Kepadatan dihitung sebagai: total_ukuran / kapasitas
        Skor = (1 - rata-rata kepadatan) * BOBOT
        
        Semakin padat kontainer, semakin rendah skornya (lebih baik).
        """
        if state.jumlah_kontainer == 0:
            return 0
        
        total_kepadatan = 0
        for kontainer in state.kontainer_list:
            kepadatan = kontainer.total_ukuran / kontainer.kapasitas
            total_kepadatan += kepadatan
        
        rata_rata_kepadatan = total_kepadatan / state.jumlah_kontainer
        return (1 - rata_rata_kepadatan) * ObjectiveFunction.BOBOT_KEPADATAN
    
    
    @staticmethod
    def hitung_objective(state: 'State') -> float:
        """
        Objective = Penalti Kapasitas + Skor Jumlah Kontainer + Skor Kepadatan
        
        Prioritas komponen (dari yang paling berpengaruh):
        1. Penalti Kapasitas (bobot: 1,000,000) - Solusi HARUS valid
        2. Jumlah Kontainer (bobot: 1,000) - Tujuan utama
        3. Kepadatan (bobot: 100) - Optimasi tambahan
        
        Nilai objective function (lebih rendah = lebih baik)
        """
        penalti_kapasitas = ObjectiveFunction.hitung_penalti_kapasitas_berlebih(state)
        skor_jumlah = ObjectiveFunction.hitung_skor_jumlah_kontainer(state)
        skor_kepadatan = ObjectiveFunction.hitung_skor_kepadatan(state)
        
        total_objective = penalti_kapasitas + skor_jumlah + skor_kepadatan
        
        return total_objective
    
    
    @staticmethod
    def print_detail_objective(state: 'State') -> None:
        penalti_kapasitas = ObjectiveFunction.hitung_penalti_kapasitas_berlebih(state)
        skor_jumlah = ObjectiveFunction.hitung_skor_jumlah_kontainer(state)
        skor_kepadatan = ObjectiveFunction.hitung_skor_kepadatan(state)
        total = ObjectiveFunction.hitung_objective(state)
        
        print("=" * 60)
        print("DETAIL OBJECTIVE FUNCTION")
        print("=" * 60)
        print(f"1. Penalti Kapasitas Berlebih: {penalti_kapasitas:,.2f}")
        print(f"   (Bobot: {ObjectiveFunction.PENALTI_KAPASITAS_BERLEBIH:,})")
        print()
        print(f"2. Skor Jumlah Kontainer: {skor_jumlah:,.2f}")
        print(f"   ({state.jumlah_kontainer} kontainer × {ObjectiveFunction.BOBOT_JUMLAH_KONTAINER:,})")
        print()
        print(f"3. Skor Kepadatan: {skor_kepadatan:,.2f}")
        print(f"   (Bobot: {ObjectiveFunction.BOBOT_KEPADATAN:,})")
        
        # Hitung kepadatan untuk detail
        if state.jumlah_kontainer > 0:
            total_kepadatan = sum(k.total_ukuran / k.kapasitas for k in state.kontainer_list)
            rata_kepadatan = total_kepadatan / state.jumlah_kontainer
            print(f"   (Rata-rata kepadatan: {rata_kepadatan:.2%})")
        
        print()
        print("=" * 60)
        print(f"TOTAL OBJECTIVE: {total:,.2f}")
        print("=" * 60)
        print()
        
        # Validasi
        if penalti_kapasitas > 0:
            print("⚠️  PERINGATAN: State tidak valid (ada kontainer yang overload)")
        else:
            print("✓ State valid (semua kontainer dalam kapasitas)")
        print()


# Fungsi helper untuk kemudahan penggunaan
def evaluate(state: 'State') -> float:
    return ObjectiveFunction.hitung_objective(state)


def print_evaluation(state: 'State') -> None:
    ObjectiveFunction.print_detail_objective(state)
