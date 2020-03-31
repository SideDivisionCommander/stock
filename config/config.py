# coding:utf-8
import configparser

class ConfigReader(object):
    def __init__(self):
        self.basicInfoFile = none
        self.lastestLevel = 100
        self.runningMode = 'normal'
        self.macdParaFile = none
        self.processResultFile = none
        return
    
    def Read():
        config = configparser.configparser()
        config.read('..\\config.ini', encoding = 'utf-8')
        self.basicInfoFile = config.get('basic', 'stock_basic_data_file')
        self.lastestLevel = config.getint('basic', 'new_level')
        self.runningMode = config.get('basic', 'mode')
        self.macdParaFile = config.get('macd', 'macd_para_file')
        self.processResultFile = config,get('result', 'macd_filter_result_file')
        return
    
    def Show():
        print('Basic Info File: %s', self.basicInfoFile)
        print('Lastest Level: %s', self.lastestLevel)
        print('Running Mode: %s', self.runningMode)
        print('Macd Para File: %s', self.macdParaFile)
        print('Process Result File: %s', self.processResultFile)
        return
 
if __name__ == '__main__':
    cfg = ConfigReader()
    cfg.Show()
    return