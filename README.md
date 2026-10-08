# AI Hedge Fund: Enterprise Value Investing System

This project is a fully automated, multi-agent AI Hedge Fund built on the principles of Warren Buffett (Value Investing), supercharged by modern quantitative mathematics, alternative data, and Artificial General Intelligence (AGI) architecture.

## 🏗️ System Architecture & Pipeline

The system is executed via `src/orchestrator.py` and follows a strict multi-phase pipeline:

### 1. The Quantitative Screener (Math First)
Instead of forcing the AI to read 100 stocks, we use `src/scanner.py` to pull the entire sector. We apply the **Piotroski F-Score** and **Joel Greenblatt's Magic Formula** to mathematically filter out garbage companies. Only the Top 3 stocks are passed to the AI.

### 2. Multi-Source Data Ingestion
For the surviving stocks, the Python pipeline pulls highly specific, free data:
*   **SEC EDGAR API:** Pulls raw XBRL financial data and 10-K text.
*   **Earnings Call RAG (`src/transcript_parser.py`):** Automatically isolates the unscripted Q&A session from the latest earnings call to catch executives off-guard.
*   **Alternative Data (`src/alt_data_scraper.py`):** Scrapes Congressional Trades (House/Senate), Corporate Insider trades, and macro news to find "Cluster Buying" catalysts.

### 3. The Multi-Agent Debate Protocol
The data is passed to a team of 7 highly specialized AI Agents, each programmed with strict academic frameworks (not generic instructions):
1.  **The Strategist:** Evaluates the Business Moat using Morningstar & Porter's 5 Forces.
2.  **The Number Cruncher:** Calculates Intrinsic Value (DCF), ROIC vs WACC (EVA), and the Altman Z-Score for bankruptcy risk.
3.  **The Judge:** Evaluates Management using "The Outsiders" framework and Agency Theory. Uses the RAG Q&A transcript to grade CEO honesty.
4.  **The Skeptic (Risk Agent):** Uses the Beneish M-Score for fraud detection. Crucially, this agent reads the Strategist and Cruncher reports and **actively debates them**, trying to poke holes in their thesis.
5.  **The Intelligence Officer:** Analyzes the Alternative Data dossier to find top-down macro catalysts (e.g., Congress buying AI power grid stocks).
6.  **The Trader:** Looks at Technical Analysis (RSI, Moving Averages) purely to time the execution (preventing the fund from catching a falling knife).
7.  **The Oracle (Lead PM):** Reads the entire debate, applies an Expected Value (EV) calculation, demands a Margin of Safety, and writes the final Investment Memo.

### 4. Long-Term Vector Memory
Implemented in `src/vector_memory.py`, the agents possess an "Elephant Brain." They save their final verdicts and debates. If they scan the same stock 6 months later, they retrieve the past memory to check if management kept their promises or if past risks materialized.

### 5. UI Presentation & Backtesting
*   **Backtesting (`src/backtester.py`):** Allows us to test the mathematical screener against 10 years of historical data to prove the strategy beats the S&P 500 (Alpha).
*   **The Dashboard (`dashboard_prototype.html`):** The final output is rendered into an interactive HTML dashboard that visually explains Valuation Metrics, Intrinsic Value spreads, and the Macro Story without financial jargon.
