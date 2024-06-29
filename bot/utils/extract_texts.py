from bs4 import BeautifulSoup
from utils.json_handler import read_json_file
from utils.check_translation import is_translated
from utils.ignore import ignore_cases, check_if_translated


def extract_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    texts = [text for text in soup.stripped_strings]
    return texts


def extract_english_text(html_content, url, translated_path, ignore_path):
    soup = BeautifulSoup(html_content, "html.parser")
    ignore_data = read_json_file(ignore_path)
    translated_data = read_json_file(translated_path)
    translated_data.setdefault(url, [])
    english_text = []
    for text in soup.stripped_strings:
        if check_if_translated(text, translated_data[url]):
            continue
        elif is_translated(text, "en") and not ignore_cases(text, ignore_data):
            english_text.append(text)
    return english_text


def extract_non_english_text(html_content, url, translated_path, ignore_path):
    soup = BeautifulSoup(html_content, "html.parser")
    ignore_data = read_json_file(ignore_path)
    translated_data = read_json_file(translated_path)

    non_english_text = []
    for text in soup.stripped_strings:
        if check_if_translated(text, translated_data[url]):
            continue
        elif not is_translated(text, "en") and not ignore_cases(text, ignore_data):
            non_english_text.append(text)

    return non_english_text
