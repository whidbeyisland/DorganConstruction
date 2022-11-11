import numpy as np
import pandas as pd
import random
import uuid

from mfg_data_formats import fmt_00001_columns

# df = pd.read_csv("continuous_factory_process.csv")
# for col in df.columns:
#     try:
#         print("'%s': [%8.8f, %8.8f]," % (col, df[col].min(), df[col].max()))
#     except:
#         pass

# Create DataFrame containing every column in mfg_data_formats
columns = fmt_00001_columns.keys()
df = pd.DataFrame(columns = columns)

for i in range(0, 5):
    row = []
    for col in columns:
        # fill the column with an appropriate random value depending on its type, e.g. "number", "datetime"
        if fmt_00001_columns[col][0] == 'number':
            min = fmt_00001_columns[col][1]
            max = fmt_00001_columns[col][2]
            val = round(random.uniform(min, max), 8)
            row.append(val)
        
        elif fmt_00001_columns[col][0] == 'datetime':
            year = random.randint(1970, 2069)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            val = '%04d-%02d-%02d %02d:%02d:%02d' % (year, month, day, hour, minute, second)
            row.append(val)
        
        elif fmt_00001_columns[col][0] == 'string':
            val = uuid.uuid4()
            row.append(val)

    row_df = pd.DataFrame([row], columns=columns)
    df = pd.concat([df, row_df], ignore_index=True)
df.to_csv('test.csv', sep=',', encoding='utf-8')