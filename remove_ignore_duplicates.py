from utils.json_handler import save_to_json, read_json_file
from utils.remove_duplicates import remove_duplicates_from_list


def remove_duplicates(path):
    json = read_json_file(path)
    unique_strings = remove_duplicates_from_list(json)
    ordered_strings = sorted(unique_strings)
    save_to_json(path, ordered_strings)


if __name__ == "__main__":
    path = "./yuno/ignore.json"
    remove_duplicates(path)
