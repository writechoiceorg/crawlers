from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract_texts import extract_english_text
from utils.json_handler import save_to_json


def handle_localize_widget(driver):
    # Hover over a div with id "localize-widget"
    localize_widget = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "localize-widget"))
    )
    webdriver.ActionChains(driver).move_to_element(localize_widget).perform()

    # Click the link with content "English"
    selector = '//a[contains(text(), "Español")]'
    english_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, selector))
    )
    english_link.click()


def handle_sidebar_links(driver):
    selector = ".Sidebar1t2G1ZJq-vU1 a"
    sidebar_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
    return [link.get_attribute("href") for link in sidebar_links]


def ideal_crawler(url, file_path, ignore_path, translated_path):
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        english_texts = {}
        links = handle_sidebar_links(driver)
        visited_links = []
        errors = []

        for link_url in links:
            if link_url in visited_links:
                continue
            try:
                driver.get(link_url)
                handle_localize_widget(driver)
                title = driver.find_element(
                    By.ID,
                    "content-head",
                ).get_attribute("outerHTML")

                article_content = driver.find_element(
                    By.CLASS_NAME, "markdown-body"
                ).get_attribute("outerHTML")

                full_content = title + article_content

                english = extract_english_text(
                    full_content, link_url, translated_path, ignore_path
                )

                if english:
                    english_texts[link_url] = english

                visited_links.append(link_url)

                save_to_json(file_path, english_texts)
            except Exception:
                errors.append(link_url)
                print(f"Error occurred while processing {link_url}")
                pass
    except Exception:
        print(f"Something went wrong at: {link_url}")
    finally:
        driver.quit()
    return errors


def run_ideal_guides():
    ignore_path = "./utils/ideal/ignore.json"
    translated_path = "./utils/ideal/translated/guides.json"
    json_file_path = "./ideal_guides_missing_translation.json"

    base_url = "https://docs.ideal.pr.gov/docs/getting-started"
    errors_guides = ideal_crawler(
        base_url, json_file_path, ignore_path, translated_path
    )

    if errors_guides:
        save_to_json("./ideal_guides_errors.json", errors_guides)

    print(f"Missing guides translations saved at {json_file_path}")


def run_ideal_apiref():
    ignore_path = "./_internal/utils/ideal/ignore.json"
    translated_path = "./_internal/utils/ideal/translated/apiref.json"
    json_file_path = "./ideal_apiref_missing_translation.json"

    base_url = "https://docs.ideal.pr.gov/reference/introduction"
    errors_api = ideal_crawler(base_url, json_file_path, ignore_path, translated_path)

    if errors_api:
        save_to_json("./ideal_apiref_errors.json", errors_api)

    print(f"Missing API ref translations saved at {json_file_path}")
