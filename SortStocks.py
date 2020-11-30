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

#currentDate = datetime.date.today()
#print(currentDate)
#eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
#alertsDirectory = '/Python Workspace/BuyPops/Alerts'
#
##stockData = pd.read_csv(eodDirectory + '3MINDIA.csv',usecols=[ 'Date','Open','High','Low','Close','Adj Close','Volume','EMA_5','EMA_13','EMA_20','EMA_50','EMA_75','EMA_100','EMA_200','EMA_300','EMA_365','RSI_14'])
#stockData = pd.read_csv(eodDirectory + '3MINDIA.csv')
#
#print(stockData.loc[stockData['Date'] == str(currentDate)])

def checkMasterBreakout():
    heading = ['Date', 'Stock', 'Alert','Price']
    alerts = []
    currentDate = datetime.date.today()
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsDirectory = '/Python Workspace/BuyPops/Alerts'
    with os.scandir(eodDirectory) as i:
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
                filename = eodDirectory + entry.name
                print(filename)
                try:
                    stockData = pd.read_csv(filename, sep = '\t')
    #                stockData = pd.read_csv(filename,usecols=[ 'Date','Open','High','Low','Close','Adj Close','Volume','EMA_5','EMA_13','EMA_20','EMA_50','EMA_75','EMA_100','EMA_200','EMA_300','EMA_365','RSI_14'])
#                    print(stockData)
 #                   print("close: ", stockData.iloc[-1]['Close'], "max: ", stockData['Close'].max())
                    if ((stockData.iloc[-1]['Close']) >= (stockData['Close'].max())):
                        print('Breakout')
                        print(symbol) 
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
        
        
def hammerToday():
    heading = ['Date', 'Stock', 'Alert','Price']
    alerts = []
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsDirectory = '/Python Workspace/BuyPops/Alerts'
    with os.scandir(eodDirectory) as i:
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
                filename = eodDirectory + entry.name
                print(filename)
                try:
                    stockData = pd.read_csv(filename, sep='\t')
                    Open = stockData.iloc[-1]['Open']
                    High = stockData.iloc[-1]['High']
                    Low = stockData.iloc[-1]['Low']
                    Close = stockData.iloc[-1]['Close']
                    HalfWay = (Low + (High - Low)/2)
                    print(symbol) 
#                    print(Open, High, Low, Close)
                    if (Open >= HalfWay and Close >= HalfWay):
                        print("Tail is longer")
                        if(((Open < Close) and ((High-Open) <= 1.5*(Open - Low))) or ((Close <= Open) and ((High - Close) <= 1.5*(Close - Low)))):
                            print('Hammer')
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

def LRCToday():
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
                filename = eodDirectory + entry.name
#                print(filename)
                try:
                    stockData = pd.read_csv(filename, sep='\t')
                    Open = stockData.iloc[-1]['Open']
                    High = stockData.iloc[-1]['High']
                    Low = stockData.iloc[-1]['Low']
                    Close = stockData.iloc[-1]['Close']
                    HalfWay = (Low + (High - Low)/2)
                    print(symbol) 
#                    print(Open, High, Low, Close)
                    if (abs(Open - Close) >= 0.75*(High - Low)):
                        LRCDetected = True
                        print("LRC Detected")
                        if(Open> Close):
                            print("Bearish LRC")
                            Note = "Bearish LRC"
                            if(Open == High):
                                print("Shaven Top")
                                Note = "Shaven Top"
                        elif(Close > Open):
                            print("Bullish LRC")
                            Note = "Bullish LRC"
                            if(Open == Low):
                                print("Shaven Bottom")
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

def checkDualCandles():
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
                filename = eodDirectory + entry.name
#                print(filename)
                try:
                    stockData = pd.read_csv(filename, sep='\t')
                    OpenPrev = stockData.iloc[-2]['Open']
                    HighPrev = stockData.iloc[-2]['High']
                    LowPrev = stockData.iloc[-2]['Low']
                    ClosePrev = stockData.iloc[-2]['Close']
                    HalfWayPrev = (LowPrev + (HighPrev - LowPrev)/2)
                    print(symbol) 
#                    print(Open, High, Low, Close)
                    if (abs(OpenPrev - ClosePrev) >= 0.75*(HighPrev - LowPrev)):
#                        LRCDetected = True
                        print("LRC Detected")
                        if(OpenPrev > ClosePrev):
                            print("Bearish LRC")
                            Open = stockData.iloc[-1]['Open']
                            High = stockData.iloc[-1]['High']
                            Low = stockData.iloc[-1]['Low']
                            Close = stockData.iloc[-1]['Close']
                            if (abs(Open - Close) >= 0.75*(High - Low)):
                                if(Close > Open):
                                    DualCandleDetected = True
                                    print("Bullish LRC")
                                    #Harami pattern
                                    if(Low >= ClosePrev and Close <= OpenPrev and High <= OpenPrev): 
                                        print("Bullish Harami")
                                        Note = "Bullish Harami"
                                    #Thrusting pattern
                                    if(Open < ClosePrev and Close <= HalfWayPrev and High <= OpenPrev): 
                                        print("Bullish Thrusting")
                                        Note = "Bullish Thrusting"
                                    #Piercing Pattern
                                    if(Open <= ClosePrev and Close > HalfWayPrev):
                                        print("Bullish Piercing")
                                        Note = "Bullish Piercing"
                                    #Semi Kick Pattern
                                    if(Open > ClosePrev and Close > OpenPrev):
                                        print("Bullish Semi Kick")
                                        Note = "Bullish Semi Kick"
                                    #Half Kick Pattern
                                    if(Open > HalfWayPrev and Close > OpenPrev):
                                        print("Bullish Half Kick")
                                        Note = "Bullish Half Kick"
                                    #Full Kick Pattern    
                                    if(Open > OpenPrev and Close > OpenPrev):
                                        print("Bullish Full Kick")
                                        Note = "Bullish Full Kick"
                                    #Engulfing pattern
                                    if(Open <= ClosePrev and Close >= OpenPrev):
                                        print("Bullish Engulfing")
                                        Note = "Bullish Engulfing"
                                    
                    if(DualCandleDetected == True):
                        DualCandleDetected = False
                        alert = [stockData.iloc[-1]['Date'], symbol, Note, stockData.iloc[-1]['Close']]
                        alerts.append(alert)
                except Exception as e:
                    print(e)
    dualCandleFormations = pd.DataFrame(alerts,columns=heading)
    print("LRC DF:")
    print(dualCandleFormations)
    with open('/Python Workspace/BuyPops/Alerts/dualCandle.csv', 'w') as newFile:
        dualCandleFormations.to_csv(newFile, index=True, sep ='\t')
        newFile.close()


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
    print("Hammer DF:")
    print(locationMap)
    with open('/Python Workspace/BuyPops/Alerts/LocationMap.csv', 'w') as newFile:
        locationMap.to_csv(newFile, index=True, sep ='\t')
        newFile.close()
    
#determineTrend()
checkLocation()    
checkMasterBreakout()
hammerToday()
checkDualCandles()
LRCToday()

