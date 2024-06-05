import tkinter as tk
import requests
from tkinter import messagebox, simpledialog
from pagbank_crawler import run_pagbank_crawler
from yuno_crawler import run_yuno_scraper
from pagbank_get_all_text import run_pagbank_text_reader
from yuno_get_all_text import run_yuno_text_reader

CURRENT_VERSION = "1.0.0"
GITHUB_REPO = "writechoiceorg/crawlers"


def password_check():
    password = simpledialog.askstring("Password", "Enter password:", show="*")
    is_correct = password == "123456"
    tries = 3
    while not is_correct and tries > 0:
        tries -= 1
        password = simpledialog.askstring(
            "Password", f"Wrong password... Try again({tries}):", show="*"
        )
        is_correct = password == "123456"
    return is_correct


def invalid_choice():
    messagebox.showerror("Invalid Choice", "Invalid choice. Please enter 1, 2, or 3.")


def run_yuno_bot():
    run_yuno_scraper()
    messagebox.showinfo("Info", "Yuno bot run successfully")


def update_yuno_content():
    correct_password = password_check()
    if correct_password:
        run_yuno_text_reader()
        messagebox.showinfo("Info", "Yuno content updated successfully")


def run_pagbank_bot():
    run_pagbank_crawler()
    messagebox.showinfo("Info", "Pagbank bot run successfully")


def update_pagbank_content():
    correct_password = password_check()
    if correct_password:
        run_pagbank_text_reader()
        messagebox.showinfo("Info", "Pagbank content updated successfully")


def check_for_updates():
    try:
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        if latest_version != CURRENT_VERSION:
            messagebox.showinfo(
                "Update Available",
                f"A new version {latest_version} is available. Please update.",
            )
        else:
            messagebox.showinfo(
                "No Update Available", "You are using the latest version."
            )
    except requests.RequestException as e:
        messagebox.showerror("Update Check Failed", f"Failed to check for updates: {e}")


def create_main_window():
    root = tk.Tk()
    root.title("Service Selector")

    # Set minimum size for the window
    root.wm_minsize(400, 300)

    # Set styles
    bg_color = "#f0f0f0"
    button_color = "#4CAF50"
    button_fg_color = "#ffffff"
    font = ("Helvetica", 12)

    root.configure(bg=bg_color)

    def yuno_choices():
        tk.Label(
            content_frame,
            text="Yuno Choices",
            font=("Helvetica", 16, "bold"),
            bg=bg_color,
        ).pack(pady=10)
        tk.Button(
            content_frame,
            text="Run Yuno bot",
            command=run_yuno_bot,
            bg=button_color,
            fg=button_fg_color,
            font=font,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Update Yuno translated content",
            command=update_yuno_content,
            bg=button_color,
            fg=button_fg_color,
            font=font,
        ).pack(pady=5)
        tk.Button(
            content_frame, text="Go back", command=lambda: show_main_options()
        ).pack(pady=5)

    def pagbank_choices():
        tk.Label(
            content_frame,
            text="Pagbank Choices",
            font=("Helvetica", 16, "bold"),
            bg=bg_color,
        ).pack(pady=10)
        tk.Button(
            content_frame,
            text="Run Pagbank bot",
            command=run_pagbank_bot,
            bg=button_color,
            fg=button_fg_color,
            font=font,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Update Pagbank translated content",
            command=update_pagbank_content,
            bg=button_color,
            fg=button_fg_color,
            font=font,
        ).pack(pady=5)
        tk.Button(
            content_frame, text="Go back", command=lambda: show_main_options()
        ).pack(pady=5)

    def show_main_options():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Button(
            content_frame,
            text="Yuno",
            command=yuno_choices,
            bg=button_color,
            fg=button_fg_color,
            font=font,
            width=20,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Pagbank",
            command=pagbank_choices,
            bg=button_color,
            fg=button_fg_color,
            font=font,
            width=20,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Check for Updates",
            command=check_for_updates,
            bg="#2196F3",
            fg=button_fg_color,
            font=font,
            width=20,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Exit",
            command=root.quit,
            bg="#f44336",
            fg=button_fg_color,
            font=font,
            width=20,
        ).pack(pady=5)

    header_frame = tk.Frame(root, bg=bg_color)
    header_frame.pack(pady=10)

    tk.Label(
        header_frame,
        text="Translation BOT",
        font=("Helvetica", 18, "bold"),
        bg=bg_color,
    ).pack()

    content_frame = tk.Frame(root, bg=bg_color)
    content_frame.pack(pady=10)

    show_main_options()

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
