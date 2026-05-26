import random
from config import (S_MASUK, S_JALAN, S_KE_RAK, S_DI_RAK, S_TGU_FIT, S_KE_FIT,
                     S_DI_FIT, S_KE_KAS, S_DI_KAS, S_KELUAR, S_BATAL, S_FORCED, S_DONE,
                     WARNA_BATAL, WARNA_FORCED, KASIR_QUEUE_SLOTS, peta_toko)
from map_utils import (astar, bilik_tersedia, kosongkan_bilik, PINTU_ROW18, 
                       LANTAI_DALAM, SEMUA_LANTAI, RAK_MAP)
from logger import tulis_log, add_data_to_excel

def get_free_queue_slot(kasir_queue_occupied):
    for slot in KASIR_QUEUE_SLOTS:
        if kasir_queue_occupied.get(slot) is None:
            return slot
    return None

def occupy_slot(kasir_queue_occupied, slot, npc_id):
    kasir_queue_occupied[slot] = npc_id

def free_slot(kasir_queue_occupied, npc_id):
    for slot in list(kasir_queue_occupied.keys()):
        if kasir_queue_occupied[slot] == npc_id:
            kasir_queue_occupied[slot] = None

def pindah(npc):
    if npc.jalur:
        nb,nk = npc.jalur.pop(0)
        npc.baris=nb; npc.kolom=nk; return True
    return False

def set_jalur(npc, tujuan, boleh_fitting=False, boleh_belakang=False):
    npc.jalur = astar((npc.baris,npc.kolom), tujuan, boleh_fitting, boleh_belakang)

def jalan_ke_pintu_keluar(npc, kasir_queue_occupied):
    if npc.queue_slot:
        free_slot(kasir_queue_occupied, npc.id)
        npc.queue_slot = None
    kosongkan_bilik(npc.id)
    tuj_r16 = min([(16,k) for k in range(13,19) if peta_toko[16][k]==0],
                  key=lambda p: abs(p[1]-npc.kolom), default=(16,15))
    j1 = astar((npc.baris,npc.kolom), tuj_r16, True)
    j2 = astar(tuj_r16, (17,15))
    j3 = astar((17,15), (19,15))
    return j1 + j2 + j3

def force_customer_leave(npc, kasir_queue_occupied):
    if npc.state in (S_DONE, S_KELUAR, S_BATAL, S_FORCED): return
    npc.warna = WARNA_FORCED
    npc.state = S_FORCED
    npc.jalur = jalan_ke_pintu_keluar(npc, kasir_queue_occupied)
    npc.log("Store closing soon — heading to exit.")

def update_npc(npc, total_stats, kasir_queue_occupied, get_date_str_func, get_jam_str_func):
    s = npc.state
    if s == S_DONE: return

    if s == S_FORCED:
        pindah(npc)
        if not npc.jalur:
            total_stats['batal'] += 1
            npc.state = S_DONE
            return True
        return False

    if s == S_MASUK:
        if not npc.jalur:
            tujuan_pilihan = [p for p in LANTAI_DALAM if 6<=p[0]<=10 and 6<=p[1]<=22]
            tuj = random.choice(tujuan_pilihan) if tujuan_pilihan else (9,13)
            set_jalur(npc, tuj)
        pindah(npc)
        if not npc.jalur:
            npc.state = S_JALAN if npc.suka_jalan>0 else S_KE_RAK

    elif s == S_JALAN:
        if not npc.jalur:
            if npc.jalan_sudah >= npc.suka_jalan:
                npc.state = S_KE_RAK; return False
            tuj = random.choice(LANTAI_DALAM) if LANTAI_DALAM else random.choice(SEMUA_LANTAI)
            set_jalur(npc, tuj)
            npc.jalan_sudah += 1
        else: pindah(npc)

    elif s == S_KE_RAK:
        if not npc.jalur:
            if npc.posisi_rak: set_jalur(npc, npc.posisi_rak)
            else:
                npc.state = S_KE_KAS if npc.niat_beli else S_BATAL; return False
        pindah(npc)
        if not npc.jalur:
            npc.state = S_DI_RAK
            npc.timer_tunggu = random.randint(2000,5000)
            npc.log(f"Browsing at {npc.nama_rak} — eyeing {npc.item_name}")

    elif s == S_DI_RAK:
        npc.timer_tunggu -= 200
        if npc.timer_tunggu <= 0:
            if not npc.niat_beli:
                npc.warna = WARNA_BATAL; npc.state = S_BATAL
                npc.log("Nothing suitable, heading out.")
            elif npc.ke_fitting:
                npc.state = S_TGU_FIT; npc.log(f"Want to try on {npc.item_name} in fitting room.")
            else:
                npc.state = S_KE_KAS; npc.log(f"Picked {npc.item_name} x{npc.quantity}, heading to cashier.")

    elif s == S_TGU_FIT:
        av = bilik_tersedia()
        if av:
            bl = min(av, key=lambda b: abs(b["pintu"][0]-npc.baris)+abs(b["pintu"][1]-npc.kolom))
            bl["penghuni"]=npc.id; npc.bilik_target=bl
            npc.state=S_KE_FIT; npc.jalur=[]; npc.log("Fitting room free → heading there...")
        else:
            npc.tunggu_fitting_timer += 200
            if npc.tunggu_fitting_timer > 8000:
                npc.log("Fitting room full, going straight to cashier."); npc.state=S_KE_KAS

    elif s == S_KE_FIT:
        if not npc.jalur:
            if npc.bilik_target: set_jalur(npc, npc.bilik_target["pintu"])
            else: npc.state=S_KE_KAS; return False
        pindah(npc)
        if not npc.jalur:
            if npc.bilik_target and npc.bilik_target["tiles"]:
                tgt = npc.bilik_target["tiles"][len(npc.bilik_target["tiles"])//2]
                j = astar((npc.baris,npc.kolom), tgt, True)
                if j:
                    npc.jalur=j; npc.state=S_DI_FIT
                    npc.timer_tunggu=random.randint(4000,7000)
                    npc.log("Trying on clothes... 🪞")
                else:
                    kosongkan_bilik(npc.id); npc.bilik_target=None; npc.state=S_KE_KAS
            else:
                kosongkan_bilik(npc.id); npc.bilik_target=None; npc.state=S_KE_KAS

    elif s == S_DI_FIT:
        if npc.jalur: pindah(npc); return False
        npc.timer_tunggu -= 200
        if npc.timer_tunggu <= 0:
            kosongkan_bilik(npc.id); npc.bilik_target=None
            npc.state=S_KE_KAS; npc.jalur=[]; npc.log("Done trying on, heading to cashier.")

    elif s == S_KE_KAS:
        if npc.queue_slot is None:
            slot = get_free_queue_slot(kasir_queue_occupied)
            if slot is None:
                return False
            npc.queue_slot = slot
            occupy_slot(kasir_queue_occupied, slot, npc.id)
        if not npc.jalur:
            set_jalur(npc, npc.queue_slot, True)
        pindah(npc)
        if not npc.jalur:
            npc.state        = S_DI_KAS
            npc.timer_tunggu = random.randint(2000,4000)
            npc.log("Queuing at cashier...")

    elif s == S_DI_KAS:
        npc.timer_tunggu -= 200
        if npc.timer_tunggu <= 0:
            add_data_to_excel(npc, get_date_str_func, get_jam_str_func)
            total_stats['beli'] += 1
            free_slot(kasir_queue_occupied, npc.id)
            npc.queue_slot = None
            npc.state = S_KELUAR
            npc.jalur = jalan_ke_pintu_keluar(npc, kasir_queue_occupied)
            npc.log(f"Payment done! Bought {npc.item_name} x{npc.quantity}. Heading to exit. 👋")

    elif s == S_BATAL:
        if not npc.jalur: npc.jalur = jalan_ke_pintu_keluar(npc, kasir_queue_occupied)
        pindah(npc)
        if not npc.jalur:
            total_stats['batal']+=1
            npc.state=S_DONE
            npc.log("Left without buying.")
            return True

    elif s == S_KELUAR:
        pindah(npc)
        if not npc.jalur:
            npc.state=S_DONE
            return True

    return False
