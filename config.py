import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

WIN_W, WIN_H = 1300, 860

peta_toko = [
    [9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,9,9,9],
    [9,9,9,1,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,1,0,0,0,0,0,0,0,0,1,9,9,9],
    [9,9,9,1,0,10,10,0,0,10,10,0,10,10,0,0,0,0,0,1,0,0,7,7,0,7,7,0,1,9,9,9],
    [9,9,9,1,0,10,10,0,0,5,5,0,5,5,0,0,0,0,0,1,0,0,7,7,0,7,7,0,1,9,9,9],
    [9,9,9,1,0,10,10,0,0,0,0,0,0,0,0,5,5,5,0,1,0,0,7,7,0,7,7,0,1,9,9,9],
    [9,9,9,1,0,10,10,0,0,0,0,0,0,0,0,5,5,5,0,0,0,0,0,0,0,0,0,0,1,9,9,9],
    [9,9,9,1,0,0,0,0,0,8,8,8,8,8,0,5,5,5,0,0,0,6,6,0,0,7,7,0,1,9,9,9],
    [9,9,9,1,1,1,1,0,0,8,1,1,1,8,0,0,0,0,0,0,0,6,6,0,0,6,6,0,1,9,9,9],
    [9,9,9,1,0,0,0,0,0,0,0,0,1,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,9,9],
    [9,9,9,1,0,3,3,0,0,0,5,0,1,1,4,4,4,4,4,1,7,7,7,0,0,6,6,0,1,9,9,9],
    [9,9,9,1,0,3,3,0,0,0,5,0,1,1,1,1,1,1,1,1,1,1,1,0,0,6,6,0,1,9,9,9],
    [9,9,9,1,0,3,3,0,0,0,5,0,1,10,10,10,0,7,7,0,6,6,6,0,0,6,6,0,1,9,9,9],
    [9,9,9,1,0,0,0,0,0,0,5,0,10,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,9,9],
    [9,9,9,1,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,0,1,9,9,9],
    [9,9,9,1,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,8,8,3,3,0,0,6,6,0,1,9,9,9],
    [9,9,9,1,0,3,3,0,0,2,2,2,2,0,0,0,0,0,0,8,8,3,3,0,0,6,6,0,1,9,9,9],
    [9,9,9,1,0,0,0,0,0,0,11,11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,9,9],
    [9,9,9,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,9,9,9],
    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
    [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
]

SZ           = 26
total_kolom  = len(peta_toko[0])
total_baris  = len(peta_toko)
canvas_width = total_kolom * SZ
canvas_height= total_baris * SZ



KASIR_QUEUE_SLOTS = [(14, 10), (14, 11), (14, 12), (14, 13)]

SIM_MS_PER_MIN = 250
DAYS_IN_MONTH = [0,31,28,31,30,31,30,31,31,30,31,30,31]
DAY_NAMES = ["MON","TUE","WED","THU","FRI","SAT","SUN"]




SPEED_LEVELS = [1, 2, 4, 8]
SPEED_LABELS = ["1×", "2×", "4×", "8×"]
SPEED_COLORS = ["#1a6a1a", "#c88800", "#cc4400", "#cc0000"]
SPEED_HOVER  = ["#22882a", "#ddaa00", "#ee5500", "#ff1111"]


CLOCK_X = 10
DATE_Y  = canvas_height - 122
CLOCK_Y = canvas_height - 62
WIDGET_W = 110


DAY_ANIM_TOTAL  = 12
DAY_ANIM_START  = 80


S_MASUK   = "WALK IN"
S_JALAN   = "BROWSING"
S_KE_RAK  = "GOING TO RACK"
S_DI_RAK  = "PICKING ITEM"
S_TGU_FIT = "WAITING FITTING"
S_KE_FIT  = "GOING TO FITTING"
S_DI_FIT  = "IN FITTING ROOM"
S_KE_KAS  = "GOING TO CASHIER"
S_DI_KAS  = "PAYING"
S_KELUAR  = "LEAVING"
S_BATAL   = "CANCELLING"
S_FORCED  = "CLOSING TIME"
S_DONE    = "DONE"

SK_DATANG  = "ARRIVING"
SK_STANDBY = "ON DUTY"
SK_PULANG  = "GOING HOME"
SK_DONE    = "OFF DUTY"


WARNA_FEMALE = "#FF69B4"
WARNA_MALE   = "#1E90FF"
WARNA_BATAL  = "#FF4444"
WARNA_FORCED = "#FF8800"

ITEM_CATALOGUE = {
    "Old Navy":         ("Pants / Jeans", 7),
    "Gap":              ("Pants / Jeans", 9),
    "Lee":              ("Pants / Jeans", 8),
    "Wrangler":         ("Pants / Jeans", 8),
    "American Eagle":   ("Pants / Jeans", 10),
    "Dockers":          ("Pants / Jeans", 9),
    "Dickies":          ("Pants / Jeans", 10),
    "Levi's (Vintage)": ("Pants / Jeans", 25),
    "Lucky Brand":      ("Pants / Jeans", 20),
    "True Religion":    ("Pants / Jeans", 35),
    "Madewell":         ("Pants / Jeans", 22),
    "Silver Jeans":     ("Pants / Jeans", 18),
    "Nike":             ("Caps / Hats", 4),
    "Adidas":           ("Caps / Hats", 4),
    "New Era":          ("Caps / Hats", 6),
    "Under Armour":     ("Caps / Hats", 5),
    "Hurley":           ("Caps / Hats", 5),
    "Quiksilver":       ("Caps / Hats", 5),
    "Starter":          ("Caps / Hats", 12),
    "Patagonia (Hat)":  ("Caps / Hats", 15),
    "Carhartt (Hat)":   ("Caps / Hats", 15),
    "Mitchell & Ness":  ("Caps / Hats", 18),
    "Brixton":          ("Caps / Hats", 12),
    "Skechers":         ("Shoes", 8),
    "Vans":             ("Shoes", 12),
    "Converse":         ("Shoes", 12),
    "Reebok":           ("Shoes", 10),
    "Puma":             ("Shoes", 10),
    "Keds":             ("Shoes", 8),
    "Nike (Vintage)":   ("Shoes", 35),
    "New Balance":      ("Shoes", 25),
    "Dr. Martens":      ("Shoes", 45),
    "Birkenstock":      ("Shoes", 40),
    "Timberland":       ("Shoes", 40),
    "Sperry":           ("Shoes", 20),
    "Columbia":         ("Jackets", 15),
    "Eddie Bauer":      ("Jackets", 15),
    "London Fog":       ("Jackets", 18),
    "L.L. Bean":        ("Jackets", 20),
    "H&M":              ("Jackets", 10),
    "The North Face":   ("Jackets", 45),
    "Patagonia":        ("Jackets", 50),
    "Arc'teryx":        ("Jackets", 60),
    "Filson":           ("Jackets", 70),
    "Pendleton":        ("Jackets", 40),
    "Barbour":          ("Jackets", 55),
    "Carhartt":         ("Jackets", 40),
    "Haggar":           ("Suits / Formal", 15),
    "Stafford":         ("Suits / Formal", 15),
    "Jones New York":   ("Suits / Formal", 20),
    "Liz Claiborne":    ("Suits / Formal", 20),
    "Calvin Klein":     ("Suits / Formal", 25),
    "Brooks Brothers":  ("Suits / Formal", 60),
    "Banana Republic":  ("Suits / Formal", 40),
    "J.Crew":           ("Suits / Formal", 45),
    "Ann Taylor":       ("Suits / Formal", 30),
    "Tahari":           ("Suits / Formal", 35),
    "Perry Ellis":      ("Suits / Formal", 25),
    "Gildan":               ("T-Shirts", 3),
    "Hanes":                ("T-Shirts", 3),
    "Fruit of the Loom":    ("T-Shirts", 3),
    "Champion":             ("T-Shirts", 5),
    "Hollister":            ("T-Shirts", 5),
    "Stüssy":               ("T-Shirts", 20),
    "Nautica":              ("T-Shirts", 8),
    "Ralph Lauren":         ("T-Shirts", 12),
    "Abercrombie & Fitch":  ("T-Shirts", 8),
    "Vintage Band/Event":   ("T-Shirts", 15),
}

ITEMS_BY_RACK = {
    "👗 Shirts":  [k for k,v in ITEM_CATALOGUE.items() if v[0]=="T-Shirts"],
    "👖 Pants":   [k for k,v in ITEM_CATALOGUE.items() if v[0]=="Pants / Jeans"],
    "🧥 Jackets": [k for k,v in ITEM_CATALOGUE.items() if v[0]=="Jackets"],
    "👞 Shoes":   [k for k,v in ITEM_CATALOGUE.items() if v[0]=="Shoes"],
    "🧢 Hats":    [k for k,v in ITEM_CATALOGUE.items() if v[0]=="Caps / Hats"],
    "🤵 Suits":   [k for k,v in ITEM_CATALOGUE.items() if v[0]=="Suits / Formal"],
}

music_playing = True
music_file = "./song/themesong.mp3"
