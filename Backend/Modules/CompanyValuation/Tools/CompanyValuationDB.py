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




