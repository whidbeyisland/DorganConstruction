import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import os
import time

from pandas_model import pandasModel

######################################
# Setting up DataFrame to display
######################################

# get path where all device output CSVs are stored
path_mfgdata = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mfg-data'))

# get the ID of every device owned by the selected customers
customer_id = '2772903375624'

device_df = pd.read_csv(os.path.join(path_mfgdata, 'device_id_customer_id.csv'))
device_df_filtered = device_df.query('customer_id == ' + customer_id)
device_list = [str(x) for x in device_df['device_id']]

# get every CSV corresponding to one of these devices

files = os.listdir(path_mfgdata)
csvs_to_read = []
for file in files:
    if file.endswith('.csv'):
        if file.split('_')[0] in device_list:
            csvs_to_read.append(file)
print(csvs_to_read)
print(len(csvs_to_read))

time.sleep(50000)

# path_csv = os.path.join(path_mfgdata, 'continuous_factory_process.csv')
# df = pd.read_csv(path_csv)

######################################
# Setting up GUI using PyQT5
######################################

app = QApplication(sys.argv)
model = pandasModel(df)
view = QTableView()
view.setModel(model)
view.resize(800, 600)
view.show()
sys.exit(app.exec_())