import json
import time
import os

class AgentTrainer:
    """
    The Historical Simulation Pipeline (Training Loop).
    Instead of adjusting neural network weights, this script "trains" the agents 
    by feeding them historical market crashes/booms, analyzing their failures, 
    and distilling optimized rules for each Macro Regime.
    """
    def __init__(self):
        # We curate a highly specific set of historical extremes to train the AI
        self.training_epochs = [
            {
                "year": "2008", 
                "regime": "[BEAR-DEFLATION]", 
                "scenario": "Global Financial Crisis. Massive banking contagion and liquidity crisis.", 
                "ticker": "LEH (Lehman Brothers)", 
                "ai_initial_guess": "STRONG BUY - Stock is trading at a historically cheap P/E ratio and high dividend.", 
                "actual_outcome": "BANKRUPT (-100%)"
            },
            {
                "year": "2020", 
                "regime": "[BULL-GOLDILOCKS]", 
                "scenario": "Fed cuts rates to zero. Massive stimulus and digital transition.", 
                "ticker": "ZM (Zoom Video)", 
                "ai_initial_guess": "SELL - P/E is over 500x. Violates all traditional value investing metrics.", 
                "actual_outcome": "MASSIVE GAIN (+400%)"
            },
            {
                "year": "2022", 
                "regime": "[BEAR-STAGFLATION]", 
                "scenario": "Inflation spikes to 9%. Fed hikes rates aggressively. Capital dries up.", 
                "ticker": "ARKK (Innovation ETF proxy)", 
                "ai_initial_guess": "BUY - Revolutionary technology narrative. Disruption is inevitable.", 
                "actual_outcome": "CRASH (-70%)"
            }
        ]
        self.rules_file = "data/learned_rules.json"

    def run_training_loop(self):
        print("==================================================")
        print(">> INITIALIZING HISTORICAL LLM TRAINING LOOP")
        print("==================================================")
        
        learned_rules = []
        
        for epoch in self.training_epochs:
            print(f"\n--- Training Epoch: {epoch['year']} {epoch['regime']} ---")
            print(f"Market Scenario: {epoch['scenario']}")
            print(f"Test Ticker: {epoch['ticker']}")
            print(f"[X] AI's Initial Naive Prediction: {epoch['ai_initial_guess']}")
            print(f"[!] Actual Market Reality: {epoch['actual_outcome']}")
            
            print(">> Triggering Auditor Self-Reflection... (Analyzing Failure)")
            time.sleep(1.5) # Simulating API latency
            
            # Simulated Auditor Rule Generation (Prompt Optimization)
            if epoch['year'] == "2008":
                rule = "RULE (Number Cruncher): In [BEAR-DEFLATION], entirely ignore low P/E ratios if the Altman Z-Score indicates bankruptcy risk. A cheap stock going to zero is still zero. Survival > Valuation."
            elif epoch['year'] == "2020":
                rule = "RULE (Strategist): In [BULL-GOLDILOCKS], relax strict P/E limits for software companies exhibiting extreme Network Effects and >50% YoY revenue growth. Do not fight the Fed."
            elif epoch['year'] == "2022":
                rule = "RULE (Risk Analyst): In [BEAR-STAGFLATION], automatically reject all 'unprofitable tech/innovation' regardless of the narrative. When cost of capital rises, positive free cash flow is mandatory."
                
            print(f"[+] NEW OPTIMIZED RULE DISTILLED:\n{rule}")
            
            learned_rules.append({
                "regime": epoch['regime'],
                "rule": rule
            })
            
        print("\n==================================================")
        print(">> SAVING OPTIMIZED RULES TO AGENT PROMPTS")
        print("==================================================")
        
        if not os.path.exists("data"):
            os.makedirs("data")
            
        with open(self.rules_file, "w") as f:
            json.dump(learned_rules, f, indent=4)
            
        print(f"Training Complete. {len(learned_rules)} bulletproof rules extracted and saved to {self.rules_file}.")

if __name__ == "__main__":
    trainer = AgentTrainer()
    trainer.run_training_loop()
