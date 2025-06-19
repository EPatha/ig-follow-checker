import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import json

def load_usernames(filepath: str, key: str) -> set:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {entry["string_list_data"][0]["value"] for entry in data.get(key, [])}
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca file:\n{e}")
        return set()

class IGCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("Instagram Follow Checker")
        master.geometry("600x500")
        master.resizable(False, False)

        self.followers_file = ""
        self.following_file = ""

        # Tombol pilih file
        tk.Button(master, text="Pilih File Followers", command=self.load_followers).pack(pady=5)
        tk.Button(master, text="Pilih File Following", command=self.load_following).pack(pady=5)
        tk.Button(master, text="Cek Siapa Tidak Follow Balik", command=self.compare).pack(pady=10)

        # Tampilkan hasil
        self.output = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=70, height=20)
        self.output.pack(padx=10, pady=10)

    def load_followers(self):
        path = filedialog.askopenfilename(title="Pilih followers.json")
        if path:
            self.followers_file = path

    def load_following(self):
        path = filedialog.askopenfilename(title="Pilih following.json")
        if path:
            self.following_file = path

    def compare(self):
        if not self.followers_file or not self.following_file:
            messagebox.showwarning("Peringatan", "Silakan pilih kedua file terlebih dahulu!")
            return

        followers = load_usernames(self.followers_file, 'relationships_followers')
        following = load_usernames(self.following_file, 'relationships_following')
        not_following_back = sorted(following - followers)

        # Hasil
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, f"Total yang kamu ikuti: {len(following)} akun\n")
        self.output.insert(tk.END, f"Tidak follow kamu balik: {len(not_following_back)} akun\n\n")
        for username in not_following_back:
            self.output.insert(tk.END, f"• {username}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = IGCheckerApp(root)
    root.mainloop()
