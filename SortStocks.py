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
from CollectEODData import updateEODData

##################################################################################
# checkTopThird(stockData):
# to check where the stock price is currently with respect to the entire price range. 
# returns True if stock is in top 1/3rd of their range
##################################################################################
def checkTopThird(stockData):
    Close = stockData.iloc[-1]['Close']
    priceMax = max(stockData['Close'])
    priceMin =  min(stockData['Close'])
    priceRange =  priceMax - priceMin
    topThird = priceMax - (priceRange/3)
    if(Close >=  topThird):
        return True
    else:
        return False
    
##################################################################################
# checkMasterBreakout(stockData):
# to check if the stock has made an all time high(close) from the given list
# returns True if stock is at all time high
##################################################################################
def checkMasterBreakout(stockData):
    if (((stockData.iloc[-1]['Close']) >= (stockData['Close'].max()) ) and 
        ((stockData.iloc[-2]['Close']) < (stockData[:-1]['Close'].max()))):
        return True
    else:
        return False

##################################################################################
# checkCandleType(stockData):
# Check the type of candlestic on the last daty
# Retursn a string as a type of detected candle
##################################################################################
def checkCandleType(stockData):
    candleType = ''
    Open = stockData.iloc[-1]['Open']
    High = stockData.iloc[-1]['High']
    Low = stockData.iloc[-1]['Low']
    Close = stockData.iloc[-1]['Close']
    HalfWay = (Low + (High - Low)/2)
#   print(Open, High, Low, Close)
    if (Open >= HalfWay and Close >= HalfWay):
        if(((Open < Close) and ((High-Open) <= 1.5*(Open - Low))) or ((Close <= Open) and ((High - Close) <= 1.5*(Close - Low)))):
            candleType = 'Hammer'
    elif(abs(Open - Close) >= 0.675*(High - Low)):
        if(Close > Open):
            candleType = "Bullish LRC"
            if(Open == Low):
                candleType = "Shaven Bottom"

    return candleType

##################################################################################
# checkCandlePattern(stockData):
# Check the cadlestick pattern made with multiple candles of latest period
# Retursn a string as a type of detected pottern
##################################################################################
def checkCandlePattern(stockData):
    candlePattern = ''
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
                    #Harami pattern
                    if(Low >= ClosePrev and Close <= OpenPrev and High <= OpenPrev): 
                       candlePattern = "Bullish Harami"
                    #Thrusting pattern
                    if(Open < ClosePrev and Close <= HalfWayPrev and High <= OpenPrev): 
                        candlePattern = "Bullish Thrusting"
                    #Piercing Pattern
                    if(Open <= ClosePrev and Close > HalfWayPrev):
                        candlePattern = "Bullish Piercing"
                    #Semi Kick Pattern
                    if(Open > ClosePrev and Close > OpenPrev):
                        candlePattern = "Bullish Semi Kick"
                    #Half Kick Pattern
                    if(Open > HalfWayPrev and Close > OpenPrev):
                        candlePattern = "Bullish Half Kick"
                    #Full Kick Pattern    
                    if(Open > OpenPrev and Close > OpenPrev):
                        candlePattern = "Bullish Full Kick"
                    #Engulfing pattern
                    if(Open <= ClosePrev and Close >= OpenPrev):
                        candlePattern = "Bullish Engulfing"
    return candlePattern

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
    
##################################################################################
# checkAlerts():
# Check All possible alerts from nifty 500 which are usable to trigger a buy signal
# Function firsts separates all stocks which are in the top third of their entire 
# price range and then check for latest candles for patterns and bullish signals 
# Generates an alerts file which has all alerts listed agaist the stock name
##################################################################################    
def checkAlerts():
    heading = ['Date', 'Stock', 'CandleType','Pattern', 'Master Breakout','Price','AlertPoints']
    alerts = []
    eodDirectory = '/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'
    alertsFile = '/Python Workspace/BuyPops/Alerts/Alerts.csv'
    count = 0
    with os.scandir(eodDirectory) as i:
        
        for entry in i:
            if entry.is_file():
                symbol = entry.name.split('.')[0]
                filename = eodDirectory + entry.name #                print(filename)
                try:
                    stockData = pd.read_csv(filename, sep='\t')
                    if(checkTopThird(stockData) == True):
                        alertPoints = 0
                        candleType = checkCandleType(stockData)
                        if(candleType != ''):
                            alertPoints += 1
                        candlePatttern = checkCandlePattern(stockData)
                        if(candlePatttern != ''):
                            count += 1
                            alertPoints += 1    
                        if(checkMasterBreakout(stockData) == True):
                            masterBreakout = 'Y'
                            alertPoints += 1
                        else:
                            masterBreakout = 'N'
                    if(alertPoints > 0):
                        alert = [stockData.iloc[-1]['Date'], symbol, candleType, candlePatttern, 
                                 masterBreakout, stockData.iloc[-1]['Close'], alertPoints]
                        alerts.append(alert)
                       
                except Exception as e:
                    print(e)
    generatedAlerts = pd.DataFrame(alerts,columns=heading)
    print(generatedAlerts)
    if os.path.isfile(alertsFile):
        with open(alertsFile, 'a') as newFile:
            generatedAlerts.to_csv(newFile, header = False, index=False, sep ='\t')
            newFile.close()
    else:
        with open(alertsFile, 'w') as newFile:
            generatedAlerts.to_csv(newFile, index=False, sep ='\t')
            newFile.close()

updateEODData()

checkAlerts()
