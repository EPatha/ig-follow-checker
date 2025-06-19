import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class IGCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("Instagram Follow Checker")
        master.geometry("900x600")
        master.resizable(False, False)

        # Frame utama
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame kiri (Followers)
        left_frame = tk.LabelFrame(main_frame, text="Followers", padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.follower_entry = tk.Entry(left_frame, width=25)
        self.follower_entry.pack(pady=(0,5))
        tk.Button(left_frame, text="Tambah Follower", command=self.add_follower).pack(pady=(0,5))
        tk.Button(left_frame, text="Load followers.json", command=self.load_followers_file).pack(pady=(0,5))
        self.follower_tree = ttk.Treeview(left_frame, columns=("username",), show="headings", height=15)
        self.follower_tree.heading("username", text="Username")
        self.follower_tree.pack()

        # Frame kanan (Following)
        right_frame = tk.LabelFrame(main_frame, text="Following", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0))
        main_frame.grid_columnconfigure(1, weight=1)

        self.following_entry = tk.Entry(right_frame, width=25)
        self.following_entry.pack(pady=(0,5))
        tk.Button(right_frame, text="Tambah Following", command=self.add_following).pack(pady=(0,5))
        tk.Button(right_frame, text="Load following.json", command=self.load_following_file).pack(pady=(0,5))
        self.following_tree = ttk.Treeview(right_frame, columns=("username",), show="headings", height=15)
        self.following_tree.heading("username", text="Username")
        self.following_tree.pack()

        # Frame bawah (Tidak follow balik)
        bottom_frame = tk.LabelFrame(master, text="Tidak Follow Balik", padx=10, pady=10)
        bottom_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(0,20))
        self.not_following_tree = ttk.Treeview(bottom_frame, columns=("username",), show="headings", height=7)
        self.not_following_tree.heading("username", text="Username")
        self.not_following_tree.pack()
        tk.Button(bottom_frame, text="Cek Tidak Follow Balik", command=self.check_not_following_back).pack(pady=5)

        # Data
        self.followers = set()
        self.following = set()

    def add_follower(self):
        username = self.follower_entry.get().strip()
        if username and username not in self.followers:
            self.followers.add(username)
            self.follower_tree.insert('', 'end', values=(username,))
            self.follower_entry.delete(0, tk.END)

    def add_following(self):
        username = self.following_entry.get().strip()
        if username and username not in self.following:
            self.following.add(username)
            self.following_tree.insert('', 'end', values=(username,))
            self.following_entry.delete(0, tk.END)

    def load_followers_file(self):
        path = filedialog.askopenfilename(title="Pilih followers.json", filetypes=[("JSON Files", "*.json")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    usernames = {entry["string_list_data"][0]["value"] for entry in data.get('relationships_followers', [])}
                    self.followers = usernames
                    self.follower_tree.delete(*self.follower_tree.get_children())
                    for username in sorted(usernames):
                        self.follower_tree.insert('', 'end', values=(username,))
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file followers:\n{e}")

    def load_following_file(self):
        path = filedialog.askopenfilename(title="Pilih following.json", filetypes=[("JSON Files", "*.json")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    usernames = {entry["string_list_data"][0]["value"] for entry in data.get('relationships_following', [])}
                    self.following = usernames
                    self.following_tree.delete(*self.following_tree.get_children())
                    for username in sorted(usernames):
                        self.following_tree.insert('', 'end', values=(username,))
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membaca file following:\n{e}")

    def check_not_following_back(self):
        not_following_back = sorted(self.following - self.followers)
        self.not_following_tree.delete(*self.not_following_tree.get_children())
        for username in not_following_back:
            self.not_following_tree.insert('', 'end', values=(username,))
        messagebox.showinfo("Hasil", f"Total tidak follow balik: {len(not_following_back)} akun")

if __name__ == "__main__":
    root = tk.Tk()
    app = IGCheckerApp(root)
    root.mainloop()
