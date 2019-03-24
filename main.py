__author__ = 'SideDivisionCommander'

import sys
import pandas as pd
from pandas import Series, DataFrame
from data import update_basic_stock_data
from macd import get_macd_golden_crossing

def welcome():
    print('''

   SSSSSSSSSSSSSSS      tttt                                               kkkkkkkk           
 SS:::::::::::::::S  ttt:::t                                               k::::::k           
S:::::SSSSSS::::::S  t:::::t                                               k::::::k           
S:::::S     SSSSSSS  t:::::t                                               k::::::k           
S:::::S        ttttttt:::::ttttttt       ooooooooooo       cccccccccccccccc k:::::k    kkkkkkk
S:::::S        t:::::::::::::::::t     oo:::::::::::oo   cc:::::::::::::::c k:::::k   k:::::k 
 S::::SSSS     t:::::::::::::::::t    o:::::::::::::::o c:::::::::::::::::c k:::::k  k:::::k  
  SS::::::SSSSStttttt:::::::tttttt    o:::::ooooo:::::oc:::::::cccccc:::::c k:::::k k:::::k   
    SSS::::::::SS    t:::::t          o::::o     o::::oc::::::c     ccccccc k::::::k:::::k    
       SSSSSS::::S   t:::::t          o::::o     o::::oc:::::c              k:::::::::::k     
            S:::::S  t:::::t          o::::o     o::::oc:::::c              k:::::::::::k     
            S:::::S  t:::::t    tttttto::::o     o::::oc::::::c     ccccccc k::::::k:::::k    
SSSSSSS     S:::::S  t::::::tttt:::::to:::::ooooo:::::oc:::::::cccccc:::::ck::::::k k:::::k   
S::::::SSSSSS:::::S  tt::::::::::::::to:::::::::::::::o c:::::::::::::::::ck::::::k  k:::::k  
S:::::::::::::::SS     tt:::::::::::tt oo:::::::::::oo   cc:::::::::::::::ck::::::k   k:::::k 
 SSSSSSSSSSSSSSS         ttttttttttt     ooooooooooo       cccccccccccccccckkkkkkkk    kkkkkkk

''')

def complete():
    print('''

        CCCCCCCCCCCCC                                                             lllllll                              tttt                              
     CCC::::::::::::C                                                             l:::::l                           ttt:::t                              
   CC:::::::::::::::C                                                             l:::::l                           t:::::t                              
  C:::::CCCCCCCC::::C                                                             l:::::l                           t:::::t                              
 C:::::C       CCCCCC   ooooooooooo      mmmmmmm    mmmmmmm   ppppp   ppppppppp    l::::l     eeeeeeeeeeee    ttttttt:::::ttttttt        eeeeeeeeeeee    
C:::::C               oo:::::::::::oo  mm:::::::m  m:::::::mm p::::ppp:::::::::p   l::::l   ee::::::::::::ee  t:::::::::::::::::t      ee::::::::::::ee  
C:::::C              o:::::::::::::::om::::::::::mm::::::::::mp:::::::::::::::::p  l::::l  e::::::eeeee:::::eet:::::::::::::::::t     e::::::eeeee:::::ee
C:::::C              o:::::ooooo:::::om::::::::::::::::::::::mpp::::::ppppp::::::p l::::l e::::::e     e:::::etttttt:::::::tttttt    e::::::e     e:::::e
C:::::C              o::::o     o::::om:::::mmm::::::mmm:::::m p:::::p     p:::::p l::::l e:::::::eeeee::::::e      t:::::t          e:::::::eeeee::::::e
C:::::C              o::::o     o::::om::::m   m::::m   m::::m p:::::p     p:::::p l::::l e:::::::::::::::::e       t:::::t          e:::::::::::::::::e 
C:::::C              o::::o     o::::om::::m   m::::m   m::::m p:::::p     p:::::p l::::l e::::::eeeeeeeeeee        t:::::t          e::::::eeeeeeeeeee  
 C:::::C       CCCCCCo::::o     o::::om::::m   m::::m   m::::m p:::::p    p::::::p l::::l e:::::::e                 t:::::t    tttttte:::::::e           
  C:::::CCCCCCCC::::Co:::::ooooo:::::om::::m   m::::m   m::::m p:::::ppppp:::::::pl::::::le::::::::e                t::::::tttt:::::te::::::::e          
   CC:::::::::::::::Co:::::::::::::::om::::m   m::::m   m::::m p::::::::::::::::p l::::::l e::::::::eeeeeeee        tt::::::::::::::t e::::::::eeeeeeee  
     CCC::::::::::::C oo:::::::::::oo m::::m   m::::m   m::::m p::::::::::::::pp  l::::::l  ee:::::::::::::e          tt:::::::::::tt  ee:::::::::::::e  
        CCCCCCCCCCCCC   ooooooooooo   mmmmmm   mmmmmm   mmmmmm p::::::pppppppp    llllllll    eeeeeeeeeeeeee            ttttttttttt      eeeeeeeeeeeeee  
                                                               p:::::p                                                                                   
                                                               p:::::p                                                                                   
                                                              p:::::::p                                                                                  
                                                              p:::::::p                                                                                  
                                                              p:::::::p                                                                                  
                                                              ppppppppp
                    
''')

def main():
    work_mode = 'routine'
    time_level = 'D'
    new_level_D = 100
    new_level_W = 13
    lower_limit_D = 0.00
    upper_limit_D = 0.80
    lower_limit_W = 0.00
    upper_limit_W = 5.00
    #file config
    stock_basic_data_file = 'stockbasic.csv'
    macd_filter_result_file_D = 'macd_crossing.txt'
    macd_para_file_D = 'macd_para.txt'
    macd_filter_result_file_W = 'macd_crossing_W.txt'
    macd_para_file_W = 'macd_para_W.txt'
    try:
        # python main.py work_mode time_level
        if len(sys.argv) != 3:
            print("Invalid input para num.")
            return -1
        else:
            work_mode = sys.argv[1]
            if work_mode != 'routine' or work_mode != 'init':
                print("Invalid input para 1, it must be \"routine\" or \"init\".")
                return -1
            work_mode = sys.argv[2]
            if time_level != 'D' or time_level != 'W':
                print("Invalid input para 2, it must be \"D\" or \"W\".)
                return -1
    except Exception:
        print("Parse para failed.")
        return -1
    welcome()
    
    # Get data from server
    if 'init' == work_mode:
        update_basic_stock_data(stock_basic_data_file, new_level_D)
    if 'D' == time_level:
        get_macd_golden_crossing(stock_basic_data_file, macd_filter_result_file_D, time_level, new_level_D, macd_para_file_D, work_mode, lower_limit_D, upper_limit_D)
    if 'W' == time_level:
        get_macd_golden_crossing(stock_basic_data_file, macd_filter_result_file_W, time_level, new_level_W, macd_para_file_W, work_mode, lower_limit_W, upper_limit_W)
    complete()
    return 0

if __name__ == "__main__":
    exit(main())
