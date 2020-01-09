#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 16:54:41 2019
Settings file
@author: neha
"""
import configparser
import logging
import logging.config


config = configparser.ConfigParser()
config.read('settings.ini')
NSEDATAPATH = config.get('Settings','NSEDATAPATH')
HISTORYPATH = config.get('Settings','HISTORYPATH')

logging.config.fileConfig(config.get('Settings','LOGCONFIG'))

LOGGER = logging.getLogger('appLogger')
LOGGER.info('Setting Completed')




