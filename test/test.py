from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome

from regions.stavropol import autoshop26
from regions.surgut import autosurgut186, profsouz, aspect, sibir

chrome_driver_path = ChromeDriverManager().install()
browser_service = Service(executable_path=chrome_driver_path)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = Chrome(service=browser_service, options=options)
lst_name = []
with open('../autolist.txt', 'r', encoding='utf-8') as f:
    lst = f.readlines()
    for item in lst:
        lst_name.append(item.split('|')[0].strip())
res_ = profsouz({}, browser)
for i in res_:
    if i[0] not in lst_name:
        print(i[0])

