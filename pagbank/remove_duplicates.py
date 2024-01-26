from pagbank._deprecated_crawler import read_json_file, save_to_json


def remove_duplicates(json_data):
    unique_strings = []
    for _, strings in json_data.items():
        for string in strings:
            if string not in unique_strings:
                unique_strings.append(string)

    return unique_strings


if __name__ == "__main__":
    json_data = read_json_file("./pagbank/missing_translation.json")

    unique_strings = remove_duplicates(json_data)

    save_to_json("./pagbank/ignore.json", unique_strings)
