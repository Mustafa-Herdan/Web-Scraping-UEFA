import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/List_of_European_Cup_and_UEFA_Champions_League_finals"

page = requests.get(url)

soup = BeautifulSoup(page.text)

table_col = soup.find("table", class_="wikitable plainrowheaders sortable")

title = table_col.find_all("th", scope="col")[0:8]

for r in title:
    for a in r.find_all("a"):
        a.extract()

titles = [i.text.strip() for i in title]

df = pd.DataFrame(columns=titles)

table_row = table_col.find_all("tr")

for row in table_row[1:-4]:
    if len(row) > 4:
        rows = row.find_all("th", scope="row")
        title_row = [x.text.strip() for x in rows]
        new_rows = row.find_all("td")
        new_title_row = [y.text.strip() for y in new_rows]
        title_row.extend(new_title_row)
        df.loc[len(df)] = title_row

df.to_csv("UEFA Champions League.csv", index=False)
