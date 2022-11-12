import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QComboBox, QWidget, QVBoxLayout
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
import os
import time
from pandas_model import pandasModel

# get path where all device output CSVs are stored
path_mfgdata = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mfg-data'))
device_df = pd.read_csv(os.path.join(path_mfgdata, 'device_id_customer_id.csv'))

"""
Function to generate a DataFrame, filtered via the filters the user chooses

Parameters:
- customers: a list of customer IDs
"""
def get_updated_df(customers):
    # get the ID of every device owned by the selected customers
    device_df_filtered = device_df.query('customer_id == @customers')
    device_list = [str(x) for x in device_df['device_id']]

    # get every CSV corresponding to one of these devices

    files = os.listdir(path_mfgdata)
    csvs_to_read = []
    for file in files:
        if file.endswith('.csv'):
            if file.split('_')[0] in device_list:
                csvs_to_read.append(file)

    # for each CSV: concatenate it with the previous one
    df = None
    for csv in csvs_to_read:
        _df = pd.read_csv(os.path.join(path_mfgdata, csv))
        if df is not None:
            df = pd.concat([df, _df], ignore_index=True).fillna('-')
        else:
            df = _df.copy(deep=True)

    return df

######################################
# Setting up GUI using PyQT5
######################################

app = QApplication(sys.argv)

# retrieve a list of all customer IDs
customer_list = [str(x) for x in device_df['customer_id'].unique()]

# first: create a view where the user is prompted to select a customer ID from a list

combobox = QComboBox()
for customer in customer_list:
    combobox.addItem(customer)

layout = QVBoxLayout()
layout.addWidget(combobox)
container = QWidget()
container.setLayout(layout)

w = QMainWindow()
w.setCentralWidget(container)
w.show()
app.exec_()

time.sleep(50000)

# create a new instance of pandasModel class containing the appropriate df, and display it as a QTableView
df = get_updated_df(['2772903375624'])
model = pandasModel(df)
view = QTableView()
view.setModel(model)
view.resize(800, 600)
view.show()

# keep window open
app.exec_()