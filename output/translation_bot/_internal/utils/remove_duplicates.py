# from yuno.yuno_translation_crawler import read_json_file, save_to_json


def remove_duplicates_from_dict(json_data):
    unique_strings = []
    for _, strings in json_data.items():
        for string in strings:
            if string not in unique_strings:
                unique_strings.append(string)

    return unique_strings


def remove_duplicates_from_list(json_data):
    unique_strings = []
    for string in json_data:
        if string not in unique_strings:
            unique_strings.append(string)

    return unique_strings
