""" Simple Option module(using QuantLib)

Example1
---------
from simpleOption import *

#Simple Example

o = Option('02/P20500')
op_price = o.v(20625, 20.8, 20190124)
print(f"{o}@{op_price:.2f}  (nk=20625,IV=20.8%)  jan24 ")

OUTPUT 1
---------
02/P20500@285.49  (nk=20625,IV=20.8%)  jan24


Example2
---------
#underlying change: 20625 >>20500

op_price2 = o.v(20500)
print(f"{o}@{op_price2:.2f} (nk=20500,IV=20.8%)  jan24")

OUTPUT 2
---------
02/P20500@285.49  (nk=20625,IV=20.8%)  jan24


Example3
---------
#underlying & IV change: 20625>>20000 &IV=25%
op_price3 = o.v(20000, 25)
print(f"{o}@{op_price3:.2f} (nk=20000,IV=25%)  jan24")

OUTPUT 3
---------
02/P20500@703.62 (nk=20000,IV=25%)  jan24

Example4
---------
#use keyword
op = Option('02/P20500')
op_price4 = op(
    underlying=20250,
    iv=25,
    evaluationDate=20190122
)

"""

from parse import parse

import European as euro
import QuantLib as qb
from RakutenCodec import getRakutenCode
from rakuten_rss import rss


class Date(qb.Date):

	def __init__(self, intDate):
		self.name = str(intDate)
		year = int(self.name[0:4])
		month = int(self.name[4:6])
		date = int(self.name[6:8])
		super().__init__(date, month, year)


def sqDate(strSQDate):
	"""Returns :SQ_Date(qb.Date)
	Parameters :StrSQDate str
		type1(monthly):  '02'
		type2(weekly) :  '02w3'
		type3(with year): '201102'
	"""

	year = 0
	month = 0
	week = 2

	if len(strSQDate) >= 6:  # type(201902,201904w1)
		year = int(strSQDate[0:4])
		s = strSQDate[4:]
	else:
		year = qb.Date.todaysDate().year()
		s = strSQDate

	month = int(s[0:2])
	week = int(s[-1]) if (len(s) > 2) else 2

	return qb.Date.nthWeekday(week, 6, month, year)


# init marketData
u = qb.SimpleQuote(20040)
r = qb.SimpleQuote(0.01)
sigma = qb.SimpleQuote(25 / 100)


def setEvaluationDate(date): qb.Settings.instance().setEvaluationDate(date)


def setting(
		underlying=None,
		iv=None,
		evaluationDate=None,
		rate=None):
	""" Market Data Setting """
	if underlying is not None: u.setValue(float(underlying))
	if iv is not None: sigma.setValue(float(iv) / 100)
	if rate is not None: r.setValue(float(rate))
	if evaluationDate is not None: setEvaluationDate(Date(evaluationDate))


def view():
	print(f"EvaluationDate={qb.Settings.instance().evaluationDate}")
	print(f"u={u.value()}")
	print(f"iv={sigma.value()}")


riskFreeCurve = qb.FlatForward(0, qb.Japan(), qb.QuoteHandle(r), qb.Actual360())
volatility = qb.BlackConstantVol(0, qb.Japan(), qb.QuoteHandle(sigma), qb.Actual360())
process = qb.BlackScholesProcess(qb.QuoteHandle(u),
                                 qb.YieldTermStructureHandle(riskFreeCurve),
                                 qb.BlackVolTermStructureHandle(volatility))
engine = qb.AnalyticEuropeanEngine(process)


class Payoff(qb.PlainVanillaPayoff):

	def __init__(self, strPayoff):
		self.name = strPayoff
		x = parse("{op_type}{strike:d}", strPayoff)
		super().__init__(
			qb.Option.Call if x['op_type'] == 'C' else qb.Option.Put, x['strike'])

	def __str__(self): return self.name


class OkanoOption(qb.EuropeanOption):

	def __init__(self, strOption):
		self.name = strOption
		x = parse("{sq_date}/{payoff}", strOption)
		self.payoff = Payoff(x['payoff'])
		super().__init__(
			self.payoff, qb.EuropeanExercise(sqDate(x['sq_date'])))
		self.setPricingEngine(engine)
		self.expiry_date = sqDate(x['sq_date'])
		x = parse("{op_type}{strike:d}", x['payoff'])
		self.type = x['op_type']
		self.strike = x['strike']

	def __str__(self): return self.name

	def v(self, *setting_args):
		setting(*setting_args)
		return self.NPV()

	def pay(self, underlying): return self.payoff(float(underlying))

	def getGreeks(self, num):
		rakutenCode = getRakutenCode(self.expiry_date.year(), self.expiry_date.month(), self.type, self.strike)
		print(rakutenCode)
		valuation_date = qb.Date.todaysDate()  # qb.Settings.instance().getEvaluationDate()  # DDMMYYYY settingに入って�?る�??
		expiry_date = self.expiry_date
		strike_price = self.strike
		if (self.type == 'C'):
			put_or_call = qb.Option.Call
		else :
			put_or_call = qb.Option.Put
		interest_rate = 0.0005
		dividend_rate = 0.02
		volatility_rate = float(rss(rakutenCode + '.OS', 'ＩＶ')) / 100
		u = int(float(rss('N225.FUT01.OS', '現在値')))  # 日経�?�物
		underlying_price = qb.SimpleQuote(u)
		market_value = float(rss(rakutenCode + '.OS', '清算値'))
		print('評価日', valuation_date)
		print('SQ日', expiry_date)
		print('行使金額', strike_price)
		print('vola', volatility_rate)
		print('原資産', u)
		print('現在値', market_value)
		option = euro.getCalibratedOption2(valuation_date, expiry_date, strike_price, put_or_call, interest_rate, dividend_rate, volatility_rate, underlying_price, market_value)
		print('test', option.delta() * num, f'{option.delta() * num:.4f}')
		return [option.delta() * num , option.gamma() * num, option.thetaPerDay() * num, option.vega() * num /100]


class Portfolio():
	"""簡単なポ�?�トフォリオクラス"""

	def __init__(self, lines):
		'''
		:param lines: str

		Example:
		p = Portfolio(
			"""
				02/C21000[1]
				02/C21250[-2]
				02/C21500[1]
			""")
		'''
		self.items = []
		self.nums = []
		self.premium = []
		for s in lines.strip().splitlines():
			x = parse("{str_op}[{num:d}]!{pre:d}", s.strip())
			self.items.append(OkanoOption(x['str_op']))
			self.nums.append(x['num'])
			self.premium.append(x['pre'])

	def v(self, *setting_args):
		setting(*setting_args)
		return sum((op.v() - pre) * num for op, num, pre in zip(self.items, self.nums, self.premium))

	def pay(self, underlying):
		# for op, num, pre in zip(self.items, self.nums, self.premium):
		# 	print((op.pay(underlying)-pre)*num)
		return sum((op.pay(underlying) - pre) * num for op, num, pre in zip(self.items, self.nums, self.premium))
