"""
📈 ফসল রোটেশন পরিকল্পনা সিস্টেম
Crop Rotation Planner Module
---------------------------------
মাটির স্বাস্থ্য বজায় রেখে ফসলের পরিকল্পনা করুন
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

ROTATION_DATA_FILE = "crop_rotations.json"

class CropRotationPlanner:
    def __init__(self):
        self.rotations = {
            "ধান-আলু": ["ধান", "আলু", "সবজি"],
            "ধান-গম": ["ধান", "গম", "লুপিন"],
            "ধান-চিনাবাদাম": ["ধান", "চিনাবাদাম", "লাউকি"],
            "ধান-পালংশাক": ["ধান", "পালংশাক", "রসুন"],
            "গম-আলু": ["গম", "আলু", "সবজি"],
            "স্ব-নির্ভর চক্র": ["ডাল", "তেল বীজ", "শস্য"]
        }
        self.data = self.load_data()
    
    def load_data(self):
        """পরিকল্পনা ডাটা লোড করুন"""
        if os.path.exists(ROTATION_DATA_FILE):
            with open(ROTATION_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """ডাটা সেভ করুন"""
        with open(ROTATION_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def get_rotation(self, plan_name):
        """রোটেশন পরিকল্পনা পান"""
        return self.rotations.get(plan_name, [])
    
    def add_plan(self, field_name, rotation_plan, start_year):
        """নতুন পরিকল্পনা যোগ করুন"""
        plan = {
            "id": len(self.data) + 1,
            "field": field_name,
            "rotation": rotation_plan,
            "start_year": start_year,
            "history": []
        }
        self.data.append(plan)
        self.save_data()
        return plan
    
    def get_next_crop(self, field_name, year):
        """পরবর্তী ফসল পান"""
        for plan in self.data:
            if plan['field'] == field_name:
                rotation = plan['rotation']
                years_passed = year - plan['start_year']
                index = years_passed % len(rotation)
                return rotation[index]
        return None


def open_crop_rotation_window(root):
    """ফসল রোটেশন পরিকল্পনা উইন্ডো খুলুন"""
    rotation_win = tk.Toplevel(root)
    rotation_win.title("📈 ফসল রোটেশন পরিকল্পনা")
    rotation_win.geometry("800x750")
    rotation_win.config(bg="#e8f5e9")
    
    planner = CropRotationPlanner()
    
    # ======= তথ্য ফ্রেম =======
    info_frame = tk.LabelFrame(rotation_win, text="📚 রোটেশন পরিকল্পনা", 
                               bg="#e8f5e9", font=("Arial", 11, "bold"))
    info_frame.pack(fill="x", padx=10, pady=10)
    
    info_text = tk.Text(info_frame, bg="white", font=("Courier", 9), height=4)
    info_text.pack(fill="x", padx=5, pady=5)
    info_text.config(state="disabled")
    
    def show_info():
        info_text.config(state="normal")
        info_text.delete(1.0, tk.END)
        text = "🔄 উপলব্ধ রোটেশন পরিকল্পনা:\n"
        for name, crops in planner.rotations.items():
            text += f"\n   {name}: {' → '.join(crops)}"
        info_text.insert(1.0, text)
        info_text.config(state="disabled")
    
    show_info()
    
    # ======= পরিকল্পনা তৈরি কাঠামো =======
    create_frame = tk.LabelFrame(rotation_win, text="✏️ নতুন পরিকল্পনা তৈরি করুন", 
                                 bg="#e8f5e9", font=("Arial", 11, "bold"), padx=15, pady=10)
    create_frame.pack(fill="x", padx=10, pady=10)
    
    # জমির নাম
    tk.Label(create_frame, text="জমির নাম:", bg="#e8f5e9", font=("Arial", 10)).pack(anchor="w", pady=5)
    field_entry = tk.Entry(create_frame, width=30)
    field_entry.pack(anchor="w", padx=20, pady=5)
    
    # রোটেশন নির্বাচন
    tk.Label(create_frame, text="রোটেশন পরিকল্পনা নির্বাচন করুন:", bg="#e8f5e9", font=("Arial", 10)).pack(anchor="w", pady=5)
    
    plan_var = tk.StringVar(value=list(planner.rotations.keys())[0])
    plan_menu = tk.OptionMenu(create_frame, plan_var, *planner.rotations.keys())
    plan_menu.config(bg="white", width=40)
    plan_menu.pack(anchor="w", padx=20, pady=5)
    
    # শুরু বছর
    year_frame = tk.Frame(create_frame, bg="#e8f5e9")
    year_frame.pack(anchor="w", padx=20, pady=5)
    
    tk.Label(year_frame, text="শুরু বছর:", bg="#e8f5e9", font=("Arial", 10)).pack(side="left", padx=5)
    year_entry = tk.Entry(year_frame, width=10)
    year_entry.pack(side="left", padx=5)
    year_entry.insert(0, "২০২৪")
    
    # ======= পরিকল্পনা প্রদর্শন ফ্রেম =======
    display_frame = tk.LabelFrame(rotation_win, text="📅 পরিকল্পনা বিবরণ", 
                                  bg="#e8f5e9", font=("Arial", 11, "bold"))
    display_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    display_text = tk.Text(display_frame, bg="white", font=("Courier", 10), height=15)
    display_text.pack(fill="both", expand=True, padx=5, pady=5)
    display_text.config(state="disabled")
    
    def preview_rotation():
        """রোটেশন প্রাকদর্শন দেখুন"""
        plan_name = plan_var.get()
        rotation = planner.get_rotation(plan_name)
        
        display_text.config(state="normal")
        display_text.delete(1.0, tk.END)
        
        output = f"""
🌾 {plan_name} রোটেশন প্রাকদর্শন
{'='*50}

3-বছরের চক্র:
"""
        for i, crop in enumerate(rotation, 1):
            output += f"\n  বছর {i}: {crop}"
        
        output += f"""

{'─'*50}

💡 সুবিধা:
  ✓ মাটির উর্বরতা বৃদ্ধি
  ✓ রোগ এবং কীটপতঙ্গ নিয়ন্ত্রণ
  ✓ জৈব উপাদান সংরক্ষণ
  ✓ ফলন বৃদ্ধি

⚠️ মনোযোগ:
  • প্রতি বছরে ফসল পরিবর্তন করুন
  • আবহাওয়া অনুযায়ী সমন্বয় করুন
  • স্থানীয় কৃষি অফিসের পরামর্শ নিন
"""
        
        display_text.insert(1.0, output)
        display_text.config(state="disabled")
    
    # ======= পরিকল্পনা তালিকা ফ্রেম =======
    list_frame = tk.LabelFrame(rotation_win, text="📋 সংরক্ষিত পরিকল্পনা", 
                               bg="#e8f5e9", font=("Arial", 11, "bold"))
    list_frame.pack(fill="x", padx=10, pady=10)
    
    tree = ttk.Treeview(list_frame, columns=("জমি", "প্রকার", "রোটেশন"), height=5, show='headings')
    
    for col in ["জমি", "প্রকার", "রোটেশন"]:
        tree.heading(col, text=col)
        tree.column(col, width=220)
    
    tree.pack(fill="x", padx=5, pady=5)
    
    def refresh_list():
        """তালিকা রিফ্রেশ করুন"""
        for item in tree.get_children():
            tree.delete(item)
        for plan in planner.data:
            rotation_str = " → ".join(plan['rotation'][:2])
            tree.insert('', 'end', values=(plan['field'], f"বছর {plan['start_year']}", rotation_str))
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(rotation_win, bg="#e8f5e9")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    def add_plan():
        """পরিকল্পনা যোগ করুন"""
        try:
            field = field_entry.get() or "অজানা জমি"
            plan_name = plan_var.get()
            year = int(year_entry.get())
            rotation = planner.get_rotation(plan_name)
            
            planner.add_plan(field, rotation, year)
            messagebox.showinfo("সফল", f"✅ {field} এর পরিকল্পনা যোগ হয়েছে!")
            field_entry.delete(0, tk.END)
            refresh_list()
        except ValueError:
            messagebox.showerror("ত্রুটি", "❌ বছর সংখ্যা হতে হবে")
    
    tk.Button(button_frame, text="👁️ প্রাকদর্শন", command=preview_rotation,
              bg="#4caf50", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="➕ পরিকল্পনা যোগ করুন", command=add_plan,
              bg="#2196f3", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 তালিকা রিফ্রেশ", command=refresh_list,
              bg="#ff9800", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=rotation_win.destroy,
              bg="#f44336", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    preview_rotation()
    refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Crop Rotation Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Rotation Planner", command=lambda: open_crop_rotation_window(root)).pack(pady=20)
    root.mainloop()
