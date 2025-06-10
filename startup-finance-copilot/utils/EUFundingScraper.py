from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class EUFundingScraper:
    URL = "https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/projects-results?isExactMatch=true&order=DESC&pageNumber=1&pageSize=10&sortBy=es_SortDate"

    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def search(self, keyword, max_results=10):
        print("Ανοίγω τη σελίδα:", self.URL)
        self.driver.get(self.URL)
        time.sleep(5)
        print(self.driver.title)

        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "global-search"))
            )
            print("Βρήκα το πεδίο αναζήτησης, στέλνω λέξη-κλειδί...")
            search_input.click()
            search_input.clear()
            search_input.send_keys(keyword)
            search_input.send_keys(Keys.RETURN)
        except Exception as e:
            print("⚠️ Timeout ή πρόβλημα στη φόρτωση πεδίου αναζήτησης:", e)
            self.driver.quit()
            return []

        try:
            wait = WebDriverWait(self.driver, 30)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "eui-card-header-title a.eui-u-text-link"))
            )

            cards = self.driver.find_elements(By.CSS_SELECTOR, "eui-card-header-title a.eui-u-text-link")
            print(f"Βρέθηκαν {len(cards)} ευκαιρίες.")
            base_url = "https://ec.europa.eu"

            results = []
            for a in cards[:len(cards)]:
                title = a.text.strip()
                href = a.get_attribute("href")
                full_url = href if href.startswith("http") else base_url + href

                # Προσπαθώ να ανέβω DOM για deadline/description
                try:
                    parent_card = a.find_element(By.XPATH, "./ancestor::eui-card")
                except:
                    parent_card = None

                if parent_card:
                    try:
                        deadline = parent_card.find_element(By.CLASS_NAME, "eui-chip__content-container").text
                    except:
                        deadline = "No Deadline"
                    try:
                        description = parent_card.find_element(By.CSS_SELECTOR, "div.showMore--one-line").text
                    except:
                        description = "No Description"
                else:
                    deadline = "No Deadline"
                    description = "No Description"

                results.append({
                    "title": title,
                    "link": full_url,
                    "deadline": deadline,
                    "description": description
                })

            return results

        except Exception as e:
            print("⚠️ Δεν βρέθηκαν αποτελέσματα ή καθυστέρησαν:", e)
            return []

        finally:
            self.driver.quit()



if __name__ == "__main__":
    scraper = EUFundingScraper()
    projects = scraper.search("renewable energy", max_results=10)

    if projects:
        for i, proj in enumerate(projects, 1):
            print(f"Project {i}:")
            print(f"Title: {proj['title']}")
            print(f"Link: {proj['link']}")
            print(f"Deadline: {proj['deadline']}")
            print(f"Description: {proj['description']}")
            print("-" * 40)
    else:
        print("⚠️ Δεν βρέθηκαν ή επέστρεψαν αποτελέσματα.")
