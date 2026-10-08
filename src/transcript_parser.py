import re

class TranscriptParser:
    """
    Phase 8: Earnings Call RAG Pipeline
    Extracts the unscripted Q&A section of earnings calls to evaluate management honesty.
    """
    def __init__(self):
        pass

    def fetch_latest_transcript(self, ticker):
        """
        Fetches the raw text of the latest earnings call.
        (Note: Free scraping of transcripts is notoriously difficult due to paywalls. 
        In a live environment, we plug in a free FMP API key here. For the architecture PoC, 
        we simulate a challenging Q&A session).
        """
        return f"""
        [Operator Instructions]
        Welcome to the {ticker} Q3 Earnings Call.
        
        --- PREPARED REMARKS ---
        CEO: We had a fantastic quarter. Revenues are up. We are very excited about the future of {ticker}.
        Our balance sheet is strong, our moat is widening, and we are committed to shareholder value.
        Everything is going exactly according to plan.
        
        --- QUESTION-AND-ANSWER SESSION ---
        Analyst (Goldman Sachs): Your debt levels actually increased by 15% this quarter despite the revenue beat. Can you explain why capital expenditures are completely missing your guidance?
        CEO: Well, John, you know, macroeconomic headwinds are unpredictable... we are investing heavily for the long term. It's a complicated macro environment right now.
        Analyst (Morgan Stanley): You didn't really answer John's question. If debt is rising, is the 4% dividend safe?
        CEO: As I said, we evaluate the dividend on a quarterly basis with the board. Let's move to the next question.
        """

    def extract_qa_section(self, full_text):
        """
        Uses RegEx to chop off the scripted 'Prepared Remarks' and extract ONLY the Q&A.
        This saves thousands of LLM tokens and forces the AI to judge the CEO's unscripted reactions.
        """
        qa_patterns = [
            r"(?i)question-and-answer session",
            r"(?i)open the call for questions",
            r"(?i)operator, we are ready for questions"
        ]
        
        for pattern in qa_patterns:
            match = re.search(pattern, full_text)
            if match:
                # Slices the text from the start of the Q&A to the end of the document
                return full_text[match.end():].strip()
                
        return "Warning: Q&A Section could not be parsed."

    def get_governance_context(self, ticker):
        """
        The final pipeline step that delivers the clean RAG context to the Governance Agent.
        """
        full_text = self.fetch_latest_transcript(ticker)
        qa_only = self.extract_qa_section(full_text)
        
        rag_context = f"--- LATEST EARNINGS CALL Q&A FOR {ticker} ---\n{qa_only}\n"
        return rag_context

if __name__ == "__main__":
    parser = TranscriptParser()
    print("Testing Earnings Call RAG Parser...")
    print(parser.get_governance_context("VST"))
