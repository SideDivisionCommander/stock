__author__ = 'SideDivisionCommander'

import os, sys
import datetime
import time
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

def save_ema(data_array, ema_file):
    tag1 = ","
    tag2 = ";"
    f = open(ema_file,'a')
    #iter every row 
    for i in range(data_array.shape[0]):  
        f.write(repr(data_array[i, 0]) + tag1)
        f.write(repr(data_array[i, 1]) + tag2)
    f.write("\n")
    f.close()
    return

def init_macd(data_array, new_level, ema_file):
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
    #allocate space for EMA_12 and EMA_26
    ema_array = np.zeros([data_array.shape[0], 2])
    #the DIFF and DEA of first time to market day is 0
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
        ema_array[i, 0] = EMA_12
        ema_array[i, 1] = EMA_26
    # Save ema_12 and ema_26 in file
    save_ema(ema_array[data_array.shape[0] - new_level:data_array.shape[0], :], ema_file)
    # return macd_array[data_array.shape[0] - new_level:data_array.shape[0], :]
    return 

def get_macd_cross_near_zero(macd_array, stock_code, macd_file):
    f = open(macd_file,'a')
    for i in range(macd_array.shape[0]):
        if i == 0 or i == 1:
            continue
        elif macd_array[i, 2] >= 0.00 and macd_array[i, 2] <= 0.10\
             and macd_array[i, 0] >= 0.00 and macd_array[i, 0] <= 0.10\
             and macd_array[i, 1] >= 0.00 and macd_array[i, 1] <= 0.10\
             and macd_array[i - 2, 0] < macd_array[i - 2, 1]\
             and macd_array[i - 1, 0] < macd_array[i - 1, 1]:
            # occur just now
            if i >= 98:
                print("occur: " + stock_code + " position: " + str(i))
                f.write(stock_code + "\n")
                f.write(str(i) + "\n")
                f.write("\n")
                f.close()
            return True
    f.close()
    return False

def update_ema(ema_file, date, data_array):
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
        close_price = get_newest_close_price(format_stock_code(data_array[row_index - 1]), date)
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
Get macd golden crossing over zero 
'''
def get_macd_golden_crossing(data, macd_file, new_level, ema_file, mode):
    all_stock_num = data.shape[0]
    stock_array = np.zeros([all_stock_num, 2])
    stock_array[:, 0] = data['code']
    stock_array[:, 1] = data['timeToMarket']

    if "init" == mode:
        #reinit ema file 
        if os.path.exists(ema_file):
        print("Removing old ema file: " + file)
        os.remove(file)
        f = open(ema_file,'a')
        #add timestamp at first row
        f.write(time.strftime("%Y-%m-%d", time.localtime()))
        f.write("\n")
        
        for i in range(all_stock_num):
            stock_code = format_stock_code(stock_array[i, 0])
            stock_time_to_market = format_stock_time_to_market(stock_array[i, 1])
            # To avoid stock with unmeaningful time
            if 'invalid' == stock_time_to_market:
                continue
            stock_k_data_array = np.array(ts.get_k_data(stock_code, start=stock_time_to_market))
            # To avoid new stock or secondary new stock
            if(stock_k_data_array.shape[0] < new_level):
                continue
            
            # To init ema file
            init_macd(stock_k_data_array, new_level, ema_file)
            #get_macd_cross_near_zero(macd_array, stock_code, macd_file)
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
        calc_macd(ema_file)
        

    else:
        print("Not valid mode, please check !")
    return 

        


