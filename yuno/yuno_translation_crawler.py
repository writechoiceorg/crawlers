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


def ignore_cases(text, url, file_path):
    ignore_data = read_json_file("./yuno/ignore.json")
    ignore_misses = read_json_file(file_path)

    if not ignore_misses:
        ignore_misses = {}
        ignore_misses[url] = []

    try:
        int(text)
        return True
    except ValueError:
        pass

    if (
        text in ignore_data
        or text in ignore_misses[url]
        or text.startswith(("https://", "http://"))
        or text in "📘🚧❗️👍."
        or not text
    ):
        return True
    return False


def is_translated(text, language):
    try:
        lang = langdetect.detect(text)
        lang2, _ = langid.classify(text)
        return lang == language and lang2 == language
    except Exception:
        return None


def extract_english_text(html_content, url, file_path):
    soup = BeautifulSoup(html_content, "html.parser")

    english_text = []
    for text in soup.stripped_strings:
        if is_translated(text, "en") and not ignore_cases(text, url, file_path):
            english_text.append(text)
    return english_text


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
        EC.presence_of_element_located(
            (By.XPATH, '//a[contains(text(), "Español (América Latina)")]')
        )
    )
    english_link.click()


def handle_sidebar_links(driver):
    sidebar_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Sidebar1t2G1ZJq-vU1 a"))
    )
    return [link.get_attribute("href") for link in sidebar_links]


def interact_with_page(url, file_path):
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        handle_localize_widget(driver)

        english_texts = {}
        links = handle_sidebar_links(driver)
        visited_links = []

        for link_url in links[:1]:
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

            english = extract_english_text(full_content, link_url, file_path)

            if english:
                english_texts[link_url] = english

            visited_links.append(link_url)
        return english_texts
    except Exception as e:
        print(f"Error occurred while processing {link_url}:\n {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    base_url1 = "https://docs.y.uno/docs/overview"
    json_file_path1 = "./yuno/missing/guides_missing_translation_guides.json"
    result1 = interact_with_page(base_url1, json_file_path1)

    base_url2 = "https://docs.y.uno/reference/introduction"
    json_file_path2 = "./yuno/missing/apiref_missing_translation.json"
    result2 = interact_with_page(base_url2)

    save_to_json(json_file_path1, result1)
    save_to_json(json_file_path2, result2)

    print(f"Missing guides translations saved to {json_file_path1}")
    print(f"Missing API ref translations saved to {json_file_path2}")
