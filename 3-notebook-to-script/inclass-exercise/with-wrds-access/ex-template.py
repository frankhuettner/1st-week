## Compute Financial Ratios using WRDS/S&P Compustat ##

# Import required libraries 
import # COMPLETE HERE !!!!!!!!!!!!!!!!!!!!!!!!!



# Get data from Compustat on WRDS for a particular stock
def get_data_from_wrds(stock):

    # COMPLETE THIS FUNCTION !!!!!!!!!!!!!!!!!!!!!!!!!
    
    return comp


# Compute year from datadate
def compute_date_and_year(comp):
    # Make a local copy to avoid manipulation of original df
    df_copy = comp.copy()

    #convert datadate to date format
    # COMPLETE HERE !!!!!!!!!!!!!!!!!!!!!!!!!
    # Note that you should manipulate the dataframe df_copy
    
    #get year from datadate
    df_copy['year'] = df_copy['datadate'].dt.year 
    return df_copy


# Define Financial Metrics
def compute_financial_metrics(comp):
    # Make a local copy to avoid manipulation of original df
    df_copy = comp.copy()
    
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

    # Efficiency Ratios and CCC
    # COMPLETE HERE !!!!!!!!!!!!!!!!!!!!!!!!!
    # Note that you should manipulate the dataframe df_copy (Ctrl + H calls the replace functionality of VS Code)
    

    
    return df_copy


if __name__ == "__main__":
    comp = get_data_from_wrds("AAPL")
    comp = compute_date_and_year(comp)
    comp = compute_financial_metrics(comp)

    # View last available values
    print(comp.sort_values('datadate').groupby('tic').tail(1))
    
