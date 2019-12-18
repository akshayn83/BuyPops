# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 21:39:08 2019

@author: Akshay
"""

import csv
#import os
#from nsepy import get_history
#from datetime import date

#data = get_history(symbol="SBIN", start=date(2019,10,1), end=date(2019,11,2))
#print(data)
#cwd = os.getcwd()
#print(cwd)
with open('/Python Workspace/BuyPops/NSEData/ind_nifty500list.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for line in csv_reader:
#        print(line['Company Name'])
        with open('/Python Workspace/BuyPops/NSEData/HistoryDataEOD/'+str(line['Company Name'])+'.csv', 'w') as new_file:
            fieldnames = ['first_name', 'last_name']
#
#        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')
#
#        csv_writer.writeheader()
#
#        for line in csv_reader:
#            del line['email']
#            csv_writer.writerow(line)