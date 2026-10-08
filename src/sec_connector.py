import requests
import os
from sec_edgar_downloader import Downloader

class SECConnector:
    """
    Handles completely free data retrieval from the US Securities and Exchange Commission (SEC).
    Includes pulling 10-K text for qualitative agents and XBRL JSON data for quantitative agents.
    """
    def __init__(self, user_email="student@example.com", company_name="ValueInvestAI"):
        # The SEC requires a User-Agent header with a company name and email to use their free API.
        self.headers = {
            "User-Agent": f"{company_name} {user_email}"
        }
        self.ticker_to_cik = self._get_ticker_to_cik_mapping()
        
        # Initialize the downloader for text filings (saves to 'data/sec_filings' directory)
        self.dl = Downloader(company_name, user_email, "data/sec_filings")

    def _get_ticker_to_cik_mapping(self):
        """Fetches the official SEC mapping of Ticker Symbols to CIK numbers."""
        url = "https://www.sec.gov/files/company_tickers.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            # The SEC returns a dict of dicts. We want { 'AAPL': '0000320193' }
            return {v['ticker']: str(v['cik_str']).zfill(10) for k, v in data.items()}
        return {}

    def download_latest_10k_text(self, ticker):
        """
        Downloads the latest 10-K filing text for the qualitative AI agents.
        Files are saved locally so we don't have to re-download them.
        """
        print(f"Downloading latest 10-K for {ticker}...")
        self.dl.get("10-K", ticker, limit=1, download_details=True)
        print(f"Saved to data/sec_filings/sec-edgar-filings/{ticker}/10-K/")

    def get_company_facts_xbrl(self, ticker):
        """
        Pulls exact, SEC-audited numerical data (Revenue, Net Income, etc.) 
        from the free data.sec.gov API for the quantitative scanner/agent.
        """
        cik = self.ticker_to_cik.get(ticker.upper())
        if not cik:
            print(f"Error: Could not find CIK for ticker {ticker}")
            return None

        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch XBRL data for {ticker}. Status: {response.status_code}")
            return None

if __name__ == "__main__":
    # Quick Test
    sec = SECConnector()
    print("Testing SEC XBRL API for XOM (ExxonMobil)...")
    facts = sec.get_company_facts_xbrl("XOM")
    if facts:
        print("Success! Retrieved facts. Entity Name:", facts.get("entityName"))
        
    print("\nTesting 10-K Downloader for XOM...")
    sec.download_latest_10k_text("XOM")
