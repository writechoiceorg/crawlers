from utils.json_handler import read_json_file, save_to_json
from utils.remove_duplicates import remove_duplicates_from_list


def process_duplicates(file_path):
    data = read_json_file(file_path)
    if isinstance(data, list):
        processed_data = remove_duplicates_from_list(data)
        save_to_json(file_path, processed_data)
    else:
        print("Error: JSON data is not a list.")


if __name__ == "__main__":
    path = "duplicates_base.json"
    process_duplicates(path)
