"""
🚜 যন্ত্রপাতি ভাড়া সেবা সিস্টেম
Machinery Rental Service Module
---------------------------------
কৃষি যন্ত্রপাতি ভাড়া করুন এবং খরচ হিসাব করুন
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

MACHINERY_DATA_FILE = "machinery_rentals.json"

class MachineryRental:
    def __init__(self):
        self.machines = {
            "ট্রাক্টর": {"daily_rate": 1500, "weekly_rate": 8000, "capacity": "50 হর্সপাওয়ার"},
            "ধানকাটা মেশিন": {"daily_rate": 2000, "weekly_rate": 10000, "capacity": "প্রতিদিন 2-3 বিঘা"},
            "ধান খোলার মেশিন": {"daily_rate": 500, "weekly_rate": 2500, "capacity": "প্রতিঘণ্টায় 1 টন"},
            "বীজ বপন মেশিন": {"daily_rate": 800, "weekly_rate": 4000, "capacity": "প্রতিদিন 2 বিঘা"},
            "সেচপাম্প": {"daily_rate": 400, "weekly_rate": 2000, "capacity": "100-150 লিটার/মিনিট"},
            "ডিজেল ইঞ্জিন": {"daily_rate": 500, "weekly_rate": 2500, "capacity": "15 হর্সপাওয়ার"},
        }
        self.rentals = self.load_data()
    
    def load_data(self):
        """ভাড়া ডাটা লোড করুন"""
        if os.path.exists(MACHINERY_DATA_FILE):
            with open(MACHINERY_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """ডাটা সেভ করুন"""
        with open(MACHINERY_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.rentals, f, ensure_ascii=False, indent=4)
    
    def add_rental(self, machine_name, days, renter_name, contact, location):
        """নতুন ভাড়া রেকর্ড যোগ করুন"""
        if machine_name not in self.machines:
            return None
        
        machine = self.machines[machine_name]
        daily_cost = machine['daily_rate'] * days
        
        rental = {
            "id": len(self.rentals) + 1,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "machine": machine_name,
            "days": days,
            "renter": renter_name,
            "contact": contact,
            "location": location,
            "daily_rate": machine['daily_rate'],
            "total_cost": daily_cost,
            "status": "Active"
        }
        self.rentals.append(rental)
        self.save_data()
        return rental


def open_machinery_rental_window(root):
    """যন্ত্রপাতি ভাড়া উইন্ডো খুলুন"""
    rental_win = tk.Toplevel(root)
    rental_win.title("🚜 যন্ত্রপাতি ভাড়া সেবা")
    rental_win.geometry("750x700")
    rental_win.config(bg="#eceff1")
    
    rental = MachineryRental()
    
    # ======= যন্ত্রপাতি তথ্য ফ্রেম =======
    info_frame = tk.LabelFrame(rental_win, text="📋 উপলব্ধ যন্ত্রপাতি", 
                               bg="#eceff1", font=("Arial", 11, "bold"))
    info_frame.pack(fill="x", padx=10, pady=10)
    
    # যন্ত্রপাতি তালিকা
    machine_text = tk.Text(info_frame, bg="white", font=("Courier", 9), height=6)
    machine_text.pack(fill="x", padx=5, pady=5)
    machine_text.config(state="disabled")
    
    def show_machines():
        machine_text.config(state="normal")
        machine_text.delete(1.0, tk.END)
        text = "\n🚜 যন্ত্রপাতি         | 📊 দৈনিক ভাড়া | 📏 ক্ষমতা\n"
        text += "-" * 70 + "\n"
        for name, details in rental.machines.items():
            text += f"{name:20} | ৳{details['daily_rate']:8} | {details['capacity']}\n"
        machine_text.insert(1.0, text)
        machine_text.config(state="disabled")
    
    show_machines()
    
    # ======= ভাড়া রেকর্ড ফ্রেম =======
    record_frame = tk.LabelFrame(rental_win, text="📝 নতুন ভাড়া রেকর্ড", 
                                 bg="#eceff1", font=("Arial", 11, "bold"), padx=15, pady=10)
    record_frame.pack(fill="x", padx=10, pady=10)
    
    # যন্ত্রপাতি নির্বাচন
    tk.Label(record_frame, text="যন্ত্রপাতি নির্বাচন:", bg="#eceff1", font=("Arial", 10)).pack(anchor="w", pady=5)
    machine_var = tk.StringVar(value=list(rental.machines.keys())[0])
    
    machine_menu = tk.OptionMenu(record_frame, machine_var, *rental.machines.keys())
    machine_menu.config(bg="white", width=30)
    machine_menu.pack(anchor="w", padx=20, pady=5)
    
    # রেন্টার তথ্য
    info_sub = tk.Frame(record_frame, bg="#eceff1")
    info_sub.pack(fill="x", padx=20, pady=10)
    
    tk.Label(info_sub, text="রেন্টারের নাম:", bg="#eceff1").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    renter_entry = tk.Entry(info_sub, width=25)
    renter_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(info_sub, text="ফোন:", bg="#eceff1").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    phone_entry = tk.Entry(info_sub, width=15)
    phone_entry.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(info_sub, text="দিনের সংখ্যা:", bg="#eceff1").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    days_entry = tk.Entry(info_sub, width=10)
    days_entry.grid(row=1, column=1, padx=5, pady=5)
    
    tk.Label(info_sub, text="অবস্থান:", bg="#eceff1").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    location_entry = tk.Entry(info_sub, width=15)
    location_entry.grid(row=1, column=3, padx=5, pady=5)
    
    # ======= ভাড়া ক্যালকুলেটর ফ্রেম =======
    calc_frame = tk.LabelFrame(rental_win, text="💰 খরচ হিসাব", 
                               bg="#eceff1", font=("Arial", 11, "bold"), padx=15, pady=10)
    calc_frame.pack(fill="x", padx=10, pady=10)
    
    calc_display = tk.Text(calc_frame, bg="white", font=("Courier", 10), height=6)
    calc_display.pack(fill="x", padx=5, pady=5)
    calc_display.config(state="disabled")
    
    def calculate_cost(*args):
        try:
            machine = machine_var.get()
            days = int(days_entry.get() or 1)
            daily_rate = rental.machines[machine]['daily_rate']
            total = daily_rate * days
            
            text = f"""
🚜 {machine}
📊 দৈনিক ভাড়া: ৳{daily_rate}
📅 মেয়াদ: {days} দিন
━━━━━━━━━━━━━━━━
💰 মোট খরচ: ৳{total}
"""
            calc_display.config(state="normal")
            calc_display.delete(1.0, tk.END)
            calc_display.insert(1.0, text)
            calc_display.config(state="disabled")
        except:
            pass
    
    days_entry.bind("<KeyRelease>", calculate_cost)
    machine_var.trace("w", calculate_cost)
    
    # ======= ভাড়ার তালিকা ফ্রেম =======
    history_frame = tk.LabelFrame(rental_win, text="📜 ভাড়া ইতিহাস", 
                                  bg="#eceff1", font=("Arial", 11, "bold"))
    history_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(history_frame, columns=("যন্ত্র", "দিন", "খরচ", "রেন্টার", "অবস্থা"), height=8, show='headings')
    
    for col in ["যন্ত্র", "দিন", "খরচ", "রেন্টার", "অবস্থা"]:
        tree.heading(col, text=col)
        tree.column(col, width=130)
    
    tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    def refresh_history():
        for item in tree.get_children():
            tree.delete(item)
        for rec in rental.rentals:
            tree.insert('', 'end', values=(
                rec['machine'],
                f"{rec['days']} দিন",
                f"৳{rec['total_cost']}",
                rec['renter'],
                rec['status']
            ))
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(rental_win, bg="#eceff1")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    def add_rental():
        try:
            rental.add_rental(
                machine_var.get(),
                int(days_entry.get()),
                renter_entry.get() or "অজানা",
                phone_entry.get() or "০",
                location_entry.get() or "অজানা"
            )
            messagebox.showinfo("সফল", "✅ ভাড়া রেকর্ড যোগ হয়েছে!")
            renter_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            days_entry.delete(0, tk.END)
            location_entry.delete(0, tk.END)
            refresh_history()
        except:
            messagebox.showerror("ত্রুটি", "❌ ডাটা যাচাই করুন")
    
    tk.Button(button_frame, text="➕ ভাড়া যোগ করুন", command=add_rental,
              bg="#00796b", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 রিফ্রেশ", command=refresh_history,
              bg="#0097a7", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=rental_win.destroy,
              bg="#c62828", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    calculate_cost()
    refresh_history()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Machinery Rental Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Rental", command=lambda: open_machinery_rental_window(root)).pack(pady=20)
    root.mainloop()
