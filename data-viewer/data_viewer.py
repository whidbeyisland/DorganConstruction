import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QComboBox, QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon
import os
import time
from datetime import datetime
from pandas_model import pandasModel

# get path where all device output CSVs are stored
path_mfgdata = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'mfg-data'))
device_df = pd.read_csv(os.path.join(path_mfgdata, 'device_id_customer_id.csv'), dtype=str)

class Window(QMainWindow):
    """
    Function to generate a DataFrame, filtered via the filters the user chooses
    Parameters:
    - customers: a list of customer IDs
    """
    def get_updated_df(self, customers):
        # get the ID of every device owned by the selected customers
        device_df_filtered = device_df.query('customer_id in @customers')
        device_list = [str(x) for x in device_df_filtered['device_id']]

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
            _df = pd.read_csv(os.path.join(path_mfgdata, csv), dtype=str)
            if df is not None:
                df = pd.concat([df, _df], ignore_index=True).fillna('-')
            else:
                df = _df.copy(deep=True)

        return df
    
    def save_csv(self):
        default_name = str(datetime.now()).replace(':', '').replace('.', '') + '.csv'
        name = QFileDialog.getSaveFileName(self, 'Save File', default_name, 'Comma-Separated Values (*.csv)')
        self.df.to_csv(name[0])
    
    def __init__(self):
        super().__init__()
  
        # setting title
        self.setWindowTitle('Data Viewer')
  
        # setting geometry
        self.setGeometry(100, 100, 1000, 800)
  
        # calling method
        self.UiComponents()
  
        # showing all the widgets
        self.show()
    
    def update_table(self):
        selected_customer = self.combobox.currentText()
        self.df = self.get_updated_df([selected_customer])
        model = pandasModel(self.df)
        self.table_view.setModel(model)
        self.table_view.resize(800, 600)
        self.table_view.show()

        # update save button
        self.save_button = QPushButton('Save CSV', self)
        self.save_button.pressed.connect(self.save_csv)
        self.save_button.setGeometry(50, 200, 100, 50)
        self.save_button.show()
    
    def UiComponents(self):
        # retrieve a list of all customer IDs
        customer_list = [str(x) for x in device_df['customer_id'].unique()]

        self.combobox = QComboBox(self)
        for customer in customer_list:
            self.combobox.addItem(customer)
        self.combobox.setGeometry(50, 50, 200, 50)
        
        self.load_button = QPushButton('Load records', self)
        # adding action to button
        self.load_button.pressed.connect(self.update_table)
        self.load_button.setGeometry(50, 125, 100, 50)

        self.table_view = QTableView()

# create pyqt5 app
app = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# keep window open
sys.exit(app.exec())