import os
import uuid
import time as time_module
from datetime import datetime, timedelta
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# Initialize API and table connections (per pyairtable migration guidelines)
api = Api(AIRTABLE_TOKEN)
companies_table = api.table(BASE_ID, "companies")
financial_statements_table = api.table(BASE_ID, "financial_statements")
market_data_table = api.table(BASE_ID, "market_data")
transactions_table = api.table(BASE_ID, "transactions")
discount_rates_table = api.table(BASE_ID, "discount_rates")
industry_multiples_table = api.table(BASE_ID, "industry_multiples")

companiesV2_table = api.table(BASE_ID, "companiesV2")
income_statements_table = api.table(BASE_ID, "income_statements")
balance_sheets_table = api.table(BASE_ID, "balance_sheets")
valuation_metrics_table = api.table(BASE_ID, "valuation_metrics")



def get_companies():
    return companies_table.all()

def get_financial_statements():
    return financial_statements_table.all()

def get_market_data():
    return market_data_table.all()

def get_transactions():
    return transactions_table.all()

def get_discount_rates():
    return discount_rates_table.all()
    
def get_industry_multiples():
    return industry_multiples_table.all()


def get_companiesV2():
    """Get all companies from the companiesV2 table"""
    return companiesV2_table.all()

def get_income_statements():
    """Get all income statements from the income_statements table"""
    return income_statements_table.all()

def get_balance_sheets():
    """Get all balance sheets from the balance_sheets table"""
    return balance_sheets_table.all()

def get_valuation_metrics():
    """Get all valuation metrics from the valuation_metrics table"""
    return valuation_metrics_table.all()

