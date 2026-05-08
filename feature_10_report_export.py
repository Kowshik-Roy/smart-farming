"""
📋 রিপোর্ট এক্সপোর্ট সিস্টেম
Report Export System Module
---------------------------------
কৃষি পরিকল্পনা এবং তথ্য PDF/টেক্সট ফাইলে এক্সপোর্ট করুন
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import json
from datetime import datetime
import os

class ReportExporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def export_farming_plan(self, division, district, soil, season, crop, plant_time, fertilizer, water):
        """চাষাবাদ পরিকল্পনা রিপোর্ট তৈরি করুন"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          কৃষি চাষাবাদ পরিকল্পনা রিপোর্ট                  ║
╚══════════════════════════════════════════════════════════════╝

📅 রিপোর্ট তারিখ: {self.timestamp}

{'─'*62}
📍 ভৌগোলিক তথ্য:
{'─'*62}

বিভাগ:     {division}
জেলা:      {district}
মাটির ধরন: {soil}
মৌসুম:     {season}

{'─'*62}
🌾 ফসলের তথ্য:
{'─'*62}

সুপারিশকৃত ফসল: {crop}
বপনের সময়:      {plant_time}
সার ব্যবস্থাপনা:  {fertilizer}
পানি ব্যবস্থাপনা:  {water}

{'═'*62}

📌 সুপারিশ:
  • স্থানীয় কৃষি অফিসের সাথে পরামর্শ করুন
  • সঠিক সময়ে বীজ বপন করুন
  • মাটির পরীক্ষা করিয়ে সার প্রয়োগ করুন
  • নিয়মিত সেচ এবং যত্ন নিন

{'═'*62}
রিপোর্ট শেষ
"""
        return report
    
    def export_production_data(self, records):
        """উৎপাদন ডাটা রিপোর্ট তৈরি করুন"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          কৃষি উৎপাদন রেকর্ড রিপোর্ট                      ║
╚══════════════════════════════════════════════════════════════╝

📅 রিপোর্ট তারিখ: {self.timestamp}

"""
        if not records:
            report += "❌ কোন রেকর্ড পাওয়া যায়নি"
        else:
            report += f"{'─'*62}\n"
            report += f"{'ফসল':<15} {'জমি':<12} {'ফলন':<15} {'প্রতি একর':<15}\n"
            report += f"{'─'*62}\n"
            
            total_yield = 0
            for rec in records:
                report += f"{rec.get('crop', 'N/A'):<15} {str(rec.get('field_area', 0)):<12} "
                report += f"{str(rec.get('yield_kg', 0)):<15} {str(rec.get('yield_per_acre', 0)):<15}\n"
                total_yield += rec.get('yield_kg', 0)
            
            report += f"{'─'*62}\n"
            report += f"মোট উৎপাদন: {total_yield} কেজি\n"
            report += f"{'═'*62}\n"
        
        return report
    
    def export_financial_summary(self, cost, revenue, profit):
        """আর্থিক সারসংক্ষেপ রিপোর্ট"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          কৃষি আর্থিক সারসংক্ষেপ রিপোর্ট                  ║
╚══════════════════════════════════════════════════════════════╝

📅 রিপোর্ট তারিখ: {self.timestamp}

{'─'*62}
💰 আর্থিক বিবরণ:
{'─'*62}

মোট খরচ:          ৳{cost:,}
মোট আয়:          ৳{revenue:,}
আপনার লাভ:       ৳{profit:,}
লাভের হার (%):   {(profit/revenue*100) if revenue > 0 else 0:.2f}%

{'═'*62}
রিপোর্ট শেষ
"""
        return report


def open_report_export_window(root):
    """রিপোর্ট এক্সপোর্ট উইন্ডো খুলুন"""
    export_win = tk.Toplevel(root)
    export_win.title("📋 রিপোর্ট এক্সপোর্ট সিস্টেম")
    export_win.geometry("750x700")
    export_win.config(bg="#fff9c4")
    
    exporter = ReportExporter()
    
    # ======= শিরোনাম ফ্রেম =======
    title_frame = tk.Frame(export_win, bg="#fbc02d")
    title_frame.pack(fill="x")
    tk.Label(title_frame, text="📋 রিপোর্ট এক্সপোর্ট সিস্টেম", 
            font=("Arial", 14, "bold"), bg="#fbc02d", fg="white", pady=10).pack()
    
    # ======= রিপোর্ট ধরন নির্বাচন ফ্রেম =======
    type_frame = tk.LabelFrame(export_win, text="📑 রিপোর্ট ধরন নির্বাচন করুন", 
                               bg="#fff9c4", font=("Arial", 11, "bold"), padx=15, pady=10)
    type_frame.pack(fill="x", padx=10, pady=10)
    
    report_var = tk.StringVar(value="চাষাবাদ")
    
    tk.Radiobutton(type_frame, text="🌾 চাষাবাদ পরিকল্পনা", variable=report_var, value="চাষাবাদ",
                  bg="#fff9c4", font=("Arial", 10)).pack(anchor="w", padx=20, pady=5)
    tk.Radiobutton(type_frame, text="📊 উৎপাদন রেকর্ড", variable=report_var, value="উৎপাদন",
                  bg="#fff9c4", font=("Arial", 10)).pack(anchor="w", padx=20, pady=5)
    tk.Radiobutton(type_frame, text="💰 আর্থিক সারসংক্ষেপ", variable=report_var, value="আর্থিক",
                  bg="#fff9c4", font=("Arial", 10)).pack(anchor="w", padx=20, pady=5)
    
    # ======= ডাটা ইনপুট ফ্রেম =======
    data_frame = tk.LabelFrame(export_win, text="📝 ডাটা প্রবেশ করুন", 
                               bg="#fff9c4", font=("Arial", 11, "bold"), padx=15, pady=10)
    data_frame.pack(fill="x", padx=10, pady=10)
    
    # দ্রুত ডাটা
    tk.Label(data_frame, text="ফসলের নাম:", bg="#fff9c4", font=("Arial", 10)).pack(anchor="w", pady=3)
    crop_entry = tk.Entry(data_frame, width=40)
    crop_entry.pack(anchor="w", padx=20, pady=3)
    
    tk.Label(data_frame, text="অঞ্চল:", bg="#fff9c4", font=("Arial", 10)).pack(anchor="w", pady=3)
    
    location_sub = tk.Frame(data_frame, bg="#fff9c4")
    location_sub.pack(anchor="w", padx=20, pady=3)
    
    tk.Label(location_sub, text="বিভাগ:", bg="#fff9c4").pack(side="left", padx=5)
    division_entry = tk.Entry(location_sub, width=15)
    division_entry.pack(side="left", padx=5)
    
    tk.Label(location_sub, text="জেলা:", bg="#fff9c4").pack(side="left", padx=15)
    district_entry = tk.Entry(location_sub, width=15)
    district_entry.pack(side="left", padx=5)
    
    # ======= রিপোর্ট প্রদর্শন ফ্রেম =======
    display_frame = tk.LabelFrame(export_win, text="📌 রিপোর্ট প্রাকদর্শন", 
                                  bg="#fff9c4", font=("Arial", 11, "bold"))
    display_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    report_text = tk.Text(display_frame, bg="white", font=("Courier", 9), wrap="word")
    report_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    def generate_preview():
        """প্রাকদর্শন তৈরি করুন"""
        report_type = report_var.get()
        
        if report_type == "চাষাবাদ":
            preview = exporter.export_farming_plan(
                division_entry.get() or "অজানা",
                district_entry.get() or "অজানা",
                "দোআঁশ",
                "খরিফ-১",
                crop_entry.get() or "ধান",
                "মে-জুন",
                "ইউরিয়া ২৫০ কেজি/হেক্টর",
                "নিয়মিত সেচ প্রয়োজন"
            )
        elif report_type == "উৎপাদন":
            preview = exporter.export_production_data([])
        else:
            preview = exporter.export_financial_summary(50000, 100000, 50000)
        
        report_text.delete(1.0, tk.END)
        report_text.insert(1.0, preview)
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(export_win, bg="#fff9c4")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    def export_to_file():
        """ফাইলে এক্সপোর্ট করুন"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report_text.get(1.0, tk.END))
                messagebox.showinfo("সফল", f"✅ রিপোর্ট সফলভাবে সংরক্ষিত হয়েছে!\n{file_path}")
        except Exception as e:
            messagebox.showerror("ত্রুটি", f"❌ ফাইল সংরক্ষণ ব্যর্থ: {e}")
    
    def copy_to_clipboard():
        """ক্লিপবোর্ডে কপি করুন"""
        try:
            text = report_text.get(1.0, tk.END)
            export_win.clipboard_clear()
            export_win.clipboard_append(text)
            messagebox.showinfo("সফল", "✅ রিপোর্ট ক্লিপবোর্ডে কপি হয়েছে!")
        except:
            messagebox.showerror("ত্রুটি", "❌ ক্লিপবোর্ড অপারেশন ব্যর্থ")
    
    tk.Button(button_frame, text="👁️ প্রাকদর্শন", command=generate_preview,
              bg="#fbc02d", fg="black", font=("Arial", 11, "bold"), padx=20, pady=8).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="💾 ফাইলে সংরক্ষণ", command=export_to_file,
              bg="#4caf50", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="📋 কপি করুন", command=copy_to_clipboard,
              bg="#2196f3", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=export_win.destroy,
              bg="#f44336", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    generate_preview()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Report Export Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Export", command=lambda: open_report_export_window(root)).pack(pady=20)
    root.mainloop()
