"""
🌏 জমির ম্যাপিং সিস্টেম
Land Mapping Module
---------------------------------
জমির অবস্থান, সীমানা এবং ফসল ম্যাপিং সংরক্ষণ করুন
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

LAND_MAP_FILE = "land_maps.json"

class LandMapping:
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """ম্যাপ ডাটা লোড করুন"""
        if os.path.exists(LAND_MAP_FILE):
            with open(LAND_MAP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """ডাটা সেভ করুন"""
        with open(LAND_MAP_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def add_land_plot(self, plot_name, area, location, soiltype, current_crop, boundary=""):
        """নতুন জমির প্লট যোগ করুন"""
        plot = {
            "id": len(self.data) + 1,
            "name": plot_name,
            "area": area,  # শতক
            "location": location,
            "soil_type": soiltype,
            "current_crop": current_crop,
            "boundary": boundary,
            "history": []
        }
        self.data.append(plot)
        self.save_data()
        return plot
    
    def get_land_summary(self):
        """জমির সারসংক্ষেপ পান"""
        summary = {
            "total_plots": len(self.data),
            "total_area": sum(p['area'] for p in self.data),
            "crops": {}
        }
        for plot in self.data:
            crop = plot['current_crop']
            if crop not in summary['crops']:
                summary['crops'][crop] = 0
            summary['crops'][crop] += plot['area']
        return summary


def open_land_mapping_window(root):
    """জমি ম্যাপিং উইন্ডো খুলুন"""
    map_win = tk.Toplevel(root)
    map_win.title("🌏 জমির ম্যাপিং সিস্টেম")
    map_win.geometry("750x650")
    map_win.config(bg="#e1f5fe")
    
    mapper = LandMapping()
    
    # ======= ইনপুট ফ্রেম =======
    input_frame = tk.LabelFrame(map_win, text="🗺️ নতুন জমির প্লট যোগ করুন", 
                                bg="#e1f5fe", font=("Arial", 11, "bold"), padx=15, pady=10)
    input_frame.pack(fill="x", padx=10, pady=10)
    
    # প্লটের নাম
    tk.Label(input_frame, text="প্লটের নাম:", bg="#e1f5fe", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(input_frame, width=25)
    name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
    
    # এলাকা
    tk.Label(input_frame, text="এলাকা (শতক):", bg="#e1f5fe", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=5)
    area_entry = tk.Entry(input_frame, width=20)
    area_entry.grid(row=0, column=3, sticky="ew", padx=10, pady=5)
    
    # অবস্থান
    tk.Label(input_frame, text="অবস্থান:", bg="#e1f5fe", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
    location_entry = tk.Entry(input_frame, width=25)
    location_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
    
    # মাটির ধরন
    tk.Label(input_frame, text="মাটির ধরন:", bg="#e1f5fe", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5)
    soil_entry = tk.Entry(input_frame, width=20)
    soil_entry.grid(row=1, column=3, sticky="ew", padx=10, pady=5)
    
    # বর্তমান ফসল
    tk.Label(input_frame, text="বর্তমান ফসল:", bg="#e1f5fe", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
    crop_entry = tk.Entry(input_frame, width=25)
    crop_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
    
    input_frame.columnconfigure(1, weight=1)
    input_frame.columnconfigure(3, weight=1)
    
    # ======= পরিসংখ্যান ফ্রেম =======
    stats_frame = tk.Frame(map_win, bg="#e1f5fe")
    stats_frame.pack(fill="x", padx=10, pady=5)
    
    total_plots_label = tk.Label(stats_frame, text="📍 মোট প্লট: 0", 
                                 bg="#e1f5fe", font=("Arial", 10, "bold"), fg="#01579b")
    total_plots_label.pack(side="left", padx=15, pady=5)
    
    total_area_label = tk.Label(stats_frame, text="📏 মোট এলাকা: 0 শতক", 
                                bg="#e1f5fe", font=("Arial", 10, "bold"), fg="#004d40")
    total_area_label.pack(side="left", padx=15, pady=5)
    
    # ======= প্লটের তালিকা ফ্রেম =======
    list_frame = tk.LabelFrame(map_win, text="🗺️ নিবন্ধিত প্লটসমূহ", 
                               bg="#e1f5fe", font=("Arial", 11, "bold"))
    list_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # টেক্সট উইজেট
    plot_text = tk.Text(list_frame, bg="white", font=("Courier", 9), height=10)
    plot_text.pack(fill="both", expand=True, padx=5, pady=5)
    plot_text.config(state="disabled")
    
    def refresh_display():
        """ডিসপ্লে রিফ্রেশ করুন"""
        summary = mapper.get_land_summary()
        total_plots_label.config(text=f"📍 মোট প্লট: {summary['total_plots']}")
        total_area_label.config(text=f"📏 মোট এলাকা: {summary['total_area']} শতক")
        
        plot_text.config(state="normal")
        plot_text.delete(1.0, tk.END)
        
        for plot in mapper.data:
            text = f"""
🗺️ {plot['name']}
   এলাকা: {plot['area']} শতক | অবস্থান: {plot['location']}
   মাটি: {plot['soil_type']} | ফসল: {plot['current_crop']}
{'-'*70}
"""
            plot_text.insert(tk.END, text)
        
        plot_text.config(state="disabled")
    
    def add_plot():
        """নতুন প্লট যোগ করুন"""
        try:
            name = name_entry.get() or "অজানা প্লট"
            area = float(area_entry.get() or 0)
            location = location_entry.get() or "অজানা"
            soil = soil_entry.get() or "অজানা"
            crop = crop_entry.get() or "খালি জমি"
            
            mapper.add_land_plot(name, area, location, soil, crop)
            messagebox.showinfo("সফল", f"✅ {name} যোগ করা হয়েছে!")
            
            name_entry.delete(0, tk.END)
            area_entry.delete(0, tk.END)
            location_entry.delete(0, tk.END)
            soil_entry.delete(0, tk.END)
            crop_entry.delete(0, tk.END)
            
            refresh_display()
        except ValueError:
            messagebox.showerror("ত্রুটি", "❌ এলাকা সংখ্যা হতে হবে")
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(map_win, bg="#e1f5fe")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Button(button_frame, text="➕ প্লট যোগ করুন", command=add_plot,
              bg="#00897b", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 রিফ্রেশ", command=refresh_display,
              bg="#0288d1", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=map_win.destroy,
              bg="#d32f2f", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    refresh_display()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Land Mapping Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Land Mapping", command=lambda: open_land_mapping_window(root)).pack(pady=20)
    root.mainloop()
