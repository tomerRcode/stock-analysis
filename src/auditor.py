import json
import os
from datetime import datetime

class ContinuousLearningAuditor:
    """
    Phase 10: The Auditor Agent (Continuous Learning Loop)
    This script is run quarterly (e.g., via a cron job). 
    It checks the Vector Memory for past predictions, compares them to actual 
    stock market realities using yfinance, and forces the AI to write new rules 
    if it made a mistake.
    """
    def __init__(self):
        self.memory_file = "data/agent_memory.json"
        self.rules_file = "data/learned_rules.json"
        
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.rules_file):
            with open(self.rules_file, "w") as f:
                json.dump([], f)
                
    def run_quarterly_audit(self):
        print("\n--- Starting Quarterly AI Performance Audit ---")
        
        # In production, we iterate through self.memory_file and check yfinance.
        # For this PoC, we simulate a historically failed prediction.
        simulated_memory = {
            "ticker": "OXY",
            "date": "2023-01-01",
            "prediction": "STRONG BUY. The Strategist loves the DAC (Direct Air Capture) technology. Moat is widening.",
            "actual_return_since_date": "-12%"
        }
        
        print(f"Auditing Past Prediction for {simulated_memory['ticker']}...")
        print(f"Past Verdict: {simulated_memory['prediction']}")
        print(f"Actual Return: {simulated_memory['actual_return_since_date']}")
        
        # Logic: If we said BUY but it lost money, the AI failed.
        if float(simulated_memory['actual_return_since_date'].strip('%')) < 0 and "BUY" in simulated_memory['prediction']:
            print(">> STATUS: MISMATCH DETECTED. Triggering Self-Correction Loop.")
            self._generate_correction(simulated_memory)
            
    def _generate_correction(self, memory):
        """
        Passes the failure to the Auditor LLM, asking it to identify its blind spot 
        and write a permanent rule upgrade for the agents, TAGGED BY REGIME.
        """
        print("\n>> Calling Auditor Agent...")
        
        # Simulated LLM output: The AI realizes it got distracted by shiny tech and ignored balance sheet debt.
        auditor_analysis = (
            "The AI over-weighted the unproven DAC technology (shiny object syndrome) "
            "and completely ignored the massive debt load acquired during the CrownRock acquisition."
        )
        
        # Notice we are now tagging the rule!
        new_rule = "[REGIME: STAGFLATION/BEAR] RULE UPGRADE (The Judge): In high-interest environments, always penalize heavily for debt acquired in M&A, regardless of future technology promises. Cash flow is king."
        
        print(f"\n[AUDITOR ANALYSIS]: {auditor_analysis}")
        print(f"[NEW PERMANENT RULE ADDED]: {new_rule}")
        
        # Save the new rule to the database. The Orchestrator will append these rules to the prompts in the future.
        with open(self.rules_file, "r") as f:
            rules = json.load(f)
        
        rules.append({
            "date": datetime.now().strftime("%Y-%m-%d"), 
            "ticker": memory['ticker'],
            "regime": "STAGFLATION / BEAR (High Interest Rates, Restrictive Capital)",
            "rule": new_rule
        })
        
        with open(self.rules_file, "w") as f:
            json.dump(rules, f, indent=4)

if __name__ == "__main__":
    auditor = ContinuousLearningAuditor()
    auditor.run_quarterly_audit()
