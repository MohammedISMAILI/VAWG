import os
import re
import pandas as pd
import geopandas as gpd
import leafmap.foliumap as leafmap
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from zipfile import ZipFile
import json
import numpy as np

df = pd.read_csv("../data/raw/Crime_Reports_20240701.csv")
crimes = ['Harassment', 'Sex Offender Violation', 'Stalking', 'Domestic Dispute']

filtered_df = df[df.loc[:,'Crime'].map(lambda x: x in crimes)]
addresses = filtered_df.Location.unique()

locator = Nominatim(user_agent='spatialthoughts', timeout=10)
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

mapping = {}
for i, address in enumerate(addresses):
    if(i%10 == 0):
        print(f'{i/len(addresses)*100:.2f}%')
    x = geocode(address)
    try:
        mapping[address] = {'Longitude': x.longitude, 'Latitude': x.latitude}
    except:
        mapping[address] = (np.nan, np.nan)

with open("mapping.json", "w") as file:
    json.dump(mapping, file, indent=4)