import customtkinter as ctk
import requests
from concurrent.futures import ThreadPoolExecutor
import threading
import os
from PIL import Image
class PathsScriptPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#031C30", border_width=2, border_color="#667A8A")

        path_image=ctk.CTkImage(Image.open("images/folder.png"), size=(50, 50))
        start_image=ctk.CTkImage(Image.open("images/start.png"),size=(25,25))
        save_image=ctk.CTkImage(Image.open("images/save.png"),size=(25,25))

        self.label = ctk.CTkLabel(self, text=" Paths Enumeration", font=("Comic Sans MS", 50,"bold"),image=path_image,compound="left")
        self.label.pack(pady=(80,0))

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter full URL (e.g., https://example.com)", width=300, fg_color="#667A8A", border_color="#667A8A", font=("Comic Sans MS", 20))
        self.url_entry.pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="Start", command=self.start_enumeration, font=("Comic Sans MS", 30,"bold"),image=start_image,compound="left", fg_color="#031C30", hover_color="#667A8A", border_width=1, border_color="#667A8A")
        self.start_btn.pack(pady=10)


        self.output_box = ctk.CTkTextbox(self, height=350, width=1500, fg_color="#667A8A")
        self.output_box.pack(pady=20)

        self.save_btn = ctk.CTkButton(self, text="Save Results", image=save_image,compound="left",command=self.save_results,font=("Comic Sans MS", 30,"bold"), fg_color="#031C30", hover_color="#667A8A",
                                    border_width=1, border_color="#667A8A")
        self.save_btn.pack(pady=10)


    def log(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def fetch_wordlist(self):
        wordlist_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/Web-Content/common.txt"
        self.log(f"[*] Downloading wordlist from:\n{wordlist_url}")
        try:
            response = requests.get(wordlist_url, timeout=15)
            response.raise_for_status()
            self.log("[+] Wordlist loaded successfully.\n")
            return response.text.splitlines()
        except requests.RequestException as e:
            self.log(f"[!] Failed to fetch wordlist: {e}")
            return []

    def check_path(self, domain, path):
        url = f"{domain.rstrip('/')}/{path}"
        try:
            response = requests.get(url, timeout=3, allow_redirects=False)
            if response.status_code != 404:
                self.log(f"[+] Found: {url} ({response.status_code})")
        except requests.RequestException:
            pass

    def enumerate_paths(self, domain, paths):
        self.log(f"\n[*] Enumerating paths on: {domain}\n")
        with ThreadPoolExecutor(max_workers=50) as executor:
            for path in paths:
                executor.submit(self.check_path, domain, path)

    def start_enumeration(self):
        domain = self.url_entry.get().strip()
        if not domain.startswith("http"):
            self.log("[-] Please include http:// or https:// in the domain.")
            return
        threading.Thread(target=self._run_enumeration, args=(domain,), daemon=True).start()

    def _run_enumeration(self, domain):
        paths = self.fetch_wordlist()
        if paths:
            self.enumerate_paths(domain, paths)

    def save_results(self):
        domain = self.url_entry.get().strip()
        if not domain:
            self.log("[-] Please enter a domain first.")
            return

        filename_base = domain.replace("https://", "").replace("http://", "").replace("/", "_")
        folder_path = "results"
        os.makedirs(folder_path, exist_ok=True)

        counter = 0
        file_path = os.path.join(folder_path, f"{filename_base}.txt")
        while os.path.exists(file_path):
            counter += 1
            file_path = os.path.join(folder_path, f"{filename_base}_{counter}.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            content = self.output_box.get("1.0", "end").strip()
            f.write(content)

        self.log(f"\n[+] Results saved to: {file_path}")
