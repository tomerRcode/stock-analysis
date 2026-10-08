import yfinance as yf
import pandas as pd

class SECDataFetcher:
    """
    Placeholder for fetching 10-K and 10-Q raw text data. 
    This will be used by the 'Business & Moat Analyst' and 'Risk Analyst' to read management's exact words.
    """
    def __init__(self, ticker):
        self.ticker = ticker
        
    def get_latest_10k_text(self):
        # TODO: Implement SEC EDGAR fetching logic (e.g., using sec-api or sec-edgar-downloader)
        pass

class FinancialDataFetcher:
    """
    Fetches quantitative data (prices, financial statements, news) using yfinance.
    This provides the raw data for the 'Number Cruncher' agent.
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_financial_statements(self):
        """Returns Annual Income Statement, Balance Sheet, and Cash Flow."""
        return {
            "income_statement": self.stock.financials,
            "balance_sheet": self.stock.balance_sheet,
            "cash_flow": self.stock.cashflow
        }

    def get_company_profile(self):
        """Returns business summary, industry, and basic valuation metrics."""
        info = self.stock.info
        return {
            "name": info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "summary": info.get("longBusinessSummary"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "dividend_yield": info.get("dividendYield"),
            "shares_outstanding": info.get("sharesOutstanding")
        }

    def get_news(self):
        """Returns recent news links and titles for the ticker."""
        return self.stock.news
