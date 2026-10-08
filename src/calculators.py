import pandas as pd

def calculate_roic(nopat, total_assets, current_liabilities, excess_cash=0):
    """
    Calculates Return on Invested Capital (ROIC).
    ROIC measures how efficiently a company uses its capital to generate profits.
    
    Invested Capital = Total Assets - Current Liabilities - Excess Cash
    """
    invested_capital = total_assets - current_liabilities - excess_cash
    
    if invested_capital <= 0:
        return 0.0
        
    return nopat / invested_capital

def calculate_dcf(fcf_projections, discount_rate, terminal_growth_rate, shares_outstanding):
    """
    Calculates intrinsic value per share using a simple Discounted Cash Flow (DCF) model.
    This tool is used by the 'Number Cruncher' to find the Margin of Safety.
    
    Args:
        fcf_projections (list of float): Projected free cash flows for the next N years.
        discount_rate (float): Required rate of return (e.g., 0.10 for 10%).
        terminal_growth_rate (float): Perpetual growth rate after the projection period (e.g., 0.025 for 2.5%).
        shares_outstanding (int): Total number of shares outstanding.
        
    Returns:
        float: Estimated intrinsic value per share.
    """
    if shares_outstanding == 0:
        return 0.0

    present_value_fcf = 0
    
    # 1. Calculate present value of projected FCFs
    for i, fcf in enumerate(fcf_projections, start=1):
        present_value_fcf += fcf / ((1 + discount_rate) ** i)
        
    # 2. Calculate Terminal Value using Gordon Growth Model
    final_year_fcf = fcf_projections[-1]
    terminal_value = (final_year_fcf * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
    
    # 3. Discount Terminal Value back to present
    present_value_tv = terminal_value / ((1 + discount_rate) ** len(fcf_projections))
    
    # 4. Calculate total intrinsic value per share
    total_value = present_value_fcf + present_value_tv
    
    return total_value / shares_outstanding
