import os
import json
from datetime import datetime

class AgentMemory:
    """
    Phase 9: Long-Term Memory (The Elephant Brain)
    Allows agents to recall past analyses, preventing them from starting from scratch.
    In a massive production environment, this is backed by a Vector Database (like ChromaDB).
    For this lightweight deployment, it uses a persistent JSON/SQLite store to track historical context.
    """
    def __init__(self, db_path="data/agent_memory.json"):
        self.db_path = db_path
        self._ensure_db()
        
    def _ensure_db(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)
                
    def save_memory(self, ticker, debate_summary, final_verdict):
        """Saves the current analysis into long-term memory."""
        with open(self.db_path, "r") as f:
            memory = json.load(f)
            
        if ticker not in memory:
            memory[ticker] = []
            
        memory[ticker].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "debate": debate_summary,
            "verdict": final_verdict
        })
        
        with open(self.db_path, "w") as f:
            json.dump(memory, f, indent=4)
            
    def retrieve_past_memory(self, ticker):
        """
        Retrieves the last known analysis for a ticker to provide historical context.
        """
        with open(self.db_path, "r") as f:
            memory = json.load(f)
            
        if ticker not in memory or len(memory[ticker]) == 0:
            return f"No prior memory found for {ticker}. This is our first time analyzing them."
            
        past_runs = memory[ticker]
        latest_run = past_runs[-1]
        
        context = (f"[MEMORY RETRIEVAL]: We analyzed {ticker} on {latest_run['date']}. \n"
                   f"- Past Debate Summary: {latest_run['debate'][:200]}...\n"
                   f"- Past Verdict: {latest_run['verdict'][:200]}...\n"
                   f"INSTRUCTION: Compare today's data against our past analysis. Did management fix the issues we flagged last time?")
        
        return context

if __name__ == "__main__":
    memory = AgentMemory()
    # Simulate saving a memory from 6 months ago
    memory.save_memory("VST", "The Skeptic warned about high capex. Strategist loved the nuclear moat.", "HOLD until capex stabilizes.")
    
    # Retrieve it today
    print(memory.retrieve_past_memory("VST"))
