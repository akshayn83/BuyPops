# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:39:08 2019

@author: Akshay
"""

import csv
from nsepy import get_history
import datetime
import time
import settings

log = settings.LOGGER

def todayAt (hr, min=0, sec=0, micros=0):
   now = datetime.datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros) 

def populateData():
    timeNow = datetime.datetime.now()
    if timeNow > todayAt(12) and timeNow < todayAt(21): # NSE server accessible only in this time.
#        data = get_history(symbol="SBIN", start=datetime.date(2019,10,1), end=datetime.date(2019,11,2))
#        log.info(data)
        
        stockFile = settings.NSEDATAPATH + 'ind_nifty500list.csv'

        with open(stockFile, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
        
            for line in csv_reader:
                log.info(line['Company Name'])
 #               with open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Company Name'])+'.csv', 'w') as new_file:
                try:
                    data = get_history(symbol=str(line['Symbol']), start=datetime.date(2015,1,1), end=datetime.date(2019,12,18))
                    saveFile = open(settings.HISTORYDATAPATH+str(line['Company Name'])+'.csv','w')
                    saveFile.write(data.to_string())
                    saveFile.close()
                    log.info('Updating::: %s',line['Company Name'])
                    time.sleep(5)
                except Exception as e:
                    log.error('Did not read %s',line['Symbol'])
                    log.error(e)

    else:
        log.info("Outside NSE server access time")
            
populateData()

#data = get_history(symbol="COALINDIA", start=datetime.date(2015,1,1), end=datetime.date(2019,12,18))
#log.info(data)
#
#        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')
#
#        csv_writer.writeheader()
#
#        for line in csv_reader:
#            del line['email']
#            csv_writer.writerow(line)