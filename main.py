__author__ = 'SideDivisionCommander'

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
    welcome()
    #file config
    stock_basic_data_file = 'stockbasic.csv'
    macd_filter_result_file = 'macd_crossing.txt'
    macd_para_file = 'macd_para.txt'
    new_level = 100
    mode = "init"
    #mode = "normal"
    #Get data from server
    #if "init" == mode:
    #    update_basic_stock_data(stock_basic_data_file, new_level)
    get_macd_golden_crossing(stock_basic_data_file, macd_filter_result_file, new_level, macd_para_file, mode)
    complete()
    return

if __name__ == "__main__":
    main()