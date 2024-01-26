from bs4 import BeautifulSoup
from utils.json_handler import read_json_file
from utils.check_translation import is_translated
from utils.ignore import ignore_cases


def extract_english_text(html_content, url, file_path, ignore_path):
    soup = BeautifulSoup(html_content, "html.parser")
    ignore_data = read_json_file(ignore_path)
    ignore_misses = read_json_file(file_path)
    if not ignore_misses:
        ignore_misses = {}
        ignore_misses[url] = []
    if url not in ignore_misses.keys():
        ignore_misses[url] = []

    english_text = []
    for text in soup.stripped_strings:
        if is_translated(text, "en") and not ignore_cases(
            text, ignore_misses[url], ignore_data
        ):
            english_text.append(text)
    return english_text


def extract_non_english_text(html_content, url, file_path, ignore_path):
    soup = BeautifulSoup(html_content, "html.parser")
    ignore_data = read_json_file(ignore_path)
    ignore_misses = read_json_file(file_path)
    if not ignore_misses:
        ignore_misses = {}
        ignore_misses[url] = []
    if url not in ignore_misses.keys():
        ignore_misses[url] = []

    non_english_text = []
    for text in soup.stripped_strings:
        if not is_translated(text, "en") and not ignore_cases(
            text, ignore_misses[url], ignore_data
        ):
            non_english_text.append(text)

    return non_english_text
