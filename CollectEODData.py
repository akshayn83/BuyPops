# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:39:08 2019

@author: Akshay
"""

import csv
# import os
#from nsepy import get_history
import datetime
import time
import settings
# import webbrowser
import requests
import yfinance as yf
import talib as ta

############################################################################
# getHistoryData(): 
# Get historical OHLC data from yahoo finance. and add indicators to the same.
# Improvement: Current all data needs to be downloaded every day
# Find way to only update and append missing data.
#############################################################################
def getHistoryData():

    stockFile = settings.NSEDATAPATH + 'ind_nifty500list.csv'
    with open(stockFile, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            with open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Symbol'])+'.csv', 'w') as newFile:
                try:
                    tickerSymb = str(line['Symbol'])+'.NS'
                    data = yf.download(tickers=tickerSymb, period="max", interval="1d")
                    #saveFile = open(settings.HISTORYPATH+str(line['Company Name'])+'.csv','w')
                    #data.reset_index(inplace=True)
                    
#                    data['EMA_5'] = ta.EMA(data['Close'], 5)
#                    data['EMA_13'] = ta.EMA(data['Close'], 13)
#                    data['EMA_20'] = ta.EMA(data['Close'], 20)
#                    data['EMA_50'] = ta.EMA(data['Close'], 50)
#                    data['EMA_75'] = ta.EMA(data['Close'], 75)
#                    data['EMA_100'] = ta.EMA(data['Close'], 100)
#                    data['EMA_200'] = ta.EMA(data['Close'], 200)
#                    data['EMA_300'] = ta.EMA(data['Close'], 300)
#                    data['EMA_365'] = ta.EMA(data['Close'], 365)
#                    data['RSI_14'] = ta.RSI(data['Close'],14)

#                    newFile.write(data.to_string())
#                    newFile.write('\n')
                    data.to_csv(newFile, index=True, sep ='\t')
                    newFile.close()
                    print('Updating::: '+str(line['Company Name']))
                    #time.sleep(5)
                except Exception as e:
                    print('Did not read'+str(line['Symbol']))
                    with open('/Python Workspace/BuyPops/Logs/BuyPopsExp.log', 'a') as exceptFile:
#                        log = "EXCEPTION:"+ str(datetime.datetime.now())+ " Data not read for : " + str(line['Symbol'] + " " + e  + "\n"
                        log = "EXCEPTION: "+ str(datetime.datetime.now())+ " Data not read for : "+ str(line['Symbol']) + " " +str(e)  + "\n"
                        exceptFile.write(log)
                        exceptFile.close()                           
                    print(e)

    #    print(data)

def todayAt(hr, min=0, sec=0, micros=0):
    now = datetime.datetime.now()
    return now.replace(hour=hr, minute=min, second=sec, microsecond=micros)



#def populateData(startDate):
#    currentDate = datetime.date.today() - datetime.timedelta(days=1)
##    startDate = datetime.date(1994, 11, 7)
#
#    print(startDate)
#    print(currentDate)
#    stockFile = settings.NSEDATAPATH + 'ind_nifty500list.csv'
#    with open(stockFile, 'r') as csv_file:
#        csv_reader = csv.DictReader(csv_file)
#
#        for line in csv_reader:
#            print(line['Company Name'])
#            with open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Company Name'])+'.csv', 'a') as new_file:
#                try:
#     #              data = get_history(symbol=str(line['Symbol']), start=datetime.date(2015,1,1), end=datetime.date(2019,12,18))
#                    tickerSymb = str(line['Symbol'])+'.NS'
#                    print(tickerSymb)
#                    data = yf.download(tickers=tickerSymb, start=str(startDate),end=str(currentDate))
#                    data.round(6)
#                    print(data)
#
#                    #data.tail()
#
#                    saveFile = open(settings.HISTORYPATH+str(line['Company Name'])+'.csv','a')
#                    #saveFile.write('\n')
#                    data.to_csv(settings.HISTORYPATH+str(line['Company Name'])+'.csv', mode='a', header=False, sep = '\t')
#                    #saveFile.write(data.to_string(header=False))
#                    saveFile.close()
#                    print('Updating::: '+str(line['Company Name']))
#                    #time.sleep(1)
#                except Exception as e:
#                    print('Did not read '+str(line['Symbol']))
#                    print(e)



################ Commenting out NSE code ####################################
#    currentDate = datetime.date.today()
#    oneDay = datetime.timedelta(days=1)
#    while currentDate >= startDate:

#        currentDate -= oneDay
#        weekno = currentDate.weekday()

#        if weekno < 5:
#            print("Weekday:" + str(weekno))
#            file_url = "https://archives.nseindia.com/products/content/sec_bhavdata_full_" + str(currentDate.day).zfill(
#                2) + str(currentDate.month).zfill(2) + str(currentDate.year) + ".csv"

#            try:
#                #                print(file_url)
#                r = requests.get(file_url, stream=True)
#                writeFile = "/Python Workspace/BuyPops/NSEData/HistoryDataEOD/bhavcopy_" + str(
#                    currentDate.year) + "_" + str(currentDate.month).zfill(2) + "_" + str(currentDate.day).zfill(
#                    2) + ".csv"
#                with open(writeFile, "wb") as csvfile:
#                     for chunk in r.iter_content(chunk_size=1024):
#
#                         # writing one chunk at a time to pdf file
#                         if chunk:
#                             csvfile.write(chunk)
#                         #                print(writeFile)
#             except Exception as e:
#                 print("Error")
#                 print(e)
#         else:
#             print("Weekend:" + str(weekno))

### Bhavcopy browser Link sample ###
#    webbrowser.open("https://archives.nseindia.com/products/content/sec_bhavdata_full_20012020.csv")
############################################################################################################


###### Code for Reading Alerts File : TBD ####################
def readAlertDefs():
    alertConfigFile = 'AlertConfig.csv'

    with open(alertConfigFile, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            print(line['Scrip Symbol'])
########################################################
            
            
def updateEODData():
    stockFile = settings.NSEDATAPATH + 'ind_nifty500list.csv'
    with open(stockFile, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            with open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Symbol'])+'.csv', 'a') as newFile:
                try:
                    tickerSymb = str(line['Symbol'])+'.NS'
                    data = yf.download(tickers=tickerSymb, period="1d", interval="1d")
                    #saveFile = open(settings.HISTORYPATH+str(line['Company Name'])+'.csv','w')
                    #data.reset_index(inplace=True)
                    
#                    data['EMA_5'] = ta.EMA(data['Close'], 5)
#                    data['EMA_13'] = ta.EMA(data['Close'], 13)
#                    data['EMA_20'] = ta.EMA(data['Close'], 20)
#                    data['EMA_50'] = ta.EMA(data['Close'], 50)
#                    data['EMA_75'] = ta.EMA(data['Close'], 75)
#                    data['EMA_100'] = ta.EMA(data['Close'], 100)
#                    data['EMA_200'] = ta.EMA(data['Close'], 200)
#                    data['EMA_300'] = ta.EMA(data['Close'], 300)
#                    data['EMA_365'] = ta.EMA(data['Close'], 365)
#                    data['RSI_14'] = ta.RSI(data['Close'],14)

#                    newFile.write(data.to_string())
#                    newFile.write('\n')
                    data.to_csv(newFile, mode = 'a', header = False, index=True, sep ='\t')
                    newFile.close()
                    print('Updating::: '+str(line['Company Name']))
                    #time.sleep(5)
                except Exception as e:
                    print('Did not read'+str(line['Symbol']))
                    with open('/Python Workspace/BuyPops/Logs/BuyPopsExp.log', 'a') as exceptFile:
#                        log = "EXCEPTION:"+ str(datetime.datetime.now())+ " Data not read for : " + str(line['Symbol'] + " " + e  + "\n"
                        log = "EXCEPTION: "+ str(datetime.datetime.now())+ " Data not read for : "+ str(line['Symbol']) + " " +str(e)  + "\n"
                        exceptFile.write(log)
                        exceptFile.close()                           
                    print(e)
#readAlertDefs()
#populateData(datetime.date.today() - datetime.timedelta(days=2))
getHistoryData()


