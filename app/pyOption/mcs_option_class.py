# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 17:19:03 2016

@author: 024536
"""

from time import time
from math import exp, sqrt
from random import gauss, seed
from numba import jit
import numpy as np

class mcsOptionClass(object):
    ''' Class for Path options in mcmc model.
    
    Attributes
    ==========
    S0 : float
        initial stock/index level
    K1 : float
        strike price
    K2 : float
        strike price
    T : float
        maturity (in year fractions)
    r : float
        constant risk-free short rate
    q : float
        constant dividended rate
    N : int
        numbers of option pay terms
    Rp: float
        fixed pay off rate of option
    sigma : float
        volatility factor in diffusion term
    optionType : string
        'call' or 'put'
    I : int
        number of paths
    M : int
        number of time steps
    bp : float
        basic point
        
    Methods
    =======
    value : float
        return present value of option
    delta : float
        return delta of option
    theta : float
        return theta of option
    gamma : float
        return gamma of option         
    vega : float
        return Vega of option
    '''    
    def __init__(self,S0,K1,K2,T,r,q,sigma,N,Rp,optionType,optionStyle='BullSpreadPathN',I=25000,M=100,seedNum=2000):
        self.S0 = S0
        self.K1 = K1
        self.K2 = K2
        self.T  = T
        self.r  = r
        self.q  = q
        self.sigma = sigma
        self.N  = N
        self.Rp = Rp
        self.optionType=optionType
        self.I  = I
        self.M  = M
        self.bp = 0.0001
        seed(seedNum)
        print optionStyle
        if optionStyle == 'BullSpreadPathN':
            self.value_ = self.valueBullSpreadPathN
        elif optionStyle == 'DoubleNoTouch':
            self.value_ = self.valueDoubleNoTouch
        elif optionStyle == 'OutOfRangeRate':
            self.value_ = self.valueOutOfRangeRate
        elif optionStyle == 'DownAndOutAlternative':
            self.value_ = self.valueDownAndOutAlternative
        elif optionStyle == 'ModerateOption':
            self.value_ = self.valueModerateOption
#        else:
#            self.value_ = self.valueBullSpreadPathN
        
    @jit
    def valueBullSpreadPathN(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
        K2 = self.K2
        q  = self.q
        N  = self.N
        I  = self.I
        M  = self.M
        dt = T/M        
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,N))
        Ts = range(N)
        for i in range(0,N):
            Ts[i] = int(round(M*(i+1)/float(N)))
        for i in range(N):
            CT[:,i] = S[:,Ts[i]]

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = np.minimum(K2-K1,np.maximum(CT.mean(axis=1)-K1,0))
        value['call'] = exp(-r*T)*payOff['call'].mean()
        # Put Spread
        payOff['put'] = np.minimum(K2-K1,np.maximum(K2-CT.mean(axis=1),0))
        value['put'] = exp(-r*T)*payOff['put'].mean()
        return value

    @jit
    def valueDoubleNoTouch(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
        K2 = self.K2
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,1))
        CT = ((S<K1)+(S>K2)).sum(axis=1)==0
        PT = np.zeros((I,1))
        PT = ((S>=K1)+(S<=K2)).sum(axis=1)==0

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT.mean()*Rp
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT.mean()*Rp
        value['put'] = exp(-r*T)*payOff['put']
        return value        

    @jit
    def valueOutOfRangeRate(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
        K2 = self.K2
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,1))
        CT = ((S>=K1)*(S<=K2)).mean(axis=1)
        PT = np.zeros((I,1))
        PT = ((S<K1)+(S>K2)).mean(axis=1)

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT.mean()*Rp
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT.mean()*Rp
        value['put'] = exp(-r*T)*payOff['put']
        return value
       
    @jit
    def valueDownAndOutAlternative(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
#        K2 = self.K2
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,1))
        CT = ((S.min(axis=1)<K1)*(S[:,-1]<S[:,0]))==0
        PT = np.zeros((I,1))
        PT = ((S.min(axis=1)<K1)*(S[:,-1]<S[:,0]))==1

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT.mean()*Rp
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT.mean()*Rp
        value['put'] = exp(-r*T)*payOff['put']
        return value
    
    @jit
    def valueModerateOption(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
        K2 = self.K2
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,3))
        CT[:,0] = S.max(axis=1)>=K2
        CT[:,1] = ((S.max(axis=1)<K2)*(S[:,-1]<=S[:,0]))
        CT[:,2] = ((S.max(axis=1)<K2)*(S[:,-1]>S[:,0])*(S[:,-1]/S[:,0]-1))
#        PT = np.zeros((I,M))
#        PT = ((S.min(axis=1)<K1)*(S[:,-1]<S[:,0]))==1
        PT = np.zeros((I,3))
        PT[:,0] = S.max(axis=1)<=K1
        PT[:,1] = ((S.max(axis=1)<K1)*(S[:,-1]>=S[:,0]))
        PT[:,2] = ((S.max(axis=1)<K1)*(S[:,-1]<S[:,0])*(1-S[:,-1]/S[:,0]))

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT[:,0].mean()*Rp+CT[:,2].mean()
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT[:,0].mean()*Rp+PT[:,2].mean()
        value['put'] = exp(-r*T)*payOff['put']
        return value 
        
    def value(self):
        value = self.value_(self.S0,self.T,self.r,self.sigma)
        return value[self.optionType]

    def delta(self):
        value_left = self.value_(self.S0-self.bp,self.T,self.r,self.sigma)
        value_right = self.value_(self.S0+self.bp,self.T,self.r,self.sigma)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)
        
    def theta(self):
        value_left = self.value_(self.S0,self.T-self.bp,self.r,self.sigma)
        value_right = self.value_(self.S0,self.T+self.bp,self.r,self.sigma)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)

    def gamma(self):
        value_left = self.value_(self.S0,self.T,self.r-self.bp,self.sigma)
        value_right = self.value_(self.S0,self.T,self.r+self.bp,self.sigma)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)

    def vega(self):
        value_left = self.value_(self.S0,self.T,self.r,self.sigma-self.bp)
        value_right = self.value_(self.S0,self.T,self.r,self.sigma+self.bp)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)

    def dictResult(self):
        value_ = self.value()
        delta_ = self.delta()
        theta_ = self.theta()
        gamma_ = self.gamma()
        vega_  = self.vega()
        return {'value' : "%.6f"%value_,'valueRatio' : "%.4f%%"%(value_/self.S0*100),
                'delta' : "%.6f"%delta_,'deltaRatio' : "%.4f%%"%(delta_/self.S0*100),
                'theta' : "%.6f"%theta_,'thetaRatio' : "%.4f%%"%(theta_/self.S0*100),
                'gamma' : "%.6f"%gamma_,'gammaRatio' : "%.4f%%"%(gamma_/self.S0*100),
                'vega'  : "%.6f"%vega_ ,'vegaRatio'  : "%.4f%%"%(vega_ /self.S0*100) }

class McsBaseOptionClass(object):
    ''' Class for Path options in mcmc model.
    
    Attributes
    ==========
    S0 : float
        initial stock/index level
    K1 : float
        strike price
    K2 : float
        strike price
    T : float
        maturity (in year fractions)
    r : float
        constant risk-free short rate
    q : float
        constant dividended rate
    N : int
        numbers of option pay terms
    Rp: float
        fixed pay off rate of option
    sigma : float
        volatility factor in diffusion term
    optionType : string
        'call' or 'put'
    I : int
        number of paths
    M : int
        number of time steps
    bp : float
        basic point
        
    Methods
    =======
    value : float
        return present value of option
    delta : float
        return delta of option
    theta : float
        return theta of option
    gamma : float
        return gamma of option         
    vega : float
        return Vega of option
    '''    
    
    detail = []

    def __init__(self):
        pass
        
    @jit
    def value_(self,S0,T,r,sigma):
        return {'call':0.0,'put':0.0}
        
    def value(self):
        value = self.value_(self.S0,self.T,self.r,self.sigma)
        return value[self.optionType]

    def delta(self):
        value_left = self.value_(self.S0-self.bp,self.T,self.r,self.sigma)
        value_right = self.value_(self.S0+self.bp,self.T,self.r,self.sigma)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)
        
    def theta(self):
        value_left = self.value_(self.S0,self.T-self.bp,self.r,self.sigma)
        value_right = self.value_(self.S0,self.T+self.bp,self.r,self.sigma)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)

    def gamma(self):
        value_left = self.value_(self.S0,self.T,self.r-self.bp,self.sigma)
        value_right = self.value_(self.S0,self.T,self.r+self.bp,self.sigma)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)

    def vega(self):
        value_left = self.value_(self.S0,self.T,self.r,self.sigma-self.bp)
        value_right = self.value_(self.S0,self.T,self.r,self.sigma+self.bp)
        return (value_right[self.optionType]-value_left[self.optionType])/(2*self.bp)

    def dictResult(self):
        value_ = self.value()
        delta_ = self.delta()
        theta_ = self.theta()
        gamma_ = self.gamma()
        vega_  = self.vega()
        return {'value' : "%.6f"%value_,'valueRatio' : "%.4f%%"%(value_/self.S0*100),
                'delta' : "%.6f"%delta_,'deltaRatio' : "%.4f%%"%(delta_/self.S0*100),
                'theta' : "%.6f"%theta_,'thetaRatio' : "%.4f%%"%(theta_/self.S0*100),
                'gamma' : "%.6f"%gamma_,'gammaRatio' : "%.4f%%"%(gamma_/self.S0*100),
                'vega'  : "%.6f"%vega_ ,'vegaRatio'  : "%.4f%%"%(vega_ /self.S0*100) }

class BullSpreadPathNClass(McsBaseOptionClass):
    
    def __init__(self,S0,K1,K2,T,r,q,sigma,N,optionType,I=25000,M=100,seedNum=2000):
        self.S0,self.T,self.r,self.q,self.sigma,self.optionType = S0,T,r,q,sigma,optionType
        self.I,self.M,self.bp = I,M,0.0001
        seed(seedNum)
        self.K1,self.K2,self.N = K1,K2,N
        
    @jit
    def value_(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
        K2 = self.K2
        q  = self.q
        N  = self.N
        I  = self.I
        M  = self.M
        dt = T/M        
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,N))
        Ts = range(N)
        for i in range(0,N):
            Ts[i] = int(round(M*(i+1)/float(N)))
        for i in range(N):
            CT[:,i] = S[:,Ts[i]]

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = np.minimum(K2-K1,np.maximum(CT.mean(axis=1)-K1,0))
        value['call'] = exp(-r*T)*payOff['call'].mean()
        # Put Spread
        payOff['put'] = np.minimum(K2-K1,np.maximum(K2-CT.mean(axis=1),0))
        value['put'] = exp(-r*T)*payOff['put'].mean()
        return value        
        
class DoubleNoTouchClass(McsBaseOptionClass):
    
    def __init__(self,S0,K1,K2,T,r,q,sigma,Rp,optionType,I=25000,M=100,seedNum=2000):
        self.S0,self.T,self.r,self.q,self.sigma,self.optionType = S0,T,r,q,sigma,optionType
        self.I,self.M,self.bp = I,M,0.0001
        seed(seedNum)
        self.K1,self.K2,self.Rp = K1,K2,Rp       
        
    @jit
    def value_(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
        K2 = self.K2
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,1))
        CT = ((S<K1)+(S>K2)).sum(axis=1)==0
        PT = np.zeros((I,1))
        PT = ((S>=K1)+(S<=K2)).sum(axis=1)==0

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT.mean()*Rp
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT.mean()*Rp
        value['put'] = exp(-r*T)*payOff['put']
        return value

class OutOfRangeRateClass(McsBaseOptionClass):
    
    def __init__(self,S0,K1,K2,T,r,q,sigma,Rp,optionType,I=25000,M=100,seedNum=2000):
        self.S0,self.T,self.r,self.q,self.sigma,self.optionType = S0,T,r,q,sigma,optionType
        self.I,self.M,self.bp = I,M,0.0001
        seed(seedNum)
        self.K1,self.K2,self.Rp = K1,K2,Rp        
        
    @jit
    def value_(self,S0,T,r,sigma):
        # Parameter
        K1 = self.K1
        K2 = self.K2
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,1))
        CT = ((S>=K1)*(S<=K2)).mean(axis=1)
        PT = np.zeros((I,1))
        PT = ((S<K1)+(S>K2)).mean(axis=1)

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT.mean()*Rp
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT.mean()*Rp
        value['put'] = exp(-r*T)*payOff['put']
        return value

class DownAndOutAlternativeClass(McsBaseOptionClass):
    
    def __init__(self,S0,K,T,r,q,sigma,Rp,optionType,I=25000,M=100,seedNum=2000):
        self.S0,self.T,self.r,self.q,self.sigma,self.optionType = S0,T,r,q,sigma,optionType
        self.I,self.M,self.bp = I,M,0.0001
        seed(seedNum)
        self.K,self.Rp = K,Rp
        
    @jit
    def value_(self,S0,T,r,sigma):
        # Parameter
        K = self.K
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,1))
        CT = ((S.min(axis=1)<K)*(S[:,-1]<S[:,0]))==0
        PT = np.zeros((I,1))
        PT = ((S.min(axis=1)>K)*(S[:,-1]>S[:,0]))==0

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT.mean()*Rp
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT.mean()*Rp
        value['put'] = exp(-r*T)*payOff['put']
        return value

class ModerateOptionClass(McsBaseOptionClass):
    
    def __init__(self,S0,K,T,r,q,sigma,Rp,optionType,I=25000,M=100,seedNum=2000):
        self.S0,self.T,self.r,self.q,self.sigma,self.optionType = S0,T,r,q,sigma,optionType
        self.I,self.M,self.bp = I,M,0.0001
        seed(seedNum)
        self.K,self.Rp = K,Rp
        
    @jit
    def value_(self,S0,T,r,sigma):
        # Parameter
        K = self.K
        q  = self.q
        I  = self.I
        M  = self.M
        dt = T/M
        Rp = self.Rp
        
        # Simulating I paths with M time steps
        S = np.zeros((I,M+1))
        for i in range(I):
            for t in range(M+1):
                if t == 0:
                    S[i,t] = S0
                else:
                    z = gauss(0.0, 1.0)
                    St = S[i,t-1]*exp((r-q-0.5*sigma**2)*dt+sigma*sqrt(dt)*z)
                    S[i,t] = St
                
        # Calculating the Monte Carlo estimator
        CT = np.zeros((I,3))
        CT[:,0] = S.max(axis=1)>=K
        CT[:,1] = ((S.max(axis=1)<K)*(S[:,-1]<=S[:,0]))
        CT[:,2] = ((S.max(axis=1)<K)*(S[:,-1]>S[:,0])*(S[:,-1]/S[:,0]-1))
#        PT = np.zeros((I,M))
#        PT = ((S.min(axis=1)<K1)*(S[:,-1]<S[:,0]))==1
        PT = np.zeros((I,3))
        PT[:,0] = S.max(axis=1)<=K
        PT[:,1] = ((S.max(axis=1)<K)*(S[:,-1]>=S[:,0]))
        PT[:,2] = ((S.max(axis=1)<K)*(S[:,-1]<S[:,0])*(1-S[:,-1]/S[:,0]))

        # Terminal pay off
        payOff,value = {},{}
        # Call Spread
        payOff['call'] = CT[:,0].mean()*Rp+CT[:,2].mean()
        value['call'] = exp(-r*T)*payOff['call']
        # Put Spread
        payOff['put'] = PT[:,0].mean()*Rp+PT[:,2].mean()
        value['put'] = exp(-r*T)*payOff['put']
        return value 
        
if __name__ == "__main__":
#    S0 = 100.0
#    K1 = 100
#    K2 = 105
#    T = 91/365.0
#    r = 0.00
#    q = 0.00
#    sigma = 0.2
#    N = 3
#    Rp = 1
#    optionType='call'
#    optionStyle = 'DoubleKnockOut'
#    I = 100
    
    S0 = 0.029893
    K1 = 0.02839835
#    K2 = 0.03138765
    K2 = S0*1.1
    T = 91/365.0
    r = 0.03
    q = 0.00
    sigma = 0.13
    N = 91
    Rp = 1
    M = 91
    optionType='call'
    optionStyle = 'ModerateOption'
    I = 250000
    
    ts = []
    ts.append(time())
#    option = BullSpreadPathNClass(S0,K1,K2,T,r,q,sigma,N,optionType,I,M)
#    option = DoubleNoTouchClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M)
#    option = OutOfRangeRateClass(S0,K1,K2,T,r,q,sigma,Rp,optionType,I,M)
#    option = DownAndOutAlternativeClass(S0,K1,T,r,q,sigma,Rp,optionType,I,M)
    option = ModerateOptionClass(S0,K2,T,r,q,sigma,Rp,optionType,I,M)
    print 'value',option.value()
    print time()-ts[-1]
    option2 = mcsOptionClass(S0,K1,K2,T,r,q,sigma,N,Rp,optionType,optionStyle,I,M)
    ts.append(time())
    print 'value',option2.value()
    print time()-ts[-1]
#    ts.append(time())
#    print 'theta',option.theta()
#    print time()-ts[-1]
#    ts.append(time())
#    print 'gamma',option.gamma()
#    print time()-ts[-1]
#    ts.append(time())
#    print 'vega',option.vega()
#    print time()-ts[-1]
#    print time()-ts[0]

