__author__ = 'SideDivisionCommander'

import os, sys
import datetime
import time
import numpy as np
from numpy import genfromtxt
import scipy as sc
import pandas as pd
import tushare as ts
from pandas import Series, DataFrame

'''
Function: 
'''
def save_macd_para(macd_para_array, macd_para_file):
    tag1 = ","
    tag2 = ";"
    f = open(macd_para_file, 'a')
    #iter every row 
    for i in range(data_array.shape[0]): 
        f.write(repr(macd_para_array[i, 0]) + tag1)
        f.write(repr(macd_para_array[i, 1]) + tag1)
        f.write(repr(macd_para_array[i, 2]) + tag2)
    f.write("\n")
    f.close()
    return

'''
Function: 
'''
def init_macd_para(stock_k_data_array, new_level, macd_para_file):
    # Allocate space for close price in data_array
    close_price_array = np.zeros([stock_k_data_array.shape[0], 1])
    # Get all open price in data_array (all num in the first column)
    close_price_array = stock_k_data_array[:, 2]
    # Allocate space for EMA 12, EMA 26, DEA
    macd_para_array = np.zeros([stock_k_data_array.shape[0], 3])
    # Init the all para of first time to market day (all zero)
    EMA_12 = 0
    EMA_26 = 0
    DIFF = 0
    DEA = 0

    for i in range(stock_k_data_array.shape[0]):
        if 0 == i:
            EMA_12 = close_price_array[i]
            EMA_26 = close_price_array[i]
            DIFF = 0
            DEA = 0
        else:
            EMA_12 = EMA_12 * 11 / 13 + close_price_array[i] * 2 / 13
            EMA_26 = EMA_26 * 25 / 27 + close_price_array[i] * 2 / 27
            DIFF = EMA_12 - EMA_26
            DEA = DEA * 8 /10 + DIFF * 2 / 10
        macd_para_array[i, 0] = EMA_12
        macd_para_array[i, 1] = EMA_26
        macd_para_array[i, 2] = DEA
    # Save last new level EMA 12, EMA 26, DEA in file
    save_macd_para(macd_para_array[stock_k_data_array.shape[0] - new_level:stock_k_data_array.shape[0], :], macd_para_file)
    return 

'''
Function: 
'''
def get_macd_cross_near_zero(macd_para_file, stock_code_array, macd_filter_result_file):
    tag1 = ';'
    tag2 = ','
    os.path.exists(macd_filter_result_file):
        print("Removing old filter macd result file: " + macd_filter_result_file)
        os.remove(macd_filter_result_file)
    f1 = open(macd_para_file, 'r')
    row_index = 0
    for line in f1:
        if row_index == 0:
            row_index += 1
            continue
        macd_para_list = line.split(tag1)
        macd_para_array = np.zeros([len(macd_para_list), 3])
        for para in macd_para_list:
            separate_para = para.split(tag2)
            EMA_12 = separate_para[0]
            EMA_26 = separate_para[1]
            DIFF = EMA_12 - EMA_26
            DEA = separate_para[2]
            MACD = (DIFF - DEA) * 2
            macd_para_array[row_index - 1, 0] = round(DIFF, 2)
            macd_para_array[row_index - 1, 1] = round(DEA, 2)
            macd_para_array[row_index - 1, 2] = round(MACD, 2)
        
        f2 = open(macd_filter_result_file, 'a')
        for i in range(macd_para_array.shape[0]):
            if i == 0 or i == 1:
                continue
            elif macd_para_array[i, 2] >= 0.00 and macd_para_array[i, 2] <= 0.10\
                and macd_para_array[i, 0] >= 0.00 and macd_para_array[i, 0] <= 0.10\
                and macd_para_array[i, 1] >= 0.00 and macd_para_array[i, 1] <= 0.10\
                and macd_para_array[i - 2, 0] < macd_para_array[i - 2, 1]\
                and macd_para_array[i - 1, 0] < macd_para_array[i - 1, 1]:
                # occur just now
                if i >= 98:
                    print("Occur: " + stock_code_array[row_index - 1] + " position: " + str(i))
                    f2.write(stock_code_array[row_index - 1] + "\n")
                    f2.write(str(i) + "\n")
                    f2.write("\n")
        f2.close()
        row_index += 1
    f1.close()
    return

def update_ema(ema_file, date, stock_code_array):
    tag = ";"
    f1 = open(ema_file, 'r')
    f2 = open('tmp.txt', 'a')
    row_index = 0
    for line in f1:
        if row_index == 0:
            row_index += 1
            f2.write(date)
            f2.write("\n")
            continue
        close_price = get_newest_close_price(format_stock_code(stock_code_array[row_index - 1]), date)
        ema_list = line.split(tag)
        newest_ema = calc_ema(ema_list[-1], close_price)
        ema_list.pop(0)
        ema_list.append(newest_ema)
        row_index += 1
        for e in ema_list:
            f2.write(e + tag)
        f2.write("\n")
    f2.close()
    f1.close()
    os.remove(ema_file)
    os.rename('tmp.txt', ema_file)
    return

def get_newest_close_price(stock_code, date):
    stock_k_data_array = np.array(ts.get_k_data(stock_code, start=date))
    return stock_k_data_array[0, 2]

def calc_ema(last_ema, newest_close_price):
    last_ema_12 = last_ema.split(',')[0]
    last_ema_26 = last_ema.split(',')[1]
    ema_12 = float(last_ema_12) * 11 / 13 + newest_close_price * 2 / 13
    ema_26 = float(last_ema_26) * 25 / 27 + newest_close_price * 2 / 27
    return repr(ema_12) + "," + repr(ema_26)

'''
Function: 
'''
def get_macd_golden_crossing(stock_basic_data_file, macd_filter_result_file, new_level, macd_para_file, mode):
    stock_basic_data = genfromtxt(stock_basic_data_file, delimiter=",")    
    if "init" == mode:
        # Update macd_para file from the time to market 
        if os.path.exists(macd_para_file):
            print("Removing old ema file: " + file)
            os.remove(file)
        f = open(macd_para_file,'a')
        # Add timestamp at first row of file
        f.write(time.strftime("%Y-%m-%d", time.localtime()))
        f.write("\n")
        f.close()
        
        for i in range(stock_basic_data.shape[0]):
            stock_code = stock_basic_data[i, 0]
            stock_time_to_market = stock_basic_data[i, 1]
            stock_k_data_array = np.array(ts.get_k_data(stock_code, start=stock_time_to_market))
            init_macd_para(stock_k_data_array, new_level, macd_para_file)

    get_macd_cross_near_zero(macd_para_file, stock_basic_data[:, 0], macd_filter_result_file)
'''
    elif "normal" == mode:
        date = time.strftime("%Y-%m-%d", time.localtime())
        f = open(ema_file, 'r')
        first_line = f.readlines()[0]:
        if date == first_line:
            print("All data has been updated.")
            f.close()
            return
        f.close()
        update_ema(ema_file, date, stock_array[:, 0])
        get_macd_cross_near_zero(ema_file, stock_array[:, 0], macd_file)

    else:
        print("Not valid mode, please check !")
'''
    return 

        


