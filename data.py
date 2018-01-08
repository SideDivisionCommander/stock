__author__ = 'SideDivisionCommander'

import os
import tushare as ts
import pandas as pd
from pandas import Series, DataFrame

def get_basic_stock_data(file):
    if os.path.exists(file):
        print("Removing old stock basic data file: " + file)
        os.remove(file)
    print("Getting the data from server")
    df = ts.get_stock_basics()
    print("Writing data to file" + file)
    df.to_csv(file)
    print("Sync stock basic data success.")