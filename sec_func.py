import requests
import pandas as pd
from headers import HEADERS
# TODO: Import beautifulsoup library

def ticker_to_cik(stock_ticker: str, leading_zero= True, header= HEADERS) -> str:
    """
    Searches for stock ticker and returns the associated CIK
    """
    ticker = stock_ticker.upper()
    tickers_json = requests.get('https://www.sec.gov/files/company_tickers.json',
                                headers = header, timeout= 5).json()

    for company in tickers_json.values():
        if company['ticker'] == ticker:
            if leading_zero:
                cik = str(company['cik_str']).zfill(10)
                return cik
            else:
                cik = str(company['cik_str'])
                return cik
    raise ValueError(f'Ticker {ticker} not found')

def accession_numbers(ticker: str, want_10_k = True, header = HEADERS) -> list:
    """
    Given the stock ticker, returns a list of the associated accession number
    for forms 10-K or 10-Q 
    """
    ticker_json = requests.get(f'https://data.sec.gov/submissions/CIK{ticker_to_cik(ticker)}.json',
                               headers= header, timeout= 5).json()
    df = pd.DataFrame.from_dict(ticker_json['filings']['recent'], orient= 'columns')
    if want_10_k:
        ten_k = df[df['form'] == '10-K']
        return [entry.replace("-", "") for entry in ten_k['accessionNumber'].to_list()]
    ten_q = df[df['form'] == '10-Q']
    return [entry.replace("-", "") for entry in ten_q['accessionNumber'].to_list()]

def build_archive_url(ticker: str,  accession_number: str) -> str:
    """
    Builds a URL needed to get access the SEC archives of a specific report
    """
    url = f'https://www.sec.gov/Archives/edgar/data/{ticker_to_cik(ticker,leading_zero= False)}/{accession_number}.FilingSummary.xml'
    return url

# TODO: Get request of xml document using URL from build_archive_url function
# TODO: Parse xml document using beautifulsoup
#   look for ShortName : HtmlFileName
# TODO: Get request HtmlFileName
# TODO: Parse table into pandas?
# TODO: Update code into objects?
# TODO: Breakdown into simpler functions?
