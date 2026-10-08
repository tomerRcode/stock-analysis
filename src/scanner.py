import pandas as pd
import yfinance as yf

class AcademicValueScanner:
    """
    Scans a list of tickers using academically validated value investing criteria.
    """
    def __init__(self, tickers):
        self.tickers = tickers
        
    def calculate_piotroski_f_score(self, ticker):
        """
        Calculates the Piotroski F-Score (0-9) based on Joseph Piotroski's 2000 paper:
        'Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers'.
        
        Evaluates Profitability, Leverage/Liquidity, and Operating Efficiency.
        A score of 8-9 is considered a strong value candidate.
        """
        # NOTE: This is a stub for the logic. In a full implementation, we fetch historical 
        # financials from yfinance and compare Current Year vs Previous Year.
        # 1. ROA > 0
        # 2. Operating Cash Flow > 0
        # 3. Change in ROA > 0
        # 4. Operating Cash Flow > Net Income
        # 5. Change in Leverage (Long Term Debt / Assets) < 0
        # 6. Change in Current Ratio > 0
        # 7. No new shares issued
        # 8. Change in Gross Margin > 0
        # 9. Change in Asset Turnover > 0
        
        # We will implement the data parsing in the next step.
        return {"ticker": ticker, "f_score": 0, "status": "Not Implemented Yet"}

    def run_screen(self):
        """
        Runs the screen across all tickers and returns the top candidates.
        """
        results = []
        for ticker in self.tickers:
            f_score = self.calculate_piotroski_f_score(ticker)
            results.append(f_score)
            
        return results

# Example usage for Energy Sector
if __name__ == "__main__":
    energy_tickers = ["XOM", "CVX", "COP", "EOG", "SLB"]
    scanner = AcademicValueScanner(energy_tickers)
    print("Running Piotroski F-Score Screen on Energy Sector...")
    print(scanner.run_screen())
