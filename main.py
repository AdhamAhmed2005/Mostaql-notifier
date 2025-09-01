import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pushbullet import Pushbullet
import time as t

API_KEY = os.getenv("PUSHBULLET_API_KEY")
pb = Pushbullet(API_KEY)

url = "https://mostaql.com/projects/skill/web-development"
seen_projects = set()

def check_projects():
    global seen_projects

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/139.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    t.sleep(5)

    titles = driver.find_elements(By.CSS_SELECTOR, ".mrg--bt-reset a")
    descriptions = driver.find_elements(By.CSS_SELECTOR, ".details-url")
    times = driver.find_elements(By.CSS_SELECTOR, "time")

    count = 0
    for title_el, desc_el, time_el in zip(titles, descriptions, times):
        title = title_el.text.strip()
        link = title_el.get_attribute("href")
        desc = desc_el.text.strip()
        project_time = time_el.text.strip()
        count += 1

        if title not in seen_projects and count <= 3:
            seen_projects.add(title)
            print("Sending notification:", title)
            pb.push_link(title, link, body=f"{desc}\nTime: {project_time}")

    driver.quit()


if __name__ == "__main__":
    check_projects()
