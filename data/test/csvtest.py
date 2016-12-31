# -*- coding: utf-8 -*-
"""
Created on Thu Sep 08 08:51:33 2016

@author: 024536
"""

import csv

data = [
{"a":1,"b":2},
{"a":3,"b":4},
{"a":5,"b":6},
]

with open("test.csv", 'wb') as csvFile:
    csvWriter = csv.DictWriter(csvFile, fieldnames=["a","b"])
    csvWriter.writerow(dict(zip(["a","b"], ["a","b"])))
    csvWriter.writerows(data)
