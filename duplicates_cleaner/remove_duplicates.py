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


def remove_duplicates_from_dict(json_data):
    unique_strings = []
    for _, strings in json_data.items():
        for string in strings:
            if string not in unique_strings:
                unique_strings.append(string)
    return unique_strings


def remove_duplicates_from_list(json_data):
    unique_strings = list(set(json_data))
    unique_strings.sort()
    return unique_strings


if __name__ == "__main__":
    filepath = "file.json"
    cleanedData = remove_duplicates_from_list(read_json_file(filepath))
    save_to_json(filepath, cleanedData)
