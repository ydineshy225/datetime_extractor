# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 15:47:20 2019

@author: DineshBabuYeddu
"""

import re

## Function to remove some special characters
def preprocess(x):
    x = x.replace('\t',' ')
    x = x.replace('\n',' ')
    x = x.replace('(',' ')
    x = x.replace(')',' ')
    x = x.replace('[',' ')
    x = x.replace(']',' ')
    x = x.replace('{',' ')
    x = x.replace('}',' ')
    x = x.replace(',',' ')
    x = x.replace('"','')
    x = x.replace("'",'')
    return(x)
    
## Different types of date regexes to extract below types of formats
DateTimeRegex = {'yearORmonthORday-yearORmonthORday-yearORmonthORday:hours:mins:secs':'\\b\d+\-\d+\-\d+\:\d+\:\d+\:\d+\\b',
             'yearORmonthORday/yearORmonthORday/yearORmonthORday:hours:mins:secs':'\\b\d+\/\d+\/\d+\:\d+\:\d+\:\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORday-hours.mins.secs.millisecs':'\\b\d+\-\d+\-\d+\-\d+\.\d+\.\d+\.\d+\-\d+\\b',
             'yearORmonthORday/yearORmonthORday/yearORmonthORday-hours.mins.secs.millisecs':'\\b\d+\/\d+\/\d+\-\d+\.\d+\.\d+\.\d+\-\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORday-hours.mins.secs':'\\b\d+\-\d+\-\d+\-\d+\.\d+\.\d+\\b',
             'yearORmonthORday/yearORmonthORday/yearORmonthORday-hours.mins.secs':'\\b\d+\/\d+\/\d+\-\d+\.\d+\.\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORdayThours:mins:secs.millisecs':'\\b\d+\-\d+\-\d+[A-Za-z]+\d+\:\d+\:\d+\.\w+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORdayThours:mins:secs+millisecs':'\\b\d+\-\d+\-\d+[A-Za-z]+\d+\:\d+\:\d+\+\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORdayThours:mins:secs*millisecs':'\\b\d+\-\d+\-\d+[A-Za-z]+\d+\:\d+\:\d+\*\d+\+\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORday*hours:mins:secs:millisecs':'\\b\d+\-\d+\-\d+\*\d+\:\d+\:\d+\:\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORday*hours:mins:secs':'\\b\d+\-\d+\-\d+\*\d+\:\d+\:\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORdayThours:mins:secs':'\\b\d+\-\d+\-\d+[A-Za-z]+\d+\:\d+\:\d+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORday hours:mins:secs.millisecs':'\\b\d+\-\d+\-\d+\s+\d+\:\d+\:\d+\.\w+\\b',
             'yearORmonthORday/yearORmonthORday/yearORmonthORday hours:mins:secs:millisecs':'\\b\d+\/\d+\/\d+\s+\d+\:\d+\:\d+\:\w+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORday hours:mins:secs AMorPM':'\\b\d+\-\d+\-\d+\s+\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'yearORmonthORday-yearORmonthORday-yearORmonthORday hours:mins:secs':'\\b\d+\-\d+\-\d+\s+\d+\:\d+\:\d+\\b',
             'yearORmonthORday/yearORmonthORday/yearORmonthORday hours:mins:secs AMorPM':'\\b\d+\/\d+\/\d+\s+\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'yearORmonthORday/yearORmonthORday/yearORmonthORday hours:mins:secs':'\\b\d+\/\d+\/\d+\s+\d+\:\d+\:\d+\\b',
             'yearORday/month/yearORday:hours:mins:secs AMorPM':'\\b\d+\/[A-Za-z]+\/\d+\:\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'yearORday/month/yearORday:hours:mins:secs':'\\b\d+\/[A-Za-z]+\/\d+\:\d+\:\d+\:\d+\\b',
             'yearORday-month-yearORday:hours:mins:secs AMorPM':'\\b\d+\-[A-Za-z]+\-\d+\:\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'yearORday-month-yearORday:hours:mins:secs':'\\b\d+\-[A-Za-z]+\-\d+\:\d+\:\d+\:\d+\\b',
             'month/yearORday/yearORday:hours:mins:secs AMorPM':'\\b[A-Za-z]+\/\d+\/\d+\:\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'month/yearORday/yearORday:hours:mins:secs':'\\b[A-Za-z]+\/\d+\/\d+\:\d+\:\d+\:\d+\\b',
             'month-yearORday-yearORday:hours:mins:secs AMorPM':'\\b[A-Za-z]+\-\d+\-\d+\:\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'month-yearORday-yearORday:hours:mins:secs':'\\b[A-Za-z]+\-\d+\-\d+\:\d+\:\d+\:\d+\\b',
             'yearORday/month/yearORday hours:mins:secs AMorPM':'\\b\d+\/[A-Za-z]+\/\d+\s+\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'yearORday/month/yearORday hours:mins:secs':'\\b\d+\/[A-Za-z]+\/\d+\s+\d+\:\d+\:\d+\\b',
             'yearORday-month-yearORday hours:mins:secs AMorPM':'\\b\d+\-[A-Za-z]+\-\d+\s+\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'yearORday-month-yearORday hours:mins:secs':'\\b\d+\-[A-Za-z]+\-\d+\s+\d+\:\d+\:\d+\\b',
             'month/yearORday/yearORday hours:mins:secs AMorPM':'\\b[A-Za-z]+\/\d+\/\d+\s+\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'month/yearORday/yearORday hours:mins:secs':'\\b[A-Za-z]+\/\d+\/\d+\s+\d+\:\d+\:\d+\\b',
             'month-yearORday-yearORday hours:mins:secs AMorPM':'\\b[A-Za-z]+\-\d+\-\d+\s+\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'month-yearORday-yearORday hours:mins:secs':'\\b[A-Za-z]+\-\d+\-\d+\s+\d+\:\d+\:\d+\\b',
             'yearORday month yearORday hours:mins:secs.millisecs':'\\b\d+\s+[A-Za-z]+\s+\d+\s+\d+\:\d+\:\d+\.\d+\\b',
             'month dayORyear hours:mins:secs +millisecs dayORyear':'\\b[A-Za-z]+\s+\d+\s+\d+\:\d+\:\d+\s+\+\d+\s+\d+\\b',
             'month dayORyear hours:mins:secs dayORyear':'\\b[A-Za-z]+\s+\d+\s+\d+\:\d+\:\d+\s+\d+\\b',
             'month dayORyear dayORyear hours:mins:secs AMorPM':'\\b[A-Za-z]+\s+\d+\s+\d+\s+\d+\:\d+\:\d+\s+[A-Z]+\\b',
             'month dayORyear dayORyear hours:mins:secs':'\\b[A-Za-z]+\s+\d+\s+\d+\s+\d+\:\d+\:\d+\\b',
             'month dayORyear hours:mins:secs +millisecs':'\\b[A-Za-z]+\s+\d+\s+\d+\:\d+\:\d+\s+\+\d+\\b',
             'dayORyear month dayORyear hours:mins:secs':'\\b\d+\s+[A-Za-z]+\s+\d+\s+\d+\:\d+\:\d+\\b',
             'month dayORyear hours:mins:secs':'\\b[A-Za-z]+\s+\d+\s+\d+\:\d+\:\d+\\b',
             'yearORmonthORday/yearORmonthORday/yearORmonthORday':'\\b\d+\/\d+\/\d+\*\d+\:\d+\:\d+\\b'}

## Consolidated regex with many possible timestamps
reg = '|'.join(DateTimeRegex.values())

## Function to extract date and time
def DateTimeExtractor(x):
    x = preprocess(x)
    DT = re.findall(reg,x)
    return(DT)