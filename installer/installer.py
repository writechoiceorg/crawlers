import os
import sys
import zipfile
import ctypes
import requests
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

GITHUB_REPO = "writechoiceorg/bot"


def is_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return False


def download_latest_release(download_path):
    try:
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        download_url = response.json()["zipball_url"]

        with requests.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(download_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded latest release to {download_path}")
    except requests.RequestException as e:
        print(f"Failed to download latest release: {e}")
        sys.exit(1)


def extract_and_install(zip_path, install_dir):
    try:
        # Ensure the installation directory exists
        os.makedirs(install_dir, exist_ok=True)

        # Extract the update zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)

        # Move the new files to the application directory
        extracted_dir = [
            d for d in os.listdir(install_dir) if d.startswith("writechoiceorg-bot")
        ][0]
        extracted_dir_path = os.path.join(install_dir, extracted_dir)
        for item in os.listdir(extracted_dir_path):
            s = os.path.join(extracted_dir_path, item)
            d = os.path.join(install_dir, item)
            if os.path.isdir(s):
                shutil.move(s, d)
            else:
                shutil.move(s, d)

        # Remove any .zip files and directories that start with "writechoice"
        for item in os.listdir(install_dir):
            item_path = os.path.join(install_dir, item)
            if item.endswith(".zip") or (
                os.path.isdir(item_path) and item.startswith("writechoice")
            ):
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

        print(f"Installed application to {install_dir}")
    except Exception as e:
        print(f"Installation Failed: {e}")
        sys.exit(1)


def main():
    if not is_admin():
        # Re-run the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, None, None, 1
        )
        sys.exit()

    def select_directory():
        install_dir = filedialog.askdirectory()
        if install_dir:
            path_var.set(install_dir)

    def install():
        install_dir = path_var.get()
        if install_dir:
            zip_path = os.path.join(install_dir, "latest_release.zip")

            # Download the latest release
            download_latest_release(zip_path)

            # Extract and install the application
            extract_and_install(zip_path, install_dir)

            messagebox.showinfo("Success", "Installation completed successfully.")
            root.destroy()
        else:
            messagebox.showerror("Error", "Please select an installation directory.")

    def cancel():
        root.destroy()

    def on_enter(event):
        event.widget.config(cursor="hand2")

    def on_leave(event):
        event.widget.config(cursor="")

    root = tk.Tk()
    root.title("Install translation bot")
    root.geometry("450x200")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    label = tk.Label(frame, text="Select the installation directory:")
    label.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

    path_var = tk.StringVar(value=os.path.dirname(os.path.abspath(sys.executable)))
    path_entry = tk.Entry(frame, textvariable=path_var, width=40)
    path_entry.grid(row=1, column=0, pady=5, padx=(0, 5), sticky="ew")

    select_button = tk.Button(frame, text="Browse...", command=select_directory)
    select_button.grid(row=1, column=1, pady=5, sticky="ew")
    select_button.bind("<Enter>", on_enter)
    select_button.bind("<Leave>", on_leave)

    button_frame = tk.Frame(frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="e")

    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel)
    cancel_button.pack(side=tk.LEFT, padx=(0, 5))
    cancel_button.bind("<Enter>", on_enter)
    cancel_button.bind("<Leave>", on_leave)

    install_button = tk.Button(button_frame, text="Install", command=install)
    install_button.pack(side=tk.LEFT)
    install_button.bind("<Enter>", on_enter)
    install_button.bind("<Leave>", on_leave)

    root.mainloop()


if __name__ == "__main__":
    main()
