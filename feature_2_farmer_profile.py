"""
👨‍🌾 কৃষক প্রোফাইল সিস্টেম
Farmer Profile Management Module
---------------------------------
কৃষকের ব্যক্তিগত তথ্য, জমির বিবরণ এবং ইতিহাস সংরক্ষণ করুন
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FARMER_DATA_FILE = "farmer_profiles.json"

class FarmerProfile:
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """প্রোফাইল ডাটা লোড করুন"""
        if os.path.exists(FARMER_DATA_FILE):
            with open(FARMER_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """ডাটা সেভ করুন"""
        with open(FARMER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def add_farmer(self, name, phone, division, district, land_area_decimal, land_type="কৃষি"):
        """নতুন কৃষক যোগ করুন"""
        farmer = {
            "id": len(self.data) + 1,
            "name": name,
            "phone": phone,
            "division": division,
            "district": district,
            "land_area": land_area_decimal,
            "land_type": land_type,
            "crops_grown": [],
            "experience_years": 0,
            "additional_info": ""
        }
        self.data.append(farmer)
        self.save_data()
        return farmer
    
    def get_farmer(self, farmer_id):
        """কৃষকের তথ্য পান"""
        for farmer in self.data:
            if farmer['id'] == farmer_id:
                return farmer
        return None
    
    def update_farmer(self, farmer_id, **kwargs):
        """কৃষকের তথ্য আপডেট করুন"""
        for farmer in self.data:
            if farmer['id'] == farmer_id:
                farmer.update(kwargs)
                self.save_data()
                return farmer
        return None
    
    def get_all_farmers(self):
        """সকল কৃষকের তালিকা পান"""
        return self.data


def open_farmer_profile_window(root):
    """কৃষক প্রোফাইল উইন্ডো খুলুন"""
    profile_win = tk.Toplevel(root)
    profile_win.title("👨‍🌾 কৃষক প্রোফাইল সিস্টেম")
    profile_win.geometry("700x650")
    profile_win.config(bg="#e3f2fd")
    
    profile = FarmerProfile()
    current_farmer_id = [None]
    
    # ======= প্রোফাইল তথ্য ফ্রেম =======
    info_frame = tk.LabelFrame(profile_win, text="📋 কৃষক তথ্য", 
                               bg="#e3f2fd", font=("Arial", 11, "bold"), padx=15, pady=10)
    info_frame.pack(fill="x", padx=10, pady=10)
    
    # নাম
    tk.Label(info_frame, text="নাম:", bg="#e3f2fd", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(info_frame, width=30)
    name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
    
    # ফোন
    tk.Label(info_frame, text="ফোন নম্বর:", bg="#e3f2fd", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
    phone_entry = tk.Entry(info_frame, width=30)
    phone_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
    
    # বিভাগ
    tk.Label(info_frame, text="বিভাগ:", bg="#e3f2fd", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=5)
    division_entry = tk.Entry(info_frame, width=20)
    division_entry.grid(row=0, column=3, sticky="ew", padx=10, pady=5)
    
    # জেলা
    tk.Label(info_frame, text="জেলা:", bg="#e3f2fd", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5)
    district_entry = tk.Entry(info_frame, width=20)
    district_entry.grid(row=1, column=3, sticky="ew", padx=10, pady=5)
    
    # জমির পরিমাণ
    tk.Label(info_frame, text="জমি (শতাংশ):", bg="#e3f2fd", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
    land_entry = tk.Entry(info_frame, width=30)
    land_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
    
    # অভিজ্ঞতা
    tk.Label(info_frame, text="অভিজ্ঞতা (বছর):", bg="#e3f2fd", font=("Arial", 10)).grid(row=2, column=2, sticky="w", pady=5)
    exp_entry = tk.Entry(info_frame, width=20)
    exp_entry.grid(row=2, column=3, sticky="ew", padx=10, pady=5)
    
    # ======= পরিসংখ্যান ফ্রেম =======
    stats_frame = tk.LabelFrame(profile_win, text="📊 পরিসংখ্যান", 
                                bg="#e3f2fd", font=("Arial", 11, "bold"), padx=15, pady=10)
    stats_frame.pack(fill="x", padx=10, pady=5)
    
    total_farmers_label = tk.Label(stats_frame, text="মোট কৃষক: 0", 
                                   bg="#e3f2fd", font=("Arial", 11, "bold"), fg="#1976d2")
    total_farmers_label.pack(side="left", padx=20, pady=5)
    
    total_land_label = tk.Label(stats_frame, text="মোট জমি: 0 শতাংশ", 
                                bg="#e3f2fd", font=("Arial", 11, "bold"), fg="#388e3c")
    total_land_label.pack(side="left", padx=20, pady=5)
    
    # ======= কৃষকদের তালিকা ফ্রেম =======
    list_frame = tk.LabelFrame(profile_win, text="📱 নিবন্ধিত কৃষকদের তালিকা", 
                               bg="#e3f2fd", font=("Arial", 11, "bold"))
    list_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # লিস্টবক্স
    farmer_listbox = tk.Listbox(list_frame, bg="white", font=("Arial", 10), height=8)
    farmer_listbox.pack(fill="both", expand=True, padx=5, pady=5)
    
    def refresh_stats():
        """পরিসংখ্যান আপডেট করুন"""
        farmers = profile.get_all_farmers()
        total_farmers = len(farmers)
        total_land = sum(f['land_area'] for f in farmers)
        
        total_farmers_label.config(text=f"মোট কৃষক: {total_farmers}")
        total_land_label.config(text=f"মোট জমি: {total_land} শতাংশ")
    
    def refresh_list():
        """তালিকা রিফ্রেশ করুন"""
        farmer_listbox.delete(0, tk.END)
        for farmer in profile.get_all_farmers():
            text = f"🧑 {farmer['name']} - {farmer['phone']} - {farmer['land_area']} শতাংশ"
            farmer_listbox.insert(tk.END, text)
        refresh_stats()
    
    def add_new_farmer():
        """নতুন কৃষক যোগ করুন"""
        try:
            name = name_entry.get() or "অজানা"
            phone = phone_entry.get() or "০"
            division = division_entry.get() or "অজানা"
            district = district_entry.get() or "অজানা"
            land = float(land_entry.get() or 0)
            
            profile.add_farmer(name, phone, division, district, land)
            messagebox.showinfo("সফল", f"✅ {name} সফলভাবে যোগ করা হয়েছে!")
            
            # ক্লিয়ার করুন
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            division_entry.delete(0, tk.END)
            district_entry.delete(0, tk.END)
            land_entry.delete(0, tk.END)
            exp_entry.delete(0, tk.END)
            
            refresh_list()
        except ValueError:
            messagebox.showerror("ত্রুটি", "❌ জমির পরিমাণ সংখ্যা হতে হবে")
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(profile_win, bg="#e3f2fd")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Button(button_frame, text="➕ নতুন কৃষক", command=add_new_farmer,
              bg="#4caf50", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 রিফ্রেশ", command=refresh_list,
              bg="#2196f3", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=profile_win.destroy,
              bg="#f44336", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Farmer Profile Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Farmer Profile", command=lambda: open_farmer_profile_window(root)).pack(pady=20)
    root.mainloop()
