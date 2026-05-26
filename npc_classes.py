import random
from config import (ITEMS_BY_RACK, WARNA_FEMALE, WARNA_MALE, WARNA_BATAL, 
                     S_MASUK, S_JALAN, S_KE_RAK, S_DI_RAK, S_TGU_FIT, S_KE_FIT, 
                     S_DI_FIT, S_KE_KAS, S_DI_KAS, S_KELUAR, S_BATAL, S_DONE,
                     SK_DATANG, SK_STANDBY, SK_PULANG, SK_DONE)
from map_utils import astar, PINTU_ROW18, LANTAI_DALAM, SEMUA_LANTAI, RAK_MAP, kosongkan_bilik
from logger import tulis_log

npc_id_counter = 0

class NPC:
    def __init__(self):
        global npc_id_counter
        npc_id_counter  += 1
        self.id    = npc_id_counter
        self.nama  = f"AiCust{npc_id_counter:03d}"
        self.gender= random.choice(["female","male"])
        self.warna = WARNA_FEMALE if self.gender=="female" else WARNA_MALE
        p = random.choice(PINTU_ROW18) if PINTU_ROW18 else (18,15)
        self.baris = p[0]; self.kolom = p[1]
        self.state = S_MASUK
        self.jalur = []
        self.timer_tunggu    = 0
        self.suka_jalan      = random.randint(0,2)
        self.jalan_sudah     = 0
        self.niat_beli       = random.random() > 0.2
        nama_rak = random.choice(list(RAK_MAP.keys()))
        lst, bisa_fitting    = RAK_MAP[nama_rak]
        self.nama_rak        = nama_rak
        self.posisi_rak      = random.choice(lst) if lst else None
        self.ke_fitting      = self.niat_beli and bisa_fitting and random.random()<0.45
        self.bilik_target    = None
        self.tunggu_fitting_timer = 0
        self.queue_slot      = None
        rack_items = ITEMS_BY_RACK.get(nama_rak, [])
        self.item_name = random.choice(rack_items) if rack_items else "Unknown"
        self.quantity  = random.choices([1, 2, 3], weights=[70, 22, 8])[0]

    def log(self, msg):
        tulis_log(f"[{self.nama}] {msg}")

class KasirNPC:
    def __init__(self, npc_id, posisi_kerja):
        self.id           = npc_id
        self.nama         = f"Cashier{npc_id}"
        self.posisi_kerja = posisi_kerja
        self.baris        = PINTU_ROW18[0][0] if PINTU_ROW18 else 18
        self.kolom        = PINTU_ROW18[0][1] if PINTU_ROW18 else 15
        self.state        = SK_DATANG
        self.jalur        = []
        self.aktif        = False

    def log(self, msg):
        tulis_log(f"[{self.nama}] {msg}")

    def reset_for_new_day(self):
        self.baris  = PINTU_ROW18[0][0] if PINTU_ROW18 else 18
        self.kolom  = PINTU_ROW18[0][1] if PINTU_ROW18 else 15
        self.state  = SK_DATANG
        self.jalur  = []
        self.aktif  = True

    def update(self):
        if not self.aktif or self.state == SK_DONE:
            return
        if self.state == SK_DATANG:
            if not self.jalur:
                j1 = astar((self.baris, self.kolom), (16,15))
                j2 = astar((16,15), self.posisi_kerja, False, True)
                self.jalur = j1 + j2
            if self.jalur:
                nb,nk = self.jalur.pop(0)
                self.baris=nb; self.kolom=nk
            if not self.jalur:
                self.state = SK_STANDBY
                self.log("Arrived at cashier, ready to serve customers.")
        elif self.state == SK_STANDBY:
            self.baris = self.posisi_kerja[0]
            self.kolom = self.posisi_kerja[1]
        elif self.state == SK_PULANG:
            if not self.jalur:
                j1 = astar(self.posisi_kerja,(16,15),False,True)
                j2 = astar((16,15),(19,15))
                self.jalur = j1 + j2
            if self.jalur:
                nb,nk = self.jalur.pop(0)
                self.baris=nb; self.kolom=nk
            if not self.jalur:
                self.state = SK_DONE
                self.aktif = False
                self.log("Going home. See you tomorrow! 👋")
