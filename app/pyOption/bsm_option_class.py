#
# Valuation of European call options in Black-Scholes-Merton Model
# incl. Vega function and implied volatility estimation
# -- class-based implementation
# bsm_option_class.py
#

from math import log, sqrt, exp
from scipy import stats

class EuropeanOptionClass(object):
    ''' Class for European options in BSM model.
    
    Attributes
    ==========
    S0 : float
        initial stock/index level
    K : float
        strike price
    T : float
        maturity (in year fractions)
    r : float
        constant risk-free short rate
    q : float
        constant dividended rate
    sigma : float
        volatility factor in diffusion term
    optionType : string
        'call' or 'put'
        
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
    imp_vol: float
        return implied volatility given option quote
    '''
    
    def __init__(self, S0, K, T, r, sigma, optionType='call', q=0):
        self.S0 = float(S0)
        self.K = K
        self.T = T
        self.r = r
        self.q = q
        self.sigma = sigma
        self.optionType = optionType
        self.d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        self.d2 = ((log(self.S0 / self.K)
            + (self.r - 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        self.Nd1 = stats.norm.cdf(self.d1, 0.0, 1.0)
        self.Nd2 = stats.norm.cdf(self.d2, 0.0, 1.0)
        self.N_d1= stats.norm.cdf(-self.d1, 0.0, 1.0)
        self.N_d2= stats.norm.cdf(-self.d2, 0.0, 1.0)

    def value(self):
        ''' Returns option value. '''
        if self.optionType == 'call':
            value = (self.S0 * exp(-self.q * self.T) * self.Nd1
            - self.K * exp(-self.r * self.T) * self.Nd2)
        else:
            value = (self.K * exp(-self.r * self.T) * self.N_d2       
            - self.S0 * exp(-self.q * self.T) * self.N_d1)
        return value
        
    def delta(self):
        ''' Returns option delta. '''
        if self.optionType == 'call':
            delta = self.Nd1
        else:
            delta = self.Nd1-1
        return delta

    def theta(self):
        ''' Returns theta of option. '''
        theta = -(self.S0 * stats.norm.pdf(self.d1, 0.0, 1.0) * self.sigma)/(2*sqrt(self.T))
        if self.optionType == 'call':
            theta -= self.r * self.K * exp(-self.r * self.T) * self.Nd2
        else:
            theta += self.r * self.K * exp(-self.r * self.T) * self.N_d2
        return theta         
    
    def gamma(self,optionType='call'):
        ''' Returns gamma of option. '''
        gamma = stats.norm.pdf(self.d1, 0.0, 1.0)/(self.S0 * self.sigma * sqrt(self.T))
        return gamma 
        
    def vega(self):
        ''' Returns Vega of option. '''
        d1 = ((log(self.S0 / self.K)
            + (self.r + 0.5 * self.sigma ** 2) * self.T)
            / (self.sigma * sqrt(self.T)))
        vega = self.S0 * stats.norm.pdf(d1, 0.0, 1.0) * sqrt(self.T)
        return vega

    def imp_vol(self, C0, sigma_est=0.2, it=100):
        ''' Returns implied volatility given option price. '''
        option = EuropeanOptionClass(self.S0, self.K, self.T, self.r, sigma_est)
        for i in range(it):
            option.sigma -= (option.value() - C0) / option.vega()
        return option.sigma
        
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

class BullSpreadClass(object):
    ''' Class for European options in BSM model.
    
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
    sigma : float
        volatility factor in diffusion term
    optionType : string
        'call' or 'put'
        
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
    imp_vol: float
        return implied volatility given option quote
    '''
    
    def __init__(self, S0, K1, K2, T, r, sigma, optionType='call', q=0):
        if optionType == 'call':
            self.option1 = EuropeanOptionClass(S0, K1, T, r, sigma, optionType, q)
            self.option2 = EuropeanOptionClass(S0, K2, T, r, sigma, optionType, q)
        else:
            self.option1 = EuropeanOptionClass(S0, K2, T, r, sigma, optionType, q)
            self.option2 = EuropeanOptionClass(S0, K1, T, r, sigma, optionType, q)
        self.S0 = float(S0)
        self.K1 = K1
        self.K2 = K2
        self.T = T
        self.r = r
        self.q = q
        self.sigma = sigma

    def value(self):
        ''' Returns option value. '''
        return self.option1.value()-self.option2.value()
        
    def delta(self):
        ''' Returns option delta. '''
        return self.option1.delta()-self.option2.delta()

    def theta(self):
        ''' Returns theta of option. '''
        return self.option1.theta()-self.option2.theta()    
    
    def gamma(self,optionType='call'):
        ''' Returns gamma of option. '''
        return self.option1.gamma()-self.option2.gamma()
        
    def vega(self):
        ''' Returns Vega of option. '''
        return self.option1.vega()-self.option2.vega()
        
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

        
if __name__ == "__main__":
    S0, K, T, r, sigma, q = 3,3,1,0.03,0.2,0.0
    option = EuropeanOptionClass(S0, K, T, r, sigma, 'call', q=0)
#    print option.dictResult()
    print option.value()
    print option.delta()
    print option.theta()
    print option.gamma()
    print option.vega()
    
    S0, K1, K2, T, r, sigma, q = 3,3,3.5,1,0.03,0.2,0.0
    optionSpread = BullSpreadClass(S0, K1, K2, T, r, sigma, 'call', q=0)
    print optionSpread.dictResult()
