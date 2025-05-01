import pandas as pd
import numpy as np
import json
with open('mapping.json') as file:
    data1 = json.load(file)
    data2 = pd.read_csv('../data/processed/empty-opencage-geocoded-8211703482.csv')
    for row in data2.iterrows():
        data1[row[1].address] = {'Longitude': row[1].Longitude, 'Latitude': row[1].Latitude}
    print(data1)

with open('final address mappings.json', 'w') as mp:
    json.dump(data1, mp, indent=4)