from sec_func import *

def main():
    nums = accession_numbers('NKE')
    nke = xml_filing_summary(stock_ticker= 'NKE', report_number=nums[0])
    print(find_statment_html(xml= nke))

if __name__ == "__main__":
    main()
