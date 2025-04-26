import customtkinter as ctk
import requests
from concurrent.futures import ThreadPoolExecutor
import threading
from PIL import Image
import os

class SubsScriptPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.lock = threading.Lock()
        self.subdomains_set = set()
        self.configure(fg_color="#031C30", border_width=2, border_color="#667A8A")



        self.wordlists = {
            "Namelist Subdomains": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/namelist.txt",
            "Top 5000 Subdomains (Small & Fast)": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/subdomains-top1million-5000.txt",
            "Bitquark Top 100000 (SLOW)": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/bitquark-subdomains-top100000.txt",
        }

        self.build_ui()

    def build_ui(self):

        subs_image=ctk.CTkImage(Image.open("images/domains.png"), size=(50, 50))
        start_image=ctk.CTkImage(Image.open("images/start.png"),size=(25,25))
        save_image=ctk.CTkImage(Image.open("images/save.png"),size=(25,25))


        ctk.CTkLabel(self, text=" Subdomain Enumeration", font=("Comic Sans MS", 50,"bold"),image=subs_image,compound="left").pack(pady=(80,0))

        self.domain_entry = ctk.CTkEntry(self, placeholder_text="Enter domain (e.g., example.com)", width=300,
                                         fg_color="#667A8A", border_color="#667A8A", font=("Comic Sans MS", 20))
        self.domain_entry.pack(pady=10)

        self.wordlist_option = ctk.CTkOptionMenu(self, values=list(self.wordlists.keys()),
                                                 button_color="#031C30", button_hover_color="#667A8A",
                                                 dropdown_hover_color="#031C30", dropdown_fg_color="#667A8A",
                                                 fg_color="#031C30", font=("Comic Sans MS", 30))
        self.wordlist_option.pack(pady=10)

        start_button = ctk.CTkButton(self, text="Start", command=self.start_enum, font=("Comic Sans MS", 30,"bold"),image=start_image,compound="left",
                                     fg_color="#031C30", hover_color="#667A8A", border_width=1, border_color="#667A8A")
        start_button.pack(pady=10)



        self.output_box = ctk.CTkTextbox(self, height=350, width=1500, fg_color="#667A8A")
        self.output_box.pack(pady=10)

        save_button = ctk.CTkButton(self, text="Save Results", command=self.save_results_to_file,image=save_image,compound="left",
                                    font=("Comic Sans MS", 30,"bold"), fg_color="#031C30", hover_color="#667A8A",
                                    border_width=1, border_color="#667A8A")
        save_button.pack(pady=10)
    def log(self, message):
        self.output_box.insert("end", message + "\n")
        self.output_box.see("end")

    def fetch_wordlist(self, url):
        self.log(f"[*] Downloading wordlist from: {url}")
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            self.subdomains_set = set(response.text.splitlines())
            self.log(f"[+] Loaded {len(self.subdomains_set)} subdomains.")
        except requests.RequestException as e:
            self.log(f"[!] Failed to download wordlist: {e}")

    def check_subdomain(self, domain, subdomain):
        for scheme in ["http", "https"]:
            url = f"{scheme}://{subdomain}.{domain}"
            try:
                response = requests.get(url, timeout=3)
                with self.lock:
                    self.log(f"[+] Discovered: {url} ({response.status_code})")
                return
            except (requests.ConnectionError, requests.exceptions.ReadTimeout):
                continue

    def start_enum(self):
        self.output_box.delete("1.0", "end")
        domain = self.domain_entry.get().strip()
        wordlist_name = self.wordlist_option.get()

        if not domain:
            self.log("[-] Please enter a valid domain.")
            return

        wordlist_url = self.wordlists.get(wordlist_name)
        if not wordlist_url:
            self.log("[-] No wordlist selected.")
            return

        self.fetch_wordlist(wordlist_url)
        if not self.subdomains_set:
            self.log("[-] No subdomains to scan.")
            return

        self.log(f"\n[*] Starting scan for: {domain} with {len(self.subdomains_set)} subdomains...\n")

        def run_enum():
            with ThreadPoolExecutor(max_workers=100) as executor:
                for sub in self.subdomains_set:
                    executor.submit(self.check_subdomain, domain, sub)
            self.log("\n[*] Scan completed.")

        threading.Thread(target=run_enum).start()

    def save_results_to_file(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            self.log("[-] Cannot save results: No domain entered.")
            return

        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

        base_filename = f"{domain} (Subdomains)"
        file_path = os.path.join(results_dir, f"{base_filename}.txt")
        counter = 1

        while os.path.exists(file_path):
            file_path = os.path.join(results_dir, f"{base_filename} ({counter}).txt")
            counter += 1

        content = self.output_box.get("1.0", "end").strip().splitlines()
        unique_lines = sorted(set(line.strip() for line in content if line.strip()))

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(unique_lines))
            self.log(f"[+] Results saved to: {file_path}")
        except Exception as e:
            self.log(f"[!] Error saving results: {e}")
