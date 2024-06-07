import os
import shutil
import sys
import zipfile
import ctypes
import time
from tkinter import messagebox


def is_admin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return False


def move_files_and_directories(directory, current_version):
    old_dir = os.path.join(directory, "old", current_version)
    internal_dir = os.path.join(directory, "_internal")

    # Create the "old" directory if it doesn't exist
    os.makedirs(old_dir, exist_ok=True)

    try:
        # Move _internal directory to old directory
        if os.path.exists(internal_dir):
            shutil.move(internal_dir, os.path.join(old_dir, "_internal"))

        # Move all .exe files to old directory
        for file in os.listdir(directory):
            if file.endswith(".exe"):
                shutil.move(os.path.join(directory, file), old_dir)

        # Move directories starting with "writechoiceorg-bot" to old directory
        for dirname in os.listdir(directory):
            if dirname.startswith("writechoiceorg-bot"):
                update_dir = os.path.join(directory, dirname)
                shutil.move(update_dir, old_dir)
        # Remove the "old" directory
        # if platform.system() == "Windows":  # Windows
        #     subprocess.check_call(["cmd", "/c", "rmdir", old_dir, "/s", "/q"])
        # else:  # Unix-like system
        #     subprocess.check_call(["rm", "-rf", "old"])

        print(f"All files and directories in {directory} have been moved.")
    except Exception as e:
        messagebox.showerror(
            "Download Failed",
            f"Failed to move files and directories in {directory}: {e}",
        )


def extract_and_replace(zip_path, extract_to, current_version):
    try:
        # Remove the old application files
        move_files_and_directories(extract_to, current_version)

        # Extract the update zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)

        # Move the new files to the application directory
        extracted_dir = [
            d for d in os.listdir(extract_to) if d.startswith("writechoiceorg-bot")
        ][0]
        extracted_dir_path = os.path.join(extract_to, extracted_dir)
        for item in os.listdir(extracted_dir_path):
            s = os.path.join(extracted_dir_path, item)
            d = os.path.join(extract_to, item)
            if os.path.isdir(s):
                shutil.move(s, d)
            else:
                shutil.move(s, d)

        # Remove any .zip files and directories that start with "writechoice"
        for item in os.listdir(extract_to):
            item_path = os.path.join(extract_to, item)
            if item.endswith(".zip") or (
                os.path.isdir(item_path) and item.startswith("writechoice")
            ):
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)

        # Restart the application
        os.execl("./bot.exe", "./bot.exe", *sys.argv)
    except Exception as e:
        messagebox.showerror(
            "Update Failed",
            f"Error: {e}",
        )


def main():
    if len(sys.argv) != 4:
        print("Usage: updater.exe <zip_path> <extract_to> <current_version>")
        sys.exit(1)

    zip_path = sys.argv[1]
    extract_to = sys.argv[2]
    current_version = sys.argv[3]

    if not is_admin():
        # Re-run the script with admin privileges
        params = f'"{zip_path}" "{extract_to}" "{current_version}"'
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()

    time.sleep(2)  # Give the main app some time to close
    extract_and_replace(zip_path, extract_to, current_version)


if __name__ == "__main__":
    main()
