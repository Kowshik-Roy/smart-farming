"""
🌾 কৃষি উৎপাদন ট্র্যাকিং সিস্টেম
Crop Production Tracking Module
---------------------------------
ফসলের উৎপাদন, বীজ, সার, ফলন সবকিছু ট্র্যাক করুন
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

# ডাটা ফাইলের নাম
PROD_DATA_FILE = "production_data.json"

class ProductionTracker:
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """ডাটা লোড করুন"""
        if os.path.exists(PROD_DATA_FILE):
            with open(PROD_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """ডাটা সেভ করুন"""
        with open(PROD_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def add_production_record(self, crop_name, field_area, seed_amount, 
                             fertilizer_used, water_used, harvest_date, yield_kg, notes=""):
        """নতুন উৎপাদন রেকর্ড যোগ করুন"""
        record = {
            "id": len(self.data) + 1,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "crop": crop_name,
            "field_area": field_area,  # শতক
            "seed_amount": seed_amount,  # কেজি
            "fertilizer_used": fertilizer_used,  # কেজি
            "water_used": water_used,  # ঘণ্টা
            "harvest_date": harvest_date,
            "yield_kg": yield_kg,
            "yield_per_acre": yield_kg / (field_area / 100) if field_area > 0 else 0,
            "notes": notes
        }
        self.data.append(record)
        self.save_data()
        return record
    
    def get_crop_history(self, crop_name):
        """নির্দিষ্ট ফসলের ইতিহাস পান"""
        return [r for r in self.data if r['crop'].lower() == crop_name.lower()]
    
    def get_average_yield(self, crop_name):
        """গড় ফলন পান"""
        records = self.get_crop_history(crop_name)
        if not records:
            return 0
        total_yield = sum(r['yield_per_acre'] for r in records)
        return total_yield / len(records)
    
    def get_summary_stats(self):
        """সামগ্রিক পরিসংখ্যান পান"""
        if not self.data:
            return {}
        
        crops = {}
        for record in self.data:
            crop = record['crop']
            if crop not in crops:
                crops[crop] = {
                    'count': 0,
                    'total_area': 0,
                    'total_yield': 0,
                    'avg_yield': 0
                }
            crops[crop]['count'] += 1
            crops[crop]['total_area'] += record['field_area']
            crops[crop]['total_yield'] += record['yield_kg']
            crops[crop]['avg_yield'] = crops[crop]['total_yield'] / crops[crop]['count']
        
        return crops


def open_production_tracker_window(root):
    """উৎপাদন ট্র্যাকিং উইন্ডো খুলুন"""
    tracker_win = tk.Toplevel(root)
    tracker_win.title("🌾 কৃষি উৎপাদন ট্র্যাকিং")
    tracker_win.geometry("700x600")
    tracker_win.config(bg="#e8f5e9")
    
    tracker = ProductionTracker()
    
    # ======= ইনপুট ফ্রেম =======
    input_frame = tk.LabelFrame(tracker_win, text="📝 নতুন উৎপাদন রেকর্ড", 
                                bg="#e8f5e9", font=("Arial", 11, "bold"))
    input_frame.pack(fill="x", padx=10, pady=10)
    
    # ফসলের নাম
    tk.Label(input_frame, text="ফসলের নাম:", bg="#e8f5e9", font=("Arial", 10)).pack(side="left", padx=5, pady=5)
    crop_entry = tk.Entry(input_frame, width=15)
    crop_entry.pack(side="left", padx=5, pady=5)
    
    # জমির আয়তন
    tk.Label(input_frame, text="জমি (শতক):", bg="#e8f5e9", font=("Arial", 10)).pack(side="left", padx=5, pady=5)
    area_entry = tk.Entry(input_frame, width=10)
    area_entry.pack(side="left", padx=5, pady=5)
    
    # ফলন
    tk.Label(input_frame, text="ফলন (কেজি):", bg="#e8f5e9", font=("Arial", 10)).pack(side="left", padx=5, pady=5)
    yield_entry = tk.Entry(input_frame, width=10)
    yield_entry.pack(side="left", padx=5, pady=5)
    
    # ======= ফলাফল ফ্রেম =======
    result_frame = tk.LabelFrame(tracker_win, text="📊 উৎপাদন ইতিহাস", 
                                 bg="#e8f5e9", font=("Arial", 11, "bold"))
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # ট্রি ভিউ
    columns = ("ফসল", "জমি (শতক)", "ফলন (কেজি)", "প্রতি একর", "তারিখ")
    tree = ttk.Treeview(result_frame, columns=columns, height=15, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)
    
    tree.pack(fill="both", expand=True)
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(tracker_win, bg="#e8f5e9")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        for record in tracker.data:
            tree.insert('', 'end', values=(
                record['crop'],
                f"{record['field_area']} শতক",
                f"{record['yield_kg']} কেজি",
                f"{record['yield_per_acre']:.2f} কেজি",
                record['date'].split()[0]
            ))
    
    def add_new_record():
        try:
            crop = crop_entry.get() or "অজানা"
            area = float(area_entry.get() or 0)
            yield_val = float(yield_entry.get() or 0)
            
            tracker.add_production_record(
                crop_name=crop,
                field_area=area,
                seed_amount=0,
                fertilizer_used=0,
                water_used=0,
                harvest_date=datetime.now().strftime("%Y-%m-%d"),
                yield_kg=yield_val,
                notes=""
            )
            messagebox.showinfo("সফল", f"✅ {crop} এর রেকর্ড যোগ হয়েছে!")
            crop_entry.delete(0, tk.END)
            area_entry.delete(0, tk.END)
            yield_entry.delete(0, tk.END)
            refresh_table()
        except ValueError:
            messagebox.showerror("ত্রুটি", "❌ সঠিক সংখ্যা দিন")
    
    tk.Button(button_frame, text="✅ রেকর্ড যোগ করুন", command=add_new_record,
              bg="#4caf50", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 রিফ্রেশ", command=refresh_table,
              bg="#2196f3", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=tracker_win.destroy,
              bg="#f44336", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Production Tracker Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Tracker", command=lambda: open_production_tracker_window(root)).pack(pady=20)
    root.mainloop()
