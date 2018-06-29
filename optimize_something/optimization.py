

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy as sp
from scipy import optimize as opt
from util import get_data, plot_data


def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'],sf=252,rfr=0, gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    def portfolio_vol(alloc,port_data=prices, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM']):
    #this function returns the standard deviation (Volatility) of the daily returns given the allocation of the portfolio
    # and the data of the assets in the portfolio
    
    
        #get daily portfolio values
        alloc_val = (port_data/port_data.iloc[0])*alloc    
        port_val = alloc_val.sum(1)
        
        return np.std(port_val)

    
    
     #A guess for allocations
    l = len(syms)
    allocs = np.ones(l)/l
    def foo(allocs):
        if all(i >= 0 for i in allocs) and all(i <= 1 for i in allocs):
            return 0
        else:
            return 1
    
    #constraint for optimization algorithm
    cons = [{'type':'eq', 'fun':lambda allocs: allocs.sum(0) - 1 }, {'type':'eq','fun': foo}]
    
    print("Now Optimizing")
    
    # Find allocation (in vector form) which minimizes volatility (standard deviation) 
    allocs = opt.minimize(portfolio_vol,allocs, method="SLSQP",constraints=cons).x
    alloc_val = (prices)*allocs    
    port_val = alloc_val.sum(1)
    print(port_val)
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr = (port_val[-1]-port_val[0])/port_val[0]
    adr = cr/sf
    sddr = np.std(port_val)
    sr = (cr-rfr)/sddr
   
    


    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp)
        

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
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
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
