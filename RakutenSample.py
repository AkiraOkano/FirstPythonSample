'''
Created on 2019/06/05

@author: aokan
'''

from com.okano.rakuten_rss import rss, rss_dict, fetch_open

print(rss('9502.T', '始�?�'))
print(rss_dict('9502.T', '始�?�', '銘柄名称', '現在値'))
print(rss('164060019.OS', '現在値'))
print(rss('194061018.OS', '?��?��'))
