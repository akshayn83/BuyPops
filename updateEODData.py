# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:27:25 2020

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


def getEMAvalue(N, price, lastEMA):
    
    print("Calculatig EMA ", N)
    
    k = 2/(N+1)
    ema = (price*k) + lastEMA*(1-k)
    
    return ema
    
    
    
def updateData(startDate):
    currentDate = datetime.date.today() - datetime.timedelta(days=1)
#    startDate = datetime.date(1994, 11, 7)

    print(startDate)
    print(currentDate)
    stockFile = settings.NSEDATAPATH + 'ind_nifty500list.csv'
    with open(stockFile, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            print(line['Company Name'])
            with open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Company Name'])+'.csv', 'a') as newFile:
                try:
     #              data = get_history(symbol=str(line['Symbol']), start=datetime.date(2015,1,1), end=datetime.date(2019,12,18))
                    tickerSymb = str(line['Symbol'])+'.NS'
                    print(tickerSymb)
                    data = yf.download(tickers=tickerSymb, start=str(startDate),end=str(currentDate))
                    data.round(6)
                    print(data)

                    #data.tail()

#                    saveFile = open(settings.HISTORYPATH+str(line['Company Name'])+'.csv','a')
                    #saveFile.write('\n')
                    data.to_csv(newFile, mode='a', header=False, sep = '\t')
                    #saveFile.write(data.to_string(header=False))
                    newFile.close()
                    print('Updating::: '+str(line['Company Name']))
                    #time.sleep(1)
                except Exception as e:
                    print('Did not read'+str(line['Symbol']))
                    with open('/Python Workspace/BuyPops/Logs/BuyPopsExp.log', 'a') as exceptFile:
#                        log = "EXCEPTION:"+ str(datetime.datetime.now())+ " Data not read for : " + str(line['Symbol'] + " " + e  + "\n"
                        log = "EXCEPTION: "+ str(datetime.datetime.now())+ " Data not read for : "+ str(line['Symbol']) + " " +str(e)  + "\n"
                        exceptFile.write(log)
                        exceptFile.close()                           

                    print(e)
    