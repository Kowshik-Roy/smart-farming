"""
🎥 ভিডিও টিউটোরিয়াল লাইব্রেরি সিস্টেম
Video Tutorial Library Module
---------------------------------
চাষাবাদ সম্পর্কিত ভিডিও টিউটোরিয়াল এবং গাইড সংরক্ষণ করুন
"""

import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import webbrowser

VIDEOS_DATA_FILE = "video_library.json"

class VideoLibrary:
    def __init__(self):
        self.videos = self.load_data()
        if not self.videos:
            self.videos = self.get_default_videos()
            self.save_data()
    
    def load_data(self):
        """ভিডিও ডাটা লোড করুন"""
        if os.path.exists(VIDEOS_DATA_FILE):
            with open(VIDEOS_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """ডাটা সেভ করুন"""
        with open(VIDEOS_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.videos, f, ensure_ascii=False, indent=4)
    
    def get_default_videos(self):
        """ডিফল্ট ভিডিও পরামর্শ"""
        return [
            {
                "id": 1,
                "title": "ধান চাষের সম্পূর্ণ পদ্ধতি",
                "category": "ধান",
                "duration": "15:32",
                "language": "বাংলা",
                "url": "https://youtube.com/watch?v=example1",
                "channel": "কৃষি শিক্ষা",
                "views": "50K",
                "rating": 4.5
            },
            {
                "id": 2,
                "title": "জৈব সার তৈরির পদ্ধতি",
                "category": "সার ব্যবস্থাপনা",
                "duration": "12:45",
                "language": "বাংলা",
                "url": "https://youtube.com/watch?v=example2",
                "channel": "জৈব কৃষি",
                "views": "30K",
                "rating": 4.7
            },
            {
                "id": 3,
                "title": "আলু চাষে বীজ নির্বাচন এবং রোপণ",
                "category": "আলু",
                "duration": "10:20",
                "language": "বাংলা",
                "url": "https://youtube.com/watch?v=example3",
                "channel": "আলু উৎপাদন",
                "views": "25K",
                "rating": 4.3
            }
        ]
    
    def add_video(self, title, category, duration, language, url, channel, rating=0):
        """নতুন ভিডিও যোগ করুন"""
        video = {
            "id": len(self.videos) + 1,
            "title": title,
            "category": category,
            "duration": duration,
            "language": language,
            "url": url,
            "channel": channel,
            "views": "নতুন",
            "rating": rating
        }
        self.videos.append(video)
        self.save_data()
        return video
    
    def search_by_category(self, category):
        """ক্যাটাগরি দ্বারা খুঁজুন"""
        return [v for v in self.videos if v['category'].lower() == category.lower()]
    
    def get_categories(self):
        """সকল ক্যাটাগরি পান"""
        categories = set(v['category'] for v in self.videos)
        return list(categories)


def open_video_library_window(root):
    """ভিডিও লাইব্রেরি উইন্ডো খুলুন"""
    video_win = tk.Toplevel(root)
    video_win.title("🎥 ভিডিও টিউটোরিয়াল লাইব্রেরি")
    video_win.geometry("900x800")
    video_win.config(bg="#f5f5f5")
    
    library = VideoLibrary()
    
    # ======= অনুসন্ধান ফ্রেম =======
    search_frame = tk.LabelFrame(video_win, text="🔍 ভিডিও খুঁজুন", 
                                 bg="#f5f5f5", font=("Arial", 11, "bold"), padx=15, pady=10)
    search_frame.pack(fill="x", padx=10, pady=10)
    
    # ক্যাটাগরি নির্বাচন
    tk.Label(search_frame, text="ক্যাটাগরি:", bg="#f5f5f5", font=("Arial", 10)).pack(side="left", padx=5)
    category_var = tk.StringVar(value="সব")
    
    categories = ["সব"] + library.get_categories()
    category_menu = tk.OptionMenu(search_frame, category_var, *categories)
    category_menu.pack(side="left", padx=5)
    
    # ভাষা নির্বাচন
    tk.Label(search_frame, text="ভাষা:", bg="#f5f5f5", font=("Arial", 10)).pack(side="left", padx=30)
    lang_var = tk.StringVar(value="সব")
    lang_menu = tk.OptionMenu(search_frame, lang_var, "সব", "বাংলা", "ইংরেজি", "হিন্দি")
    lang_menu.pack(side="left", padx=5)
    
    # ======= ভিডিও লিস্ট ফ্রেম =======
    list_frame = tk.LabelFrame(video_win, text="📽️ উপলব্ধ ভিডিওচিত্র", 
                               bg="#f5f5f5", font=("Arial", 11, "bold"))
    list_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(list_frame, columns=("শিরোনাম", "ক্যাটাগরি", "সময়", "রেটিং", "চ্যানেল"), 
                        height=15, show='headings')
    
    for col in ["শিরোনাম", "ক্যাটাগরি", "সময়", "রেটিং", "চ্যানেল"]:
        tree.heading(col, text=col)
        if col == "শিরোনাম":
            tree.column(col, width=300)
        elif col == "চ্যানেল":
            tree.column(col, width=150)
        else:
            tree.column(col, width=80)
    
    tree.pack(fill="both", expand=True, padx=5, pady=5)
    
    def refresh_list():
        """তালিকা রিফ্রেশ করুন"""
        for item in tree.get_children():
            tree.delete(item)
        
        videos_to_show = library.videos
        
        # ক্যাটাগরি ফিল্টার
        if category_var.get() != "সব":
            videos_to_show = [v for v in videos_to_show if v['category'] == category_var.get()]
        
        # ভাষা ফিল্টার
        if lang_var.get() != "সব":
            videos_to_show = [v for v in videos_to_show if v['language'] == lang_var.get()]
        
        for video in videos_to_show:
            tree.insert('', 'end', values=(
                video['title'],
                video['category'],
                video['duration'],
                f"⭐ {video['rating']}",
                video['channel']
            ))
    
    def play_video():
        """নির্বাচিত ভিডিও চালান"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("সতর্কতা", "❌ একটি ভিডিও নির্বাচন করুন")
            return
        
        # নির্বাচিত আইটেম পান
        item = selected[0]
        values = tree.item(item, 'values')
        title = values[0]
        
        # ভিডিও খুঁজুন এবং চালান
        for video in library.videos:
            if video['title'] == title:
                webbrowser.open(video['url'])
                messagebox.showinfo("চালু হচ্ছে", f"🎥 ভিডিও চালু হচ্ছে: {title}")
                return
    
    # ======= নতুন ভিডিও যোগ করার ফ্রেম =======
    add_frame = tk.LabelFrame(video_win, text="➕ নতুন ভিডিও যোগ করুন", 
                              bg="#f5f5f5", font=("Arial", 11, "bold"), padx=15, pady=10)
    add_frame.pack(fill="x", padx=10, pady=10)
    
    add_sub = tk.Frame(add_frame, bg="#f5f5f5")
    add_sub.pack(fill="x")
    
    tk.Label(add_sub, text="শিরোনাম:", bg="#f5f5f5").grid(row=0, column=0, sticky="w", padx=5, pady=3)
    title_entry = tk.Entry(add_sub, width=30)
    title_entry.grid(row=0, column=1, padx=5, pady=3)
    
    tk.Label(add_sub, text="ক্যাটাগরি:", bg="#f5f5f5").grid(row=0, column=2, sticky="w", padx=5, pady=3)
    category_entry = tk.Entry(add_sub, width=20)
    category_entry.grid(row=0, column=3, padx=5, pady=3)
    
    tk.Label(add_sub, text="URL:", bg="#f5f5f5").grid(row=1, column=0, sticky="w", padx=5, pady=3)
    url_entry = tk.Entry(add_sub, width=30)
    url_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=3, sticky="ew")
    
    def add_video():
        """নতুন ভিডিও যোগ করুন"""
        try:
            library.add_video(
                title_entry.get() or "বিনা শিরোনাম",
                category_entry.get() or "অন্যান্য",
                "00:00",
                "বাংলা",
                url_entry.get() or "#",
                "ব্যবহারকারী যোগ করা"
            )
            messagebox.showinfo("সফল", "✅ ভিডিও যোগ হয়েছে!")
            title_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            url_entry.delete(0, tk.END)
            refresh_list()
        except:
            messagebox.showerror("ত্রুটি", "❌ ডাটা যাচাই করুন")
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(video_win, bg="#f5f5f5")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Button(button_frame, text="▶️ চালান", command=play_video,
              bg="#e91e63", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="➕ যোগ করুন", command=add_video,
              bg="#2196f3", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 রিফ্রেশ", command=refresh_list,
              bg="#ff9800", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=video_win.destroy,
              bg="#f44336", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Video Library Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Library", command=lambda: open_video_library_window(root)).pack(pady=20)
    root.mainloop()
