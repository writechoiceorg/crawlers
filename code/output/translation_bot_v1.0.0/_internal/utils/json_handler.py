import json


def save_to_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def read_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data_dict = json.load(file)
        return data_dict
    except Exception:
        return {}
