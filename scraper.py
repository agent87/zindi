import requests
from bs4 import BeautifulSoup

URL = "https://m.egwwritings.org/rw/book/13880.480#480"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(class_="egw_content_wrapper")
for result in results:
    print(result)