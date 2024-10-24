import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import os
import sys
import subprocess
from pagbank_crawler import run_pagbank_apiref, run_pagbank_guides
from yuno_crawler import run_yuno_apiref, run_yuno_guides
from ideal_crawler import run_ideal_apiref, run_ideal_guides
from time import sleep
from packaging import version

# from pagbank_get_all_text import run_pagbank_text_reader
# from yuno_get_all_text import run_yuno_text_reader

GITHUB_REPO = "writechoiceorg/bot"
CURRENT_VERSION = "v1.1.3"


def search_updates():
    try:
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        current_num = CURRENT_VERSION.lstrip("v")
        latest_num = latest_version.lstrip("v")

        if version.parse(latest_num) > version.parse(current_num):
            if messagebox.askyesno(
                "Update Available",
                f"A new version {latest_version} is available. Do you want to update?",
            ):
                download_url = response.json()["zipball_url"]
                download_update(download_url)
                return True
            else:
                return False
    except requests.RequestException as e:
        messagebox.showerror("Update Check Failed", f"Failed to check for updates: {e}")


def check_for_updates():
    update = search_updates()
    if not update:
        messagebox.showinfo("No Update Available", "You are using the latest version.")


def download_update(download_url):
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        zip_path = os.path.join(os.path.dirname(sys.executable), "update.zip")
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        launch_updater(zip_path)
    except Exception as e:
        messagebox.showerror("Download Failed", f"Failed to download the update: {e}")


def launch_updater(zip_path):
    updater_executable = os.path.join(os.path.dirname(sys.executable), "updater.exe")
    subprocess.Popen(
        [
            updater_executable,
            zip_path,
            os.path.dirname(sys.executable),
            CURRENT_VERSION,
        ],
        shell=True,
    )
    sys.exit()


def password_check():
    password = simpledialog.askstring("Password", "Enter password:", show="*")
    is_correct = password == "123456"
    tries = 3
    while not is_correct and tries > 0:
        sleep(0.5)
        tries -= 1
        password = simpledialog.askstring(
            "Password", f"Wrong password... Try again({tries}):", show="*"
        )
        is_correct = password == "123456"
    return is_correct


def invalid_choice():
    messagebox.showerror("Invalid Choice", "Invalid choice. Please enter 1, 2, or 3.")


def run_yuno_bot_guides():
    run_yuno_guides()
    messagebox.showinfo("Info", "Yuno guides check successful")


def run_yuno_bot_apiref():
    run_yuno_apiref()
    messagebox.showinfo("Info", "Yuno API check successful")


# def update_yuno_content():
#     correct_password = password_check()
#     if correct_password:
#         run_yuno_text_reader()
#         messagebox.showinfo("Info", "Yuno content updated successfully")


def run_pagbank_bot_guides():
    run_pagbank_guides()
    messagebox.showinfo("Info", "Pagbank guides check successful")


def run_pagbank_bot_apiref():
    run_pagbank_apiref()
    messagebox.showinfo("Info", "Pagbank API check successful")


# def update_pagbank_content():
#     correct_password = password_check()
#     if correct_password:
#         run_pagbank_text_reader()
#         messagebox.showinfo("Info", "Pagbank content updated successfully")


def run_ideal_bot_guides():
    run_ideal_guides()
    messagebox.showinfo("Info", "Ideal guides check successful")


def run_ideal_bot_apiref():
    run_ideal_apiref()
    messagebox.showinfo("Info", "Ideal API check successful")


def create_main_window():
    root = tk.Tk()
    root.title(f"Translation bot - {CURRENT_VERSION}")

    root.wm_minsize(500, 400)

    main_font = "Inter"

    bg_color = "#f0f0f0"
    button_color = "#4CAF50"
    button_color_pagbank = "#18a589"
    button_color_yuno = "#513CE1"
    button_color_ideal = "#00D1A2"
    button_fg_color = "#ffffff"
    button_width = 26
    font = (main_font, 12, "bold")

    root.configure(bg=bg_color)

    icon_path = "./_internal/utils/imgs/wc-icon.png"
    window_icon = tk.PhotoImage(file=icon_path)
    root.iconphoto(False, window_icon)

    def yuno_choices():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(
            content_frame,
            text="Yuno",
            font=(main_font, 16, "bold"),
            bg=bg_color,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Guides",
            command=run_yuno_bot_guides,
            bg=button_color_yuno,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="API Reference",
            command=run_yuno_bot_apiref,
            bg=button_color_yuno,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        # tk.Button(
        #     content_frame,
        #     text="Update translated database",
        #     command=update_yuno_content,
        #     bg=button_color_yuno,
        #     fg=button_fg_color,
        #     font=font,
        #     width=button_width,
        # ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Back",
            command=show_main_options,
            bg="#2196F3",
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)

    def pagbank_choices():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(
            content_frame,
            text="Pagbank",
            font=(main_font, 16, "bold"),
            bg=bg_color,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Guides",
            command=run_pagbank_bot_guides,
            bg=button_color_pagbank,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="API Reference",
            command=run_pagbank_bot_apiref,
            bg=button_color_pagbank,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        # tk.Button(
        #     content_frame,
        #     text="Update translated database",
        #     command=update_pagbank_content,
        #     bg=button_color_pagbank,
        #     fg=button_fg_color,
        #     font=font,
        #     width=button_width,
        # ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Back",
            command=show_main_options,
            bg="#2196F3",
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)

    def ideal_choices():
        for widget in content_frame.winfo_children():
            widget.destroy()
        tk.Label(
            content_frame,
            text="IDEAL",
            font=(main_font, 16, "bold"),
            bg=bg_color,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Guides",
            command=run_ideal_bot_guides,
            bg=button_color_ideal,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="API Reference",
            command=run_ideal_bot_apiref,
            bg=button_color_ideal,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        # tk.Button(
        #     content_frame,
        #     text="Update translated database",
        #     command=update_pagbank_content,
        #     bg=button_color_pagbank,
        #     fg=button_fg_color,
        #     font=font,
        #     width=button_width,
        # ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Back",
            command=show_main_options,
            bg="#2196F3",
            fg=button_fg_color,
            font=font,
            width=button_width,
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
            width=button_width,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Pagbank",
            command=pagbank_choices,
            bg=button_color,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="IDEAL",
            command=ideal_choices,
            bg=button_color,
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Check for Updates",
            command=check_for_updates,
            bg="#2196F3",
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)
        tk.Button(
            content_frame,
            text="Exit",
            command=root.quit,
            bg="#f44336",
            fg=button_fg_color,
            font=font,
            width=button_width,
        ).pack(pady=5)

    header_frame = tk.Frame(root, bg=bg_color)
    header_frame.pack(pady=5)

    img = tk.PhotoImage(file="./_internal/utils/imgs/logo-wc.png")

    img_label = tk.Label(root, image=img, bg=bg_color)
    img_label.image = img
    img_label.pack()

    content_frame = tk.Frame(root, bg=bg_color)
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    show_main_options()

    root.after(1, search_updates)

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
