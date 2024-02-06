from sec_func import *

def main():
    print(ticker_to_cik('NKE'))
    nums = accession_numbers('NKE')
    print(nums)
    print(build_archive_url('NKE', accession_number= nums[0]))
    xml_filing_summary(stock_ticker= 'NKE', report_number=nums[0])

if __name__ == "__main__":
    main()
