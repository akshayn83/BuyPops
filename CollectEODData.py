# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:39:08 2019

@author: Akshay
"""

import csv
#import os
from nsepy import get_history
import datetime
import time

def todayAt (hr, min=0, sec=0, micros=0):
   now = datetime.datetime.now()
   return now.replace(hour=hr, minute=min, second=sec, microsecond=micros) 

def populateData():
    timeNow = datetime.datetime.now()
    if timeNow > todayAt(12) and timeNow < todayAt(21): # NSE server accessible only in this time.
#        data = get_history(symbol="SBIN", start=datetime.date(2019,10,1), end=datetime.date(2019,11,2))
#        print(data)

        with open('/Python Workspace/BuyPops/NSEData/ind_nifty500list.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
        
            for line in csv_reader:
                print(line['Company Name'])
 #               with open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Company Name'])+'.csv', 'w') as new_file:
                try:
                    data = get_history(symbol=str(line['Symbol']), start=datetime.date(2015,1,1), end=datetime.date(2019,12,18))
                    saveFile = open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Company Name'])+'.csv','w')
                    saveFile.write(data.to_string())
                    saveFile.close()
                    print('Updating::: '+str(line['Company Name']))
                    time.sleep(5)
                except Exception as e:
                    print('Did not read'+str(line['Symbol']))
                    print(e)
##               fieldnames = ['first_name', 'last_name']        

    else:
        print("Outside NSE server access time")
    
#cwd = os.getcwd()
#print(cwd)
        
populateData()

#data = get_history(symbol="COALINDIA", start=datetime.date(2015,1,1), end=datetime.date(2019,12,18))
#print(data)
#
#        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')
#
#        csv_writer.writeheader()
#
#        for line in csv_reader:
#            del line['email']
#            csv_writer.writerow(line)