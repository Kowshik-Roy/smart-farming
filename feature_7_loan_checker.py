"""
💰 ঋণ যোগ্যতা চেকার সিস্টেম
Loan Eligibility Checker Module
---------------------------------
কৃষকদের কৃষি ঋণের যোগ্যতা নির্ধারণ করুন
"""

import tkinter as tk
from tkinter import messagebox

class LoanEligibilityChecker:
    def __init__(self):
        self.rules = {
            "বয়স": {"min": 18, "max": 65},
            "ন্যূনতম জমি": {"min": 0.5},  # শতাংশ
            "ন্যূনতম অভিজ্ঞতা": {"min": 1},  # বছর
            "সর্বোচ্চ ঋণ": {"max_per_acre": 50000}  # টাকা
        }
    
    def check_eligibility(self, age, land_area_decimal, farming_experience, previous_loans=0):
        """ঋণ যোগ্যতা চেক করুন"""
        is_eligible = True
        reasons = []
        
        # বয়স চেক
        if age < self.rules["বয়স"]["min"] or age > self.rules["বয়স"]["max"]:
            is_eligible = False
            reasons.append(f"❌ বয়স সীমা বাইরে ({self.rules['বয়স']['min']}-{self.rules['বয়স']['max']} বছর)")
        else:
            reasons.append(f"✅ বয়স যোগ্য ({age} বছর)")
        
        # জমির পরিমাণ চেক
        land_area_percent = land_area_decimal / 100
        if land_area_percent < self.rules["ন্যূনতম জমি"]["min"]:
            is_eligible = False
            reasons.append(f"❌ জমির পরিমাণ কম ({land_area_decimal} দশমিক)")
        else:
            reasons.append(f"✅ জমির পরিমাণ যোগ্য ({land_area_decimal} দশমিক)")
        
        # অভিজ্ঞতা চেক
        if farming_experience < self.rules["ন্যূনতম অভিজ্ঞতা"]["min"]:
            is_eligible = False
            reasons.append(f"❌ কৃষি অভিজ্ঞতা কম ({farming_experience} বছর)")
        else:
            reasons.append(f"✅ অভিজ্ঞতা যোগ্য ({farming_experience} বছর)")
        
        # ঋণের পরিমাণ গণনা
        max_loan = land_area_percent * self.rules["সর্বোচ্চ ঋণ"]["max_per_acre"]
        
        return {
            "is_eligible": is_eligible,
            "reasons": reasons,
            "max_loan": max_loan,
            "previous_loans": previous_loans
        }


def open_loan_eligibility_window(root):
    """ঋণ যোগ্যতা চেকার উইন্ডো খুলুন"""
    loan_win = tk.Toplevel(root)
    loan_win.title("💰 ঋণ যোগ্যতা চেকার")
    loan_win.geometry("700x750")
    loan_win.config(bg="#fff8e1")
    
    checker = LoanEligibilityChecker()
    
    # ======= শিরোনাম =======
    title_frame = tk.Frame(loan_win, bg="#fbc02d")
    title_frame.pack(fill="x")
    tk.Label(title_frame, text="💰 কৃষি ঋণ যোগ্যতা পরীক্ষা", 
            font=("Arial", 14, "bold"), bg="#fbc02d", fg="white", pady=10).pack()
    
    # ======= ইনপুট ফ্রেম =======
    input_frame = tk.LabelFrame(loan_win, text="📝 আপনার তথ্য প্রদান করুন", 
                                bg="#fff8e1", font=("Arial", 11, "bold"), padx=20, pady=15)
    input_frame.pack(fill="x", padx=10, pady=10)
    
    # বয়স
    tk.Label(input_frame, text="বয়স (বছর):", bg="#fff8e1", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
    age_entry = tk.Entry(input_frame, width=20)
    age_entry.grid(row=0, column=1, padx=10, pady=8)
    tk.Label(input_frame, text="(১৮-৬৫ বছর)", bg="#fff8e1", font=("Arial", 9), fg="gray").grid(row=0, column=2, sticky="w")
    
    # জমির পরিমাণ
    tk.Label(input_frame, text="জমির পরিমাণ (দশমিক):", bg="#fff8e1", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
    land_entry = tk.Entry(input_frame, width=20)
    land_entry.grid(row=1, column=1, padx=10, pady=8)
    tk.Label(input_frame, text="(কমপক্ষে ০.৫ দশমিক)", bg="#fff8e1", font=("Arial", 9), fg="gray").grid(row=1, column=2, sticky="w")
    
    # কৃষি অভিজ্ঞতা
    tk.Label(input_frame, text="কৃষি অভিজ্ঞতা (বছর):", bg="#fff8e1", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=8)
    exp_entry = tk.Entry(input_frame, width=20)
    exp_entry.grid(row=2, column=1, padx=10, pady=8)
    tk.Label(input_frame, text="(১ বছরের বেশি)", bg="#fff8e1", font=("Arial", 9), fg="gray").grid(row=2, column=2, sticky="w")
    
    # পূর্ববর্তী ঋণ
    tk.Label(input_frame, text="পূর্ববর্তী ঋণ (টাকা):", bg="#fff8e1", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=8)
    prev_loan_entry = tk.Entry(input_frame, width=20)
    prev_loan_entry.grid(row=3, column=1, padx=10, pady=8)
    tk.Label(input_frame, text="(যদি থাকে তো)", bg="#fff8e1", font=("Arial", 9), fg="gray").grid(row=3, column=2, sticky="w")
    
    # ======= ফলাফল ফ্রেম =======
    result_frame = tk.LabelFrame(loan_win, text="📊 যোগ্যতা পরীক্ষার ফলাফল", 
                                 bg="#fff8e1", font=("Arial", 11, "bold"))
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    result_text = tk.Text(result_frame, bg="white", font=("Courier", 10), height=18)
    result_text.pack(fill="both", expand=True, padx=5, pady=5)
    result_text.config(state="disabled")
    
    def check():
        """যোগ্যতা পরীক্ষা করুন"""
        try:
            age = int(age_entry.get())
            land = float(land_entry.get())
            exp = int(exp_entry.get())
            prev_loan = float(prev_loan_entry.get() or 0)
            
            result = checker.check_eligibility(age, land, exp, prev_loan)
            
            result_text.config(state="normal")
            result_text.delete(1.0, tk.END)
            
            if result['is_eligible']:
                status = "✅ আপনি ঋণের জন্য যোগ্য"
                status_color = "সবুজ"
            else:
                status = "❌ আপনি এখনো ঋণের যোগ্য নন"
                status_color = "লাল"
            
            output = f"""
╔════════════════════════════════════════════╗
║         ঋণ যোগ্যতা চেক রিপোর্ট          ║
╚════════════════════════════════════════════╝

📊 আপনার তথ্য:
{'─'*44}
  • বয়স: {age} বছর
  • জমি: {land} দশমিক
  • অভিজ্ঞতা: {exp} বছর
  • পূর্ব ঋণ: ৳{prev_loan:,}

✨ যোগ্যতা পরীক্ষা:
{'─'*44}
"""
            
            for reason in result['reasons']:
                output += f"\n{reason}"
            
            output += f"""

╔════════════════════════════════════════════╗
║              চূড়ান্ত ফলাফল              ║
╠════════════════════════════════════════════╣
║ {status:<42} ║
"""
            
            if result['is_eligible']:
                output += f"""╠════════════════════════════════════════════╣
║ 💰 সর্বোচ্চ ঋণ সীমা: ৳{result['max_loan']:,} ║
"""
            
            output += """╚════════════════════════════════════════════╝

📞 যোগাযোগ করুন:
  • কৃষি অফিস - আপনার এলাকা
  • ব্যাংক শাখা (কৃষি বিভাগ)
  • জেলা কৃষক উন্নয়ন কর্মসূচি
"""
            
            result_text.insert(1.0, output)
            result_text.config(state="disabled")
            
        except ValueError:
            messagebox.showerror("ত্রুটি", "❌ সঠিক সংখ্যা দিন")
    
    def clear():
        """ক্লিয়ার করুন"""
        age_entry.delete(0, tk.END)
        land_entry.delete(0, tk.END)
        exp_entry.delete(0, tk.END)
        prev_loan_entry.delete(0, tk.END)
        result_text.config(state="normal")
        result_text.delete(1.0, tk.END)
        result_text.config(state="disabled")
    
    # ======= বোতাম ফ্রেম =======
    button_frame = tk.Frame(loan_win, bg="#fff8e1")
    button_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Button(button_frame, text="✅ পরীক্ষা করুন", command=check,
              bg="#fbc02d", fg="black", font=("Arial", 11, "bold"), padx=20, pady=8).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🔄 পরিষ্কার করুন", command=clear,
              bg="#1976d2", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="❌ বন্ধ করুন", command=loan_win.destroy,
              bg="#d32f2f", fg="white", font=("Arial", 10), padx=15).pack(side="left", padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Loan Eligibility Test")
    root.geometry("400x200")
    tk.Button(root, text="Open Checker", command=lambda: open_loan_eligibility_window(root)).pack(pady=20)
    root.mainloop()
