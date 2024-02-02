import requests
import pandas as pd
from headers import HEADERS

def ticker_to_cik(ticker: str, headers= HEADERS) -> str:
    """
    Searches for stock ticker and returns the associated CIK
    """
    ticker = ticker.upper()
    tickers_json = requests.get('https://www.sec.gov/files/company_tickers.json', headers = HEADERS).json()

    for company in tickers_json.values():
        if company['ticker'] == ticker:
            cik = str(company['cik_str']).zfill(10)
            return cik
    raise ValueError(f'Ticker {ticker} not found')
