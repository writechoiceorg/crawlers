from yuno_translation_crawler import read_json_file, save_to_json


def remove_duplicates(json_data):
    unique_strings = []
    for string in json_data:
        if string not in unique_strings:
            unique_strings.append(string)

    return unique_strings


if __name__ == "__main__":
    json_data = read_json_file("./yuno/ignore.json")

    unique_strings = remove_duplicates(json_data)

    save_to_json("./yuno/ignore.json", unique_strings)
