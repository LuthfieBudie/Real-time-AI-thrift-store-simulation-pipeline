import customtkinter as ctk
import tkinter as tk
import random
from config import (WIN_W, WIN_H, SPEED_LEVELS, SPEED_LABELS, SPEED_COLORS, 
                     SPEED_HOVER, DAYS_IN_MONTH, DAY_NAMES, DAY_ANIM_TOTAL, 
                     DAY_ANIM_START, S_DONE, S_KELUAR, S_BATAL, S_FORCED, SK_DONE, 
                     SK_STANDBY, SK_PULANG, music_file, canvas_width, canvas_height)
from map_utils import PINTU_ROW18, POSISI_KASIR_NPC_1, POSISI_KASIR_NPC_2
from logger import tulis_log, get_log_buf, get_log_dirty, set_log_dirty
from audio import autostart_music, toggle_music_state, stop_music, is_music_available, play_sfx_day
from npc_classes import NPC, KasirNPC
from drawing import draw_bg, draw_npcs, draw_clock
from simulation import update_npc, force_customer_leave, get_free_queue_slot, occupy_slot, free_slot

app = None
canvas = None
textbox_log = None
frame_npc_list = None
label_widgets = {}
panel_kanan = None
lbl_total = None
lbl_beli = None
lbl_batal = None
btn_music = None
speed_btns = []

sim_minutes    = 0
sim_year  = 2026
sim_month = 1
sim_day_of_month = 1
sim_day = 0
speed_level = 0
music_playing = True
total_kunjungan = 0
total_beli_stat = 0
total_batal_stat = 0

daftar_npc_aktif = []
kasir_npc_1 = None
kasir_npc_2 = None
kasir_queue_occupied = {}

day_anim_active = False
day_anim_offset = 0
day_anim_frame = 0

next_spawn_at = 0

kasir_sudah_datang  = False
kasir_sudah_pulang  = False
spawn_sudah_dimulai = False
closing_forced      = False

def get_tick_ms():
    return max(30, 250 // SPEED_LEVELS[speed_level])

def get_loop_ms():
    return max(20, 150 // SPEED_LEVELS[speed_level])

def get_jam_str():
    h = sim_minutes // 60
    m = sim_minutes % 60
    return f"{h:02d}:{m:02d}"

def is_store_open():
    h = sim_minutes // 60
    m = sim_minutes % 60
    if h < 6: return False
    if h == 6 and m < 5: return False
    if h >= 22: return False
    if h == 21 and m >= 40: return False
    return True

def get_date_str():
    return f"{sim_day_of_month:02d}/{sim_month:02d}/{str(sim_year)[2:]}"

def get_weekday_name():
    return DAY_NAMES[(3 + sim_day) % 7]

def advance_date():
    global sim_day_of_month, sim_month, sim_year
    is_leap = (sim_year % 4 == 0 and sim_year % 100 != 0) or (sim_year % 400 == 0)
    days_this_month = DAYS_IN_MONTH[sim_month] + (1 if sim_month == 2 and is_leap else 0)
    sim_day_of_month += 1
    if sim_day_of_month > days_this_month:
        sim_day_of_month = 1
        sim_month += 1
        if sim_month > 12:
            sim_month = 1
            sim_year += 1

def reset_next_spawn():
    global next_spawn_at
    next_spawn_at = sim_minutes + random.randint(25, 50)

def do_spawn_customer():
    global next_spawn_at, total_kunjungan, daftar_npc_aktif
    if is_store_open():
        npc = NPC()
        daftar_npc_aktif.append(npc)
        tambah_label_npc(npc)
        npc.log(f"Entered store ({'Female' if npc.gender=='female' else 'Male'}) — browsing {npc.nama_rak}")
        update_stat()
        total_kunjungan += 1
    reset_next_spawn()

def trigger_day_animation():
    global day_anim_active, day_anim_offset, day_anim_frame
    day_anim_active = True
    day_anim_offset = DAY_ANIM_START
    day_anim_frame  = 0
    play_sfx_day(music_playing)
    _step_day_anim()

def _step_day_anim():
    global day_anim_active, day_anim_offset, day_anim_frame
    if day_anim_frame >= DAY_ANIM_TOTAL:
        day_anim_active = False; day_anim_offset = 0; return
    t    = day_anim_frame / DAY_ANIM_TOTAL
    ease = 1 - (1 - t) ** 3
    day_anim_offset = int(DAY_ANIM_START * (1 - ease))
    day_anim_frame += 1
    app.after(25, _step_day_anim)

def tambah_label_npc(npc):
    f  = ctk.CTkFrame(frame_npc_list, fg_color="#1E1E1E", corner_radius=8)
    f.pack(fill="x", pady=3, padx=5)
    icon  = "♀" if (hasattr(npc,'gender') and npc.gender=="female") else "♂"
    warna = getattr(npc,'warna',"#FFD700")
    lb = ctk.CTkLabel(f, text=f"{icon} {npc.nama}\n{npc.state}",
                      font=ctk.CTkFont(size=11), text_color=warna,
                      anchor="w", justify="left")
    lb.pack(padx=10, pady=5, fill="x")
    label_widgets[f"npc_{npc.id}"] = (f, lb)
    app.after(50, lambda: frame_npc_list._parent_canvas.yview_moveto(1.0))

def update_label_npc(npc):
    key = f"npc_{npc.id}"
    if key in label_widgets:
        icon  = "♀" if (hasattr(npc,'gender') and npc.gender=="female") else "♂"
        warna = getattr(npc,'warna',"#FFD700")
        label_widgets[key][1].configure(
            text=f"{icon} {npc.nama}\n{npc.state}", text_color=warna)

def hapus_label_npc(key):
    if key in label_widgets:
        label_widgets[key][0].destroy()
        del label_widgets[key]

def tambah_label_kasir():
    for knpc in [kasir_npc_1, kasir_npc_2]:
        key = f"kasir_{knpc.id}"
        if key not in label_widgets:
            f = ctk.CTkFrame(frame_npc_list, fg_color="#1E1200", corner_radius=8)
            f.pack(fill="x", pady=3, padx=5)
            lb = ctk.CTkLabel(f, text=f"⭐ {knpc.nama}\n{knpc.state}",
                              font=ctk.CTkFont(size=11), text_color="#FFD700",
                              anchor="w", justify="left")
            lb.pack(padx=10, pady=5, fill="x")
            label_widgets[key] = (f, lb)

def update_label_kasir():
    for knpc in [kasir_npc_1, kasir_npc_2]:
        key = f"kasir_{knpc.id}"
        if key in label_widgets:
            label_widgets[key][1].configure(text=f"⭐ {knpc.nama}\n{knpc.state}")

def update_stat():
    lbl_total.configure(text=f"Total Visitors     : {total_kunjungan}")
    lbl_beli.configure(text=f"Successful Purchase: {total_beli_stat}")
    lbl_batal.configure(text=f"Cancelled Purchase : {total_batal_stat}")

def flush_log():
    if get_log_dirty():
        teks = "\n".join(get_log_buf())
        textbox_log.configure(state="normal")
        textbox_log.delete("1.0", "end")
        textbox_log.insert("1.0", teks)
        textbox_log.see("end")
        textbox_log.configure(state="disabled")
        set_log_dirty(False)
    app.after(600, flush_log)

def set_speed(idx):
    global speed_level
    speed_level = idx
    for i, btn in enumerate(speed_btns):
        if i == idx:
            btn.configure(fg_color=SPEED_COLORS[i], border_color=SPEED_HOVER[i],
                          text_color="#ffffff", border_width=2,
                          font=ctk.CTkFont(size=12, weight="bold"))
        else:
            btn.configure(fg_color="#1e1e1e", border_color="#333333",
                          text_color="#555555", border_width=1,
                          font=ctk.CTkFont(size=12))

def toggle_music():
    global music_playing
    if not is_music_available():
        return
    music_playing = toggle_music_state(music_playing)
    if music_playing:
        btn_music.configure(fg_color="#1a6a1a", text_color="#ffffff", text="🔊 MUSIC ON")
    else:
        btn_music.configure(fg_color="#4a1a1a", text_color="#ff5555", text="🔇 MUSIC OFF")

def tick_waktu():
    global sim_minutes, kasir_sudah_datang, kasir_sudah_pulang
    global spawn_sudah_dimulai, closing_forced, sim_day, next_spawn_at

    sim_minutes = (sim_minutes + 1) % 1440
    h = sim_minutes // 60
    m = sim_minutes % 60

    if h == 6 and m == 0 and not kasir_sudah_datang:
        kasir_sudah_datang = True
        kasir_npc_1.reset_for_new_day()
        kasir_npc_2.reset_for_new_day()
        tambah_label_kasir()
        tulis_log("06:00 — Cashier 1 & 2 arriving for shift!")

    if h == 6 and m == 5 and not spawn_sudah_dimulai:
        spawn_sudah_dimulai = True
        tulis_log("06:05 — Store open! Customers welcome.")
        do_spawn_customer()

    if spawn_sudah_dimulai and is_store_open() and sim_minutes >= next_spawn_at:
        do_spawn_customer()

    if h == 21 and m == 40 and not closing_forced:
        closing_forced = True
        count = 0
        for npc in daftar_npc_aktif:
            if npc.state not in (S_DONE, S_KELUAR, S_BATAL, S_FORCED):
                force_customer_leave(npc, kasir_queue_occupied)
                count += 1
        if count > 0:
            tulis_log(f"21:40 — Store closing in 20 min! {count} customers escorted out.")

    if h == 22 and m == 0 and not kasir_sudah_pulang:
        kasir_sudah_pulang = True
        for knpc in [kasir_npc_1, kasir_npc_2]:
            if knpc.aktif and knpc.state == SK_STANDBY:
                knpc.state = SK_PULANG; knpc.jalur = []
                knpc.log("22:00 — Time to head home!")

    if h == 0 and m == 0:
        kasir_sudah_datang  = False
        kasir_sudah_pulang  = False
        spawn_sudah_dimulai = False
        closing_forced      = False
        next_spawn_at       = 0
        for slot in [(14, 10), (14, 11), (14, 12), (14, 13)]:
            kasir_queue_occupied[slot] = None
        sim_day += 1
        advance_date()
        tulis_log(f"🌙 Midnight — entering Day {sim_day}")
        trigger_day_animation()

    app.after(get_tick_ms(), tick_waktu)

def loop_simulasi():
    global daftar_npc_aktif, total_beli_stat, total_batal_stat
    
    kasir_npc_1.update()
    kasir_npc_2.update()
    update_label_kasir()
    
    npc_to_remove = []
    for npc in daftar_npc_aktif:
        if npc.state != S_DONE:
            stats = {'beli': total_beli_stat, 'batal': total_batal_stat}
            is_done = update_npc(npc, stats, kasir_queue_occupied, get_date_str, get_jam_str)
            total_beli_stat = stats['beli']
            total_batal_stat = stats['batal']
            if is_done:
                npc_to_remove.append(npc.id)
                hapus_label_npc(f"npc_{npc.id}")
            else:
                update_label_npc(npc)
    
    update_stat()
    daftar_npc_aktif[:] = [n for n in daftar_npc_aktif if n.id not in npc_to_remove]
    
    draw_npcs(canvas, daftar_npc_aktif, kasir_npc_1, kasir_npc_2, 
              lambda: draw_clock(canvas, sim_minutes, sim_day, day_anim_offset,
                                get_jam_str, get_date_str, get_weekday_name, is_store_open, canvas_width),
              26)
    app.after(get_loop_ms(), loop_simulasi)

def init_ui():
    global app, canvas, textbox_log, frame_npc_list, label_widgets, panel_kanan
    global lbl_total, lbl_beli, lbl_batal, btn_music, speed_btns
    global kasir_npc_1, kasir_npc_2, kasir_queue_occupied

    app = ctk.CTk()
    app.title("Thrift Shop Simulation")
    app.configure(fg_color="#0A0A0A")

    app.update_idletasks()
    sw = app.winfo_screenwidth()
    sh = app.winfo_screenheight()
    x  = (sw - WIN_W) // 2
    y  = (sh - WIN_H) // 2
    app.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    frame_utama = ctk.CTkFrame(app, fg_color="#0A0A0A")
    frame_utama.pack(fill="both", expand=True)

    frame_canvas = ctk.CTkFrame(frame_utama, fg_color="#121212", corner_radius=15)
    frame_canvas.pack(side="left", padx=15, pady=15, fill="both", expand=True)

    canvas = tk.Canvas(frame_canvas, width=canvas_width, height=canvas_height,
                       bg="#121212", highlightthickness=0)
    canvas.place(relx=0.5, rely=0.5, anchor="center")

    panel_kanan = ctk.CTkFrame(frame_utama, width=290, fg_color="#181818", corner_radius=15)
    panel_kanan.pack(side="right", fill="y", padx=(0,15), pady=15)
    panel_kanan.pack_propagate(False)

    ctk.CTkLabel(panel_kanan, text="📊 ACTIVITY LOG",
                 font=ctk.CTkFont(size=14, weight="bold"),
                 text_color="#00FFCC").pack(pady=(15,10))

    textbox_log = ctk.CTkTextbox(panel_kanan, fg_color="#0D0D0D", text_color="#A0A0A0",
                                  font=ctk.CTkFont(size=11), wrap="word", height=220)
    textbox_log.pack(fill="x", padx=12, pady=(0,10))
    textbox_log.configure(state="disabled")

    ctk.CTkLabel(panel_kanan, text="👥 ACTIVE NPCs",
                 font=ctk.CTkFont(size=12, weight="bold"),
                 text_color="#666666").pack(pady=(5,5))

    frame_npc_list = ctk.CTkScrollableFrame(panel_kanan, fg_color="#121212",
                                             scrollbar_button_color="#222222",
                                             scrollbar_button_hover_color="#333333")
    frame_npc_list.pack(fill="both", expand=True, padx=10, pady=(0,10))

    frame_stat = ctk.CTkFrame(panel_kanan, fg_color="#202020", corner_radius=10)
    frame_stat.pack(fill="x", padx=12, pady=(0,15))
    lbl_total = ctk.CTkLabel(frame_stat, text="Total Visitors     : 0",
                              font=ctk.CTkFont(size=11), text_color="#BBBBBB")
    lbl_total.pack(pady=(8,2))
    lbl_beli  = ctk.CTkLabel(frame_stat, text="Successful Purchase: 0",
                              font=ctk.CTkFont(size=11, weight="bold"), text_color="#00FF88")
    lbl_beli.pack(pady=2)
    lbl_batal = ctk.CTkLabel(frame_stat, text="Cancelled Purchase : 0",
                              font=ctk.CTkFont(size=11), text_color="#FF5555")
    lbl_batal.pack(pady=(2,8))

    frame_speed = ctk.CTkFrame(panel_kanan, fg_color="#101010", corner_radius=10)
    frame_speed.pack(fill="x", padx=12, pady=(0, 12))

    ctk.CTkLabel(frame_speed, text="⚡ SPEED UP",
                 font=ctk.CTkFont(size=10, weight="bold"),
                 text_color="#888888").pack(pady=(8, 4))

    frame_speed_btns = ctk.CTkFrame(frame_speed, fg_color="transparent")
    frame_speed_btns.pack(pady=(0, 8))

    for i, lbl_s in enumerate(SPEED_LABELS):
        btn = ctk.CTkButton(
            frame_speed_btns, text=lbl_s, width=54, height=34, corner_radius=7,
            fg_color="#1e1e1e", hover_color=SPEED_HOVER[i], border_color="#333333",
            border_width=1, text_color="#555555", font=ctk.CTkFont(size=12),
            command=lambda x=i: set_speed(x))
        btn.pack(side="left", padx=3)
        speed_btns.append(btn)
    set_speed(0)

    btn_music = ctk.CTkButton(
        panel_kanan, text="🔊 MUSIC ON", height=34, corner_radius=7,
        fg_color="#1a6a1a", hover_color="#22882a", border_color="#333333",
        border_width=1, text_color="#ffffff", font=ctk.CTkFont(size=11, weight="bold"),
        command=toggle_music)
    btn_music.pack(fill="x", padx=12, pady=(0, 12))

    # Initialize cashier NPCs
    kasir_npc_1 = KasirNPC(1, POSISI_KASIR_NPC_1)
    kasir_npc_2 = KasirNPC(2, POSISI_KASIR_NPC_2)

    for slot in [(14, 10), (14, 11), (14, 12), (14, 13)]:
        kasir_queue_occupied[slot] = None

    tulis_log("Thrift Shop Simulation started.")
    tulis_log(f"Queue slots: {[(14, 10), (14, 11), (14, 12), (14, 13)]}")
    tulis_log("Clock starts at 00:00 — Cashiers arrive at 06:00")
    tulis_log("Excel logging: Thrift_Sales_Dataset.xlsx")
    if is_music_available():
        tulis_log("Music system initialized. Click MUSIC ON to play.")
    else:
        tulis_log("Warning: Pygame not available, music disabled.")

    draw_bg(canvas)
    app.after(400,  flush_log)
    app.after(500,  tick_waktu)
    app.after(1200, loop_simulasi)

    def on_closing():
        stop_music()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.after(800, lambda: music_playing if autostart_music(music_playing) else None)
    app.mainloop()

if __name__ == "__main__":
    init_ui()
