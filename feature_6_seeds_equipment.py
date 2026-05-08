"""
📱 বীজ ও সরঞ্জাম ডিরেক্টরি সিস্টেম
Seeds & Equipment Directory Module
---------------------------------
স্থানীয় বীজের দোকান এবং সরঞ্জাম সরবরাহকারী খুঁজে পান
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

SEEDS_DATA_FILE = "seeds_equipment_directory.json"

class SeedsEquipmentDirectory:
    def __init__(self):
        self.data = self.load_data()
        if not self.data:
            self.data = self.get_default_data()
            self.save_data()
    
    def load_data(self):
        """ডিরেক্টরি ডাটা লোড করুন"""
        if os.path.exists(SEEDS_DATA_FILE):
            with open(SEEDS_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """ডাটা সেভ করুন"""
        with open(SEEDS_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def get_default_data(self):
        """ডিফল্ট ডাটা রিটার্ন করুন"""
        return [
            {
                "id": 1,
                "name": "রফি বীজের দোকান",
                "type": "বীজ সরবরাহকারী",
                "products": ["ধানের বীজ", "গমের বীজ", "আলুর বীজ"],
                "division": "ঢাকা",
                "district": "ঢাকা",
                "location": "নিউ মার্কেট",
                "phone": "০১৭XX-XXXXXX",
                "rating": 4.5
            },
            {
                "id": 2,
                "name": "আহমেদ কৃষি দোকান",
                "type": "সম্পূর্ণ সরঞ্জাম",
                "products": ["সার", "কীটনাশক", "সরঞ্জাম"],
                "division": "চট্টগ্রাম",
                "district": "চট্টগ্রাম",
                "location": "আন্দারকিল্লা",
                "phone": "০১৮XX-XXXXXX",
                "rating": 4.2
            }
        ]
    
    def add_store(self, name, store_type, products, division, district, location, phone, rating=0):
        """নতুন দোকান যোগ করুন"""
        store = {
            "id": len(self.data) + 1,
            "name": name,
            "type": store_type,
            "products": products if isinstance(products, list) else [products],
            "division": division,
            "district": district,
            "location": location,
            "phone": phone,
            "rating": rating
        }
        self.data.append(store)
        self.save_data()
        return store
    
    def search_by_product(self, product_name):
        """পণ্য অনুযায়ী খুঁজুন"""
        return [s for s in self.data if product_name.lower() in [p.lower() for p in s['products']]]
    
    def search_by_location(self, division):
        """অঞ্চল অনুযায়ী খুঁজুন"""
        return [s for s in self.data if s['division'].lower() == division.lower()]


def open_seeds_equipment_window(root):
    """বীজ ও সরঞ্জাম ডিরেক্টরি উইন্ডো খুলুন"""
    dir_win = tk.Toplevel(root)
    dir_win.title("📱 বীজ ও সরঞ্জাম ডিরেক্টরি")
    dir_win.geometry("800x750")
    dir_win.config(bg="#f3e5f5")
    
    directory = SeedsEquipmentDirectory()
    
    # ======= অনুসন্ধান ফ্রেম =======
    search_frame = tk.LabelFrame(dir_win, text="🔍 অনুসন্ধান করুন", 
                                 bg="#f3e5f5", font=("Arial", 11, "bold"), padx=15, pady=10)
    search_frame.pack(fill="x", padx=10, pady=10)
    
    # অনুসন্ধান বিকল্প
    search_type_frame = tk.Frame(search_frame, bg="#f3e5f5")
    search_type_frame.pack(anchor="w", pady=5)
    
    search_var = tk.StringVar(value="পণ্য")
    tk.Radiobutton(search_type_frame, text="📦 পণ্য অনুযায়ী", variable=search_var, value="পণ্য",
                  bg="#f3e5f5", font=("Arial", 10)).pack(side="left", padx=10)
    tk.Radiobutton(search_type_frame, text="📍 অঞ্চল অনুযায়ী", variable=search_var, value="অঞ্চল",
                  bg="#f3e5f5", font=("Arial", 10)).pack(side="left", padx=10)
    
    # অনুসন্ধান ইনপুট
    input_frame = tk.Frame(search_frame, bg="#f3e5f5")
    input_frame.pack(fill="x", pady=5)
    
    tk.Label(input_frame, text="অনুসন্ধান:", bg="#f3e5f5", font=("Arial", 10)).pack(side="left", padx=5)
    search_entry = tk.Entry(input_frame, width=30)
    search_entry.pack(side="left", padx=5)
    
    # ======= দোকানের তালিকা ফ্রেম =======
    list_frame = tk.LabelFrame(dir_win, text="📋 দোকান এবং সরবরাহকারী", 
                               bg="#f3e5f5", font=("Arial", 11, "bold"))
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # ট্রি ভিউ
    columns = ("দোকানের নাম", "ধরন", "পণ্য", "অঞ্চল", "ফোন", "রেটিং")
    tree = ttk.Treeview(list_frame, columns=columns, height=15, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        if col == "পণ্য":
            tree.column(col, width=150)
        elif col == "দোকানের নাম":
            tree.column(col, width=140)
        else:
            tree.column(col, width=100)
    
    tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    def refresh_list(stores=None):
        """তালিকা রিফ্রেশ করুন"""
        for item in tree.get_children():
            tree.delete(item)
        
        if stores is None:
            stores = directory.data
        
        for store in stores:
            products_str = ", ".join(store['products'][:2])
            if len(store['products']) > 2:
                products_str += "..."
            
            tree.insert('', 'end', values=(
                store['name'],
                store['type'],
                products_str,
                store['division'],
                store['phone'],
                f"⭐ {store['rating']}"
            ))
    
    def search():
        """অনুসন্ধান করুন"""
        search_text = search_entry.get().strip()
        if not search_text:
            refresh_list()
            return
        
        if search_var.get() == "পণ্য":
            results = directory.search_by_product(search_text)
        else:
            results = directory.search_by_location(search_text)
        
        if results:
            refresh_list(results)
        else:
            messagebox.showinfo("ফলাফল", "❌ কোন দোকান পাওয়া যায়নি")
            refresh_list()
    
    # ======= নতুন দোকান যোগ করার ফ্রেম =======
    add_frame = tk.LabelFrame(dir_win, text="➕ নতুন দোকান যোগ করুন", 
                              bg="#f3e5f5", font=("Arial", 11, "bold"), padx=15, pady=10)
    add_frame.pack(fill="x", padx=10, pady=10)
    
    add_sub = tk.Frame(add_frame, bg="#f3e5f5")
    add_sub.pack(fill="x")
    
    tk.Label(add_sub, text="দোকানের নাম:", bg="#f3e5f5").grid(row=0, column=0, sticky="w", padx=5, pady=3)
    store_name_entry = tk.Entry(add_sub, width=25)
    store_name_entry.grid(row=0, column=1, padx=5, pady=3)
    
    tk.Label(add_sub, text="ধরন:", bg="#f3e5f5").grid(row=0, column=2, sticky="w", padx=5, pady=3)
    type_var = tk.StringVar(value="বীজ সরবরাহকারী")
    type_menu = tk.OptionMenu(add_sub, type_var, "বীজ সরবরাহকারী", "সম্পূর্ণ সরঞ্জাম", "সার বিক্রেতা")
    type_menu.grid(row=0, column=3, padx=5, pady=3)
    
    tk.Label(add_sub, text="ফোন:", bg="#f3e5f5").grid(row=1, column=0, sticky="w", padx=5, pady=3)
    phone_entry = tk.Entry(add_sub, width=25)
    phone_entry.grid(row=1, column=1, padx=5, pady=3)
    
    tk.Label(add_sub, text="অঞ্চল:", bg="#f3e5f5").grid(row=1, column=2, sticky="w", padx=5, pady=3)
    location_entry = tk.Entry(add_sub, width=20)
    location_entry.grid(row=1, column=3, padx=5, pady=3)
    
    def add_store():
        """নতুন দোকান যোগ করুন"""
        try:
            directory.add_store(
                store_name_entry.get() or "অজানা",
                type_var.get(),
                search_entry.get() or "বিভিন্ন",
                location_entry.get() or "অজানা",
                "অজানা",
                "অজানা",
                phone_entry.get() or "০"
            )
            messagebox.showinfo("সফল", "✅ দোকান যোগ হয়েছে!")
            store_name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            location_entry.delete(0, tk.END)
            refresh_list()
        except:
            messagebox.showerror("ত্রুটি", "❌ ডাটা যাচাই করুন")
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(dir_win, bg="#f3e5f5")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Button(button_frame, text="🔍 অনুসন্ধান", command=search,
              bg="#7b1fa2", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="➕ যোগ করুন", command=add_store,
              bg="#6a1b9a", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 সব দেখুন", command=refresh_list,
              bg="#512da8", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=dir_win.destroy,
              bg="#d32f2f", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Seeds & Equipment Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Directory", command=lambda: open_seeds_equipment_window(root)).pack(pady=20)
    root.mainloop()
