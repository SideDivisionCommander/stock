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
def get_basic_data(stock_basic_data_file):
    stock_basic_data = {}
    stock_basic_data['code'] = []
    stock_basic_data['timeToMarket'] = []
    with open(stock_basic_data_file, 'r') as f:
        for line in f:
            l = line.split(',')
            stock_code = l[0]
            time_to_market = l[1]
            stock_basic_data['code'].append(stock_code)
            stock_basic_data['timeToMarket'].append(time_to_market)
    return stock_basic_data
 
'''
Function: 
'''
def save_macd_para(macd_para_array, macd_para_file, date):
    tag1 = ","
    tag2 = ";"
    with open(macd_para_file, 'a') as f:
        f.write(date + tag2)
        #iter every row
        for i in range(macd_para_array.shape[0]): 
            f.write(repr(macd_para_array[i, 0]) + tag1)
            f.write(repr(macd_para_array[i, 1]) + tag1)
            f.write(repr(macd_para_array[i, 2]) + tag2)
        f.write("\n")
    return

'''
Function: 
'''
def init_macd_para(stock_k_data_array, new_level, macd_para_file, date):
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
    save_macd_para(macd_para_array[stock_k_data_array.shape[0] - new_level:stock_k_data_array.shape[0], :], macd_para_file, date)
    return 

'''
Function: 
'''
def get_macd_cross_near_zero(macd_para_file, stock_code_array, macd_filter_result_file, lower_limit, upper_limit):
    tag1 = ';'
    tag2 = ','
    if os.path.exists(macd_filter_result_file):
        print("Removing old filter macd result file: " + macd_filter_result_file)
        os.remove(macd_filter_result_file)
    with open(macd_para_file, 'r') as f1: 
        row_index = 0
        for line in f1:
            '''
            if row_index == 0:
                row_index += 1
                continue
            '''
            macd_para_list = line.split(tag1)
            #pop the first element in list, because it is date
            macd_para_list.pop(0)
            #pop the last element in list, because it is null
            macd_para_list.pop(len(macd_para_list)-1)
            macd_para_array = np.zeros([len(macd_para_list), 3])
            para_index = 0
            for para in macd_para_list:
                separate_para = para.split(tag2)
                EMA_12 = float(separate_para[0])
                EMA_26 = float(separate_para[1])
                DIFF = EMA_12 - EMA_26
                DEA = float(separate_para[2])
                MACD = (DIFF - DEA) * 2
                macd_para_array[para_index, 0] = round(DIFF, 2)
                macd_para_array[para_index, 1] = round(DEA, 2)
                macd_para_array[para_index, 2] = round(MACD, 2)
                para_index += 1
            
            with open(macd_filter_result_file, 'a') as f2:
                for i in range(macd_para_array.shape[0]):
                    if i == 0 or i == 1:
                        continue
                    elif macd_para_array[i, 2] >= lower_limit and macd_para_array[i, 2] <= upper_limit\
                        and macd_para_array[i, 0] >= lower_limit and macd_para_array[i, 0] <= upper_limit\
                        and macd_para_array[i, 1] >= lower_limit and macd_para_array[i, 1] <= upper_limit\
                        and macd_para_array[i - 2, 0] < macd_para_array[i - 2, 1]\
                        and macd_para_array[i - 1, 0] < macd_para_array[i - 1, 1]:
                        # occur just now
                        if i >= 99:
                            print("Occur: " + stock_code_array[row_index] + " position: " + str(i))
                            f2.write(stock_code_array[row_index] + "\n")
                            f2.write(str(i) + "\n")
                            f2.write("\n")
            row_index += 1
    return

'''
Function:
'''
def update_macd_para(macd_para_file, date, stock_basic_data, time_level):
    tag = ';'
    tmp_txt = 'tmp.txt'
    with open(macd_para_file, 'r') as f1:
        with open(tmp_txt, 'a') as f2:
            row_index = 0
            for line in f1:
                '''
                if row_index == 0:
                    f2.write(date)
                    f2.write("\n")
                    row_index += 1
                    continue
                '''
                macd_para_list = line.split(tag)
                last_date = macd_para_list[0]
                close_price_array = get_newest_close_price(stock_basic_data[row_index], time_level, last_date)
                #pop the first element in list, because it is date
                macd_para_list.pop(0) 
                #pop the last element in list, because it is null
                macd_para_list.pop()
                if close_price_array.shape[0] >= 90:
                    print("Data is too old, please run in init mode first.")
                    os.remove(tmp_txt)
                    return
                for i in range(close_price_array.shape[0]):
                    newest_macd_para = calc_macd_para(macd_para_list[-1], close_price_array[i])
                    macd_para_list.pop(0)
                    macd_para_list.append(newest_macd_para)
                if close_price_array.shape[0] >= 1:
                    f2.write(date + tag)
                else:
                    f2.write(last_date + tag)
                for para in macd_para_list:
                    f2.write(para + tag)
                f2.write("\n")
                row_index += 1
                if row_index%100 == 0:
                    print("Update macd para " + str(row_index) + " complete")
    os.remove(macd_para_file)
    os.rename(tmp_txt, macd_para_file)
    return

'''
Function:
'''
def get_newest_close_price(stock_code, time_level, date):
    stock_k_data_array = np.array(ts.get_k_data(stock_code, ktype=time_level, start=date))
    if stock_k_data_array.shape[0] == 0:
        return np.zeros([0, 0])
    return stock_k_data_array[:, 2]

'''
Function:
'''
def calc_macd_para(last_macd_para, last_close_price):
    tag = ','
    separate_para = last_macd_para.split(tag) 
    EMA_12 = separate_para[0]
    EMA_26 = separate_para[1]
    DEA = separate_para[2]
    EMA_12 = float(EMA_12) * 11 / 13 + last_close_price * 2 / 13
    EMA_26 = float(EMA_26) * 25 / 27 + last_close_price * 2 / 27
    DIFF = EMA_12 - EMA_26
    DEA = float(DEA )* 8 / 10 + DIFF * 2 / 10
    return repr(EMA_12) + ',' + repr(EMA_26) + ',' + repr(DEA)

'''
Function: 
'''
def get_macd_golden_crossing(stock_basic_data_file, macd_filter_result_file, time_level, new_level, macd_para_file, mode, lower_limit=0.00, upper_limit=0.10):
    #stock_basic_data = genfromtxt(stock_basic_data_file, delimiter=",")
    stock_basic_data = get_basic_data(stock_basic_data_file) 
    
    if "init" == mode:
        # Update macd_para file from the time to market 
        if os.path.exists(macd_para_file):
            print("Removing old macd para file: " + macd_para_file)
            os.remove(macd_para_file)
        date = time.strftime("%Y-%m-%d", time.localtime())
        for i in range(len(stock_basic_data['code'])):
            stock_code = stock_basic_data['code'][i]
            stock_time_to_market = stock_basic_data['timeToMarket'][i]
            stock_k_data_array = np.array(ts.get_k_data(stock_code, ktype=time_level, start=stock_time_to_market))
            init_macd_para(stock_k_data_array, new_level, macd_para_file, date)
            if i%100 == 0:
                print("Init macd para " + str(i) + " complete")
    elif "routine" == mode:
        date = time.strftime("%Y-%m-%d", time.localtime())
        update_macd_para(macd_para_file, date, stock_basic_data['code'], time_level)
    else:
        print("Not valid mode, please check !")
        return
    
    get_macd_cross_near_zero(macd_para_file, stock_basic_data['code'], macd_filter_result_file, lower_limit, upper_limit)
    return 

        


