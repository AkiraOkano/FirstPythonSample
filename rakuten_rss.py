"""楽天RSS用モジュール
"""
from lib.ddeclient import DDEClient


def rss(code, item):

	dde = DDEClient("rss", str(code))
	try:
		res = dde.request(item).decode('sjis').strip()
	except:
		print('fail: code@', code)
		res = 0
	finally:
		dde.__del__()
	return res


def rss_dict(code, *args):
	"""

	Parameters
	----------
	code : str
	args : *str

	Returns
	-------
	dict

	Examples
	----------


	"""

	dde = DDEClient("rss", str(code))
	res = {}
	try:
		for item in args:
			res[item] = dde.request(item).decode('sjis').strip()
	except:
		print('fail: code@', code)
		res = {}
	finally:
		dde.__del__()
	return res


def fetch_open(code):
	"""

	Parameters
	----------
	code : int
	Examples
	---------
	>>> fetch_open(9551)
	50050
	"""

	return float(rss(str(code) + '.T', '始�?�'))
