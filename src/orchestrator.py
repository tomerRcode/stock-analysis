import os
import sqlite3
from google import genai
from src.sec_connector import SECConnector
from src.scanner import AcademicValueScanner
from src.alt_data_scraper import AltDataScraper
from src.transcript_parser import TranscriptParser

# Hardcoded Agent Prompts from our AGENTS.md Foundation
PROMPTS = {
    "macro_regime_analyst": "You are the Chief Macro Strategist. Use the Bridgewater 'All Weather' framework (Growth Rising/Falling vs Inflation Rising/Falling). Read the provided macro news and analyst consensus. Output EXACTLY ONE of the 4 regimes: [BULL-GOLDILOCKS] (Growth Up, Inflation Down), [BULL-LATE CYCLE] (Growth Up, Inflation Up), [BEAR-STAGFLATION] (Growth Down, Inflation Up), or [BEAR-DEFLATION] (Growth Down, Inflation Down). If data conflicts, defer to the news narrative.",
    "business_analyst": "You are The Strategist, a Business & Moat Analyst. Use Morningstar's Economic Moat framework (Network Effect, Intangible Assets, Cost Advantage, Switching Costs, Efficient Scale) to rate the moat as Wide, Narrow, or None. Apply Michael Porter's Five Forces to assess industry rivalry and pricing power. Define the Circle of Competence.",
    "financial_analyst": "You are The Number Cruncher, a Financial Analyst. Use Aswath Damodaran's (NYU Stern) valuation principles. 1. Calculate a rigorous DCF. 2. Compare Return on Invested Capital (ROIC) vs Weighted Average Cost of Capital (WACC) to find Economic Value Added (EVA). 3. Capitalize R&D expenses. 4. Evaluate bankruptcy risk using the Altman Z-Score.",
    "governance_analyst": "You are The Judge, a Management Analyst. 1. Evaluate capital allocation (dividends vs buybacks vs M&A) using 'The Outsiders'. 2. Apply Agency Theory for misalignment. 3. CRITICAL: Analyze the Earnings Call Q&A transcript. Is the CEO defensive? Are they dodging debt questions? Grade their honesty.",
    "risk_analyst": "You are The Skeptic, a Risk Analyst. Apply the Beneish M-Score to detect earnings manipulation and accounting fraud. Conduct macro stress testing (what happens if interest rates rise 2% or a recession hits?). Build a 'Bear Case' scenario and identify specific value traps.",
    "intelligence_officer": "You are The Intelligence Officer. You analyze Alternative Data. Your job is to look at Corporate Insider Buying (SEC Form 4) and Congressional Trades (Capitol Trades). Identify if there is 'cluster buying' (multiple politicians buying the same sector). Identify macro bottlenecks (e.g., power grid constraints). Provide this as an 'Alpha Indicator' to support the fundamental valuation.",
    "execution_trader": "You are The Trader, the Technical Analyst and Execution Desk. You DO NOT make fundamental buy decisions. Your job is to evaluate price action, momentum, and volume. Use Technical Analysis (RSI, MACD, 50-day/200-day moving averages) to optimize the entry point. If a stock is fundamentally approved but technically in a death spiral, advise to 'Wait for consolidation'. If it is breaking out, advise to 'Execute immediately'.",
    "lead_analyst": "You are The Oracle, the Lead Portfolio Manager. Synthesize reports from the Strategist, Number Cruncher, Judge, Skeptic, Intelligence Officer, and Trader. Use an Expected Value (EV) framework. Never compromise on the Margin of Safety. Use the Trader's report strictly for timing the execution. Write the final Investment Memo."
}

class ValueInvestOrchestrator:
    """
    The automated Python orchestrator that manages the end-to-end pipeline:
    Scanner -> SEC Data Pull -> AI Agent Analysis -> Database Storage.
    """
    def __init__(self, tickers):
        self.tickers = tickers
        self.sec = SECConnector()
        self.scanner = AcademicValueScanner(tickers)
        self.alt_scraper = AltDataScraper()
        self.transcript = TranscriptParser()
        
        # Ensure API key is set for Gemini LLM SDK
        if not os.environ.get("GEMINI_API_KEY"):
            print("WARNING: GEMINI_API_KEY environment variable not set. Please set it to run the AI Agents.")
        
        # Initialize the new Google GenAI SDK
        self.client = genai.Client()
        self.init_db()

    def init_db(self):
        """Sets up a free local SQLite database to store memos (Long-Term Memory)."""
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect("data/investment_memory.db")
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS investment_memos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                memo_content TEXT
            )
        ''')
        self.conn.commit()

    def call_agent(self, agent_role, system_prompt, input_data):
        """Helper to call Gemini API for a specific agent role."""
        print(f"[{agent_role.upper()}] Analyzing data...")
        if not os.environ.get("GEMINI_API_KEY"):
            return f"[{agent_role}] Simulated report (No API Key provided)."
            
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-pro',
                contents=f"System Instructions: {system_prompt}\n\nData for Analysis:\n{input_data}"
            )
            return response.text
        except Exception as e:
            return f"Error calling {agent_role}: {e}"

    def run_pipeline(self):
        print("\n--- PHASE 0: Macro Regime Detection (Bridgewater Framework) ---")
        # In production, this fetches live news headlines from Reuters/Bloomberg/WSJ
        simulated_macro_news = (
            "Federal Reserve signals rate cuts are paused due to sticky services inflation. "
            "However, Q3 GDP growth surprised to the upside at 3.2%, driven by strong consumer spending "
            "and massive capital expenditures in the tech sector. Analysts remain incredibly bullish on equities."
        )
        current_regime = self.call_agent("macro_regime_analyst", PROMPTS["macro_regime_analyst"], simulated_macro_news)
        print(f">> ACTIVE MARKET REGIME (Determined by News & Analyst Consensus): {current_regime}")
        
        print("\n--- PHASE 1: Quantitative Scanner ---")
        # In the future, this will run the actual F-Score math. For now, we take the top ticker.
        top_ticker = self.tickers[0] 
        print(f"Top Candidate Identified by Scanner: {top_ticker}")
        
        print(f"\n--- PHASE 2: Data Acquisition (Free SEC API) ---")
        self.sec.download_latest_10k_text(top_ticker)
        xbrl_data = self.sec.get_company_facts_xbrl(top_ticker)
        
        # Truncate XBRL data for the prompt to fit context windows efficiently
        data_summary = f"Ticker: {top_ticker}\nXBRL Data Snippet: {str(xbrl_data)[:1500]}"
        
        print("\n--- PHASE 3: Multi-Agent Analysis & Debate ---")
        
        # 1. Fundamental Base
        business_report = self.call_agent("business_analyst", PROMPTS["business_analyst"], data_summary)
        financial_report = self.call_agent("financial_analyst", PROMPTS["financial_analyst"], data_summary)
        
        # 2. The Debate (Risk Agent Critiques the Fundamentals)
        print(">> Risk Agent is critiquing the fundamental thesis...")
        debate_input = f"Raw Data:\n{data_summary}\n\nStrategist Thesis:\n{business_report}\n\nFinancial Thesis:\n{financial_report}\n\nYour job is to attack these theses. Find the flaws in their logic and highlight the hidden risks."
        risk_report = self.call_agent("risk_analyst", PROMPTS["risk_analyst"], debate_input)
        
        # 3. Alternative Data
        alt_data = self.alt_scraper.get_full_intelligence_dossier(ticker=top_ticker, days_back=180)
        alt_data_summary = f"Ticker: {top_ticker}\n{alt_data}"
        intel_report = self.call_agent("intelligence_officer", PROMPTS["intelligence_officer"], alt_data_summary)
        
        # 4. Governance (RAG Transcript parsing)
        qa_transcript = self.transcript.get_governance_context(ticker=top_ticker)
        gov_input = f"Raw SEC Data:\n{data_summary}\n\nEarnings Call Q&A:\n{qa_transcript}"
        governance_report = self.call_agent("governance_analyst", PROMPTS["governance_analyst"], gov_input)
        
        print("\n--- PHASE 4: Lead Analyst Synthesis ---")
        
        # We simulate the Technical Analyst pulling basic yfinance price/volume data
        tech_data_summary = f"Ticker: {top_ticker}\nPrice Action: (Simulated technical data for RSI and Moving Averages)"
        trader_report = self.call_agent("execution_trader", PROMPTS["execution_trader"], tech_data_summary)
        
        synthesis_input = f"""
        Business Report:\n{business_report}\n
        Financial Report:\n{financial_report}\n
        Governance Report:\n{governance_report}\n
        Risk Agent's Critique (The Debate):\n{risk_report}\n
        Intelligence (Alt Data) Report:\n{intel_report}\n
        Execution Desk (Timing) Report:\n{trader_report}\n
        """
        final_memo = self.call_agent("lead_analyst", PROMPTS["lead_analyst"], synthesis_input)
        
        print("\n--- PHASE 5: Saving to Long-Term Memory ---")
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO investment_memos (ticker, memo_content) VALUES (?, ?)", (top_ticker, final_memo))
        self.conn.commit()
        print(f"Successfully saved final memo for {top_ticker} to SQLite database.")
        
        print("\n=== FINAL INVESTMENT MEMO ===")
        print(final_memo)
        
if __name__ == "__main__":
    energy_sector = ["XOM", "CVX", "COP"]
    orchestrator = ValueInvestOrchestrator(energy_sector)
    orchestrator.run_pipeline()
