import pandas as pd
import numpy as np

import mfg_data_formats as mdf

df = pd.read_csv("continuous_factory_process.csv")

# for col in df.columns:
#     try:
#         print("'%s': [%8.8f, %8.8f]," % (col, df[col].min(), df[col].max()))
#     except:
#         pass

# Create DataFrame containing every column in mfg_data_formats
print(mdf.fmt_00001_columns.keys())
df = pd.DataFrame(columns = mdf.fmt_00001_columns.keys())