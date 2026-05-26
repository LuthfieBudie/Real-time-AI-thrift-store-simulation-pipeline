import heapq
from config import peta_toko, total_baris, total_kolom


def astar(start, goal, boleh_fitting=False, boleh_belakang_kasir=False):
    terlarang = {1,2,3,4,5,6,7,8,9,10,11}
    if boleh_fitting:        terlarang.discard(4)
    if boleh_belakang_kasir: terlarang.discard(11)
    open_set = []
    heapq.heappush(open_set, (0, start))
    came = {}
    g = {start: 0}
    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur == goal:
            path = []
            while cur in came:
                path.append(cur); cur = came[cur]
            path.reverse(); return path
        for db, dk in ((-1,0),(1,0),(0,-1),(0,1)):
            nb, nk = cur[0]+db, cur[1]+dk
            n2 = (nb, nk)
            if not (0 <= nb < total_baris and 0 <= nk < total_kolom): continue
            if peta_toko[nb][nk] in terlarang: continue
            ng = g[cur] + 1
            if ng < g.get(n2, 999999):
                came[n2] = cur; g[n2] = ng
                heapq.heappush(open_set, (ng+abs(nb-goal[0])+abs(nk-goal[1]), n2))
    return []





PINTU_ROW17 = [(17,k) for k in range(13,19) if peta_toko[17][k]==0]
PINTU_ROW18 = [(18,k) for k in range(13,19) if peta_toko[18][k]==0]
PINTU_ROW19 = [(19,k) for k in range(13,19) if peta_toko[19][k]==0]





def sebelah(tipe_list):
    h = set()
    if isinstance(tipe_list, int): tipe_list = [tipe_list]
    for b in range(total_baris):
        for k in range(total_kolom):
            if peta_toko[b][k] in tipe_list:
                for db,dk in ((-1,0),(1,0),(0,-1),(0,1)):
                    nb,nk=b+db,k+dk
                    if 0<=nb<total_baris and 0<=nk<total_kolom:
                        if peta_toko[nb][nk]==0: h.add((nb,nk))
    return list(h)

SEBELAH_BAJU   = sebelah(5)
SEBELAH_CELANA = sebelah(6)
SEBELAH_JAKET  = sebelah(3)
SEBELAH_SEPATU = sebelah(7)
SEBELAH_TOPI   = sebelah(8)
SEBELAH_JAS    = sebelah(10)

SEMUA_LANTAI = [(b,k) for b in range(total_baris) for k in range(total_kolom) if peta_toko[b][k]==0]
LANTAI_DALAM = [(b,k) for b in range(1,17) for k in range(4,28) if peta_toko[b][k]==0]

kasir_posisi_list = []
for b in range(total_baris):
    for k in range(total_kolom):
        if peta_toko[b][k]==11: kasir_posisi_list.append((b,k))

POSISI_KASIR_NPC_1 = kasir_posisi_list[0] if len(kasir_posisi_list)>=1 else (10,15)
POSISI_KASIR_NPC_2 = kasir_posisi_list[1] if len(kasir_posisi_list)>=2 else (10,16)

RAK_MAP = {
    "👗 Shirts":  (SEBELAH_BAJU,   True),
    "👖 Pants":   (SEBELAH_CELANA, True),
    "🧥 Jackets": (SEBELAH_JAKET,  False),
    "👞 Shoes":   (SEBELAH_SEPATU, False),
    "🧢 Hats":    (SEBELAH_TOPI,   False),
    "🤵 Suits":   (SEBELAH_JAS,    True),
}

BILIK_FITTING = []
baris_fitting = 9
for k in range(14, 19):
    if peta_toko[baris_fitting][k] == 4:
        BILIK_FITTING.append({
            "tiles": [(baris_fitting, k)],
            "pintu": (baris_fitting - 1, k),
            "penghuni": None
        })

def bilik_tersedia():
    return [b for b in BILIK_FITTING if b["penghuni"] is None]

def kosongkan_bilik(nid):
    for b in BILIK_FITTING:
        if b["penghuni"]==nid: b["penghuni"]=None; return
