import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class IGCheckerApp:
    def __init__(self, master):
        self.master = master
        master.title("Instagram Follow Checker")
        # Menggunakan ukuran window yang lebih fleksibel dan responsive
        master.geometry("1100x700")
        master.minsize(900, 600)
        master.resizable(True, True)

        # Frame utama
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame kiri (Followers)
        left_frame = tk.LabelFrame(main_frame, text="Followers", padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        tk.Button(left_frame, text="Load followers.json", command=self.load_followers_file).pack(pady=(0,5))
        # Scrollbar untuk followers
        follower_scroll = tk.Scrollbar(left_frame)
        follower_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.follower_tree = ttk.Treeview(left_frame, columns=("username",), show="headings", height=18, yscrollcommand=follower_scroll.set)
        self.follower_tree.heading("username", text="Username")
        self.follower_tree.pack(fill=tk.BOTH, expand=True)
        follower_scroll.config(command=self.follower_tree.yview)

        # Frame kanan (Following)
        right_frame = tk.LabelFrame(main_frame, text="Following", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10,0))
        main_frame.grid_columnconfigure(1, weight=1)

        tk.Button(right_frame, text="Load following.json", command=self.load_following_file).pack(pady=(0,5))
        # Scrollbar untuk following
        following_scroll = tk.Scrollbar(right_frame)
        following_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.following_tree = ttk.Treeview(right_frame, columns=("username",), show="headings", height=18, yscrollcommand=following_scroll.set)
        self.following_tree.heading("username", text="Username")
        self.following_tree.pack(fill=tk.BOTH, expand=True)
        following_scroll.config(command=self.following_tree.yview)

        # Frame bawah (Tidak follow balik)
        bottom_frame = tk.LabelFrame(master, text="Tidak Follow Balik", padx=10, pady=10)
        bottom_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(0,20))
        tk.Button(bottom_frame, text="Load hasil cek", command=self.check_not_following_back).pack(pady=(0,5))
        # Scrollbar untuk tidak follow balik
        not_following_scroll = tk.Scrollbar(bottom_frame)
        not_following_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.not_following_tree = ttk.Treeview(bottom_frame, columns=("username",), show="headings", height=7, yscrollcommand=not_following_scroll.set)
        self.not_following_tree.heading("username", text="Username")
        self.not_following_tree.pack(fill=tk.BOTH, expand=True)
        not_following_scroll.config(command=self.not_following_tree.yview)

        # Data
        self.followers = set()
        self.following = set()

    def load_followers_file(self):
        path = filedialog.askopenfilename(title="Pilih followers.json", filetypes=[("JSON Files", "*.json")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Jika data adalah list, langsung proses
                    if isinstance(data, list):
                        usernames = {entry["string_list_data"][0]["value"] for entry in data}
                    # Jika data adalah dict, ambil key 'relationships_followers'
                    elif isinstance(data, dict):
                        usernames = {entry["string_list_data"][0]["value"] for entry in data.get('relationships_followers', [])}
                    else:
                        usernames = set()
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
                    if isinstance(data, list):
                        usernames = {entry["string_list_data"][0]["value"] for entry in data}
                    elif isinstance(data, dict):
                        usernames = {entry["string_list_data"][0]["value"] for entry in data.get('relationships_following', [])}
                    else:
                        usernames = set()
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
