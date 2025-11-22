
import json
import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox

JSON_FILE = "farm_guide.json"


def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} পাওয়া যায়নি।")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def scan_images_folder():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(base_dir, "images")
    if not os.path.exists(images_dir):
        print("Warning: images folder নেই।")
        return []
    return [os.path.join(images_dir, f) for f in os.listdir(images_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))]


class FarmApp(tk.Tk):
    def __init__(self, data):
        super().__init__()
        self.title(f"Farm Guide - {data.get('crop','Crop')}")
        self.geometry("950x650")
        self.configure(bg="#f0f8ff")  
        self.data = data
        self.image_index = 0
        self.images = scan_images_folder()
        self.photo_cache = [None] * len(self.images)
        self.create_styles()
        self.create_widgets()

    def create_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')  
        style.configure("TFrame", background="#f0f8ff")
        style.configure("TLabel", background="#f0f8ff", font=("Helvetica", 12))
        style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#2e8b57")
        style.configure("TButton", font=("Helvetica", 11, "bold"), foreground="white", background="#2e8b57")
        style.map("TButton", background=[('active', '#3cb371')])

    def create_widgets(self):
      
        left = ttk.Frame(self)
        left.pack(side="left", fill="y", padx=15, pady=15)

        lbl = ttk.Label(left, text=f"{self.data.get('crop','')} — {self.data.get('variety','')}", style="Header.TLabel")
        lbl.pack(pady=10)

        txt_frame = ttk.Frame(left)
        txt_frame.pack()
        txt = tk.Text(txt_frame, width=50, height=30, wrap="word", bg="#ffffff", fg="#000000", font=("Helvetica", 11))
        txt.pack()

       
        txt.insert("end", "=== সার ব্যবহার ===\n\n")
        for f in self.data.get("fertilizer_use", []):
            txt.insert("end", f"{f['stage']}\n  {f['fertilizer']} — {f['amount']}\n  {f['instructions']}\n\n")

       
        txt.insert("end", "=== কীটনাশক/রোগ ===\n\n")
        for p in self.data.get("pesticide_use", []):
            txt.insert("end", f"{p['problem']}\n  {p['product']} ({p['dose']})\n  {p['method']}\n  সতর্কতা: {p['safety']}\n\n")

     
        txt.insert("end", "=== ক্যালেন্ডার ===\n\n")
        for m, tasks in self.data.get("calendar_view", {}).items():
            txt.insert("end", f"{m}: {', '.join(tasks)}\n")

      
        txt.insert("end", f"\nনোট: {self.data.get('notes','')}\n")
        txt.config(state="disabled")

      
        right = ttk.Frame(self)
        right.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.canvas = tk.Canvas(right, width=500, height=400, bg="#e0ffff", bd=2, relief="ridge")
        self.canvas.pack()

        btn_frame = ttk.Frame(right)
        btn_frame.pack(pady=10)
        prev_btn = ttk.Button(btn_frame, text="◀ পূর্বের", command=self.show_prev)
        prev_btn.pack(side="left", padx=10)
        next_btn = ttk.Button(btn_frame, text="পরের ▶", command=self.show_next)
        next_btn.pack(side="left", padx=10)

        if self.images:
            self.show_image(0)
        else:
            self.canvas.create_text(250, 200, text="কোন ছবি নেই", font=("Helvetica", 14), fill="red")

 
    def show_image(self, idx):
        if not self.images:
            return
        path = self.images[idx]
        print("Loading image:", path)  # debug
        if self.photo_cache[idx] is None:
            try:
                img = Image.open(path)
                img.thumbnail((500, 400))
                self.photo_cache[idx] = ImageTk.PhotoImage(img)
            except Exception as e:
                self.canvas.delete("all")
                self.canvas.create_text(250, 200, text=f"Error loading image:\n{e}", font=("Helvetica", 12), fill="red")
                return
        self.canvas.delete("all")
        self.canvas.create_image(250, 200, image=self.photo_cache[idx])

    def show_next(self):
        if not self.images: return
        self.image_index = (self.image_index + 1) % len(self.images)
        self.show_image(self.image_index)

    def show_prev(self):
        if not self.images: return
        self.image_index = (self.image_index - 1) % len(self.images)
        self.show_image(self.image_index)


def main():
    try:
        data = load_json(JSON_FILE)
    except FileNotFoundError:
        messagebox.showerror("Error", f"{JSON_FILE} পাওয়া যায়নি। একই ফোল্ডারে রাখুন।")
        return
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"JSON ফাইল পড়তে সমস্যা: {e}")
        return

    app = FarmApp(data)
    app.mainloop()

if __name__ == "__main__":
    main()
