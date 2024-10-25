## Compute Financial Ratios using WRDS/S&P Compustat ##

# Import required libraries 
import pandas as pd
import os
from finance_lib_no_wrds import calculate_ccc, get_data_from_csv

# Note that we already import a function called get_data_from_csv
# This may lead to a conflict about name if we define another function
# with the same name.
# To avoid this, 
# - we can import the function with a different name, e.g.,
#       from finance_lib_no_wrds import get_data_from_csv as load_data_from_csv
# - we can define the function with a different name, e.g.,
#       def get_stock_data_from_csv(stock)
# - we can import the module finance_lib_no_wrds and refer to the function as
#       finance_lib_no_wrds.get_data_from_csv()
# Here, I'll prefer to use the second option.
def get_stock_data_from_csv(stock):
    # Since the file sp500_data.csv is in the same directory as the Python script, 
    # we can construct the path as follows 
    file_path = os.path.join(os.path.dirname(__file__), 'sp500_data.csv')
    # Note that this requires another import os
    # It works also on different operating systems (Windows, Mac, Linux)
    # An alternative is to specify the file location with the absolute path
    # e.g., file_path = 'C:/Users/.../sp500_data.csv' 
    # But this would break if you work on a different computer

    # No need to complete the function if you use the imported version
    df_complete = get_data_from_csv(file_path) 
    df_stock = df_complete[df_complete['tic'] == stock]

    return df_stock


# Compute year from datadate
def compute_date_and_year(df):
    # Make a local copy to avoid manipulation of original df
    df_copy = df.copy()
    
    #convert datadate to date format
    df_copy['datadate'] = pd.to_datetime(df_copy['datadate']) #convert datadate to date fmt
   
    #get year from datadate
    df_copy['year'] = df_copy['datadate'].dt.year 
    
    return df_copy


## Define Financial Metrics
def compute_financial_metrics(df, days_in_year=365):
    # Make a local copy to avoid manipulation of original df
    df_copy = df.copy()
    
    # Leverage Ratios
    df_copy['debt'] = df_copy['dltt'] + df_copy['dlc'] # TOTAL DEBT = LONG TERM + SHORT TERM DEBT
    df_copy['de_ratio'] = df_copy['debt'] / df_copy['seq'] # D/E RATIO = TOTAL DEBT / TOTAL SHAREHOLDER'S EQUITY
    df_copy['da_ratio'] = df_copy['debt'] / df_copy['at'] # D/A RATIO = TOTAL DEBT / TOTAL ASSETS

    # Liquidity Ratios 
    df_copy['current_ratio'] = df_copy['act'] / df_copy['lct'] # CURRENT RATIO = CURRENT ASSETS / CURRENT LIABILITIES
    df_copy['quick_ratio'] = (df_copy['act'] - df_copy['invt']) / df_copy['lct'] # QUICK RATIO = (CURRENT ASSETS-INVENTORY) / CURRENT LIABILITIES

    # Profitability Ratios 
    df_copy['roa'] = df_copy['ni'] / df_copy['at'] # ROA = NET INCOME / TOTAL ASSETS
    df_copy['roe'] = df_copy['ni'] / df_copy['seq'] # ROE = NET INCOME / TOTAL SHAREHOLDER'S EQUITY
    df_copy['gross_margin'] = (df_copy['sale'] - df_copy['cogs']) / df_copy['sale'] # GROSS MARGIN = (SALES - COGS)/ SALES
    df_copy['operating_margin'] = df_copy['oibdp'] / df_copy['sale'] # OPERATING MARGIN = OPERATING INCOME / SALES


    # Efficiency Ratios 
    df_copy['lag_invt'] = df_copy.groupby('tic')['invt'].shift() # Compute Lag Inventory 
    df_copy['avg_invt'] = (df_copy['invt'] + df_copy['lag_invt']) / 2 # Compute Average Inventory

    df_copy['days_in_inventory'] = df_copy['avg_invt'] / (df_copy['cogs'] / days_in_year) # DAYS IN INVENTORY = AVERAGE INVENTORY / (COGS/360)
    df_copy['inventory_turns'] = days_in_year / df_copy['days_in_inventory'] # INVENTORY TURNS = 360 / DAYS IN INVENTORY

    df_copy['days_sales_outstanding'] = df_copy['rect'] / (df_copy['sale'] / days_in_year) # DAYS SALES OUTSTANDING =  ACCOUNTS RECEIVABLE / (SALES/360)
    df_copy['days_payable_outstanding'] = df_copy['ap'] / (df_copy['cogs'] / days_in_year) # DAYS PAYABLE OUTSTANDING = ACCOUNTS PAYABLE / (COSGS/360)

    df_copy['ppe_turnover'] = df_copy['sale'] / df_copy['ppent'] # PPE TURNOVER = SALES / PPE 
    df_copy['asset_turnover'] = df_copy['sale'] / df_copy['at'] # ASSET TURNOVER = SALES / TOTAL ASSETS

    # CCC
    # You can use the already calculated 3 metrics: days_in_inventory, days_sales_outstanding, days_payable_outstanding
    df_copy['ccc'] = calculate_ccc(dio=df_copy['days_in_inventory'], dso=df_copy['days_sales_outstanding'], dpo=df_copy['days_payable_outstanding'], days_in_year=days_in_year)
    # Or you refer to the basics inputs
    df_copy['ccc'] = calculate_ccc(inventory=df_copy['avg_invt'], 
                                   accounts_receivable=df_copy['rect'], 
                                   revenue=df_copy['sale'], 
                                   cost_of_goods_sold=df_copy['cogs'], 
                                   accounts_payable=df_copy['ap'], 
                                   days_in_year=days_in_year)
    # What's remarkable: we defined the functino calculate_ccc() with floats, i.e., numbers as inputs. Here, we 
    # are using vectors (i.e., pandas dataframes series) as inputs. This is possible because Python just applies the computation
    # entry-wise to the vectors, which is the prespecified way of adding, subtracting, multiplying, dividing dataframe series.
    return df_copy


if __name__ == "__main__":
    df_AAPL = get_stock_data_from_csv("AAPL")
    df_AAPL = compute_date_and_year(df_AAPL)
    df_AAPL = compute_financial_metrics(df_AAPL, days_in_year=365)

    # View last available values
    from pprint import pprint
    pprint(df_AAPL.sort_values('datadate').groupby('tic').tail(1))
    
