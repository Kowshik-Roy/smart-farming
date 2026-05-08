"""
📊 সার ক্যালকুলেটর সিস্টেম
Fertilizer Calculator Module
---------------------------------
ফসল এবং জমির পরিমাণ অনুযায়ী সঠিক সার পরিমাণ নির্ণয় করুন
"""

import tkinter as tk
from tkinter import messagebox

# বিভিন্ন ফসলের সার প্রয়োজনীয়তা (প্রতি হেক্টর)
FERTILIZER_REQUIREMENTS = {
    "ধান": {
        "ইউরিয়া": 150,
        "টিএসপি": 60,
        "এমওপি": 40,
        "গোবর সার": 5000
    },
    "গম": {
        "ইউরিয়া": 120,
        "টিএসপি": 75,
        "এমওপি": 45,
        "সিংগল সুপার সালফেট": 50,
        "গোবর সার": 5000
    },
    "আলু": {
        "ইউরিয়া": 100,
        "টিএসপি": 100,
        "এমওপি": 150,
        "জিংক সালফেট": 25,
        "গোবর সার": 10000
    },
    "সবজি": {
        "ইউরিয়া": 120,
        "টিএসপি": 80,
        "এমওপি": 60,
        "গোবর সার": 8000
    }
}


def open_fertilizer_calculator_window(root):
    """সার ক্যালকুলেটর উইন্ডো খুলুন"""
    calc_win = tk.Toplevel(root)
    calc_win.title("📊 সার ক্যালকুলেটর")
    calc_win.geometry("700x700")
    calc_win.config(bg="#fff3e0")
    
    # ======= ইনপুট ফ্রেম =======
    input_frame = tk.LabelFrame(calc_win, text="📝 সার হিসাব করুন", 
                                bg="#fff3e0", font=("Arial", 11, "bold"), padx=15, pady=10)
    input_frame.pack(fill="x", padx=10, pady=10)
    
    # ফসল নির্বাচন
    tk.Label(input_frame, text="ফসল নির্বাচন করুন:", bg="#fff3e0", font=("Arial", 10)).pack(anchor="w", pady=5)
    crop_var = tk.StringVar(value="ধান")
    
    crops_frame = tk.Frame(input_frame, bg="#fff3e0")
    crops_frame.pack(anchor="w", padx=20, pady=5)
    
    for crop in FERTILIZER_REQUIREMENTS.keys():
        tk.Radiobutton(crops_frame, text=crop, variable=crop_var, value=crop,
                      bg="#fff3e0", font=("Arial", 10)).pack(side="left", padx=10)
    
    # জমির পরিমাণ
    tk.Label(input_frame, text="জমির পরিমাণ (দশমিক/হেক্টর):", bg="#fff3e0", font=("Arial", 10)).pack(anchor="w", pady=5)
    
    area_frame = tk.Frame(input_frame, bg="#fff3e0")
    area_frame.pack(anchor="w", padx=20, pady=5, fill="x")
    
    tk.Label(area_frame, text="দশমিক:", bg="#fff3e0", font=("Arial", 10)).pack(side="left", padx=5)
    decimal_entry = tk.Entry(area_frame, width=10)
    decimal_entry.pack(side="left", padx=5)
    
    tk.Label(area_frame, text="অথবা হেক্টর:", bg="#fff3e0", font=("Arial", 10)).pack(side="left", padx=30)
    hectare_entry = tk.Entry(area_frame, width=10)
    hectare_entry.pack(side="left", padx=5)
    
    # ======= ফলাফল ফ্রেম =======
    result_frame = tk.LabelFrame(calc_win, text="📋 নির্ধারিত সার পরিমাণ", 
                                 bg="#fff3e0", font=("Arial", 11, "bold"), padx=15, pady=10)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    result_text = tk.Text(result_frame, bg="white", font=("Arial", 11), height=20)
    result_text.pack(fill="both", expand=True, padx=5, pady=5)
    result_text.config(state="disabled")
    
    # ======= নির্দেশনা ফ্রেম =======
    note_frame = tk.Frame(calc_win, bg="#fbf1c7", relief="sunken", bd=1)
    note_frame.pack(fill="x", padx=10, pady=5)
    tk.Label(note_frame, text="💡 টিপস: জমির পরিমাণ শতক বা হেক্টার যেকোনো একটিতে দিন", 
            bg="#fbf1c7", font=("Arial", 9), fg="#e65100", justify="left").pack(anchor="w", padx=5, pady=3)
    
    def calculate():
        """সার পরিমাণ হিসাব করুন"""
        try:
            crop = crop_var.get()
            
            # জমির পরিমাণ রূপান্তর
            decimal = decimal_entry.get().strip()
            hectare = hectare_entry.get().strip()
            
            if decimal and not hectare:
                # দশমিক থেকে হেক্টার
                area_hectare = float(decimal) / 100
            elif hectare and not decimal:
                area_hectare = float(hectare)
            elif decimal and hectare:
                messagebox.showwarning("সতর্কতা", "❌ দুটি একসাথে দিবেন না, একটি দিন")
                return
            else:
                messagebox.showwarning("সতর্কতা", "❌ জমির পরিমাণ দিন")
                return
            
            # সার পরিমাণ হিসাব
            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            
            output = f"""
🌾 ফসল: {crop}
📏 জমির পরিমাণ: {area_hectare:.2f} হেক্টর ({area_hectare * 100:.0f} দশমিক)

{'='*60}
📊 প্রয়োজনীয় সার পরিমাণ:
{'='*60}

"""
            
            fertilizers = FERTILIZER_REQUIREMENTS[crop]
            for fert_name, qty_per_hectare in fertilizers.items():
                total_qty = qty_per_hectare * area_hectare
                if fert_name == "গোবর সার":
                    output += f"\n🌿 {fert_name}: {total_qty:.0f} কেজি"
                else:
                    output += f"\n💊 {fert_name}: {total_qty:.1f} কেজি"
            
            output += f"""

{'='*60}
💰 খরচ অনুমান (অনুমানিক):
{'='*60}

প্রতিটি সার কিনুন এবং খরচ লিপিবদ্ধ করুন:
   • ইউরিয়া (টাকা/কেজি): প্রায় ৩৫-৪০ টাকা
   • টিএসপি (টাকা/কেজি): প্রায় ৪৫-৫০ টাকা
   • এমওপি (টাকা/কেজি): প্রায় ৪০-৪৫ টাকা
   • গোবর সার: স্থানীয় বাজার দেখুন

{'='*60}
"""
            
            result_text.insert(1.0, output)
            result_text.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("ত্রুটি", "❌ সঠিক সংখ্যা দিন")
    
    def clear_results():
        """ফলাফল পরিষ্কার করুন"""
        decimal_entry.delete(0, tk.END)
        hectare_entry.delete(0, tk.END)
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.config(state="disabled")
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(calc_win, bg="#fff3e0")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Button(button_frame, text="🧮 হিসাব করুন", command=calculate,
              bg="#ff9800", fg="white", font=("Arial", 11, "bold"), padx=20, pady=8).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 পরিষ্কার করুন", command=clear_results,
              bg="#2196f3", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=calc_win.destroy,
              bg="#f44336", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Fertilizer Calculator Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Calculator", command=lambda: open_fertilizer_calculator_window(root)).pack(pady=20)
    root.mainloop()
