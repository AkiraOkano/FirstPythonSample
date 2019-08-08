'''
Created on 2019/06/05

@author: aokan
https://github.com/mmport80/QuantLib-with-Python-Blog-Examples/blob/master/blog_american_and_european_option.py
'''
from QuantLib import AmericanExercise, FDAmericanEngine, Date, SimpleQuote, Japan
from QuantLib import EuropeanExercise, PlainVanillaPayoff, AnalyticEuropeanEngine, VanillaOption
from QuantLib import Option, UnitedStates, ActualActual, Settings, FlatForward, BlackConstantVol, QuoteHandle
from QuantLib import YieldTermStructureHandle, BlackVolTermStructureHandle, BlackScholesMertonProcess
from QuantLib.QuantLib import BlackScholesProcess

import QuantLib as qb
from rakuten_rss import rss, rss_dict, fetch_open


def getProcess(valuation_date, interest_rate, dividend_rate, volatility_rate, underlying_price):
    ###################################################

    # #2)

    # Date setup

    ###################################################
    # Assumptions
    calendar = Japan()
    day_counter = ActualActual()
    Settings.instance().evaluation_date = valuation_date
    ###################################################

    # #3)

    # Curve setup
    ###################################################
    interest_curve = FlatForward(valuation_date, interest_rate, day_counter)
    dividend_curve = FlatForward(valuation_date, dividend_rate, day_counter)
    volatility_curve = BlackConstantVol(valuation_date, calendar, volatility_rate, day_counter)
    # Collate market data together
    u = QuoteHandle(underlying_price)
    d = YieldTermStructureHandle(dividend_curve)
    r = YieldTermStructureHandle(interest_curve)
    v = BlackVolTermStructureHandle(volatility_curve)

    return BlackScholesMertonProcess(u, d, r, v)

###################################################

# #4)
# Option setup


###################################################
def getEuroOption(expiry_date, put_or_call, strike_price, process):
    exercise = EuropeanExercise(expiry_date)
    payoff = PlainVanillaPayoff(put_or_call, strike_price)

    # Option Setup
    option = VanillaOption(payoff, exercise)
    engine = AnalyticEuropeanEngine(process)
    option.setPricingEngine(engine)

    return option


def getAmericanOption(valuation_date, expiry_date, put_or_call, strike_price, process):
    exercise = AmericanExercise(valuation_date, expiry_date)
    payoff = PlainVanillaPayoff(put_or_call, strike_price)

    # Option Setup
    option = VanillaOption(payoff, exercise)
    time_steps = 100
    grid_points = 100

    # engine = BinomialVanillaEngine(process,'crr',time_steps)
    engine = FDAmericanEngine(process, time_steps, grid_points)

    option.setPricingEngine(engine)
    return option
###################################################

# #5)

# #Collate results


###################################################
def getAmericanResults(option):
    print ("NPV: ", option.NPV())
    print ("Delta: ", option.delta())
    print ("Gamma: ", option.gamma())

    # print "Theta: ", option.theta()


def getEuropeanResults(option):

    print ("NPV: ", option.NPV())
    print ("Delta: ", option.delta())
    print ("Gamma: ", option.gamma())
    print ("Vega: ", option.vega())
    print ("Theta: ", option.theta())
    print ("Rho: ", option.rho())
    print ("Dividend Rho: ", option.dividendRho())
    print ("Theta per Day: ", option.thetaPerDay())
    print ("Strike Sensitivity: ", option.strikeSensitivity())

###################################################

# #1)

# #Inputs


###################################################
# dates
def getCalibratedOption():

    valuation_date = Date(5, 6, 2019)  # DDMMYYYY
    expiry_date = Date(14, 6, 2019)

# terms and conditions
    strike_price = float(rss('194061018.OS', '権利行使価格'))  # 06 C21000

    put_or_call = Option.Call

# #see idivs.org for expected dividend yields
    interest_rate = 0.0005
    dividend_rate = 0.02
    volatility_rate = float(rss('194071018.OS', 'IV')) / 100
    u = int(float(rss('N225M.FUT01.OS', '現在値')))  # 日経�??��物 =RSS|N225M.FUT01.OS!現在値
    underlying_price = SimpleQuote(u)
    market_value = float(rss('194061018.OS', '現在値'))

    process = getProcess(valuation_date, interest_rate, dividend_rate, volatility_rate, underlying_price)

    eOption = getEuroOption(expiry_date, put_or_call, strike_price, process)
    implied_volatility_rate = eOption.impliedVolatility(market_value, process)
    calibrated_process = getProcess(valuation_date, interest_rate, dividend_rate, implied_volatility_rate, underlying_price)
    calibrated_eOption = getEuroOption(expiry_date, put_or_call, strike_price, calibrated_process)
    return calibrated_eOption;


def getCalibratedOption2(valuation_date, expiry_date, strike_price, put_or_call, interest_rate,
						dividend_rate, volatility_rate, underlying_price, market_value):

    process = getProcess(valuation_date, interest_rate, dividend_rate, volatility_rate, underlying_price)
    eOption = getEuroOption(expiry_date, put_or_call, strike_price, process)
    implied_volatility_rate = eOption.impliedVolatility(market_value, process)
    calibrated_process = getProcess(valuation_date, interest_rate, dividend_rate, implied_volatility_rate, underlying_price)
    calibrated_eOption = getEuroOption(expiry_date, put_or_call, strike_price, calibrated_process)
    return calibrated_eOption;

