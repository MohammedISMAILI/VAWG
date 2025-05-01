import json
import numpy as np
import pandas as pd
with open("mapping.json", 'r') as f:
    data = json.load(f)
    empty = []
    for key, value in data.items():
        if(not np.isnan(value[0])):
            continue
        empty.append(key)
    df = pd.DataFrame({'id': range(len(empty)), 'address': empty})
df.to_csv("empty.csv",index=False)