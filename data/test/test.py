# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 13:12:32 2016

@author: 024536
"""

import tdbpy

pSetting={
    'szIP':"172.22.137.140",
    'szPort':"20004",
    'szUser':"liyonghan",
    'szPassword':"liyo1234",
    'nTimeOutVal':10,
    'nRetryCount':10,
    'nRetryGap':10
}

a=tdbpy.tdbapipy()
b={}
a.TDB_Open(pSetting,b)
print b
if b['szInfo']=="retrieve code table: success!":
    #c=[]
    #print a.TDB_GetCodeTable('CF',c)
    ##print c
    #for i in range(len(c)):
    #    c[i]['chCNName']=c[i]['chCNName'].decode('gbk')

    req1 = {
        "chCode":"IF1609.CF",
        "nBeginDate":20160905,
        "nEndDate":20160906,
        "nBeginTime":0,
        "nEndTime":0,
        "nAutoComplete":0
        }
    d = []
    print a.TDB_GetFutureAB(req1,d)
#    e = []
#    print a.TDB_GetFuture(req1,e)
    
    req2 = {
        "chCode":"600030.SH",
        "nBeginDate":20160906,
        "nEndDate":20160906,
        "nBeginTime":0,
        "nEndTime":0,
        "nAutoComplete":0
    }
#    f = []
#    print a.TDB_GetTickAB(req2,f)
#    g = []
#    print a.TDB_GetTick(req2,g)

#    h = []
#    print a.TDB_GetTransaction(req2,h)
#    i = []
#    print a.TDB_GetOrder(req2,i)
#    j = []
#    print a.TDB_GetOrderQueue(req2,j)
    
#    k = []
#    print a.TDB_GetFormula("",k)
    
#    l = {}
#    print a.TDB_GetCodeInfo("IF1609.C",l)
    
    print a.TDB_Close()




