from bs4 import BeautifulSoup
import urllib3
import re
from datetime import datetime
import requests
import json
today = str(datetime.now().strftime("%Y-%m-%d"))
http = urllib3.PoolManager()
def get_tickers():
   r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
   json_file = json.loads(r.text)
   symbols = [j['symbol'] for j in json_file]
   return symbols

def get_data(ticker):
    ticker = ticker.upper()
    url = "https://finance.yahoo.com/quote/"+ticker+"?p="+ticker+"&.tsrc=fin-srch"
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'lxml')

    results = soup.find_all("table", class_="W(100%)")
    res = ''
    for item in results:
        res += str(item.tbody)

    result = re.sub(r'<[^>]+>', '!', res)
    result = re.sub(r'![!>]+!', '| ', result)
    result = list(result.split('| '))[1:-1]
    data_list = [(i, j) for i, j in zip(result[::2], result[1::2])]
    data_list = [(x,y) for (x,y) in data_list if x!="1y Target Est" and x!="Volume" and x!="Day's Range"]
    data_dir = {}
    for item in data_list:
        data_dir[item[0]] = item[1]
    data_dir["beta"] = data_dir.pop("Beta (3Y Monthly)")
    data_dir["forward_dividend_yield"] = data_dir.pop("Forward Dividend &amp; Yield")
    data_dir["open"] = data_dir.pop("Open")
    data_dir["previous_close"] = data_dir.pop("Previous Close")
    data_dir["market_cap"] = data_dir.pop("Market Cap")
    data_dir["week_52_range"] = data_dir.pop("52 Week Range")
    data_dir["ask"] = data_dir.pop("Ask")
    data_dir["bid"] = data_dir.pop("Bid")
    data_dir["avg_volume"] = data_dir.pop("Avg. Volume")
    data_dir["eps"] = data_dir.pop("EPS (TTM)")
    data_dir["pe_ratio"] = data_dir.pop("PE Ratio (TTM)")
    data_dir["earnings_date"] = data_dir.pop("Earnings Date")
    data_dir["ex_dividend_date"] = data_dir.pop("Ex-Dividend Date")
    data_dir["datetime"] = today
    data_dir["ticker"] = ticker
    data_dir["earnings_date"] = data_dir["earnings_date"].replace('!!','')
    return data_dir
