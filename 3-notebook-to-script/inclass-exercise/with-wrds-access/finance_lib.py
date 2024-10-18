import wrds
import pandas as pd

# Define a constant dictionary mapping Compustat variables to their descriptions
DEFAULT_VAR_DESCRIPTIONS = {
    'gvkey': 'Global Company Key',
    'tic': 'Ticker Symbol',
    'conm': 'Company Name',
    'datadate': 'Data Date',
    'lt': 'Total Liabilities',
    'at': 'Total Assets',
    'lct': 'Current Liabilities',
    'act': 'Current Assets',
    'seq': "Total Shareholder's Equity",
    'dltt': 'Long Term Debt',
    'dlc': 'Short Term Debt',
    'ni': 'Net Income',
    'sale': 'Sales',
    'cogs': 'Cost of Goods Sold',
    'oibdp': 'Operating Income Before Depreciation',
    'oiadp': 'Operating Income After Depreciation',
    'invt': 'Inventory',
    'ppent': 'Net Property, Plant, and Equipment',
    'wcap': 'Working Capital',
    'csho': 'Number of Shares Outstanding',
    'prcc_f': 'Stock Price at the End of the Fiscal Year',
    're': 'Retained Earnings',
    'rect': 'Accounts Receivable',
    'ap': 'Accounts Payable'
}

def get_wrds_data(username, sql_query, var_descriptions=DEFAULT_VAR_DESCRIPTIONS):
    """
    Execute a SQL query on WRDS, return the results as a DataFrame, and update column names with descriptions.
    
    Args:
    username (str): WRDS username for authentication
    sql_query (str): SQL query to execute
    var_descriptions (dict, optional): Dictionary mapping variable names to their descriptions.
                                       Defaults to DEFAULT_VAR_DESCRIPTIONS.
    
    Returns:
    pandas.DataFrame: Results of the SQL query with updated column names

    Example:
    >>> sql_query = '''
    ...     SELECT gvkey, tic, conm, datadate, at, lt
    ...     FROM comp.funda
    ...     WHERE tic = 'AAPL'
    ...     AND datadate = '2022-09-30'
    ... '''
    >>> df = get_wrds_data('your_username', sql_query)
    >>> print(df.columns)
    Index(['gvkey', 'tic', 'conm', 'datadate', 'at', 'lt'], dtype='object')
    """
    with wrds.Connection(wrds_username=username) as db:
        df = pd.DataFrame(db.raw_sql(sql_query))
    
    return df


def calculate_dso(accounts_receivable, revenue, days_in_year=365):
    """
    Calculate Days Sales Outstanding (DSO) = Accounts Receivable / Revenue * Days in Year.
    """
    if revenue == 0:
        raise ValueError("Revenue cannot be zero.")
    return accounts_receivable / revenue * days_in_year


def calculate_dio(inventory, cost_of_goods_sold, days_in_year=365):
    """
    Calculate Days Inventory Outstanding (DIO) = Inventory / Cost of Goods Sold * Days in Year.
    """
    if cost_of_goods_sold == 0:
        raise ValueError("Cost of Goods Sold cannot be zero.")
    return (inventory / cost_of_goods_sold) * days_in_year


def calculate_dpo(accounts_payable, cost_of_goods_sold, days_in_year=365):
    """
    Calculate Days Payables Outstanding (DPO) = Accounts Payable / Cost of Goods Sold * Days in Year.
    """
    if cost_of_goods_sold == 0:
        raise ValueError("Cost of Goods Sold cannot be zero.")
    return (accounts_payable / cost_of_goods_sold) * days_in_year

def calculate_ccc(dso=None, dio=None, dpo=None, accounts_receivable=None, revenue=None, inventory=None, cost_of_goods_sold=None, accounts_payable=None, days_in_year=365):
    """
    Calculate the Cash Conversion Cycle (CCC).

    This function calculates the Cash Conversion Cycle using either provided ratios (dso, dio, dpo) 
    or raw financial data. If both ratios and raw data are provided, priority is given to the ratios.

    Parameters:
    dso (float, optional): Days Sales Outstanding
    dio (float, optional): Days Inventory Outstanding
    dpo (float, optional): Days Payable Outstanding
    accounts_receivable (float, optional): Accounts Receivable value
    revenue (float, optional): Revenue value
    inventory (float, optional): Inventory value
    cogs (float, optional): Cost of Goods Sold value
    accounts_payable (float, optional): Accounts Payable value
    days_in_year (int, optional): Number of days in a year. Defaults to 365.

    Returns:
    float: Cash Conversion Cycle (CCC) value
    or
    str: Error message if required data is missing

    Note:
    - The function requires either the ratio (dso, dio, dpo) or the corresponding financial data for each component.
    - If both ratio and financial data are provided for a component, the ratio takes precedence.
    - The default value for days_in_year is 365, but can be adjusted if needed (e.g., for leap years or different accounting periods).
    """
    if dso is None:
        if accounts_receivable is None or revenue is None:
            return "Either dso or both accounts_receivable and revenue must be provided"
        dso = (accounts_receivable / revenue) * days_in_year
        
    
    # fill in some lines about dio and dpo
    if dio is None:
        if inventory is None or cost_of_goods_sold is None:
            return "Either dio or both inventory and cogs must be provided"
        dio = (inventory / cost_of_goods_sold) * days_in_year
        
    if dpo is None:
        if accounts_payable is None or cost_of_goods_sold is None:
            return "Either dpo or both accounts_payable and cogs must be provided"
        dpo = (accounts_payable / cost_of_goods_sold) * days_in_year

    return dso + dio - dpo


if __name__ == "__main__":
    
    # Example SQL query
    sql_query = """
    SELECT gvkey, tic, conm, datadate,  
        lt, at, lct, act, seq, dltt, dlc, ni, sale, cogs, oibdp, oiadp, invt, ppent, wcap, csho, prcc_f, re, rect, ap
    FROM comp.funda
    WHERE indfmt='INDL' 
    AND datafmt='STD'
    AND popsrc='D'
    AND consol='C'
    AND datadate >= '01/01/2010' 
    AND tic in ('AAPL')
    """

    # Use the function to get the data with default column names
    username = 'frankhuettner'
    comp = get_wrds_data(username, sql_query)

    # Inspect data
    print(comp.head())
    print(comp.columns)

    # Example of using custom variable descriptions
    custom_descriptions = {
        'tic': 'Custom Ticker Description',
        'at': 'Custom Assets Description'
    }
    comp_custom = get_wrds_data(username, sql_query, custom_descriptions)
    print(comp_custom.columns)