import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def fetch_leaderboard():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(), options=options)
    driver.get("https://pewpew.live/era2")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'score_table')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    rows = soup.find('table', {'id': 'score_table'}).find('tbody').find_all('tr')
    leaderboard = [{
        'rank': int(row.find_all('td')[0].text.strip('.')),
        'score': float(row.find_all('td')[1].text.strip()),
        'username': ''.join(part.text for part in row.find_all('td')[2].find_all('span')),
        'country': row.find_all('td')[3].text.strip(),
        'wr': int(row.find_all('td')[4].text.strip()) if row.find_all('td')[4].text.strip().isdigit() else 0
    } for row in rows if len(row.find_all('td')) >= 5]

    return leaderboard

leaderboard = fetch_leaderboard()

if leaderboard:
    with open('output.json', 'w') as f:
        json.dump(leaderboard, f, ensure_ascii=False, indent=4)
