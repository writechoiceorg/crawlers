from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import langdetect
import langid


def read_json_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data_dict = json.load(file)
        return data_dict
    except Exception:
        return {}


def ignore_string_cases(string, url):
    ignore_data = read_json_file("./ignore.json")
    if url in ignore_data.keys():
        ignore_string = [True for data in ignore_data[url] if string == data]
    else:
        ignore_string = False

    try:
        int(string)
        return True
    except ValueError:
        pass

    if (
        string.startswith(("https://", "http://"))
        or string in "📘🚧❗️👍."
        or not string
        or ignore_string
    ):
        return True
    return False


def is_english(text):
    try:
        lang = langdetect.detect(text)
        lang2, _ = langid.classify(text)
        return lang == "en" and lang2 == "en"
    except Exception:
        return None


def extract_non_english_text(html_content, url):
    soup = BeautifulSoup(html_content, "html.parser")

    non_english_text = []
    for text in soup.stripped_strings:
        if not is_english(text) and ignore_string_cases(text, url):
            non_english_text.append(text)

    return non_english_text


def save_to_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def handle_localize_widget(driver):
    # Hover over a div with id "localize-widget"
    localize_widget = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "localize-widget"))
    )
    webdriver.ActionChains(driver).move_to_element(localize_widget).perform()

    # Click the link with content "English"
    english_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "English")]'))
    )
    english_link.click()


def handle_sidebar_links(driver):
    sidebar_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Sidebar1t2G1ZJq-vU1 a"))
    )
    return [link.get_attribute("href") for link in sidebar_links]


def interact_with_page(url):
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        handle_localize_widget(driver)

        non_english_texts = {}
        links = handle_sidebar_links(driver)
        visited_links = []

        for link_url in links:
            if link_url in visited_links:
                continue

            driver.get(link_url)

            title = driver.find_element(By.ID, "content-head").get_attribute(
                "outerHTML"
            )

            article_content = driver.find_element(
                By.CLASS_NAME, "markdown-body"
            ).get_attribute("outerHTML")

            full_content = title + article_content

            non_english = extract_non_english_text(full_content, link_url)

            if non_english:
                non_english_texts[link_url] = non_english

            visited_links.append(link_url)
        return non_english_texts
    except Exception as e:
        print(f"Error occurred while processing {link_url}:\n {e}")
    finally:
        driver.quit()


base_url = "https://dev.pagbank.uol.com.br/reference/introducao"
result = interact_with_page(base_url)

# Save non-English texts to a JSON file
json_file_path = "missing_translation.json"
save_to_json(json_file_path, result)

print(f"Missing translations saved to {json_file_path}")
