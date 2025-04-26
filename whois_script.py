import customtkinter as ctk
import whois
import os
from PIL import Image
class WhoisScriptPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#031C30", border_width=2, border_color="#667A8A")

        whois_image=ctk.CTkImage(Image.open("images/paper.png"), size=(50, 50))
        start_image=ctk.CTkImage(Image.open("images/start.png"),size=(25,25))
        save_image=ctk.CTkImage(Image.open("images/save.png"),size=(25,25))
        label = ctk.CTkLabel(self, text=" WHOIS Lookup", font=("Comic Sans MS", 50,"bold"),image=whois_image,compound="left")
        label.pack(pady=(80,0))

        self.domain_entry = ctk.CTkEntry(self, placeholder_text="Enter domain name (e.g., example.com)",width=300, fg_color="#667A8A", border_color="#667A8A", font=("Comic Sans MS", 20))
        self.domain_entry.pack(pady=10)

        check_btn = ctk.CTkButton(self, text="Start", image=start_image,compound="left",command=self.get_domain_info, font=("Comic Sans MS", 30,"bold"), fg_color="#031C30", hover_color="#667A8A", border_width=1, border_color="#667A8A")
        check_btn.pack(pady=10)



        self.result_textbox = ctk.CTkTextbox(self, height=350, width=1500, fg_color="#667A8A")
        self.result_textbox.pack(pady=20)

        save_btn = ctk.CTkButton(self, text="Save Result", image=save_image,compound="left",command=self.save_result,font=("Comic Sans MS", 30,"bold"), fg_color="#031C30", hover_color="#667A8A",
                                    border_width=1, border_color="#667A8A")
        save_btn.pack(pady=10)

        self.current_domain = ""

    def get_domain_info(self):
        domain = self.domain_entry.get().strip()
        self.result_textbox.delete("1.0", "end")  

        if not domain:
            self.result_textbox.insert("end", "Please enter a domain name.")
            return

        try:
            domain_info = whois.whois(domain)
            self.current_domain = domain
            self.result_textbox.insert("end", "--- Domain Information ---\n\n")
            for key, value in domain_info.items():
                self.result_textbox.insert("end", f"{key}: {value}\n")
        except Exception as e:
            self.result_textbox.insert("end", "An error occurred while retrieving domain information:\n")
            self.result_textbox.insert("end", str(e))
            self.current_domain = ""

    def save_result(self):
        if not self.current_domain:
            self.result_textbox.insert("end", "\n\nNo domain info to save.")
            return

        result = self.result_textbox.get("1.0", "end").strip()
        if not result:
            self.result_textbox.insert("end", "\n\nNo result to save.")
            return

        folder = "results"
        os.makedirs(folder, exist_ok=True)

        base_name = f"{self.current_domain} (whois)"
        filename = os.path.join(folder, f"{base_name}.txt")

        counter = 1
        while os.path.exists(filename):
            filename = os.path.join(folder, f"{base_name} ({counter}).txt")
            counter += 1

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(result)
            self.result_textbox.insert("end", f"\n\nResult saved to: {filename}")
        except Exception as e:
            self.result_textbox.insert("end", f"\n\nFailed to save result:\n{e}")



