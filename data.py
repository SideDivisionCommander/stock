__author__ = 'SideDivisionCommander'

import os
import tushare as ts
import pandas as pd
import numpy as np
import scipy as sc
from pandas import Series, DataFrame

'''
Function: To fill the missing number "0" in stock code if necessary
'''
def format_stock_code(code):
    formatted_code = str(int(code))
    if len(formatted_code) < 6:
        prefix = ''
        for j in range(6 - len(formatted_code)):
            prefix = prefix + '0'
        formatted_code = prefix + formatted_code
    return formatted_code

'''
Function: To adjust time format into "YYYY-mm-dd"
'''
def format_stock_time_to_market(time):
    formatted_time_to_market = str(int(time))
    if len(formatted_time_to_market) != 8:
        return 'invalid'
    formatted_time_to_market = formatted_time_to_market[:4] + '-' + formatted_time_to_market[4:6] + '-' + formatted_time_to_market[6:]
    return formatted_time_to_market

'''
Function: 
'''
def save_info_into_file(filtered_stock_dict, stock_basic_data_file):
    if os.path.exists(stock_basic_data_file):
        print("Removing old stock basic data file: " + stock_basic_data_file)
        os.remove(stock_basic_data_file)
    with open(stock_basic_data_file, 'a') as f:
        for i in range(len(filtered_stock_dict['code'])):
            f.write(filtered_stock_dict['code'][i])
            f.write(',')
            f.write(filtered_stock_dict['timeToMarket'][i])
            f.write('\n')
    return

'''
Function: 
'''
def filter_stock_basic_data(stock_basic_data, new_level, stock_basic_data_file):
    stock_array = np.zeros([stock_basic_data.shape[0], 2])
    stock_array[:, 0] = stock_basic_data['code']
    stock_array[:, 1] = stock_basic_data['timeToMarket']
    filtered_stock_dict = {}
    filtered_stock_dict['code'] = []
    filtered_stock_dict['timeToMarket'] = []
    #unnecessary_line_index_list = []
    for i in range(stock_basic_data.shape[0]):
        stock_code = format_stock_code(stock_array[i, 0])
        stock_time_to_market = format_stock_time_to_market(stock_array[i, 1])
        # To avoid stock with unmeaningful time
        if 'invalid' == stock_time_to_market:
            #unnecessary_line_index_list.append(i)
            continue
        stock_k_data_array = np.array(ts.get_k_data(stock_code, start=stock_time_to_market))
        # To avoid new stock or secondary new stock
        if(stock_k_data_array.shape[0] < new_level):
            #unnecessary_line_index_list.append(i)
            continue
        #filtered_stock_array[i, 0] = stock_code
        #filtered_stock_array[i, 1] = stock_array[i, 1]
        filtered_stock_dict['code'].append(stock_code)
        filtered_stock_dict['timeToMarket'].append(stock_time_to_market)
        if i%100 == 0:
            print("Update stock basic date " + str(i) + " complete")
    '''
    t = 0
    print(len(unnecessary_line_index_list))
    for index in unnecessary_line_index_list:
        sc.delete(filtered_stock_array, index-t, 0)
        t += 1
    '''
    return filtered_stock_dict

'''
Function: 
'''
def update_basic_stock_data(stock_basic_data_file, new_level):    
    print("Getting the data from server ...")
    df = ts.get_stock_basics()
    df.to_csv('ddd.csv')
    df = pd.read_csv('ddd.csv', encoding='utf-8')
    print("Updating stock basic data ...")
    filtered_stock_dict = filter_stock_basic_data(df, new_level, stock_basic_data_file)
    print("Save processed stock data into file: " + stock_basic_data_file)
    save_info_into_file(filtered_stock_dict, stock_basic_data_file)
    os.remove('ddd.csv')
    print("Update stock basic data success !")
    return
