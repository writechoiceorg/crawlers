from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract_texts import extract_non_english_text
from utils.json_handler import save_to_json


def handle_localize_widget(driver):
    # Hover over a div with id "localize-widget"
    localize_widget = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "localize-widget"))
    )
    webdriver.ActionChains(driver).move_to_element(localize_widget).perform()

    # Click the link with content "English"
    selector = '//a[contains(text(), "English")]'
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


def interact_with_page(url, file_path, ignore_path):
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

            non_english = extract_non_english_text(
                full_content, link_url, file_path, ignore_path
            )

            if non_english:
                non_english_texts[link_url] = non_english

            visited_links.append(link_url)

            save_to_json(file_path, non_english_texts)
        return non_english_texts
    except Exception as e:
        print(f"Error occurred while processing {link_url}:\n {e}")
    finally:
        driver.quit()


def pagbank_crawler():
    ignore_path = "./pagbank/ignore.json"

    json_file_path = "./pagbank/missing_translation.json"
    base_url = "https://dev.pagbank.uol.com.br/reference/introducao"
    interact_with_page(base_url, json_file_path, ignore_path)

    print(f"Missing translations saved to {json_file_path}")
