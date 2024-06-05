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
