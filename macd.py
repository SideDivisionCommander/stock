__author__ = 'SideDivisionCommander'

import os
import datetime
import numpy as np
import pandas as pd
import tushare as ts
from pandas import Series, DataFrame

def format_stock_code(code):
    formatted_code = str(int(code))
    if len(formatted_code) < 6:
        prefix = ''
        for j in range(6 - len(formatted_code)):
            prefix = prefix + '0'
        formatted_code = prefix + formatted_code
    return formatted_code

def format_stock_time_to_market(time):
    formatted_time_to_market = str(int(time))
    if len(time) != 8:
        return 'invalid'
    formatted_time_to_market = formatted_time_to_market[:4] + '-' + formatted_time_to_market[4:6] + '-' + formatted_time_to_market[6:]
    return formatted_time_to_market

# return last 100 daily macd
def get_macd(data_array):
    #allocate space for open price in data_array
    open_price_array = np.zeros([data_array.shape[0], 1])
    #allocate space for close price in data_array
    close_price_array = np.zeros([data_array.shape[0], 1])
    #get all open price in data_array (all num in the first column)
    open_price_array = data_array[:, 1]
    #get close open price in data_array (all num in the close column)
    close_price_array = data_array[:, 2]
    #allocate space for DEA, DIFF, MACD
    macd_array = np.zeros([data_array.shape[0], 3])

    # the DIFF and DEA of first day is 0
    DIFF = 0
    DEA = 0
    MACD = 0
    EMA_12 = 0
    EMA_26 = 0
    for i in range(data_array.shape[0]):
        if 0 == i:
            DIFF = 0
            DEA = 0
            MACD = 0
            EMA_12 = close_price_array[i]
            EMA_26 = close_price_array[i]
        else:
            EMA_12 = EMA_12 * 11 / 13 + close_price_array[i] * 2 / 13
            EMA_26 = EMA_26 * 25 / 27 + close_price_array[i] * 2 / 27
            DIFF = EMA_12 - EMA_26
            DEA = DEA * 8 /10 + DIFF * 2 / 10
            MACD = (DIFF - DEA) * 2
        macd_array[i, 0] = round(DIFF, 2)
        macd_array[i, 1] = round(DEA, 2)
        macd_array[i, 2] = round(MACD, 2)
    return macd_array[data_array.shape[0] - 100:data_array.shape[0], :]

'''
Get macd golden crossing over zero 
'''
def get_macd_golden_crossing(data, file):
    all_stock_num = data.shape[0]
    stock_array = np.zeros([all_stock_num, 2])
    stock_array[:, 0] = data['code']
    stock_array[:, 1] = data['timeToMarket']

    for i in range(all_stock_num):
        stock_code = format_stock_code(stock_array[i, 0])
        stock_time_to_market = format_stock_time_to_market(stock_array[i, 1])
        # To avoid stock with unmeaningful time
        if 'invalid' == stock_time_to_market:
            continue
        stock_k_data_array = np.array(ts.get_k_data(stock_code, start=stock_time_to_market))
        # To avoid new stock or secondary new stock
        if(stock_k_data_array.shape[0] < 100):
            continue
        macd_array = get_macd(stock_k_data_array)
        get_macd_cross_near_zero(macd_array, stock_code)

        


