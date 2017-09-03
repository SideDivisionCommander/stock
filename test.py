
import tushare as ts
import numpy as np
import pandas as pd
import datetime
import os
from pandas import Series, DataFrame
'''
df means dataframe, this is a type of variable in pandas
get_stock_basics() returns
code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,
总股本(万) totalAssets,总资产(万)liquidAssets,流动资产 fixedAssets,固定资产 reserved,
公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
undp,未分利润 perundp, 每股未分配 rev,收入同比(%) profit,利润同比(%) gpr,毛利率(%) npr,净利润率(%) 
holders,股东人数
'''

# df = ts.get_stock_basics()
# print (df)
'''
in pandas, ix is a choices for indexing
and ix supports mixed integer and label based access
'''
# date = df.ix['600848']['timeToMarket']
# print (date)
# info = df.ix['600848']
# print (info)
# print (df.index.values[0])

'''
BM账面市值比=市净率的倒数
'''

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

def get_macd_cross_near_zero(macd_array, stock_code):
    f = open('macd_near_zero.txt','a')
    for i in range(macd_array.shape[0]):
        if i == 0 or i == 1:
            continue
        elif macd_array[i, 2] >= 0.00 and macd_array[i, 2] <= 0.10\
             and abs(macd_array[i, 0]) <= 0.05\
             and abs(macd_array[i, 1]) <= 0.05\
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

# get from server

#df = ts.get_stock_basics()
#df.to_csv('stockbasic.csv')

df = pd.read_csv('stockbasic.csv')
all_stock_num = df.shape[0]
stock_array = np.zeros([all_stock_num, 2])
stock_array[:, 0] = df['code']
stock_array[:, 1] = df['timeToMarket']

#print (stock_array)

for i in range(all_stock_num):
    '''
    if(i == 300):
        break
    '''
    stock_code = str(int(stock_array[i, 0]))
    stock_time_to_market = str(int(stock_array[i, 1]))
    # avoid unmeaningful time
    if len(stock_time_to_market) != 8:
        continue
    sto_time_format = stock_time_to_market[:4] + '-' + stock_time_to_market[4:6] + '-' + stock_time_to_market[6:]
    print(sto_time_format)
    sto = ts.get_k_data(stock_code, start=sto_time_format)
    sto_data_array = np.array(sto)
    # To avoid new stock or secondary new stock
    if(sto_data_array.shape[0] < 100):
        continue
    macd_array = get_macd(sto_data_array)
    get_macd_cross_near_zero(macd_array, stock_code)

    
#date = df.ix['002605']['timeToMarket']

# it seems that api:get_k_data() only returns 232 rows equally 58 days 60 ktype data.

#INFO = ts.get_k_data('002605', start='2011-08-05')  # 2011-08-05 is the timeToMarket of 002605
#DATA_ARRAY = np.array(INFO)
print("################################################################")

#get_macd(DATA_ARRAY)
