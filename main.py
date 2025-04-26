import customtkinter as ctk
import subs_script
import emails_script
import whois_script
import paths_script
from PIL import Image
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")  
    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RecDragon")
        self.geometry("800x600")
        self.iconbitmap(resource_path("images/sea-dragon_38125.ico"))

        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#031C30", border_width=2, border_color="#667A8A")
        self.sidebar.pack(side="left", fill="y")

        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="right", expand=True, fill="both")

        home_image = ctk.CTkImage(Image.open(resource_path("images/home.png")), size=(30, 30))
        self.btn_home = ctk.CTkButton(self.sidebar, text=" Home", command=self.load_home, anchor="w",
                                      fg_color="#031C30", image=home_image, hover_color="#667A8A",
                                      font=("Comic Sans MS", 35))
        self.btn_home.pack(pady=(80, 20), padx=20, fill="x")

        subs_image = ctk.CTkImage(Image.open(resource_path("images/domains.png")), size=(30, 30))
        self.btn_subs = ctk.CTkButton(self.sidebar, text=" Subdomains", command=self.load_subs, anchor="w",
                                      fg_color="#031C30", image=subs_image, hover_color="#667A8A",
                                      font=("Comic Sans MS", 35))
        self.btn_subs.pack(pady=20, padx=20, fill="x")

        email_image = ctk.CTkImage(Image.open(resource_path("images/email.png")), size=(30, 30))
        self.btn_emails = ctk.CTkButton(self.sidebar, text=" Emails", command=self.load_emails, anchor="w",
                                        fg_color="#031C30", image=email_image, hover_color="#667A8A",
                                        font=("Comic Sans MS", 35))
        self.btn_emails.pack(pady=20, padx=20, fill="x")

        whois_image = ctk.CTkImage(Image.open(resource_path("images/paper.png")), size=(30, 30))
        self.btn_whois = ctk.CTkButton(self.sidebar, text=" Whois", command=self.load_whois, anchor="w",
                                       fg_color="#031C30", image=whois_image, hover_color="#667A8A",
                                       font=("Comic Sans MS", 35))
        self.btn_whois.pack(pady=20, padx=20, fill="x")

        paths_image = ctk.CTkImage(Image.open(resource_path("images/folder.png")), size=(30, 30))
        self.btn_paths = ctk.CTkButton(self.sidebar, text=" Paths", command=self.load_paths, anchor="w",
                                       fg_color="#031C30", image=paths_image, hover_color="#667A8A",
                                       font=("Comic Sans MS", 35))
        self.btn_paths.pack(pady=20, padx=20, fill="x")

        self.current_frame = None
        self.load_home()

    def clear_main_area(self):
        if self.current_frame:
            self.current_frame.destroy()

    def load_home(self):
        self.clear_main_area()
        welcome_image = ctk.CTkImage(Image.open(resource_path("images/agreement.png")), size=(50, 50))
        self.current_frame = ctk.CTkFrame(self.main_area, fg_color="#031C30", border_width=1, border_color="#667A8A")
        self.current_frame.pack(expand=True, fill="both")
        label = ctk.CTkLabel(self.current_frame, text=" Welcome to RecDragon", image=welcome_image, compound="left",
                             font=("Comic Sans MS", 50), text_color="white")
        label.pack(pady=400)

    def load_subs(self):
        self.clear_main_area()
        self.current_frame = subs_script.SubsScriptPage(self.main_area)
        self.current_frame.pack(expand=True, fill="both")

    def load_emails(self):
        self.clear_main_area()
        self.current_frame = emails_script.EmailsScriptPage(self.main_area)
        self.current_frame.pack(expand=True, fill="both")

    def load_whois(self):
        self.clear_main_area()
        self.current_frame = whois_script.WhoisScriptPage(self.main_area)
        self.current_frame.pack(expand=True, fill="both")

    def load_paths(self):
        self.clear_main_area()
        self.current_frame = paths_script.PathsScriptPage(self.main_area)
        self.current_frame.pack(expand=True, fill="both")

if __name__ == "__main__":
    app = App()
    app.mainloop()

