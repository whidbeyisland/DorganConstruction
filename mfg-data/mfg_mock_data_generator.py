import pandas as pd
import numpy as np
import random

from mfg_data_formats import fmt_00001_columns

df = pd.read_csv("continuous_factory_process.csv")

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
        min = fmt_00001_columns[col][0]
        max = fmt_00001_columns[col][1]
        val = round(random.uniform(min, max), 8)
        row.append(val)
    row_df = pd.DataFrame([row], columns=columns)
    df = pd.concat([df, row_df], ignore_index=True)
df.to_csv('test.csv', sep=',', encoding='utf-8')