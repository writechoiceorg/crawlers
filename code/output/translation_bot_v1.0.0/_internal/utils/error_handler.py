from utils.json_handler import read_json_file, save_to_json


def error_handler(path, new_error):
    errors = read_json_file(path)
    errors.append(new_error)
    save_to_json(path, errors)
