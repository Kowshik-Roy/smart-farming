
import tkinter as tk
from tkinter import messagebox, Toplevel, Text, Scrollbar, BOTH
import requests
import sqlite3
import json
from datetime import datetime
from PIL import Image, ImageTk
from tkcalendar import Calendar
from database import init_db, load_json_to_db
import os

# ============ নতুন ফিচার মডিউল ইম্পোর্ট করুন ============
try:
    from feature_1_production_tracking import open_production_tracker_window
    from feature_2_farmer_profile import open_farmer_profile_window
    from feature_3_land_mapping import open_land_mapping_window
    from feature_4_fertilizer_calculator import open_fertilizer_calculator_window
    from feature_5_machinery_rental import open_machinery_rental_window
    from feature_6_seeds_equipment import open_seeds_equipment_window
    from feature_7_loan_checker import open_loan_eligibility_window
    from feature_8_crop_rotation import open_crop_rotation_window
    from feature_9_video_library import open_video_library_window
    from feature_10_report_export import open_report_export_window
except ImportError as e:
    print(f"⚠️ কিছু ফিচার ইম্পোর্ট ব্যর্থ হয়েছে: {e}")

# ---------------- ডাটাবেস ইনিশিয়ালাইজেশন ----------------
try:
    init_db()
    load_json_to_db("crop_data.json")
except Exception as e:
    print(f"ডাটাবেস ইরর: {e}")

# ---------------- GUI সেটআপ ----------------
root = tk.Tk()
root.title("🌾 স্মার্ট কৃষি পরিকল্পনা")
root.geometry("700x900")   # স্টার্টে একটু বড় উইন্ডো
root.resizable(True, True) # ইউজার চাইলে উইন্ডো রিসাইজ করতে পারবে
root.config(bg="#e8f5e9")

# টাইটেল বার বোতাম ইন-অ্যাপ (যদি আপনার সিস্টেমের নিজস্ব বোতন দৃশ্যমান না হয়)
control_frame = tk.Frame(root, bg="#e8f5e9")
control_frame.place(relx=1.0, y=0, anchor='ne')

tk.Button(control_frame, text="🗕", font=("Arial", 10), width=3, pady=1, command=lambda: root.iconify(), bg="#f4f4f4").pack(side="left")
tk.Button(control_frame, text="🗖", font=("Arial", 10), width=3, pady=1, command=lambda: root.state('zoomed') if root.state()!='zoomed' else root.state('normal'), bg="#f4f4f4").pack(side="left")
tk.Button(control_frame, text="✕", font=("Arial", 10), width=3, pady=1, command=root.destroy, bg="#f44336", fg="white").pack(side="left")

# Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 500) // 2
y = (screen_height - 900) // 2  # উচ্চতা বৃদ্ধি করা হয়েছে
root.geometry(f"500x900+{x}+{y}")

# ============ Scrollable Canvas সেটআপ ============
from tkinter import Canvas, Scrollbar

main_frame = tk.Frame(root, bg="#e8f5e9")
main_frame.pack(fill="both", expand=True)

canvas = Canvas(main_frame, bg="#e8f5e9", highlightthickness=0)
scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#e8f5e9")

window_item = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# ensure scrollable_frame always fills canvas width (responsive center/alignment)
def _on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", _on_frame_configure)

# adjust the frame width dynamically as the canvas is resized

def _on_canvas_configure(event):
    canvas.itemconfigure(window_item, width=event.width)

canvas.bind("<Configure>", _on_canvas_configure)

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# মাউস স্ক্রল সাপোর্ট
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root.bind_all("<MouseWheel>", _on_mousewheel)

# ============ সমস্ত উইজেট এখন scrollable_frame এ থাকবে ============

# সুবিধার জন্য একটি alias
app = scrollable_frame

# ভেরিয়েবল
division = tk.StringVar()
district = tk.StringVar()
soil_type = tk.StringVar()
season = tk.StringVar()
search_text = tk.StringVar()
result = tk.StringVar()
weather_result = tk.StringVar()

# বিভাগ অনুযায়ী জেলা
districts_by_division = {
    "ঢাকা": ["ঢাকা", "গাজীপুর", "নারায়ণগঞ্জ"],
    "চট্টগ্রাম": ["চট্টগ্রাম", "কক্সবাজার", "কুমিল্লা"],
    "রাজশাহী": ["রাজশাহী", "বগুড়া", "পাবনা"],
    "খুলনা": ["খুলনা", "যশোর", "বাগেরহাট"],
    "বরিশাল": ["বরিশাল", "ভোলা", "পটুয়াখালী"],
    "সিলেট": ["সিলেট", "মৌলভীবাজার", "হবিগঞ্জ"],
    "রংপুর": ["রংপুর", "দিনাজপুর", "কুড়িগ্রাম"],
    "ময়মনসিংহ": ["ময়মনসিংহ", "নেত্রকোণা", "শেরপুর"]
}

# মাটির ধরনের অপশন
soil_options = [
    "দোআঁশ",
    "বেলে দোআঁশ", 
    "পলি দোআঁশ",
    "এঁটেল",
    "বেলে",
    "পলি",
    "লাল",
    "কালো"
]

# মৌসুমের অপশন
season_options = [
    "রবি",
    "খরিফ-১",
    "খরিফ-২",
    "বোরো",
    "আমন",
    "আউশ",
    "গ্রীষ্ম",
    "বর্ষা"
]

# ---------------- নতুন ৭টি ফিচারের ফাংশন ----------------

def show_detailed_weather():
    weather_win = Toplevel(root)
    weather_win.title("বিস্তারিত আবহাওয়া")
    weather_win.geometry("500x600")
    weather_win.config(bg="#e3f2fd")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 500) // 2
    y = (screen_height - 600) // 2
    weather_win.geometry(f"500x600+{x}+{y}")
    
    city = district.get() or "ঢাকা"
    
    # Header
    header_frame = tk.Frame(weather_win, bg="#e3f2fd")
    header_frame.pack(fill="x", padx=20, pady=15)
    
    tk.Label(header_frame, text=f"🌤️ {city} - আবহাওয়া", 
            font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#1565c0").pack()
    
    # Current Date
    current_date = datetime.now().strftime("%d %B, %Y")
    tk.Label(header_frame, text=f"📅 {current_date}", 
            font=("Arial", 12), bg="#e3f2fd").pack()

    # Sample Weather Data (বাংলাদেশের বিভিন্ন শহরের জন্য)
    weather_data = {
        "ঢাকা": {
            "current": {"temp": 28, "condition": "হালকা মেঘলা", "humidity": 65, "wind": 12},
            "forecast": [
                {"day": "আজ", "high": 30, "low": 25, "condition": "হালকা মেঘলা", "rain": "২০%"},
                {"day": "আগামীকাল", "high": 31, "low": 26, "condition": "রৌদ্রোজ্জ্বল", "rain": "১০%"},
                {"day": "পরশু", "high": 29, "low": 24, "condition": "বৃষ্টির সম্ভাবনা", "rain": "৬০%"}
            ]
        },
        "চট্টগ্রাম": {
            "current": {"temp": 26, "condition": "আদ্র", "humidity": 75, "wind": 15},
            "forecast": [
                {"day": "আজ", "high": 28, "low": 24, "condition": "আদ্র", "rain": "৩০%"},
                {"day": "আগামীকাল", "high": 27, "low": 23, "condition": "হালকা বৃষ্টি", "rain": "৭০%"},
                {"day": "পরশু", "high": 29, "low": 25, "condition": "মেঘলা", "rain": "৪০%"}
            ]
        },
        "রাজশাহী": {
            "current": {"temp": 32, "condition": "রৌদ্রোজ্জ্বল", "humidity": 55, "wind": 10},
            "forecast": [
                {"day": "আজ", "high": 34, "low": 28, "condition": "রৌদ্রোজ্জ্বল", "rain": "৫%"},
                {"day": "আগামীকাল", "high": 33, "low": 27, "condition": "হালকা মেঘলা", "rain": "১৫%"},
                {"day": "পরশু", "high": 35, "low": 29, "condition": "রৌদ্রোজ্জ্বল", "rain": "০%"}
            ]
        },
        "খুলনা": {
            "current": {"temp": 29, "condition": "মেঘলা", "humidity": 70, "wind": 14},
            "forecast": [
                {"day": "আজ", "high": 31, "low": 26, "condition": "মেঘলা", "rain": "৪০%"},
                {"day": "আগামীকাল", "high": 30, "low": 25, "condition": "বৃষ্টি", "rain": "৮০%"},
                {"day": "পরশু", "high": 32, "low": 27, "condition": "হালকা মেঘলা", "rain": "২৫%"}
            ]
        },
        "সিলেট": {
            "current": {"temp": 25, "condition": "হালকা বৃষ্টি", "humidity": 80, "wind": 8},
            "forecast": [
                {"day": "আজ", "high": 27, "low": 23, "condition": "হালকা বৃষ্টি", "rain": "৭০%"},
                {"day": "আগামীকাল", "high": 26, "low": 22, "condition": "বৃষ্টি", "rain": "৯০%"},
                {"day": "পরশু", "high": 28, "low": 24, "condition": "মেঘলা", "rain": "৫০%"}
            ]
        }
    }
    
    # Get data for selected city or default to Dhaka
    city_weather = weather_data.get(city, weather_data["ঢাকা"])
    current = city_weather["current"]
    forecast = city_weather["forecast"]

    # Current Weather Card
    current_frame = tk.Frame(weather_win, relief="solid", borderwidth=2, bg="white", bd=1)
    current_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Label(current_frame, text="📊 বর্তমান আবহাওয়া", 
            font=("Arial", 14, "bold"), bg="white").pack(pady=10)
    
    # Current weather details in grid
    details_frame = tk.Frame(current_frame, bg="white")
    details_frame.pack(pady=10)
    
    # Row 1
    tk.Label(details_frame, text=f"🌡️ তাপমাত্রা: {current['temp']}°C", 
            font=("Arial", 12, "bold"), bg="white", fg="#d32f2f").grid(row=0, column=0, sticky="w", padx=20, pady=5)
    tk.Label(details_frame, text=f"☁️ অবস্থা: {current['condition']}", 
            font=("Arial", 12), bg="white").grid(row=0, column=1, sticky="w", padx=20, pady=5)
    
    # Row 2
    tk.Label(details_frame, text=f"💧 আর্দ্রতা: {current['humidity']}%", 
            font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", padx=20, pady=5)
    tk.Label(details_frame, text=f"🌬️ বাতাস: {current['wind']} km/h", 
            font=("Arial", 12), bg="white").grid(row=1, column=1, sticky="w", padx=20, pady=5)

    # 3-Day Forecast
    tk.Label(weather_win, text="📅 ৩ দিনের আবহাওয়া পূর্বাভাস", 
            font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=(20, 10))
    
    for day_data in forecast:
        day_frame = tk.Frame(weather_win, relief="solid", borderwidth=1, bg="white")
        day_frame.pack(fill="x", padx=20, pady=5)
        
        # Day header
        header_frame = tk.Frame(day_frame, bg="white")
        header_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(header_frame, text=f"📅 {day_data['day']}", 
                font=("Arial", 12, "bold"), bg="white").pack(side="left")
        
        # Weather details
        details_frame = tk.Frame(day_frame, bg="white")
        details_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(details_frame, text=f"🌡️ {day_data['high']}° / {day_data['low']}°", 
                font=("Arial", 11), bg="white").pack(side="left", padx=5)
        tk.Label(details_frame, text=f"☁️ {day_data['condition']}", 
                font=("Arial", 11), bg="white").pack(side="left", padx=20)
        tk.Label(details_frame, text=f"🌧️ {day_data['rain']}", 
                font=("Arial", 11), bg="white", fg="blue").pack(side="left", padx=5)

    # Farming Advice based on weather
    advice_frame = tk.Frame(weather_win, relief="solid", borderwidth=2, bg="#e8f5e9")
    advice_frame.pack(fill="x", padx=20, pady=15)
    
    tk.Label(advice_frame, text="💡 কৃষি পরামর্শ", 
            font=("Arial", 14, "bold"), bg="#e8f5e9").pack(pady=10)
    
    # Generate advice based on current weather
    if "বৃষ্টি" in current['condition']:
        advice = """• বৃষ্টির সম্ভাবনা আছে, সেচ কম দিন
• ফসল সংগ্রহ এড়িয়ে চলুন
• জলাবদ্ধতা প্রতিরোধ করুন
• রোগ-পোকা monitoring বাড়ান"""
    elif current['temp'] > 30:
        advice = """• তাপমাত্রা বেশি, বেশি সেচ দিন
• ফসল ছায়ায় রাখুন
• সকাল-সন্ধ্যায় কাজ করুন
• পানির সংকট এড়াতে মালচিং করুন"""
    elif current['temp'] < 25:
        advice = """• ঠাণ্ডা আবহাওয়া, কম সেচ দিন
• শীতকালীন ফসলের যত্ন নিন
• ফসল cover করুন
• সার প্রয়োগ বাড়ান"""
    else:
        advice = """• আবহাওয়া অনুকূল
• নিয়মিত সেচ ও যত্ন চালিয়ে যান
• ফসলের স্বাভাবিক বৃদ্ধি পর্যবেক্ষণ করুন
• সময়মতো সার প্রয়োগ করুন"""
    
    tk.Label(advice_frame, text=advice, font=("Arial", 11), 
            bg="#e8f5e9", justify="left").pack(anchor="w", padx=20, pady=10)

    # Refresh button
    def refresh_weather():
        weather_win.destroy()
        show_detailed_weather()
    
    button_frame = tk.Frame(weather_win, bg="#e3f2fd")
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="🔄 রিফ্রেশ", command=refresh_weather,
              bg="#2196f3", fg="white", font=("Arial", 12), 
              width=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ", command=weather_win.destroy,
              bg="#f44336", fg="white", font=("Arial", 12), 
              width=15).pack(side="left", padx=5)

def show_market_price():
    price_win = Toplevel(root)
    price_win.title("ফসলের বাজার দর")
    price_win.geometry("500x400")
    price_win.config(bg="#fff3e0")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 500) // 2
    y = (screen_height - 400) // 2
    price_win.geometry(f"500x400+{x}+{y}")
    
    # Sample market data
    market_data = {
        "ধান": {"price": "২৮-৩২ টাকা/কেজি", "trend": "স্থিতিশীল"},
        "গম": {"price": "৩০-৩৫ টাকা/কেজি", "trend": "বৃদ্ধি"},
        "আলু": {"price": "২০-২৫ টাকা/কেজি", "trend": "হ্রাস"},
        "টমেটো": {"price": "৪০-৬০ টাকা/কেজি", "trend": "অস্থিতিশীল"},
        "পেঁয়াজ": {"price": "৫০-৭০ টাকা/কেজি", "trend": "বৃদ্ধি"},
        "বেগুন": {"price": "৩০-৪০ টাকা/কেজি", "trend": "স্থিতিশীল"},
        "মরিচ": {"price": "৮০-১২০ টাকা/কেজি", "trend": "বৃদ্ধি"}
    }
    
    tk.Label(price_win, text="📈 আজকের বাজার দর", font=("Arial", 16, "bold"), bg="#fff3e0").pack(pady=10)
    
    for crop, info in market_data.items():
        frame = tk.Frame(price_win, relief="ridge", borderwidth=1, bg="white")
        frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame, text=f"🌾 {crop}", font=("Arial", 12, "bold"), bg="white", width=15).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(frame, text=f"💰 {info['price']}", font=("Arial", 11), bg="white").grid(row=0, column=1, sticky="w", padx=5)
        
        trend_icon = "📈" if info['trend'] == "বৃদ্ধি" else "📉" if info['trend'] == "হ্রাস" else "➡️"
        trend_color = "green" if info['trend'] == "বৃদ্ধি" else "red" if info['trend'] == "হ্রাস" else "blue"
        tk.Label(frame, text=f"{trend_icon} {info['trend']}", 
                fg=trend_color, bg="white").grid(row=0, column=2, sticky="w", padx=5)

def show_nearby_offices():
    office_win = Toplevel(root)
    office_win.title("নিকটবর্তী কৃষি অফিস")
    office_win.geometry("500x400")
    office_win.config(bg="#f3e5f5")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 500) // 2
    y = (screen_height - 400) // 2
    office_win.geometry(f"500x400+{x}+{y}")
    
    offices = {
        "ঢাকা": [
            {"name": "কৃষি সম্প্রসারণ অধিদপ্তর, ঢাকা", "phone": "০২-৯৫৫০০১১", "address": "কৃষি মন্ত্রণালয়, ঢাকা"},
            {"name": "বাংলাদেশ কৃষি গবেষণা ইনস্টিটিউট", "phone": "০২-৫৫০১৪৪৪১", "address": "জয়দেবপুর, গাজীপুর"},
            {"name": "বিএডিসি অফিস, ঢাকা", "phone": "০২-৫৫০১২৪৪১", "address": "কাওরান বাজার, ঢাকা"}
        ],
        "চট্টগ্রাম": [
            {"name": "কৃষি অফিস, চট্টগ্রাম", "phone": "০৩১-৬৩৩৩৩", "address": "আগ্রাবাদ, চট্টগ্রাম"},
            {"name": "চট্টগ্রাম কৃষি বিশ্ববিদ্যালয়", "phone": "০৩১-৬৫৯০৯০", "address": "হাটহাজারী, চট্টগ্রাম"}
        ],
        "রাজশাহী": [
            {"name": "কৃষি অফিস, রাজশাহী", "phone": "০৭২১-৭৭৬৬৬", "address": "বোয়ালিয়া, রাজশাহী"},
            {"name": "বোরো গবেষণা কেন্দ্র", "phone": "০৭২১-৭৭১০০", "address": "ঈশ্বরদী, পাবনা"}
        ],
        "খুলনা": [
            {"name": "কৃষি অফিস, খুলনা", "phone": "০৪১-৭২১১১", "address": "খান জাহান আলী, খুলনা"},
            {"name": "লবণাক্ততা গবেষণা কেন্দ্র", "phone": "০৪১-৭৬০০০", "address": "খুলনা"}
        ]
    }
    
    selected_division = division.get() or "ঢাকা"
    
    tk.Label(office_win, text=f"🏢 {selected_division} - কৃষি অফিস", 
            font=("Arial", 16, "bold"), bg="#f3e5f5").pack(pady=10)
    
    if selected_division in offices:
        for office in offices[selected_division]:
            frame = tk.Frame(office_win, relief="solid", borderwidth=1, bg="white")
            frame.pack(fill="x", padx=20, pady=5)
            
            tk.Label(frame, text=f"📍 {office['name']}", font=("Arial", 11, "bold"), bg="white").pack(anchor="w", padx=5)
            tk.Label(frame, text=f"📞 {office['phone']}", fg="blue", bg="white").pack(anchor="w", padx=5)
            tk.Label(frame, text=f"🏠 {office['address']}", bg="white").pack(anchor="w", padx=5)
    else:
        tk.Label(office_win, text="এই বিভাগের তথ্য পাওয়া যায়নি", bg="#f3e5f5").pack(pady=20)

def profit_calculator():
    calc_win = Toplevel(root)
    calc_win.title("লাভ-লোকসান ক্যালকুলেটর")
    calc_win.geometry("400x500")
    calc_win.config(bg="#e8f5e9")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 400) // 2
    y = (screen_height - 500) // 2
    calc_win.geometry(f"400x500+{x}+{y}")
    
    tk.Label(calc_win, text="💰 লাভ-লোকসান ক্যালকুলেটর", 
            font=("Arial", 16, "bold"), bg="#e8f5e9").pack(pady=10)
    
    # Input fields
    tk.Label(calc_win, text="ফসলের নাম:", bg="#e8f5e9").pack(pady=5)
    crop_name = tk.Entry(calc_win, width=30)
    crop_name.pack(pady=5)
    
    tk.Label(calc_win, text="জমির পরিমাণ (একর):", bg="#e8f5e9").pack(pady=5)
    land_area = tk.Entry(calc_win, width=30)
    land_area.pack(pady=5)
    
    tk.Label(calc_win, text="উৎপাদন খরচ (টাকা):", bg="#e8f5e9").pack(pady=5)
    production_cost = tk.Entry(calc_win, width=30)
    production_cost.pack(pady=5)
    
    tk.Label(calc_win, text="আনুমানিক উৎপাদন (কেজি):", bg="#e8f5e9").pack(pady=5)
    expected_yield = tk.Entry(calc_win, width=30)
    expected_yield.pack(pady=5)
    
    tk.Label(calc_win, text="বাজার মূল্য (টাকা/কেজি):", bg="#e8f5e9").pack(pady=5)
    market_price = tk.Entry(calc_win, width=30)
    market_price.pack(pady=5)
    
    result_label = tk.Label(calc_win, text="", font=("Arial", 11), fg="blue", bg="#e8f5e9")
    result_label.pack(pady=10)
    
    def calculate_profit():
        try:
            area = float(land_area.get())
            cost = float(production_cost.get())
            yield_kg = float(expected_yield.get())
            price = float(market_price.get())
            
            total_income = yield_kg * price
            net_profit = total_income - cost
            profit_per_acre = net_profit / area if area > 0 else 0
            
            result_text = f"""
📊 গণনা ফলাফল:
------------------------
মোট আয়: {total_income:,.2f} টাকা
মোট খরচ: {cost:,.2f} টাকা
নিট লাভ: {net_profit:,.2f} টাকা
প্রতি একরে লাভ: {profit_per_acre:,.2f} টাকা
------------------------
"""
            result_label.config(text=result_text)
            
        except ValueError:
            messagebox.showerror("ইরর", "দয়া করে সঠিক সংখ্যা লিখুন")
    
    tk.Button(calc_win, text="🧮 গণনা করুন", command=calculate_profit, 
              bg="#4caf50", fg="white", font=("Arial", 12)).pack(pady=10)

def farmer_forum():
    forum_win = Toplevel(root)
    forum_win.title("কৃষক কমিউনিটি")
    forum_win.geometry("600x500")
    forum_win.config(bg="#f1f8e9")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 600) // 2
    y = (screen_height - 500) // 2
    forum_win.geometry(f"600x500+{x}+{y}")
    
    tk.Label(forum_win, text="👥 কৃষক কমিউনিটি ফোরাম", 
            font=("Arial", 16, "bold"), bg="#f1f8e9").pack(pady=10)
    
    # Forum posts (sample data)
    posts = [
        {"user": "রফিকুল ইসলাম", "question": "ধানের পাতা পোড়া রোগের সমাধান কী?", "answers": 5, "time": "২ ঘন্টা আগে"},
        {"user": "আনোয়ার হোসেন", "question": "গমের উন্নত জাত সম্পর্কে জানতে চাই", "answers": 3, "time": "৫ ঘন্টা আগে"},
        {"user": "সালমা বেগম", "question": "কীভাবে জৈব সার তৈরি করব?", "answers": 8, "time": "১ দিন আগে"},
        {"user": "জাহাঙ্গীর আলম", "question": "আলুর ডগা পচা রোগের চিকিৎসা?", "answers": 2, "time": "২ দিন আগে"}
    ]
    
    for post in posts:
        frame = tk.Frame(forum_win, relief="solid", borderwidth=1, bg="white")
        frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame, text=f"👤 {post['user']}", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", padx=5)
        tk.Label(frame, text=f"❓ {post['question']}", wraplength=500, bg="white").pack(anchor="w", padx=5)
        tk.Label(frame, text=f"💬 {post['answers']}টি উত্তর | ⏰ {post['time']}", 
                fg="green", bg="white").pack(anchor="w", padx=5)

def government_schemes():
    scheme_win = Toplevel(root)
    scheme_win.title("সরকারি সুযোগ-সুবিধা")
    scheme_win.geometry("500x400")
    scheme_win.config(bg="#e8eaf6")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 500) // 2
    y = (screen_height - 400) // 2
    scheme_win.geometry(f"500x400+{x}+{y}")
    
    schemes = [
        {"name": "কৃষি উপকরণ সহায়তা", "details": "সার, বীজ, কীটনাশক সহায়তা", "contact": "কৃষি সম্প্রসারণ অধিদপ্তর"},
        {"name": "ফসল বীমা", "details": "প্রাকৃতিক দুর্যোগে ফসল বীমা", "contact": "সদর দপ্তর, ঢাকা"},
        {"name": "কৃষি ঋণ", "details": "সুবিধাজনক হারেও কৃষি ঋণ", "contact": "বাংলাদেশ ব্যাংক"},
        {"name": "ই-কৃষি সেবা", "details": "মোবাইল অ্যাপের মাধ্যমে কৃষি পরামর্শ", "contact": "৩৩৩১ নম্বরে কল করুন"}
    ]
    
    tk.Label(scheme_win, text="🏛️ সরকারি সুযোগ-সুবিধা", 
            font=("Arial", 16, "bold"), bg="#e8eaf6").pack(pady=10)
    
    for scheme in schemes:
        frame = tk.Frame(scheme_win, relief="ridge", borderwidth=1, bg="white")
        frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame, text=f"✅ {scheme['name']}", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=5)
        tk.Label(frame, text=f"📋 {scheme['details']}", bg="white").pack(anchor="w", padx=5)
        tk.Label(frame, text=f"📞 {scheme['contact']}", fg="blue", bg="white").pack(anchor="w", padx=5)

def disease_diagnosis():
    disease_win = Toplevel(root)
    disease_win.title("ফসলের রোগ-বালাই")
    disease_win.geometry("500x400")
    disease_win.config(bg="#ffebee")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 500) // 2
    y = (screen_height - 400) // 2
    disease_win.geometry(f"500x400+{x}+{y}")
    
    diseases = {
        "ধান": ["ব্লাস্ট রোগ", "টুংরো রোগ", "বাদামি দাগ রোগ", "খোলপচা রোগ"],
        "গম": ["রাস্ট রোগ", "কালো দাগ রোগ", "পাউডারি মিলডিউ"], 
        "আলু": ["লেট ব্লাইট রোগ", "আর্লি ব্লাইট রোগ", "স্ক্যাব রোগ"],
        "টমেটো": ["মোজাইক ভাইরাস", "পাতা কুঞ্চন রোগ", "ব্যাকটেরিয়াল উইল্ট"]
    }
    
    tk.Label(disease_win, text="🩺 ফসলের রোগ-বালাই", 
            font=("Arial", 16, "bold"), bg="#ffebee").pack(pady=10)
    
    for crop, disease_list in diseases.items():
        frame = tk.Frame(disease_win, relief="solid", borderwidth=1, bg="white")
        frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame, text=f"🌾 {crop}", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=5)
        
        for disease in disease_list:
            tk.Label(frame, text=f"⚠️ {disease}", bg="white").pack(anchor="w", padx=20)

# ---------------- মূল ফাংশনসমূহ ----------------

def update_districts(*args):
    selected_div = division.get()
    district_list = districts_by_division.get(selected_div, [])
    menu = district_option["menu"]
    menu.delete(0, "end")
    for dist in district_list:
        menu.add_command(label=dist, command=lambda d=dist: district.set(d))
    if district_list:
        district.set(district_list[0])

def update_soils(*args):
    selected_div = division.get()
    selected_dist = district.get()
    
    # বিভিন্ন এলাকার জন্য উপযুক্ত মাটির ধরন সাজেশন
    if selected_div == "ঢাকা":
        soil_suggestions = ["দোআঁশ", "এঁটেল", "পলি দোআঁশ"]
    elif selected_div == "রাজশাহী":
        soil_suggestions = ["বেলে দোআঁশ", "লাল", "দোআঁশ"]
    elif selected_div == "খুলনা":
        soil_suggestions = ["পলি", "এঁটেল", "দোআঁশ"]
    elif selected_div == "সিলেট":
        soil_suggestions = ["এঁটেল", "পলি", "দোআঁশ"]
    else:
        soil_suggestions = soil_options
    
    menu = soil_option["menu"]
    menu.delete(0, "end")
    for soil in soil_suggestions:
        menu.add_command(label=soil, command=lambda s=soil: soil_type.set(s))
    if soil_suggestions:
        soil_type.set(soil_suggestions[0])

def update_seasons(*args):
    current_month = datetime.now().month
    
    # মাস অনুযায়ী মৌসুম সাজেশন
    if current_month in [11, 12, 1, 2]:
        season_suggestions = ["রবি", "বোরো"]
    elif current_month in [3, 4, 5]:
        season_suggestions = ["খরিফ-১", "আউশ"]
    elif current_month in [6, 7, 8]:
        season_suggestions = ["খরিফ-২", "আমন", "বর্ষা"]
    else:  # 9, 10
        season_suggestions = ["আমন", "খরিফ-২"]
    
    menu = season_option["menu"]
    menu.delete(0, "end")
    for seas in season_suggestions:
        menu.add_command(label=seas, command=lambda s=seas: season.set(s))
    if season_suggestions:
        season.set(season_suggestions[0])

def show_suggestion():
    # Validation check
    if not division.get() or not district.get() or not soil_type.get() or not season.get():
        messagebox.showwarning("সতর্কতা", "দয়া করে সবগুলো ফিল্ড পূরণ করুন!")
        return
        
    print(f"🔍 Searching for: Division={division.get()}, District={district.get()}, Soil={soil_type.get()}, Season={season.get()}")
        
    try:
        with sqlite3.connect("farming.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT crop, plant_time, fertilizer, water
                FROM crops
                WHERE division=? AND district=? AND soil=? AND season=?
            """, (division.get(), district.get(), soil_type.get(), season.get()))
            row = cursor.fetchone()
            
            print(f"📊 Database query result: {row}")
            
    except sqlite3.Error as e:
        messagebox.showerror("ডাটাবেস ইরর", str(e))
        return

    if row:
        crop, plant_time, fertilizer, water = row
        # ছোট উইন্ডোতে ফলাফল দেখানো
        show_suggestion_window(crop, plant_time, fertilizer, water)
        print(f"✅ Found crop: {crop}")
    else:
        show_suggestion_window("ফসলের তথ্য পাওয়া যায়নি", "আলু, গম, বা সরিষা চাষ করুন", "", "")
        print("❌ No crop found for the given criteria")

def show_suggestion_window(crop, plant_time, fertilizer, water):
    """ছোট উইন্ডোতে ফসলের সাজেশন দেখানো"""
    suggestion_win = Toplevel(root)
    suggestion_win.title("🌾 ফসলের সাজেশন")
    suggestion_win.geometry("400x300")
    suggestion_win.config(bg="#e8f5e9")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 400) // 2
    y = (screen_height - 300) // 2
    suggestion_win.geometry(f"400x300+{x}+{y}")
    
    # Header
    header_frame = tk.Frame(suggestion_win, bg="#4caf50", relief="raised", bd=2)
    header_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(header_frame, text="🌾 ফসলের সাজেশন", 
            font=("Arial", 16, "bold"), bg="#4caf50", fg="white", pady=10).pack()
    
    # Content Frame
    content_frame = tk.Frame(suggestion_win, bg="#e8f5e9")
    content_frame.pack(fill="both", expand=True, padx=15, pady=10)
    
    if crop == "ফসলের তথ্য পাওয়া যায়নি":
        tk.Label(content_frame, text="❌ " + crop, 
                font=("Arial", 14, "bold"), bg="#e8f5e9", fg="#d32f2f").pack(pady=5)
        tk.Label(content_frame, text=plant_time, 
                font=("Arial", 12), bg="#e8f5e9", wraplength=350, justify="left").pack(pady=10)
    else:
        # Crop Info
        info_text = f"""
🎯 **সুপারিশকৃত ফসল:** {crop}

📅 **বপনের সময়:** {plant_time}

🌿 **সার ব্যবস্থাপনা:** {fertilizer}

💧 **পানি ব্যবস্থাপনা:** {water}

📍 **আপনার এলাকা:** {division.get()}, {district.get()}
🌱 **মাটির ধরন:** {soil_type.get()}
📆 **মৌসুম:** {season.get()}
"""
        
        # Text widget for better formatting
        text_widget = tk.Text(content_frame, wrap="word", font=("Arial", 11), 
                             bg="#f1f8e9", relief="flat", height=10, width=45)
        text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Insert text with some basic formatting
        text_widget.insert("1.0", info_text)
        
        # Configure tags for formatting
        text_widget.tag_configure("bold", font=("Arial", 11, "bold"))
        text_widget.tag_configure("normal", font=("Arial", 11))
        
        # Apply formatting (basic approach)
        text_widget.config(state="disabled")  # Make it read-only
    
    # Button Frame
    button_frame = tk.Frame(suggestion_win, bg="#e8f5e9")
    button_frame.pack(fill="x", padx=20, pady=10)
    
    tk.Button(button_frame, text="✅ ঠিক আছে", command=suggestion_win.destroy,
              bg="#4caf50", fg="white", font=("Arial", 12), width=15).pack(side="right", padx=5)
    
    tk.Button(button_frame, text="📝 নতুন খোঁজ", 
              command=lambda: [suggestion_win.destroy(), clear_all()],
              bg="#2196f3", fg="white", font=("Arial", 12), width=15).pack(side="right", padx=5)

def search_crop():
    text = search_text.get()
    if not text:
        messagebox.showwarning("সতর্কতা", "দয়া করে ফসলের নাম লিখুন!")
        return
        
    try:
        with sqlite3.connect("farming.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT division, district, soil, season, plant_time, fertilizer, water
                FROM crops
                WHERE crop LIKE ?
            """, ('%' + text + '%',))
            rows = cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("ডাটাবেস ইরর", str(e))
        return

    if rows:
        output = ""
        for row in rows:
            output += f"📍 বিভাগ: {row[0]}, জেলা: {row[1]}\n🌱 মাটি: {row[2]}, মৌসুম: {row[3]}\n📅 সময়: {row[4]}\n🌿 সার: {row[5]}\n💧 পানি: {row[6]}\n{'-'*40}\n"
        result.set(output)
    else:
        result.set(f"❌ '{text}' ফসলের তথ্য পাওয়া যায়নি!")

def show_weather():
    if not district.get():
        messagebox.showwarning("সতর্কতা", "দয়া করে জেলা নির্বাচন করুন!")
        return
        
    city = district.get()
    api_key = "4a75508c602e3226a2bd138bfe043fa0"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=bn"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            weather_result.set("⚠️ আবহাওয়া তথ্য পাওয়া যায়নি!")
            return

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        weather_result.set(
            f"🌤️ {city} এর আবহাওয়া:\n"
            f"🌡️ তাপমাত্রা: {temp}°C\n"
            f"☁️ অবস্থা: {desc}\n"
            f"💧 আর্দ্রতা: {humidity}%\n"
            f"🌬️ বাতাসের গতি: {wind} m/s"
        )
    except Exception as e:
        weather_result.set("❌ আবহাওয়া আনতে সমস্যা হয়েছে\n" + str(e))

def show_crop_window(file_path, bg_color, title):
    crop_win = Toplevel(root)
    crop_win.title(title)
    crop_win.geometry("500x600")
    crop_win.config(bg=bg_color)
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 500) // 2
    y = (screen_height - 600) // 2
    crop_win.geometry(f"500x600+{x}+{y}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = ""
        for step, desc in data.items():
            text += f"📌 {step}:\n{desc}\n\n"

    except Exception as e:
        text = f"⚠️ ফাইল লোড করা সম্ভব হয়নি: {e}"

    text_area = tk.Text(crop_win, wrap="word", font=("Arial", 12))
    text_area.pack(expand=True, fill="both", padx=10, pady=10)
    text_area.insert("end", text)
    text_area.config(state="disabled")
    
    # স্ক্রলবার যোগ করুন
    scrollbar = Scrollbar(text_area)
    scrollbar.pack(side="right", fill="y")
    text_area.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_area.yview)

def show_new_rice_variety():
    rice_win = Toplevel(root)
    rice_win.title("🌾 ধানের নতুন জাত")
    rice_win.geometry("700x600")
    rice_win.config(bg="#e8f5e9")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 700) // 2
    y = (screen_height - 600) // 2
    rice_win.geometry(f"700x600+{x}+{y}")
    
    # Title
    tk.Label(rice_win, text="🌾 ধানের নতুন জাত সমূহ", 
            bg="#e8f5e9", font=("Arial", 16, "bold"), fg="#2e7d32").pack(pady=10)
    
    # Create main frame
    main_frame = tk.Frame(rice_win, bg="#e8f5e9")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Left frame for image
    left_frame = tk.Frame(main_frame, bg="#e8f5e9")
    left_frame.pack(side="left", fill="both", padx=(0, 10))
    
    # Right frame for text
    right_frame = tk.Frame(main_frame, bg="#e8f5e9")
    right_frame.pack(side="right", fill="both", expand=True)
    
    # Image display
    img_label = tk.Label(left_frame, bg="white", relief="solid", borderwidth=1, 
                        width=300, height=250)
    img_label.pack(pady=5)
    img_label.config(text="ছবি লোড হচ্ছে...", font=("Arial", 10))
    
    # Image navigation buttons
    nav_frame = tk.Frame(left_frame, bg="#e8f5e9")
    nav_frame.pack(pady=5)
    
    # Image list - আপনার ছবির পাথগুলো এখানে দিন
    image_paths = [
        "images/rice_variety1.jpg",
        "images/rice_variety2.jpg", 
        "images/rice_variety3.jpg",
        "images/rice_variety4.jpg"
    ]
    
    # Check which images actually exist
    available_images = []
    for img_path in image_paths:
        if os.path.exists(img_path):
            available_images.append(img_path)
        else:
            print(f"Warning: {img_path} not found")
    
    current_image_index = 0
    photo_references = []  # To prevent garbage collection
    
    def show_image(index):
        nonlocal current_image_index
        if not available_images:
            img_label.config(text="ছবি পাওয়া যায়নি\n(images folder চেক করুন)", font=("Arial", 10))
            return
            
        current_image_index = index % len(available_images)
        try:
            image = Image.open(available_images[current_image_index])
            image = image.resize((280, 230), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            # Keep reference to prevent garbage collection
            if len(photo_references) <= current_image_index:
                photo_references.append(photo)
            else:
                photo_references[current_image_index] = photo
                
            img_label.config(image=photo, text="")
            update_rice_info(current_image_index)
            
        except Exception as e:
            img_label.config(text=f"ছবি লোড করতে সমস্যা:\n{str(e)}", font=("Arial", 9))
    
    def next_image():
        if available_images:
            show_image((current_image_index + 1) % len(available_images))
    
    def prev_image():
        if available_images:
            show_image((current_image_index - 1) % len(available_images))
    
    # Navigation buttons
    btn_frame = tk.Frame(nav_frame, bg="#e8f5e9")
    btn_frame.pack()
    
    tk.Button(btn_frame, text="◀ পূর্বের", command=prev_image, 
              bg="#2196f3", fg="white", font=("Arial", 10), width=8).pack(side="left", padx=5)
    
    tk.Button(btn_frame, text="পরের ▶", command=next_image,
              bg="#2196f3", fg="white", font=("Arial", 10), width=8).pack(side="left", padx=5)
    
    # Rice variety information
    info_text = tk.Text(right_frame, wrap="word", font=("Arial", 11), 
                       bg="white", relief="solid", borderwidth=1,
                       width=40, height=20)
    info_text.pack(fill="both", expand=True)
    
    # Rice varieties data
    rice_varieties = [
        {
            "name": "ব্রি ধান ৮৯",
            "features": "উচ্চ ফলনশীল, রোগ প্রতিরোধী জাত",
            "planting_time": "জুন-জুলাই",
            "harvest": "নভেম্বর-ডিসেম্বর", 
            "area": "সমগ্র বাংলাদেশ",
            "yield": "হেক্টরপ্রতি ৬-৭ টন",
            "special": "লক্ষ্মী ছড়ার রোগ প্রতিরোধী"
        },
        {
            "name": "ব্রি ধান ৯২", 
            "features": "খরাসহিষ্ণু, স্বাদ ভালো",
            "planting_time": "মে-জুন",
            "harvest": "অক্টোবর-নভেম্বর",
            "area": "উত্তরাঞ্চল",
            "yield": "হেক্টরপ্রতি ৫-৬ টন",
            "special": "পানির অভাবেও ভালো ফলন"
        },
        {
            "name": "ব্রি ধান ৯৭",
            "features": "পোকামাকড় প্রতিরোধী, উচ্চ ফলন",
            "planting_time": "জুলাই-আগস্ট", 
            "harvest": "ডিসেম্বর-জানুয়ারি",
            "area": "মধ্য ও দক্ষিণাঞ্চল",
            "yield": "হেক্টরপ্রতি ৬.৫-৭.৫ টন",
            "special": "ব্লাস্ট রোগ প্রতিরোধী"
        },
        {
            "name": "ব্রি ধান ১০০",
            "features": "জিংক সমৃদ্ধ, পুষ্টিগুণ বেশি",
            "planting_time": "জুলাই-আগস্ট",
            "harvest": "ডিসেম্বর-জানুয়ারি", 
            "area": "সমগ্র বাংলাদেশ",
            "yield": "হেক্টরপ্রতি ৫.৫-৬.৫ টন",
            "special": "জিংক সমৃদ্ধ ধান, পুষ্টিকর"
        }
    ]
    
    def update_rice_info(index):
        if index < len(rice_varieties):
            variety = rice_varieties[index]
            info_text.config(state="normal")
            info_text.delete(1.0, tk.END)
            
            info = f"""🎯 {variety['name']}

📊 বৈশিষ্ট্য:
   • {variety['features']}
   • {variety['special']}

📅 চাষের সময়:
   • বপনের সময়: {variety['planting_time']}
   • ফসল সংগ্রহ: {variety['harvest']}

📍 উপযোগী এলাকা:
   • {variety['area']}

🌾 ফলন:
   • {variety['yield']}

💡 বিশেষ দ্রষ্টব্য:
   • ব্রি কর্তৃক অনুমোদিত
   • উচ্চ ফলনশীল জাত
   • রোগ প্রতিরোধী ক্ষমতা
   • স্থানীয় কৃষি বিভাগ থেকে বীজ সংগ্রহ করুন
"""
            info_text.insert(1.0, info)
            info_text.config(state="disabled")
    
    # Image counter
    counter_label = tk.Label(left_frame, text=f"ছবি 1/{len(available_images) if available_images else 0}", 
                            bg="#e8f5e9", font=("Arial", 10))
    counter_label.pack(pady=5)
    
    def update_counter():
        if available_images:
            counter_label.config(text=f"ছবি {current_image_index + 1}/{len(available_images)}")
        else:
            counter_label.config(text="ছবি নেই")
    
    # Modified show_image function to update counter
    def show_image_with_counter(index):
        show_image(index)
        update_counter()
    
    # Initialize
    if available_images:
        show_image_with_counter(0)
    else:
        # Show default information if no images
        info_text.config(state="normal")
        info_text.delete(1.0, tk.END)
        default_info = """🌾 ধানের নতুন জাত সমূহ

ছবি যোগ করার জন্য:
1. Project folder-এ 'images' নামে ফোল্ডার তৈরি করুন
2. নিম্নলিখিত নামে ছবি যোগ করুন:
   • rice_variety1.jpg
   • rice_variety2.jpg  
   • rice_variety3.jpg
   • rice_variety4.jpg

ব্রি ধান ৮৯:
• উচ্চ ফলনশীল, রোগ প্রতিরোধী

ব্রি ধান ৯২:
• খরাসহিষ্ণু, স্বাদ ভালো

ব্রি ধান ৯৭:
• পোকামাকড় প্রতিরোধী

ব্রি ধান ১০০:
• জিংক সমৃদ্ধ, পুষ্টিগুণ বেশি
"""
        info_text.insert(1.0, default_info)
        info_text.config(state="disabled")
    
    # Update navigation functions
    def next_with_counter():
        next_image()
        update_counter()
    
    def prev_with_counter():
        prev_image()
        update_counter()
    
    # Update button commands
    for widget in btn_frame.winfo_children():
        if isinstance(widget, tk.Button):
            if widget['text'] == "পরের ▶":
                widget.config(command=next_with_counter)
            elif widget['text'] == "◀ পূর্বের":
                widget.config(command=prev_with_counter)

def open_second_window():
    second_win = Toplevel(root)
    second_win.title("দ্বিতীয় উইন্ডো - ফসল নির্বাচন")
    second_win.geometry("500x600")
    second_win.config(bg="#f0f4c3")
    
    # Full HD ডিসপ্লের জন্য সেন্টারে উইন্ডো স্থাপন
    x = (screen_width - 500) // 2
    y = (screen_height - 600) // 2
    second_win.geometry(f"500x600+{x}+{y}")

    tk.Label(second_win, text="👉 কোন ফসলের চাষ পদ্ধতি দেখতে চাও?", 
             bg="#f0f4c3", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(second_win, text="🌾 ধান চাষের পদ্ধতি", 
              command=lambda: show_crop_window("rice_data.json", "#e8f5e9", "ধান চাষের পদ্ধতি"),
              bg="#4caf50", fg="white", font=("Arial", 12), width=25).pack(pady=5)
    tk.Button(second_win, text="🌾 গম চাষের পদ্ধতি", 
              command=lambda: show_crop_window("wheat_data.json", "#fff3e0", "গম চাষের পদ্ধতি"),
              bg="#ff9800", fg="white", font=("Arial", 12), width=25).pack(pady=5)
    tk.Button(second_win, text="🥬 সবজি চাষের পদ্ধতি", 
              command=lambda: show_crop_window("vegetable_data.json", "#dcedc8", "সবজি চাষের পদ্ধতি"),
              bg="#8bc34a", fg="white", font=("Arial", 12), width=25).pack(pady=5)
    tk.Button(second_win, text="🥔 আলু চাষের পদ্ধতি", 
              command=lambda: show_crop_window("potato_data.json", "#ffebee", "আলু চাষের পদ্ধতি"),
              bg="#e91e63", fg="white", font=("Arial", 12), width=25).pack(pady=5)
    tk.Button(second_win, text="🌾 ধানের নতুন জাত", 
              command=show_new_rice_variety,
              bg="#2196f3", fg="white", font=("Arial", 12), width=25).pack(pady=5)

    # রিমাইন্ডার সেকশন
    tk.Label(second_win, text="⏰ রিমাইন্ডার সেট করুন", bg="#f0f4c3", font=("Arial", 13, "bold")).pack(pady=10)

    tk.Label(second_win, text="তারিখ নির্বাচন:", bg="#f0f4c3", font=("Arial", 11)).pack(pady=2)
    cal = Calendar(second_win, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=5)

    tk.Label(second_win, text="সময় নির্বাচন:", bg="#f0f4c3", font=("Arial", 11)).pack(pady=2)
    hour_spin = tk.Spinbox(second_win, from_=0, to=23, width=5, font=("Arial", 11))
    hour_spin.pack(pady=2)
    minute_spin = tk.Spinbox(second_win, from_=0, to=59, width=5, font=("Arial", 11))
    minute_spin.pack(pady=2)

    tk.Label(second_win, text="রিমাইন্ডার মেসেজ:", bg="#f0f4c3", font=("Arial", 11)).pack(pady=2)
    msg_entry = tk.Entry(second_win, width=30, font=("Arial", 11))
    msg_entry.pack(pady=5)

    def set_reminder():
        date = cal.get_date()
        hour = int(hour_spin.get())
        minute = int(minute_spin.get())
        msg = msg_entry.get() or "স্মার্ট ফার্মিং টাস্ক রিমাইন্ডার!"
        schedule_reminder(date, hour, minute, msg)
        messagebox.showinfo("রিমাইন্ডার", f"রিমাইন্ডার সেট করা হয়েছে {date} তারিখে {hour}:{minute} সময়ে")

    tk.Button(second_win, text="রিমাইন্ডার সেট করুন", command=set_reminder, 
              bg="#ff9800", fg="white", font=("Arial", 11)).pack(pady=10)

def schedule_reminder(date, hour, minute, msg):
    print(f"রিমাইন্ডার সেট করা হয়েছে {date} তারিখে {hour}:{minute} সময়ে, মেসেজ: {msg}")

# ---------------- মেইন উইন্ডো UI ----------------

# Menu Bar তৈরি করুন
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File মেনু
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="ফাইল", menu=file_menu)
file_menu.add_command(label="এক্সিট", command=root.quit)

# Features মেনু
features_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="বিশেষ ফিচার", menu=features_menu)
features_menu.add_command(label="🌦️ বিস্তারিত আবহাওয়া", command=show_detailed_weather)
features_menu.add_command(label="💰 বাজার দর", command=show_market_price)
features_menu.add_command(label="🏢 কৃষি অফিস", command=show_nearby_offices)
features_menu.add_command(label="🧮 লাভ গণনা", command=profit_calculator)
features_menu.add_command(label="👥 কৃষক ফোরাম", command=farmer_forum)
features_menu.add_command(label="🏛️ সরকারি সুবিধা", command=government_schemes)
features_menu.add_command(label="🩺 রোগ-বালাই", command=disease_diagnosis)

# Help মেনু
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="হেল্প", menu=help_menu)
help_menu.add_command(label="ব্যবহার নির্দেশিকা")
help_menu.add_command(label="About")

# Main Content
tk.Label(app, text="🌾 স্মার্ট কৃষি পরিকল্পনা", bg="#e8f5e9", font=("Arial", 18, "bold"), fg="#2e7d32").pack(pady=15)

# বিভাগ নির্বাচন
tk.Label(app, text="🇧🇩 বিভাগ নির্বাচন করুন:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=5)
division_menu = tk.OptionMenu(app, division, *districts_by_division.keys(), command=lambda x: (update_districts(), update_soils(), update_seasons()))
division_menu.config(width=25, font=("Arial", 11), bg="white")
division_menu.pack(pady=2)

# জেলা নির্বাচন
tk.Label(app, text="📍 জেলা নির্বাচন করুন:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=5)
district_option = tk.OptionMenu(app, district, "")
district_option.config(width=25, font=("Arial", 11), bg="white")
district_option.pack(pady=2)
district.trace_add('write', lambda *args: (update_soils(), update_seasons()))

# মাটির ধরন নির্বাচন
tk.Label(app, text="🌱 মাটির ধরন নির্বাচন করুন:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=5)
soil_option = tk.OptionMenu(app, soil_type, *soil_options)
soil_option.config(width=25, font=("Arial", 11), bg="white")
soil_option.pack(pady=2)

# মৌসুম নির্বাচন
tk.Label(app, text="📅 মৌসুম নির্বাচন করুন:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=5)
season_option = tk.OptionMenu(app, season, *season_options)
season_option.config(width=25, font=("Arial", 11), bg="white")
season_option.pack(pady=2)

# বাটন গুলো
tk.Button(app, text="✅ ফসলের সাজেশন পান", command=show_suggestion, bg="#4caf50", fg="white", font=("Arial", 12), width=20).pack(pady=12)
tk.Button(app, text="☁️ আবহাওয়া দেখুন", command=show_weather, bg="#03a9f4", fg="white", font=("Arial", 12), width=20).pack(pady=6)

tk.Label(app, textvariable=weather_result, wraplength=460, justify="left", fg="#01579b", bg="#e8f5e9", font=("Arial", 11)).pack(pady=5)

# ফসল খোঁজা
tk.Label(app, text="🔍 ফসলের নাম দিয়ে খোঁজো:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=5)
tk.Entry(app, textvariable=search_text, font=("Arial", 11), width=30).pack()
tk.Button(app, text="🔍 খোঁজো", command=search_crop, bg="#1976d2", fg="white", font=("Arial", 12), width=20).pack(pady=8)

tk.Button(app, text="➕ অন্যান্য ফসলের তথ্য", command=open_second_window, bg="#ff9800", fg="white", font=("Arial", 12), width=20).pack(pady=8)

# নতুন ফিচার বাটন ফ্রেম
feature_frame = tk.Frame(app, bg="#e8f5e9")
feature_frame.pack(pady=10)

tk.Button(feature_frame, text="🌦️ বিস্তারিত আবহাওয়া", command=show_detailed_weather,
          bg="#2196f3", fg="white", font=("Arial", 10), width=15).grid(row=0, column=0, padx=5, pady=2)

tk.Button(feature_frame, text="💰 বাজার দর", command=show_market_price,
          bg="#ff9800", fg="white", font=("Arial", 10), width=15).grid(row=0, column=1, padx=5, pady=2)

tk.Button(feature_frame, text="🏢 কৃষি অফিস", command=show_nearby_offices,
          bg="#4caf50", fg="white", font=("Arial", 10), width=15).grid(row=1, column=0, padx=5, pady=2)

tk.Button(feature_frame, text="🧮 লাভ গণনা", command=profit_calculator,
          bg="#9c27b0", fg="white", font=("Arial", 10), width=15).grid(row=1, column=1, padx=5, pady=2)

tk.Button(feature_frame, text="👥 কৃষক ফোরাম", command=farmer_forum,
          bg="#607d8b", fg="white", font=("Arial", 10), width=15).grid(row=2, column=0, padx=5, pady=2)

tk.Button(feature_frame, text="🏛️ সরকারি সুবিধা", command=government_schemes,
          bg="#795548", fg="white", font=("Arial", 10), width=15).grid(row=2, column=1, padx=5, pady=2)

tk.Button(feature_frame, text="🩺 রোগ-বালাই", command=disease_diagnosis,
          bg="#f44336", fg="white", font=("Arial", 10), width=15).grid(row=3, column=0, padx=5, pady=2)

# নতুন ফিচারের বোতাম
new_feature_frame = tk.LabelFrame(app, text="✨ নতুন ফিচার", bg="#f1f8e9", font=("Arial", 11, "bold"), padx=10, pady=10)
new_feature_frame.pack(fill="x", padx=10, pady=10)

tk.Button(new_feature_frame, text="🌾 উৎপাদন ট্র্যাকিং", command=lambda: open_production_tracker_window(root),
          bg="#81c784", fg="white", font=("Arial", 9), width=18).grid(row=0, column=0, padx=3, pady=3)

tk.Button(new_feature_frame, text="👨‍🌾 কৃষক প্রোফাইল", command=lambda: open_farmer_profile_window(root),
          bg="#66bb6a", fg="white", font=("Arial", 9), width=18).grid(row=0, column=1, padx=3, pady=3)

tk.Button(new_feature_frame, text="🌏 জমির ম্যাপিং", command=lambda: open_land_mapping_window(root),
          bg="#4caf50", fg="white", font=("Arial", 9), width=18).grid(row=0, column=2, padx=3, pady=3)

tk.Button(new_feature_frame, text="📊 সার ক্যালকুলেটর", command=lambda: open_fertilizer_calculator_window(root),
          bg="#388e3c", fg="white", font=("Arial", 9), width=18).grid(row=1, column=0, padx=3, pady=3)

tk.Button(new_feature_frame, text="🚜 যন্ত্রপাতি ভাড়া", command=lambda: open_machinery_rental_window(root),
          bg="#00796b", fg="white", font=("Arial", 9), width=18).grid(row=1, column=1, padx=3, pady=3)

tk.Button(new_feature_frame, text="📱 বীজ ডিরেক্টরি", command=lambda: open_seeds_equipment_window(root),
          bg="#7b1fa2", fg="white", font=("Arial", 9), width=18).grid(row=1, column=2, padx=3, pady=3)

tk.Button(new_feature_frame, text="💰 ঋণ চেকার", command=lambda: open_loan_eligibility_window(root),
          bg="#f57f17", fg="white", font=("Arial", 9), width=18).grid(row=2, column=0, padx=3, pady=3)

tk.Button(new_feature_frame, text="📈 ফসল রোটেশন", command=lambda: open_crop_rotation_window(root),
          bg="#f57c00", fg="white", font=("Arial", 9), width=18).grid(row=2, column=1, padx=3, pady=3)

tk.Button(new_feature_frame, text="🎥 ভিডিও লাইব্রেরি", command=lambda: open_video_library_window(root),
          bg="#e91e63", fg="white", font=("Arial", 9), width=18).grid(row=2, column=2, padx=3, pady=3)

tk.Button(new_feature_frame, text="📋 রিপোর্ট এক্সপোর্ট", command=lambda: open_report_export_window(root),
          bg="#1565c0", fg="white", font=("Arial", 9), width=18).grid(row=3, column=0, columnspan=3, padx=3, pady=3, sticky="ew")

# ফলাফল দেখানোর লেবেল
result_label = tk.Label(app, textvariable=result, wraplength=460, justify="left", fg="#1b5e20", bg="#e8f5e9", font=("Arial", 11))
result_label.pack(pady=10)

# তথ্য ক্লিয়ার করার বাটন
def clear_all():
    division.set("")
    district.set("")
    soil_type.set("")
    season.set("")
    search_text.set("")
    result.set("")
    weather_result.set("")

tk.Button(app, text="🧹 সবকিছু ক্লিয়ার করুন", command=clear_all, bg="#f44336", fg="white", font=("Arial", 10), width=15).pack(pady=5)

# মেইন লুপ শুরু করুন
root.mainloop()