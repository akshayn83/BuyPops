# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:11:51 2020

@author: Akshay
"""
import csv
import os
#from nsepy import get_history
import datetime
#import time
#import settings
import pandas as pd
import trendet
import investpy
##################################################################################
# checkLocation():
# to check where the stock price is currently with respect to the entire price range. 
# currently returns only stocks which are in top 1/3rd of their range
#
##################################################################################
def checkLocation():
    heading = ['Date', 'Stock', 'Alert','Price']
    alerts = []
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsDirectory = '/Python Workspace/BuyPops/Alerts'
    with os.scandir(eodDirectory) as i:
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
                filename = eodDirectory + entry.name
                try:
                    stockData = pd.read_csv(filename, sep='\t')
                    Close = stockData.iloc[-1]['Close']
                    priceMax = max(stockData['Close'])
                    priceMin =  min(stockData['Close'])
                    priceRange =  priceMax - priceMin
                    topThird = priceMax - (priceRange/3)
                    if(Close >=  topThird):
                        alert = [stockData.iloc[-1]['Date'], symbol, 'Top Third', stockData.iloc[-1]['Close']]
                        alerts.append(alert)
                except Exception as e:
                    print(e)
    locationMap = pd.DataFrame(alerts,columns=heading)
    print("Location DF:")
    print(locationMap)
    with open('/Python Workspace/BuyPops/Alerts/LocationMap.csv', 'w') as newFile:
        locationMap.to_csv(newFile, index=True, sep ='\t')
        newFile.close()
    return locationMap
    
##################################################################################
# checkMasterBreakout(sortedList):
# to check if the stock has made an all time high from the given list
# generates an output file with stocks that have mede an all time high
#
##################################################################################
def checkMasterBreakout(sortedList):
    heading = ['Date', 'Stock', 'Alert','Price']
    alerts = []
    currentDate = datetime.date.today()
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsDirectory = '/Python Workspace/BuyPops/Alerts'
    with os.scandir(eodDirectory) as i:
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
                for i in range(0,len(sortedList)): # this is a workaround since 'in was not working for unknown reasons         
                    if(symbol == sortedList[i]):
                        filename = eodDirectory + entry.name
                        try:
                            stockData = pd.read_csv(filename, sep = '\t')
            #                stockData = pd.read_csv(filename,usecols=[ 'Date','Open','High','Low','Close','Adj Close','Volume','EMA_5','EMA_13','EMA_20','EMA_50','EMA_75','EMA_100','EMA_200','EMA_300','EMA_365','RSI_14'])
                            #print(stockData)
                        
         #                   print("close: ", stockData.iloc[-1]['Close'], "max: ", stockData['Close'].max())
                            if (((stockData.iloc[-1]['Close']) >= (stockData['Close'].max()) ) and 
                                ((stockData.iloc[-2]['Close']) < (stockData[:-1]['Close'].max()))):
                                alert = [stockData.iloc[-1]['Date'], symbol, 'Master Breakout', stockData.iloc[-1]['Close']]
                                alerts.append(alert)
                        except Exception as e:
                            print(e)
    masterBreakouts = pd.DataFrame(alerts,columns=heading)
    print("Breakout DF:")
    print(masterBreakouts)
    with open('/Python Workspace/BuyPops/Alerts/MasterBreakout.csv', 'w') as newFile:
        masterBreakouts.to_csv(newFile, index=True, sep ='\t')
        newFile.close()
        
##################################################################################
# checkMasterBreakout(sortedList):
# to check if the stock has made a hammer formation fromk the given list
# generates an output file with stocks that have mede a hammer
#
##################################################################################    
def hammerToday(sortedList):
    heading = ['Date', 'Stock', 'Alert','Price']
    alerts = []
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsDirectory = '/Python Workspace/BuyPops/Alerts'
#    print(sortedList)
    with os.scandir(eodDirectory) as i:
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
#                print(symbol)
#                print(type(symbol))
                for i in range(0,len(sortedList)): # this is a workaround since 'in was not working for unknown reasons         
                    if(symbol == sortedList[i]):
                        filename = eodDirectory + entry.name
    #                    print(filename)
                        try:
                            stockData = pd.read_csv(filename, sep='\t')
                            Open = stockData.iloc[-1]['Open']
                            High = stockData.iloc[-1]['High']
                            Low = stockData.iloc[-1]['Low']
                            Close = stockData.iloc[-1]['Close']
                            HalfWay = (Low + (High - Low)/2)
        #                    print(Open, High, Low, Close)
                            if (Open >= HalfWay and Close >= HalfWay):
                                if(((Open < Close) and ((High-Open) <= 1.5*(Open - Low))) or ((Close <= Open) and ((High - Close) <= 1.5*(Close - Low)))):
                                    alert = [stockData.iloc[-1]['Date'], symbol, 'Hammer', stockData.iloc[-1]['Close']]
                                    alerts.append(alert)
                        except Exception as e:
                            print(e)
    hammerFormations = pd.DataFrame(alerts,columns=heading)
    print("Hammer DF:")
    print(hammerFormations)
    with open('/Python Workspace/BuyPops/Alerts/HammerToday.csv', 'w') as newFile:
        hammerFormations.to_csv(newFile, index=True, sep ='\t')
        newFile.close()

def LRCToday(sortedList):
    heading = ['Date', 'Stock', 'Alert','Price']
    alerts = []
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsDirectory = '/Python Workspace/BuyPops/Alerts'
    Note = ""
    LRCDetected = False
    with os.scandir(eodDirectory) as i:
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
                for i in range(0,len(sortedList)): # this is a workaround since 'in was not working for unknown reasons         
                    if(symbol == sortedList[i]):
                        filename = eodDirectory + entry.name
        #                print(filename)
                        try:
                            stockData = pd.read_csv(filename, sep='\t')
                            Open = stockData.iloc[-1]['Open']
                            High = stockData.iloc[-1]['High']
                            Low = stockData.iloc[-1]['Low']
                            Close = stockData.iloc[-1]['Close']
                            HalfWay = (Low + (High - Low)/2)
        #                    print(Open, High, Low, Close)
                            if (abs(Open - Close) >= 0.675*(High - Low)):
                                if(Open> Close):
                                    Note = "Bearish LRC"
                                    if(Open == High):
                                        Note = "Shaven Top"
                                elif(Close > Open):
                                    LRCDetected = True
                                    Note = "Bullish LRC"
                                    if(Open == Low):
                                        Note = "Shaven Bottom"
                            if(LRCDetected == True):
                                LRCDetected = False
                                alert = [stockData.iloc[-1]['Date'], symbol, Note, stockData.iloc[-1]['Close']]
                                alerts.append(alert)
                        except Exception as e:
                            print(e)
    longRangeCandleFormations = pd.DataFrame(alerts,columns=heading)
    print("LRC DF:")
    print(longRangeCandleFormations)
    with open('/Python Workspace/BuyPops/Alerts/LRCToday.csv', 'w') as newFile:
        longRangeCandleFormations.to_csv(newFile, index=True, sep ='\t')
        newFile.close()

##################################################################################
# checkDualCandles(sortedList):
# to check if the stock has made a bullish dual candle formation fromk the given list
# generates an output file with stocks that have mede a bullish dual candle
#
##################################################################################
def checkDualCandles(sortedList):
    heading = ['Date', 'Stock', 'Alert','Price']
    alerts = []
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsDirectory = '/Python Workspace/BuyPops/Alerts'
    Note = ""
    DualCandleDetected = False
    with os.scandir(eodDirectory) as i:
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
                for i in range(0,len(sortedList)): # this is a workaround since 'in was not working for unknown reasons         
                    if(symbol == sortedList[i]):
                        filename = eodDirectory + entry.name
        #                print(filename)
                        try:
                            stockData = pd.read_csv(filename, sep='\t')
                            OpenPrev = stockData.iloc[-2]['Open']
                            HighPrev = stockData.iloc[-2]['High']
                            LowPrev = stockData.iloc[-2]['Low']
                            ClosePrev = stockData.iloc[-2]['Close']
                            HalfWayPrev = (LowPrev + (HighPrev - LowPrev)/2) 
        #                    print(Open, High, Low, Close)
                            if (abs(OpenPrev - ClosePrev) >= 0.675*(HighPrev - LowPrev)):
        #                        LRCDetected = True
                                if(OpenPrev > ClosePrev):
                                    Open = stockData.iloc[-1]['Open']
                                    High = stockData.iloc[-1]['High']
                                    Low = stockData.iloc[-1]['Low']
                                    Close = stockData.iloc[-1]['Close']
                                    if (abs(Open - Close) >= 0.675*(High - Low)):
                                        if(Close > Open):
                                            DualCandleDetected = True
                                            #Harami pattern
                                            if(Low >= ClosePrev and Close <= OpenPrev and High <= OpenPrev): 
                                                Note = "Bullish Harami"
                                            #Thrusting pattern
                                            if(Open < ClosePrev and Close <= HalfWayPrev and High <= OpenPrev): 
                                                Note = "Bullish Thrusting"
                                            #Piercing Pattern
                                            if(Open <= ClosePrev and Close > HalfWayPrev):
                                                Note = "Bullish Piercing"
                                            #Semi Kick Pattern
                                            if(Open > ClosePrev and Close > OpenPrev):
                                                Note = "Bullish Semi Kick"
                                            #Half Kick Pattern
                                            if(Open > HalfWayPrev and Close > OpenPrev):
                                                Note = "Bullish Half Kick"
                                            #Full Kick Pattern    
                                            if(Open > OpenPrev and Close > OpenPrev):
                                                Note = "Bullish Full Kick"
                                            #Engulfing pattern
                                            if(Open <= ClosePrev and Close >= OpenPrev):
                                                Note = "Bullish Engulfing"
                                            
                            if(DualCandleDetected == True):
                                DualCandleDetected = False
                                alert = [stockData.iloc[-1]['Date'], symbol, Note, stockData.iloc[-1]['Close']]
                                alerts.append(alert)
                        except Exception as e:
                            print(e)
    dualCandleFormations = pd.DataFrame(alerts,columns=heading)
    print("Dual Candle DF:")
    print(dualCandleFormations)
    with open('/Python Workspace/BuyPops/Alerts/dualCandle.csv', 'w') as newFile:
        dualCandleFormations.to_csv(newFile, index=True, sep ='\t')
        newFile.close()


#####################################################################################
# determineTrend():
# to determin short term, medium term and long term trends of stocks in a given list
#  WIP
#
#####################################################################################
def determineTrend():
    
    df = trendet.identify_trends(stock='BBVA',
                                 country='Spain',
                                 from_date='01/01/2018',
                                 to_date='01/01/2019',
                                 window_size=5,
                                 trend_limit=3,
                                 labels=['A', 'B', 'C'])
    
    df.reset_index(inplace=True)
    print(df)
    

#determineTrend()

#def createList()
locMap = checkLocation()    

hammerToday(locMap['Stock'])
checkMasterBreakout(locMap['Stock'])
checkDualCandles(locMap['Stock'])
LRCToday(locMap['Stock'])

