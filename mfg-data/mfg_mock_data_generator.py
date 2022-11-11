import numpy as np
import pandas as pd
import random
import sys
import uuid

from mfg_data_formats import device_ids, formats_dict

# generate a dictionary in mfg_data_formats.py based on a sample document
# df = pd.read_csv("continuous_factory_process.csv")
# for col in df.columns:
#     try:
#         print("'%s': [%8.8f, %8.8f]," % (col, df[col].min(), df[col].max()))
#     except:
#         pass

format = 'format00001'
num_rows = 10
num_files = 10

# Create DataFrame containing every column in mfg_data_formats
sub_dict = formats_dict[format]
columns = sub_dict.keys()
df = pd.DataFrame(columns = columns)

for i in range(0, num_files):
    # pick a random mock device ID - this CSV will belong to that device
    device_id = random.choice(device_ids)

    for j in range(0, num_rows):
        row = []
        for col in columns:
            # fill the column with an appropriate random value depending on its type, e.g. "number", "datetime"
            if sub_dict[col][0] == 'number':
                min = sub_dict[col][1]
                max = sub_dict[col][2]
                val = round(random.uniform(min, max), 8)
                row.append(val)
            
            elif sub_dict[col][0] == 'datetime':
                year = random.randint(1970, 2069)
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                hour = random.randint(0, 23)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                val = '%04d-%02d-%02d %02d:%02d:%02d' % (year, month, day, hour, minute, second)
                row.append(val)
            
            elif sub_dict[col][0] == 'string':
                val = uuid.uuid4()
                row.append(val)

        row_df = pd.DataFrame([row], columns=columns)
        df = pd.concat([df, row_df], ignore_index=True)
    
    file_name = '%s_%s_%d.csv' % (device_id, format, random.randint(10000000, 99999999))
    df.to_csv(file_name, sep=',', encoding='utf-8')