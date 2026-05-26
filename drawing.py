from config import (peta_toko, total_baris, total_kolom, SZ, 
                    CLOCK_X, DATE_Y, CLOCK_Y, WIDGET_W, canvas_width, canvas_height, SK_DONE, S_DONE)


def _c(h, n):
    r,g,b = int(h[1:3],16),int(h[3:5],16),int(h[5:7],16)
    r=max(0,min(255,r+n)); g=max(0,min(255,g+n)); b=max(0,min(255,b+n))
    return f"#{r:02x}{g:02x}{b:02x}"

def draw_rack_baju(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; ym=(y1+y2)//2; base="#8B4A8B"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-20),tags="bg")
    cv.create_rectangle(x1+1,y1+1,x2-1,y1+4,fill=_c(base,40),outline="",tags="bg")
    cv.create_line(x1+2,y1+5,x2-2,y1+5,fill="#cccccc",width=2,tags="bg")
    baju_warna=["#ff88cc","#ffcc44","#88aaff","#ff7744","#44cc88","#ee44aa"]
    step=max(6,(x2-x1-6)//4)
    for i,gx in enumerate(range(x1+5,x2-3,step)):
        wc=baju_warna[i%len(baju_warna)]
        cv.create_line(gx+1,y1+5,gx+1,ym-3,fill="#bbbbbb",width=1,tags="bg")
        cv.create_arc(gx-2,ym-6,gx+4,ym,start=0,extent=180,outline="#dddddd",style="arc",width=1,tags="bg")
        cv.create_rectangle(gx-2,ym,gx+4,ym+7,fill=wc,outline="",tags="bg")
        cv.create_rectangle(gx-5,ym,gx-1,ym+3,fill=wc,outline="",tags="bg")
        cv.create_rectangle(gx+5,ym,gx+7,ym+3,fill=wc,outline="",tags="bg")

def draw_rack_celana(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; ym=(y1+y2)//2; base="#1a4a7a"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-20),tags="bg")
    cv.create_rectangle(x1+1,y1+1,x2-1,y1+4,fill=_c(base,40),outline="",tags="bg")
    cv.create_line(x1+2,y1+5,x2-2,y1+5,fill="#88ccff",width=2,tags="bg")
    celana_warna=["#3366aa","#224488","#4477bb","#1a3366","#5588cc"]
    step=max(6,(x2-x1-6)//4)
    for i,gx in enumerate(range(x1+5,x2-3,step)):
        wc=celana_warna[i%len(celana_warna)]
        cv.create_line(gx+1,y1+5,gx+1,ym-3,fill="#aaaaaa",width=1,tags="bg")
        cv.create_arc(gx-2,ym-6,gx+4,ym,start=0,extent=180,outline="#88ccff",style="arc",width=1,tags="bg")
        cv.create_rectangle(gx-3,ym,gx,ym+9,fill=wc,outline="",tags="bg")
        cv.create_rectangle(gx+2,ym,gx+5,ym+9,fill=wc,outline="",tags="bg")
        cv.create_rectangle(gx-3,ym,gx+5,ym+3,fill=_c(wc,15),outline="",tags="bg")

def draw_rack_jaket(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; ym=(y1+y2)//2; base="#4a3010"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-15),tags="bg")
    cv.create_rectangle(x1+1,y1+1,x2-1,y1+4,fill=_c(base,35),outline="",tags="bg")
    cv.create_line(x1+2,y1+5,x2-2,y1+5,fill="#c8a060",width=2,tags="bg")
    jaket_warna=["#7a4010","#5a3008","#9a5018","#3d2008","#8a4818"]
    step=max(6,(x2-x1-6)//4)
    for i,gx in enumerate(range(x1+5,x2-3,step)):
        wc=jaket_warna[i%len(jaket_warna)]
        cv.create_line(gx+1,y1+5,gx+1,ym-3,fill="#c8a060",width=1,tags="bg")
        cv.create_arc(gx-2,ym-6,gx+4,ym,start=0,extent=180,outline="#c8a060",style="arc",width=1,tags="bg")
        cv.create_rectangle(gx-3,ym,gx+5,ym+9,fill=wc,outline="",tags="bg")
        cv.create_polygon(gx-3,ym,gx,ym,gx-1,ym+3,fill=_c(wc,25),tags="bg")
        cv.create_polygon(gx+5,ym,gx+2,ym,gx+3,ym+3,fill=_c(wc,25),tags="bg")
        cv.create_rectangle(gx-6,ym+1,gx-2,ym+6,fill=wc,outline="",tags="bg")
        cv.create_rectangle(gx+6,ym+1,gx+8,ym+6,fill=wc,outline="",tags="bg")
        cv.create_line(gx+1,ym+3,gx+1,ym+9,fill=_c(wc,40),width=1,tags="bg")

def draw_rack_sepatu(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; ym=(y1+y2)//2; base="#2a4a2a"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-15),tags="bg")
    for gy_shelf in [ym-2,y2-6]:
        cv.create_rectangle(x1+1,gy_shelf,x2-1,gy_shelf+2,fill=_c(base,30),outline="",tags="bg")
    for ox,wc in [(x1+2,"#cc8833"),(xm-4,"#884422"),(x2-10,"#dd9944")]:
        cv.create_oval(ox,ym-8,ox+7,ym-3,fill=wc,outline=_c(wc,-20),tags="bg")
        cv.create_rectangle(ox+2,ym-10,ox+4,ym-8,fill=_c(wc,15),outline="",tags="bg")
        cv.create_rectangle(ox,ym-3,ox+7,ym-1,fill="#222222",outline="",tags="bg")
        for ty in range(ym-9,ym-4,2):
            cv.create_line(ox+1,ty,ox+6,ty,fill="#eeeeee",width=1,tags="bg")
    for ox,wc in [(x1+3,"#553322"),(x2-10,"#334488")]:
        cv.create_oval(ox,y2-11,ox+7,y2-6,fill=wc,outline=_c(wc,-20),tags="bg")
        cv.create_rectangle(ox,y2-6,ox+7,y2-4,fill="#222222",outline="",tags="bg")

def draw_rack_topi(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; ym=(y1+y2)//2; base="#1a3a3a"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-15),tags="bg")
    cv.create_rectangle(x1+1,y1+1,x2-1,y1+4,fill=_c(base,40),outline="",tags="bg")
    cv.create_line(xm,y1+4,xm,y2-3,fill=_c(base,35),width=2,tags="bg")
    topi_warna=["#228833","#cc2222","#2244cc","#cc8822","#882288","#228899"]
    posisi_topi=[(x1+4,y1+3),(x2-8,y1+3),(x1+4,ym-2),(x2-8,ym-2),(xm-3,ym+5)]
    for i,(gx,gy) in enumerate(posisi_topi):
        wc=topi_warna[i%len(topi_warna)]
        cv.create_oval(gx-1,gy+4,gx+7,gy+7,fill=wc,outline="",tags="bg")
        cv.create_arc(gx,gy,gx+6,gy+6,start=0,extent=180,fill=wc,outline=_c(wc,-20),tags="bg")
        cv.create_line(gx+3,gy+5,gx+8,gy+5,fill=_c(wc,-25),width=2,tags="bg")

def draw_rack_jas(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; ym=(y1+y2)//2; base="#1a1a2e"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-10),tags="bg")
    cv.create_rectangle(x1+1,y1+1,x2-1,y1+4,fill=_c(base,40),outline="",tags="bg")
    cv.create_line(x1+2,y1+5,x2-2,y1+5,fill="#8888ff",width=2,tags="bg")
    jas_warna=["#111122","#0d0d2e","#181830","#090918","#1e1e3a"]
    step=max(6,(x2-x1-6)//4)
    for i,gx in enumerate(range(x1+5,x2-3,step)):
        wc=jas_warna[i%len(jas_warna)]
        cv.create_line(gx+1,y1+5,gx+1,ym-3,fill="#8888ff",width=1,tags="bg")
        cv.create_arc(gx-2,ym-6,gx+4,ym,start=0,extent=180,outline="#aaaaff",style="arc",width=1,tags="bg")
        cv.create_rectangle(gx-4,ym,gx+6,ym+10,fill=wc,outline="#333355",tags="bg")
        cv.create_polygon(gx-4,ym,gx-1,ym,gx+1,ym+4,fill="#dddddd",tags="bg")
        cv.create_polygon(gx+6,ym,gx+3,ym,gx+1,ym+4,fill="#dddddd",tags="bg")
        cv.create_polygon(gx,ym+3,gx+2,ym+3,gx+3,ym+7,gx+1,ym+10,gx-1,ym+7,fill="#cc2222",tags="bg")
        cv.create_oval(gx,ym+5,gx+2,ym+7,fill="#888899",outline="",tags="bg")
        cv.create_rectangle(gx-3,ym+7,gx,ym+10,fill=_c(wc,10),outline="#333355",tags="bg")
        cv.create_polygon(gx-2,ym+7,gx-1,ym+5,gx,ym+7,fill="#ffffff",tags="bg")

def draw_kasir(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; base="#c8a020"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-30),width=1,tags="bg")
    cv.create_rectangle(x1+1,y1+1,x2-1,y1+SZ//3,fill=_c(base,40),outline="",tags="bg")
    cv.create_line(x1,y1,x2,y1,fill=_c(base,55),width=1,tags="bg")
    cv.create_line(x1,y1,x1,y2,fill=_c(base,55),width=1,tags="bg")
    cv.create_line(x1,y2-1,x2,y2-1,fill=_c(base,-35),width=1,tags="bg")
    cv.create_rectangle(xm-4,y1+1,xm+3,y1+SZ//3-1,fill="#111111",outline="#665500",tags="bg")
    cv.create_rectangle(xm-3,y1+2,xm+2,y1+SZ//3-2,fill="#0033cc",outline="",tags="bg")
    cv.create_rectangle(xm+4,y1+2,xm+8,y1+8,fill="#222222",outline="#444444",tags="bg")
    cv.create_rectangle(xm+5,y1+3,xm+7,y1+5,fill="#444444",outline="",tags="bg")

def draw_belakang_kasir(cv,x1,y1,x2,y2):
    base="#1c1500"
    cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,8),tags="bg")
    cv.create_rectangle(x1+2,y1+2,x2-2,y2-2,fill="#231a00",outline="",tags="bg")

def draw_fitting(cv,x1,y1,x2,y2):
    xm=(x1+x2)//2; ym=(y1+y2)//2; base="#3d2260"
    cv.create_rectangle(x1,y1,x2,y2,fill="#2a1a44",outline=_c(base,-10),tags="bg")
    cv.create_rectangle(x1+2,y1+2,x2-2,y2-2,fill=base,outline=_c(base,15),tags="bg")
    for gx in range(x1+5,x2-2,3):
        cv.create_line(gx,y1+3,gx,y2-3,fill=_c(base,-8),width=1,tags="bg")
    cv.create_rectangle(x1+2,y1+2,x2-2,y1+5,fill=_c(base,30),outline="",tags="bg")
    cv.create_oval(x2-8,ym-2,x2-4,ym+2,fill="#c8a030",outline="",tags="bg")

def draw_bg(canvas):
    cv = canvas
    cv.create_rectangle(0,0,canvas_width,canvas_height,fill="#0d0d0d",outline="",tags="bg")
    for b in range(total_baris):
        for k in range(total_kolom):
            t  = peta_toko[b][k]
            x1=k*SZ; y1=b*SZ; x2=x1+SZ; y2=y1+SZ
            if t==0:
                base="#c8b88a" if (k+b)%2==0 else "#b8a87a"
                cv.create_rectangle(x1,y1,x2,y2,fill=base,outline=_c(base,-10),tags="bg")
                cv.create_line(x1,y1,x2,y1,fill=_c(base,-12),width=1,tags="bg")
                cv.create_line(x1,y1,x1,y2,fill=_c(base,-12),width=1,tags="bg")
            elif t==1:
                base="#2c2c3e"
                cv.create_rectangle(x1,y1,x2,y2,fill=base,outline="",tags="bg")
                cv.create_line(x1,y1,x2,y1,fill=_c(base,22),width=1,tags="bg")
                cv.create_line(x1,y1,x1,y2,fill=_c(base,22),width=1,tags="bg")
                cv.create_line(x1,y2-1,x2,y2-1,fill=_c(base,-18),width=1,tags="bg")
                cv.create_line(x2-1,y1,x2-1,y2,fill=_c(base,-18),width=1,tags="bg")
                if b%2==0:
                    xm=(x1+x2)//2
                    cv.create_line(xm,y1+2,xm,y2-2,fill=_c(base,-10),width=1,tags="bg")
            elif t==5:  draw_rack_baju(cv,x1,y1,x2,y2)
            elif t==6:  draw_rack_celana(cv,x1,y1,x2,y2)
            elif t==3:  draw_rack_jaket(cv,x1,y1,x2,y2)
            elif t==7:  draw_rack_sepatu(cv,x1,y1,x2,y2)
            elif t==8:  draw_rack_topi(cv,x1,y1,x2,y2)
            elif t==10: draw_rack_jas(cv,x1,y1,x2,y2)
            elif t==2:  draw_kasir(cv,x1,y1,x2,y2)
            elif t==11: draw_belakang_kasir(cv,x1,y1,x2,y2)
            elif t==4:  draw_fitting(cv,x1,y1,x2,y2)
            elif t==9:
                shade="#111118" if (k+b)%3==0 else "#0d0d14"
                cv.create_rectangle(x1,y1,x2,y2,fill=shade,outline="",tags="bg")

def draw_clock(canvas, sim_minutes, sim_day, day_anim_offset, get_jam_str_func, 
               get_date_str_func, get_weekday_name_func, is_store_open_func, canvas_width):
    canvas.delete("clock")
    jam_str  = get_jam_str_func()
    date_str = get_date_str_func()
    wday_str = get_weekday_name_func()
    h = sim_minutes // 60

    if 6 <= h < 9:
        clr_bg="#0d2b45"; clr_bdr="#1a6ea8"; clr_txt="#87ceeb"; clr_lbl="#5ba3d0"
    elif 9 <= h < 17:
        clr_bg="#1a2a0a"; clr_bdr="#3a7a10"; clr_txt="#a8ff40"; clr_lbl="#70cc20"
    elif 17 <= h < 20:
        clr_bg="#2a1a00"; clr_bdr="#cc6600"; clr_txt="#ffaa40"; clr_lbl="#cc8820"
    elif 20 <= h < 22:
        clr_bg="#1a0a2a"; clr_bdr="#6633aa"; clr_txt="#cc88ff"; clr_lbl="#8844cc"
    else:
        clr_bg="#0d0d18"; clr_bdr="#333355"; clr_txt="#4444aa"; clr_lbl="#222244"

    status_txt = "OPEN" if is_store_open_func() else "CLOSED"
    status_clr = "#00ff88" if is_store_open_func() else "#ff0000"

    d_bg  = "#0a1520"
    d_bdr = "#2a5a8a"
    d_txt = "#7ab8e8"
    d_lbl = "#3d7aaa"

    cw = WIDGET_W

    ax1, ay1 = CLOCK_X, DATE_Y
    ax2, ay2 = ax1 + cw, ay1 + 48
    canvas.create_rectangle(ax1+3,ay1+3,ax2+3,ay2+3,fill="#000000",outline="",tags="clock")
    canvas.create_rectangle(ax1,ay1,ax2,ay2,fill=d_bg,outline=d_bdr,width=2,tags="clock")
    canvas.create_line(ax1+3,ay1+1,ax2-3,ay1+1,fill=d_bdr,width=1,tags="clock")
    canvas.create_text(ax1+7,ay1+9,text="DATE",anchor="w",
                       fill=d_lbl,font=("Courier",6,"bold"),tags="clock")
    canvas.create_text(ax2-7,ay1+9,text=wday_str,anchor="e",
                       fill=d_lbl,font=("Courier",6,"bold"),tags="clock")
    canvas.create_text((ax1+ax2)//2, ay1+28, text=date_str,
                       fill=d_txt, font=("Courier",13,"bold"), tags="clock")
    canvas.create_line(ax1+5,ay2-5,ax2-5,ay2-5,fill=d_bdr,width=1,tags="clock")

    cx1, cy1 = CLOCK_X, CLOCK_Y
    cx2, cy2 = cx1 + cw, cy1 + 52
    canvas.create_rectangle(cx1+3,cy1+3,cx2+3,cy2+3,fill="#000000",outline="",tags="clock")
    canvas.create_rectangle(cx1,cy1,cx2,cy2,fill=clr_bg,outline=clr_bdr,width=2,tags="clock")
    canvas.create_line(cx1+3,cy1+1,cx2-3,cy1+1,fill=clr_bdr,width=1,tags="clock")
    canvas.create_text(cx1+7,cy1+10,text="TIME",anchor="w",
                       fill=clr_lbl,font=("Courier",7,"bold"),tags="clock")
    canvas.create_text(cx2-7,cy1+10,text=status_txt,anchor="e",
                       fill=status_clr,font=("Courier",7,"bold"),tags="clock")
    canvas.create_text(cx1+cw//2-10,cy1+30,text=jam_str,
                       fill=clr_txt,font=("Courier",20,"bold"),tags="clock")
    canvas.create_line(cx1+5,cy2-6,cx2-5,cy2-6,fill=clr_bdr,width=1,tags="clock")

    if sim_day >= 1:
        dw = 72
        ddx1 = cx2 + 4 + day_anim_offset
        ddx2 = ddx1 + dw
        ddy1, ddy2 = cy1, cy2
        db_bg="#1a1000"; db_bdr="#c8880a"; db_txt="#ffd060"; db_lbl="#a86a08"
        if ddx1 < canvas_width + 10:
            canvas.create_rectangle(ddx1+3,ddy1+3,ddx2+3,ddy2+3,fill="#000000",outline="",tags="clock")
            canvas.create_rectangle(ddx1,ddy1,ddx2,ddy2,fill=db_bg,outline=db_bdr,width=2,tags="clock")
            canvas.create_rectangle(cx2-1,cy1+10,ddx1+2,cy2-10,fill=db_bg,outline="",tags="clock")
            canvas.create_line(cx2,cy1+10,ddx1+1,cy1+10,fill=db_bdr,width=1,tags="clock")
            canvas.create_line(cx2,cy2-10,ddx1+1,cy2-10,fill=db_bdr,width=1,tags="clock")
            canvas.create_line(ddx1+3,ddy1+1,ddx2-3,ddy1+1,fill=db_bdr,width=1,tags="clock")
            canvas.create_text(ddx1+7,ddy1+10,text="DAY",anchor="w",
                               fill=db_lbl,font=("Courier",7,"bold"),tags="clock")
            canvas.create_text(ddx1+dw//2,ddy1+30,text=str(sim_day),
                               fill=db_txt,font=("Courier",20,"bold"),tags="clock")
            sx,sy = ddx2-8,ddy1+8
            canvas.create_polygon(sx,sy-4,sx+2,sy-1,sx+5,sy-1,sx+3,sy+1,sx+4,sy+4,
                                   sx,sy+2,sx-4,sy+4,sx-3,sy+1,sx-5,sy-1,sx-2,sy-1,
                                   fill=db_bdr,outline="",tags="clock")
            canvas.create_line(ddx1+5,ddy2-6,ddx2-5,ddy2-6,fill=db_bdr,width=1,tags="clock")

def draw_npcs(canvas, daftar_npc_aktif, kasir_npc_1, kasir_npc_2, draw_clock_func, SZ):
    canvas.delete("npc")
    if kasir_npc_1.aktif and kasir_npc_1.state != SK_DONE:
        cx=kasir_npc_1.kolom*SZ+SZ//2; cy=kasir_npc_1.baris*SZ+SZ//2; r=9
        canvas.create_oval(cx-r+2,cy-r+2,cx+r+2,cy+r+2,fill="#000000",outline="",tags="npc")
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="#FFD700",outline="#FFF8DC",width=2,tags="npc")
        canvas.create_text(cx,cy,text="C1",fill="#1a0d00",font=("Arial",7,"bold"),tags="npc")
    if kasir_npc_2.aktif and kasir_npc_2.state != SK_DONE:
        cx=kasir_npc_2.kolom*SZ+SZ//2; cy=kasir_npc_2.baris*SZ+SZ//2; r=9
        canvas.create_oval(cx-r+2,cy-r+2,cx+r+2,cy+r+2,fill="#000000",outline="",tags="npc")
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="#FFB830",outline="#FFF8DC",width=2,tags="npc")
        canvas.create_text(cx,cy,text="C2",fill="#1a0d00",font=("Arial",7,"bold"),tags="npc")
    for npc in daftar_npc_aktif:
        if npc.state == S_DONE: continue
        cx=npc.kolom*SZ+SZ//2; cy=npc.baris*SZ+SZ//2; r=8
        canvas.create_oval(cx-r+1,cy-r+1,cx+r+1,cy+r+1,fill="#000000",outline="",tags="npc")
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=npc.warna,outline="white",width=1,tags="npc")
        canvas.create_text(cx,cy,text=f"{npc.id%100:02d}",fill="white",font=("Arial",7,"bold"),tags="npc")
    draw_clock_func()