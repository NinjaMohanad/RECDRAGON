import requests
import re
import customtkinter as ctk
import os
from PIL import Image
def load_prefixes_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        prefixes = [line.strip() for line in response.text.splitlines() if line.strip()]
        return prefixes
    except requests.RequestException as e:
        print(f"[!] Error fetching wordlist: {e}")
        return []

def bing_search(domain):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    emails = set()

    for i in range(0, 50, 10):
        url = f"https://www.bing.com/search?q=@{domain}&first={i}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            found = re.findall(r"[a-zA-Z0-9_.+-]+@" + re.escape(domain), response.text)
            emails.update(found)
        except requests.RequestException:
            break

    return list(emails)

def guess_emails_from_wordlist(domain, wordlist):
    return [f"{prefix}@{domain}" for prefix in wordlist]

def save_results_to_file(domain, emails):
    if not os.path.exists('results'):
        os.makedirs('results')

    filename = f"results/{domain} (emails).txt"
    counter = 1
    while os.path.exists(filename):
        filename = f"results/{domain} (emails) ({counter}).txt"
        counter += 1

    with open(filename, 'w') as file:
        for email in emails:
            file.write(f"{email}\n")

    print(f"[+] Results saved to {filename}")

class EmailsScriptPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#031C30", border_width=2, border_color="#667A8A")

        email_image=ctk.CTkImage(Image.open("images/email.png"), size=(50, 50))
        start_image=ctk.CTkImage(Image.open("images/start.png"),size=(25,25))
        save_image=ctk.CTkImage(Image.open("images/save.png"),size=(25,25))

        label = ctk.CTkLabel(self, text=" Email Enumeration", font=("Comic Sans MS", 50,"bold"),image=email_image,compound="left")
        label.pack(pady=(80,0))

        self.domain_entry = ctk.CTkEntry(self, placeholder_text="Enter domain (e.g., example.com)", width=300, fg_color="#667A8A", border_color="#667A8A", font=("Comic Sans MS", 20))
        self.domain_entry.pack(pady=10)

        start_btn = ctk.CTkButton(self, text="Start", command=self.start_email_enum, image=start_image,compound="left",font=("Comic Sans MS", 30,"bold"), fg_color="#031C30", hover_color="#667A8A", border_width=1, border_color="#667A8A")
        start_btn.pack(pady=10)


        self.result_area = ctk.CTkTextbox(self, height=350, width=1500, fg_color="#667A8A", wrap="word", state="disabled")
        self.result_area.pack(pady=20)

        save_btn = ctk.CTkButton(self, text="Save Results",image=save_image,compound="left", command=self.save_results,font=("Comic Sans MS", 30,"bold"), fg_color="#031C30", hover_color="#667A8A",
                                    border_width=1, border_color="#667A8A")
        save_btn.pack(pady=10)

    def start_email_enum(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            self.display_result("[!] Please enter a valid domain.")
            return

        self.display_result(f"\nStarting email enumeration for {domain}...\n")

        wordlist_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/Names/names.txt"
        prefixes = load_prefixes_from_url(wordlist_url)

        bing_emails = bing_search(domain)

        guessed_emails = guess_emails_from_wordlist(domain, prefixes)

        all_emails = list(set(bing_emails + guessed_emails))

        if all_emails:
            self.display_result(f"\n[+] Found {len(all_emails)} email(s):\n")
            for email in all_emails:
                self.display_result(f" - {email}")
        else:
            self.display_result("[!] No emails found.")

        self.all_emails = all_emails

    def display_result(self, text):
        self.result_area.configure(state="normal")
        self.result_area.insert("end", text + "\n")
        self.result_area.configure(state="disabled")

    def save_results(self):
        if hasattr(self, 'all_emails') and self.all_emails:
            save_results_to_file(self.domain_entry.get().strip(), self.all_emails)
        else:
            self.display_result("[!] No results to save.")
