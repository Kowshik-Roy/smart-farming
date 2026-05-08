"""
🌾 স্মার্ট কৃষি অ্যাপ - নতুন ফিচার লঞ্চার
Smart Farming App - New Features Launcher
=========================================

এই প্রোগ্রাম সমস্ত নতুন ফিচার চালাতে পারে।
"""

import tkinter as tk
from tkinter import messagebox, Text, Scrollbar, VERTICAL
import sys

# সমস্ত নতুন ফিচার ইম্পোর্ট করুন
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
    print(f"❌ ফিচার ইম্পোর্ট ব্যর্থ: {e}")
    sys.exit(1)

class FeaturesLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🌾 নতুন ফিচার লঞ্চার")
        self.root.geometry("700x850")
        self.root.config(bg="#c8e6c9")
        
        # সেন্টার করুন
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 850) // 2
        root.geometry(f"700x850+{x}+{y}")
        
        self.features = [
            {
                "name": "🌾 কৃষি উৎপাদন ট্র্যাকিং",
                "desc": "ফসলের উৎপাদন এবং ফলন ট্র্যাক করুন",
                "func": open_production_tracker_window,
                "color": "#81c784"
            },
            {
                "name": "👨‍🌾 কৃষক প্রোফাইল সিস্টেম",
                "desc": "কৃষকের ব্যক্তিগত তথ্য এবং জমি পরিচালনা করুন",
                "func": open_farmer_profile_window,
                "color": "#66bb6a"
            },
            {
                "name": "🌏 জমির ম্যাপিং",
                "desc": "জমির অবস্থান এবং সীমানা চিহ্নিত করুন",
                "func": open_land_mapping_window,
                "color": "#4caf50"
            },
            {
                "name": "📊 সার ক্যালকুলেটর",
                "desc": "ফসল অনুযায়ী সঠিক সার পরিমাণ জানুন",
                "func": open_fertilizer_calculator_window,
                "color": "#388e3c"
            },
            {
                "name": "🚜 যন্ত্রপাতি ভাড়া সেবা",
                "desc": "কৃষি যন্ত্রপাতি ভাড়া এবং খরচ পরিচালনা করুন",
                "func": open_machinery_rental_window,
                "color": "#2e7d32"
            },
            {
                "name": "📱 বীজ ও সরঞ্জাম ডিরেক্টরি",
                "desc": "আপনার এলাকায় বীজ এবং সরঞ্জাম আপদ সরবরাহকারী খুঁজুন",
                "func": open_seeds_equipment_window,
                "color": "#7b1fa2"
            },
            {
                "name": "💰 ঋণ যোগ্যতা চেকার",
                "desc": "কৃষি ঋণের যোগ্যতা এবং সর্বোচ্চ সীমা জানুন",
                "func": open_loan_eligibility_window,
                "color": "#fbc02d"
            },
            {
                "name": "📈 ফসল রোটেশন পরিকল্পনা",
                "desc": "মাটির স্বাস্থ্য বজায় রেখে ফসল পরিকল্পনা করুন",
                "func": open_crop_rotation_window,
                "color": "#f57c00"
            },
            {
                "name": "🎥 ভিডিও টিউটোরিয়াল লাইব্রেরি",
                "desc": "চাষাবাদ সম্পর্কিত ভিডিও টিউটোরিয়াল সংগ্রহ করুন",
                "func": open_video_library_window,
                "color": "#e91e63"
            },
            {
                "name": "📋 রিপোর্ট এক্সপোর্ট সিস্টেম",
                "desc": "পরিকল্পনা এবং তথ্য PDF/টেক্সট ফাইলে রূপান্তর করুন",
                "func": open_report_export_window,
                "color": "#1565c0"
            }
        ]
        
        self.create_ui()
    
    def create_ui(self):
        """UI তৈরি করুন"""
        # শিরোনাম
        title_frame = tk.Frame(self.root, bg="#2e7d32")
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="🌾 স্মার্ট কৃষি অ্যাপ - নতুন ফিচার",
                font=("Arial", 16, "bold"), bg="#2e7d32", fg="white", pady=15).pack()
        
        # তথ্য ফ্রেম
        info_frame = tk.Frame(self.root, bg="#c8e6c9")
        info_frame.pack(fill="x", padx=15, pady=10)
        tk.Label(info_frame, text="✨ ১০টি নতুন ফিচার আপনার কৃষি অ্যাপে যুক্ত হয়েছে!",
                font=("Arial", 11), bg="#c8e6c9", fg="#1b5e20", wraplength=600, justify="left").pack(anchor="w")
        
        # ফিচার তালিকা ফ্রেম
        list_frame = tk.LabelFrame(self.root, text="📚 ফিচার তালিকা",
                                   bg="#c8e6c9", font=("Arial", 11, "bold"), padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # ক্যানভাস এবং স্ক্রোলবার
        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.config(yscrollcommand=scrollbar.set)
        
        # ফ্রেম ভিতরে ক্যানভাসে
        inner_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        # ফিচার বোতাম তৈরি করুন
        for i, feature in enumerate(self.features, 1):
            button_frame = tk.Frame(inner_frame, bg="white", relief="raised", bd=1)
            button_frame.pack(fill="x", padx=8, pady=8)
            
            # নম্বর এবং নাম
            header_frame = tk.Frame(button_frame, bg=feature['color'])
            header_frame.pack(fill="x", padx=2, pady=2)
            
            tk.Label(header_frame, text=f"{i}. {feature['name']}",
                    font=("Arial", 11, "bold"), bg=feature['color'],
                    fg="white", justify="left").pack(anchor="w", padx=10, pady=8)
            
            # বর্ণনা
            desc_frame = tk.Frame(button_frame, bg="white")
            desc_frame.pack(fill="x", padx=10, pady=(5, 10))
            
            tk.Label(desc_frame, text=feature['desc'],
                    font=("Arial", 9), bg="white", fg="#333333",
                    justify="left", wraplength=600).pack(anchor="w")
            
            # চালু বোতাম
            btn_frame = tk.Frame(button_frame, bg="white")
            btn_frame.pack(fill="x", padx=10, pady=(0, 8))
            
            tk.Button(btn_frame, text="▶️ চালু করুন",
                     command=lambda f=feature['func']: f(self.root),
                     bg=feature['color'], fg="white", font=("Arial", 10),
                     padx=20, pady=6, relief="raised", bd=1).pack(side="left")
        
        # আপডেট স্ক্রোল অঞ্চল
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # নিচের ফ্রেম
        bottom_frame = tk.Frame(self.root, bg="#c8e6c9")
        bottom_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Button(bottom_frame, text="💡 গাইড পড়ুন",
                 command=self.show_guide,
                 bg="#1976d2", fg="white", font=("Arial", 10), padx=20, pady=8).pack(side="left", padx=5)
        
        tk.Button(bottom_frame, text="❌ বন্ধ করুন",
                 command=self.root.quit,
                 bg="#d32f2f", fg="white", font=("Arial", 10), padx=20, pady=8).pack(side="right", padx=5)
    
    def show_guide(self):
        """গাইড দেখান"""
        guide_win = tk.Toplevel(self.root)
        guide_win.title("📚 নতুন ফিচার গাইড")
        guide_win.geometry("700x600")
        guide_win.config(bg="#e8f5e9")
        
        guide_text = tk.Text(guide_win, bg="white", font=("Courier", 9), wrap="word")
        guide_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        guide_content = """
📚 নতুন ফিচার ব্যবহার গাইড
========================

1️⃣ কৃষি উৎপাদন ট্র্যাকিং
   • আপনার প্রতিটি ফসলের উৎপাদন রেকর্ড করুন
   • জমি, বীজ, সার, পানি - সব কিছু ট্র্যাক করুন
   • প্রতি একরে ফলন হিসাব করুন

2️⃣ কৃষক প্রোফাইল
   • আপনার নাম, ফোন এবং জমির তথ্য সংরক্ষণ করুন
   • বহু কৃষকের তথ্য পরিচালনা করুন
   • সামগ্রিক পরিসংখ্যান দেখুন

3️⃣ জমির ম্যাপিং
   • প্রতিটি জমির অবস্থান চিহ্নিত করুন
   • মাটির ধরন এবং বর্তমান ফসল নোট করুন

4️⃣ সার ক্যালকুলেটর
   • ফসল নির্বাচন করুন
   • জমির পরিমাণ দিন (দশমিক বা হেক্টার)
   • প্রয়োজনীয় সার পরিমাণ স্বয়ংক্রিয়ভাবে পাবেন

5️⃣ যন্ত্রপাতি ভাড়া
   • ট্রাক্টর, ধানকাটা মেশিন ইত্যাদি ভাড়া নিন
   • খরচ স্বয়ংক্রিয়ভাবে হিসাব হয়

6️⃣ বীজ ও সরঞ্জাম ডিরেক্টরি
   • পণ্য অনুযায়ী সরবরাহকারী খুঁজুন
   • অঞ্চল অনুযায়ী ফিল্টার করুন

7️⃣ ঋণ যোগ্যতা চেকার
   • আপনার বয়স, জমি এবং অভিজ্ঞতা দিন
   • সর্বোচ্চ ঋণ সীমা জানুন

8️⃣ ফসল রোটেশন পরিকল্পনা
   • 3-বছরের চক্র অনুযায়ী ফসল পরিকল্পনা করুন
   • মাটির স্বাস্থ্য বজায় রাখুন

9️⃣ ভিডিও টিউটোরিয়াল
   • ধানচাষ, সার ব্যবস্থাপনা ইত্যাদি ভিডিও দেখুন
   • নতুন ভিডিও যোগ করুন

🔟 রিপোর্ট এক্সপোর্ট
   • আপনার পরিকল্পনা এবং তথ্য রিপোর্ট তৈরি করুন
   • PDF বা টেক্সট ফাইলে সংরক্ষণ করুন

💡 টিপস:
• প্রতিটি ফিচার স্বাধীনভাবে কাজ করে
• আপনার আসল main.py ফাইল সম্পূর্ণ অপরিবর্তিত
• যেকোনো সময় নতুন ফিচার যুক্ত করা যায়
• সব ডাটা JSON ফাইলে নিরাপদে সংরক্ষিত থাকে
"""
        
        guide_text.insert(1.0, guide_content)
        guide_text.config(state="disabled")


def main():
    root = tk.Tk()
    app = FeaturesLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
