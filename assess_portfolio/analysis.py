
root_dir = r"C:\Users\329982789\Desktop\ML for Trading\ML4T_2018Spring\ML4T_2018Spring"
base_dir = r"C:\Users\329982789\Desktop\ML for Trading\ML4T_2018Spring\ML4T_2018Spring\assess_portfolio"
import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data



# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=True):
    
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    # Get daily portfolio value
    alloc_val = (prices/prices.iloc[0])*allocs*sv    
    port_val = alloc_val.sum(1)
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr = (port_val[-1]-port_val[0])/port_val[0]
    adr = cr/sf
    sddr = np.std(port_val/port_val[0])
    sr = (cr-rfr)/sddr# add code here to compute stats

    # Compare daily portfolio value with SPY using a normalized plot
    norm_SPY = (prices_SPY/prices_SPY.iloc[0])*sv
    if gen_plot:
        df_temp = pd.concat([port_val, norm_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp)
        pass

    # Add code here to properly compute end value
    ev = port_val[-1]

    return cr, adr, sddr, sr, ev

def test_code():
    # It is only here to help set up and test code

    # Define input parameters

    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.4, 0.3, 0.3, 0]
    start_val = 1000000  
    risk_free_rate = 0.009
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        rfr = risk_free_rate, \
        sv = start_val, \
        sf = sample_freq, \
        gen_plot = True)

    # Print statistics
    print ("Start Date:", start_date)
    print ("End Date:", end_date)
    print ("Symbols:", symbols)
    print ("Allocations:", allocations)
    print ("Sharpe Ratio:", sr)
    print ("Volatility (stdev of daily returns):", sddr)
    print ("Average Daily Return:", adr)
    print ("Cumulative Return:", cr)

if __name__ == "__main__":
    test_code()
