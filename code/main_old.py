import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import os
import zipfile
import io
import shutil
import sys
import subprocess
from pagbank_crawler import run_pagbank_crawler
from yuno_crawler import run_yuno_scraper
from pagbank_get_all_text import run_pagbank_text_reader
from yuno_get_all_text import run_yuno_text_reader
from time import sleep
import ctypes

GITHUB_REPO = "writechoiceorg/bot"
CURRENT_VERSION = "v1.0.5"


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


def extract_update_from_response(response, extract_to):
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        messagebox.showerror(f"Extraction Failed: {e}")
        return False


def download_update(download_url):
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        extraction = extract_update_from_response(response, "./")
        if extraction is False:
            messagebox.showerror("Download Failed", "Failed to extract update.")
        move_files_from_update_directory("./")
        launch_updater(sys.executable)
    except Exception as e:
        messagebox.showerror("Download Failed", f"Failed to download the update: {e}")
        return False


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def move_files_from_update_directory(dest_dir):
    if not is_admin():
        # Re-run the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()
    try:
        # Find the directory that begins with "writechoiceorg-bot"
        update_dir = None
        for dirname in os.listdir("./"):
            if dirname.startswith("writechoiceorg-bot"):
                update_dir = os.path.join("./", dirname)
                break

        if not update_dir:
            print("No update directory found.")
            return False

        internal_dir = os.path.join(dest_dir, "_internal")
        if os.path.exists(internal_dir):
            shutil.rmtree(internal_dir)

        for item in os.listdir(update_dir):
            s = os.path.join(update_dir, item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        return True
    except Exception as e:
        messagebox.showerror("Failed to move files", f"{e}")
        return False


def launch_updater(current_executable):
    updater_script = os.path.join("./", "updater.py")
    with open(updater_script, "w") as f:
        f.write(
            f"""
import os
import shutil
import sys
import time

def main():
    dest_dir = os.path.dirname(sys.executable)
    bot_exe = os.path.join(dest_dir, "bot.exe")

    current_executable = r"{current_executable}"

    # Give the main app some time to close
    time.sleep(2)

    
    os.execl(bot_exe, bot_exe, *sys.argv)

if __name__ == "__main__":
    main()
"""
        )
    subprocess.Popen([sys.executable, updater_script])
    sys.exit()


def check_for_updates(on_startup=False):
    try:
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        if latest_version != CURRENT_VERSION:
            if messagebox.askyesno(
                "Update Available",
                f"A new version {latest_version} is available. Do you want to update?",
            ):
                download_url = response.json()["zipball_url"]
                download_update(download_url)
                messagebox.showinfo(
                    "Update",
                    "Update downloaded and installed.",
                )
        elif on_startup:
            messagebox.showinfo(
                "No Update Available", "You are using the latest version."
            )
    except requests.RequestException as e:
        if on_startup:
            messagebox.showerror(
                "Update Check Failed", f"Failed to check for updates: {e}"
            )
    # finally:
    # updater = os.path.join("./", "updater.py")
    # if os.path.exists(updater):
    #     os.remove(updater)


def create_main_window():
    root = tk.Tk()
    root.title(f"Service Selector {CURRENT_VERSION}")

    # Set minimum size for the window
    root.wm_minsize(400, 300)

    # Set styles
    bg_color = "#f0f0f0"
    button_color = "#4CAF50"
    button_fg_color = "#ffffff"
    font = ("Helvetica", 12)

    root.configure(bg=bg_color)

    def yuno_choices():
        for widget in content_frame.winfo_children():
            widget.destroy()
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
            content_frame,
            text="Go back",
            command=show_main_options,
            bg=button_color,
            fg=button_fg_color,
            font=font,
        ).pack(pady=5)

    def pagbank_choices():
        for widget in content_frame.winfo_children():
            widget.destroy()
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
            content_frame,
            text="Go back",
            command=show_main_options,
            bg=button_color,
            fg=button_fg_color,
            font=font,
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
            command=lambda: check_for_updates(on_startup=False),
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
        text="Service Selector",
        font=("Helvetica", 18, "bold"),
        bg=bg_color,
    ).pack()

    content_frame = tk.Frame(root, bg=bg_color)
    content_frame.pack(pady=10)

    show_main_options()
    root.after(1000, lambda: check_for_updates(on_startup=True))

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
