import requests
import os
import shutil
import sys
import zipfile
import io

CURRENT_VERSION = "v1.0.1"
GITHUB_REPO = "writechoiceorg/bot"


def download_and_extract_update():
    try:
        # Get the latest release info
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        )
        response.raise_for_status()
        download_url = response.json()["zipball_url"]

        # Download the zip file
        response = requests.get(download_url, stream=True)
        response.raise_for_status()

        # Extract the zip file to a temporary directory
        # temp_dir = "./updates"
        # os.makedirs(temp_dir, exist_ok=True)

        if extract_update_from_response(response, "./"):
            print("Update extracted successfully.")
            move_files_from_update_directory("./")
            # shutil.rmtree(temp_dir)
            # Now you can move files as needed to install the update
        else:
            print("Failed to extract update.")

    except requests.RequestException as e:
        print(f"Update Check Failed: {e}")


def move_files_from_update_directory(dest_dir):
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

        # Move all contents of the update directory to the destination directory
        for item in os.listdir(update_dir):
            s = os.path.join(update_dir, item)
            d = os.path.join(dest_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        return True
    except Exception as e:
        print(f"Failed to move files: {e}")
        return False


def extract_update_from_response(response, extract_to):
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Extraction Failed: {e}")
        return False


# Run the function to download and extract the update
download_and_extract_update()
