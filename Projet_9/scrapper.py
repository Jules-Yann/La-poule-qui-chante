import pandas as pd
from requests import get
from scrapy import Selector

df = pd.DataFrame(columns=['Zone', 'Distance'])

# Retrieving the site code
url = "https://www.distance-between-countries.com/countries/distance_between_countries.php?from=France&language=French"
response = get(url)
source = None
if response.status_code == 200:
    source = response.text

# Selection of data to scrapped
selector = Selector(text=source)
table = selector.css("table.center_bordered > tr > td").getall()

# Values selection and add to dataframe
for country in table:
    selector = Selector(text=country)
    zone = selector.css("b > a::text").get()
    distance = selector.css("td::text").getall()
    if(zone is not None):
      df = df.append(pd.Series([zone, distance[1]], index=df.columns), ignore_index=True)

# Formatting values
df['Distance'] = df['Distance'].str.replace('est de', '')
df['Distance'] = df['Distance'].str.replace(',', '')
df['Distance'] = df['Distance'].str.replace('kilomètres', '')
df['Distance'] = df['Distance'].str.replace(' ', '')

# Dataframe to csv
df.to_csv('./data/distance.csv')