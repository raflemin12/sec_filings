import requests
import pandas as pd
from headers import HEADERS

def ticker_to_cik(ticker: str, header= HEADERS) -> str:
    """
    Searches for stock ticker and returns the associated CIK
    """
    ticker = ticker.upper()
    tickers_json = requests.get('https://www.sec.gov/files/company_tickers.json',
                                headers = header, timeout= 5).json()

    for company in tickers_json.values():
        if company['ticker'] == ticker:
            cik = str(company['cik_str']).zfill(10)
            return cik
    raise ValueError(f'Ticker {ticker} not found')

def accession_numbers_doc(ticker: str, want_10_k = True, header = HEADERS) -> dict:
    """
    Given the stock ticker, returns a dict of the associated accession number and document
    for forms 10-K or 10-Q 
    """
    ticker_json = requests.get(f'https://data.sec.gov/submissions/CIK{ticker_to_cik(ticker)}.json',
                               headers= header, timeout= 5).json()
    df = pd.DataFrame.from_dict(ticker_json['filings']['recent'], orient= 'columns')
    if want_10_k:
        ten_k = df[df['form'] == '10-K']
        return ten_k[['accessionNumber', 'primaryDocument']].to_csv('split', index= False)
    else:
        ten_q = df[df['form'] == '10-Q']
        return ten_q[['accessionNumber', 'primaryDocument']].to_csv('split', index= False)
