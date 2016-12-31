# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:24:33 2016

@author: 024536
"""

import os
import zipfile
import shutil

def FileToZip(filepath,filenamezip,isdelete=True):
    if not os.path.exists(filepath):
        return
    with zipfile.ZipFile(filenamezip,'w',zipfile.ZIP_DEFLATED) as filezip:
        for filename in os.listdir(filepath):  
            filezip.write(filepath+os.sep+filename,filename)
    if isdelete:
        shutil.rmtree(filepath)
        
        
        



