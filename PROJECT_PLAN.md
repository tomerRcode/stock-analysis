# Project Plan: Value Invest AI Team

## Phase 1: Foundation (Current)
- [x] Define project goals and core principles (`README.md`).
- [x] Characterize the AI agents and their specific roles (`AGENTS.md`).
- [ ] Set up the development environment and choose the agent framework (e.g., Python, LangChain, AutoGen, or Antigravity subagents).

## Phase 2: Data Acquisition & Tooling
- [x] Implement tools for fetching financial statements (10-Ks, 10-Qs) using SEC EDGAR or financial APIs (e.g., Alpha Vantage, Financial Modeling Prep).
- [x] Implement tools for fetching news, earnings call transcripts, and management commentary.
- [x] Implement quantitative calculation tools (DCF models, ROIC calculators).

## Phase 3: Agent Implementation
- [x] Develop the **Business & Moat Analyst** prompt and capabilities.
- [x] Develop the **Financial Analyst** prompt and quantitative tools.
- [x] Develop the **Management Analyst** prompt and qualitative assessment tools.
- [x] Develop the **Risk Analyst** prompt.
- [x] Develop the **Lead Analyst** prompt for synthesis and final decision making.

## Phase 4: Quantitative Scanner
- [x] Implement a sector-wide scanner to filter stocks before deep agent analysis.
- [x] Integrate academic value screening frameworks (e.g., Piotroski F-Score).

## Phase 5: Free SEC EDGAR & Alt Data Integration
- [x] Connected to SEC's free REST API for financials.
- [x] Built the Alternative Data Scraper (Congress Trades, Insider Trades, News).

## Phase 6: Automated Python Orchestrator
- [x] Built `orchestrator.py` to manage the end-to-end pipeline automatically.
- [x] Implemented Multi-Agent Debate Protocol.

## Phase 7: UI & Backtesting
- [x] Built HTML UI Prototype for educational data display.
- [x] Built Python Backtesting Engine to test Phase 1 quantitative strategies.

## Phase 8: Data Heterogeneity (Earnings Call RAG)
- [x] Implement a Retrieval-Augmented Generation (RAG) pipeline to fetch and parse Earnings Call Transcripts.
- [x] Upgrade The Judge to analyze CEO sentiment and Q&A defensiveness.

## Phase 9: Long-Term Vector Memory
- [x] Install a Vector Database (e.g., ChromaDB).
- [x] Engineer the system to save past agent debates and retrieve them during future scans to build compounding knowledge.

## Phase 10: Continuous Learning (The Auditor Agent)
- [x] Create The Auditor Agent.
- [x] Build a quarterly feedback loop that compares past predictions to actual stock performance.
- [x] Allow The Auditor to rewrite agent system prompts to self-correct flaws.
