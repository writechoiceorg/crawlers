from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.extract_texts import extract_text
from utils.json_handler import save_to_json
from utils.error_handler import error_handler
from crawler_yuno import handle_sidebar_links


def handle_localize_widget(driver):
    try:
        localize_widget = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "localize-widget"))
        )
        webdriver.ActionChains(driver).move_to_element(localize_widget).perform()
        active_lang = (
            WebDriverWait(driver, 10)
            .until(EC.presence_of_element_located((By.ID, "localize-active-lang")))
            .get_attribute("innerHTML")
        )
        english_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//a[contains(text(), "English")]')
            )
        )
    except Exception:
        pass

    if "English" not in active_lang:
        english_link.click()


def interact_with_page(url, file_path):
    try:
        driver = webdriver.Chrome()
        driver.get(url)

        texts = {}
        links = handle_sidebar_links(driver)
        visited_links = []

        for link_url in links:
            if link_url in visited_links:
                continue
            if link_url == "https://docs.y.uno/docs/algeria":
                break
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

                if full_content:
                    texts[link_url] = extract_text(full_content)

                visited_links.append(link_url)

                save_to_json(file_path, texts)
            except Exception as e:
                error_handler("./yuno/errors.json", link_url)
                print(f"Error occurred while processing {link_url}:\n {e}")
                pass
    except Exception as err:
        print(f"Something went wrong at: {link_url}\n {err}")
    finally:
        driver.quit()


def run_page_text_reader():
    base_url = "https://docs.y.uno/docs/overview"
    json_file_path = "./yuno/translated/guides.json"
    interact_with_page(base_url, json_file_path)

    print(f"Missing guides translations saved to {json_file_path}")

    base_url = "https://docs.y.uno/reference/introduction"
    json_file_path = "./yuno/translated/apiref.json"
    interact_with_page(base_url, json_file_path)

    print(f"Missing API ref translations saved to {json_file_path}")


if __name__ == "__main__":
    run_page_text_reader()
