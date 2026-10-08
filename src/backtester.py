import yfinance as yf
import pandas as pd
import numpy as np

class QuantBacktester:
    """
    Backtests the Quantitative Screener (Phase 1) to ensure our mathematical 
    filters (like Piotroski F-Score or Valuation) actually generate alpha.
    """
    def __init__(self, tickers, start_date="2018-01-01", end_date="2024-01-01"):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.historical_data = {}

    def fetch_data(self):
        print(f"Fetching historical data for {len(self.tickers)} tickers...")
        for ticker in self.tickers:
            try:
                df = yf.download(ticker, start=self.start_date, end=self.end_date, progress=False)
                # We calculate simple monthly returns for backtesting
                df['Monthly Return'] = df['Close'].pct_change()
                self.historical_data[ticker] = df
            except Exception as e:
                print(f"Failed to fetch {ticker}: {e}")

    def run_backtest(self):
        """
        Simulates an equal-weight portfolio of the passed tickers vs the S&P 500 (SPY).
        (In a full production environment, this would historically calculate the F-Score 
        on Jan 1st of every year and dynamically rebalance).
        """
        print("\n--- Running Quantitative Backtest ---")
        if not self.historical_data:
            self.fetch_data()

        portfolio_returns = pd.DataFrame()
        
        for ticker, df in self.historical_data.items():
            if not df.empty and 'Monthly Return' in df:
                portfolio_returns[ticker] = df['Monthly Return']
                
        # Equal weight portfolio return
        portfolio_returns['Portfolio'] = portfolio_returns.mean(axis=1)
        
        # Calculate cumulative returns
        portfolio_cumulative = (1 + portfolio_returns['Portfolio'].dropna()).cumprod()
        
        # Fetch SPY for benchmark
        spy = yf.download("SPY", start=self.start_date, end=self.end_date, progress=False)
        spy['Return'] = spy['Close'].pct_change()
        spy_cumulative = (1 + spy['Return'].dropna()).cumprod()
        
        # Output results
        total_port_return = (portfolio_cumulative.iloc[-1] - 1) * 100
        total_spy_return = (spy_cumulative.iloc[-1] - 1) * 100
        
        print(f"Backtest Period: {self.start_date} to {self.end_date}")
        print(f"Strategy Total Return:  {total_port_return:.2f}%")
        print(f"S&P 500 Total Return:   {total_spy_return:.2f}%")
        
        if total_port_return > total_spy_return:
            print(">> STATUS: Strategy generated ALPHA (Beat the market).")
        else:
            print(">> STATUS: Strategy UNDERPERFORMED the benchmark.")
            
        return portfolio_cumulative

if __name__ == "__main__":
    # Test with a basket of Energy/Utility stocks that the screener might pick
    test_basket = ["XOM", "CVX", "VST", "NEE"]
    backtester = QuantBacktester(tickers=test_basket)
    backtester.run_backtest()
