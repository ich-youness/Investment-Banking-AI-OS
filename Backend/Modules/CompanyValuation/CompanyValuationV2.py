from agno.agent import Agent
# from agno.tools.duckduckgo import ExaTools
from agno.tools.yfinance import YFinanceTools
from agno.models.xai import xAI
import asyncio
from typing import Dict, Any
import json
from agno.tools.exa import ExaTools
from agno.tools.calculator import CalculatorTools
from agno.tools.googlesearch import GoogleSearchTools
from dotenv import load_dotenv
from agno.team import Team
from Tools.CompanyValuationDB import get_companiesV2, get_income_statements, get_balance_sheets, get_valuation_metrics
import os
load_dotenv()

class FinancialAnalysisAgents:
    def __init__(self, xai_api_key: str):
        self.xai_api_key =xai_api_key
        
    def create_income_statement_analyst(self) -> Agent:
        """Agent 1: Income Statement Analysis Specialist"""
        return Agent(
            name="Income Statement Analyst",
            model= xAI(id="grok-3-mini", api_key=self.xai_api_key),
            tools=[ CalculatorTools(),get_companiesV2, get_income_statements, get_balance_sheets, get_valuation_metrics],
            instructions="""You are a financial analyst specializing in income statement analysis. Your role is to:
            
1. Analyze revenue growth trends and calculate growth rates
2. Calculate and interpret key margins:
   - Gross Margin = (Revenue - COGS) / Revenue
   - Operating Margin = Operating Income / Revenue  
   - Net Margin = Net Income / Revenue
3. Analyze EBITDA and operating performance
4. Identify trends in profitability and operational efficiency
5. Provide insights on revenue quality and cost structure

When analyzing:
- Calculate quarter-over-quarter and year-over-year changes
- Benchmark performance against industry standards
- Identify strengths and weaknesses in profitability
- Focus on sustainable growth patterns""",
            markdown=True
        )
    
    def create_balance_sheet_analyst(self) -> Agent:
        """Agent 2: Balance Sheet Analysis Specialist"""
        return Agent(
            name="Balance Sheet Analyst",
            model= xAI(id="grok-3-mini", api_key=self.xai_api_key),
            tools=[CalculatorTools(),get_companiesV2, get_income_statements, get_balance_sheets, get_valuation_metrics],
            instructions="""You are a financial analyst specializing in balance sheet analysis. Your role is to:

1. Analyze capital structure:
   - Debt-to-Equity Ratio = Total Debt / Shareholders' Equity
   - Debt-to-Assets Ratio = Total Debt / Total Assets
   
2. Assess liquidity position:
   - Current Ratio = Current Assets / Current Liabilities
   - Quick Ratio = (Current Assets - Inventory) / Current Liabilities
   
3. Evaluate financial health:
   - Book Value per Share = Shareholders' Equity / Shares Outstanding
   - Working Capital = Current Assets - Current Liabilities
   
4. Analyze asset quality and composition
5. Assess solvency and financial stability

Key focus areas:
- Debt management and leverage
- Liquidity risk assessment
- Asset efficiency
- Financial flexibility""",
            markdown=True
        )
    
    def create_valuation_analyst(self) -> Agent:
        """Agent 3: Valuation by Multiples Specialist"""
        return Agent(
            name="Valuation Analyst",
            model= xAI(id="grok-3-mini", api_key=self.xai_api_key),
            tools=[YFinanceTools(), CalculatorTools(),GoogleSearchTools(),ExaTools(), get_companiesV2, get_income_statements, get_balance_sheets, get_valuation_metrics],
            instructions="""You are a valuation expert specializing in multiples analysis. Your role is to:

1. Calculate Enterprise Value (EV):
   EV = Market Capitalization + Total Debt - Cash & Equivalents

2. Apply appropriate industry multiples:
   - EV/Revenue for growth companies
   - EV/EBITDA for mature companies  
   - P/E Ratio for profitable companies
   - P/B Ratio for financial institutions

3. Perform comparable company analysis:
   - Identify relevant peer group
   - Calculate industry average multiples
   - Apply multiples to target company metrics

4. Provide valuation ranges and sensitivity analysis

Valuation Framework:
- Select appropriate multiples based on industry
- Calculate implied enterprise value
- Derive equity value: Equity Value = EV - Debt + Cash
- Provide realistic valuation ranges with justification""",
            markdown=True
        )
    
    def create_chief_financial_analyst(self) -> Team:
        """Master agent that coordinates all three specialists"""
        return Team(
            name="Chief Financial Analyst",
            model= xAI(id="grok-3-mini", api_key=self.xai_api_key),
            members=[
                self.create_income_statement_analyst(),
                self.create_balance_sheet_analyst(), 
                self.create_valuation_analyst()
            ],
            instructions="""You are the Chief Financial Analyst coordinating a team of three specialists. Your role is to:

1. Delegate analysis to the appropriate specialist agents
2. Synthesize findings from all three analysis domains
3. Provide comprehensive company valuation and investment recommendation
4. Identify interconnections between income statement, balance sheet, and valuation

Coordinate this analysis workflow:
- Income Statement Analyst → Profitability & Growth
- Balance Sheet Analyst → Financial Health & Structure  
- Valuation Analyst → Market Valuation & Comparables

Provide integrated insights on:
- Overall financial health score
- Investment attractiveness
- Key risks and opportunities
- Fair value estimation""",
            markdown=True
        )

# Example usage and demonstration
async def demonstrate_agents():
    # Initialize the agents (replace with your OpenAI API key)
    financial_agents = FinancialAnalysisAgents(xai_api_key=os.getenv("XAI_API_KEY"))
    
    # Create the master agent
    chief_analyst = financial_agents.create_chief_financial_analyst()
    
    # Example analysis request
    analysis_request = """
    Please perform a comprehensive financial analysis of Apple Inc. (AAPL) including:
    
    1. Income Statement Analysis:
       - Revenue growth trends last 4 quarters
       - Margin analysis (gross, operating, net)
       - EBITDA and profitability assessment
    
    2. Balance Sheet Analysis:
       - Debt-to-equity and current ratios
       - Liquidity position
       - Capital structure evaluation
    
    3. Valuation Analysis:
       - EV/EBITDA multiple compared to peers
       - P/E ratio analysis
       - Fair value estimation using multiples
    
    Provide an integrated investment recommendation based on your findings.
    """
    
    # Run the analysis
    # print("🚀 Starting comprehensive financial analysis...")
    # response = chief_analyst.run(analysis_request)
    # print("📊 ANALYSIS COMPLETE:")
    # print(response.content)
    
    # Individual agent demonstrations
    print("\n" + "="*50)
    print("INDIVIDUAL AGENT DEMONSTRATIONS")
    print("="*50)
    
    # Income Statement Analyst
    income_analyst = financial_agents.create_income_statement_analyst()
    # income_response =  
    # income_analyst.print_response("Analyze Apple's Q3 2024 revenue growth and margins")
    # income_analyst.print_response("Analyze the Maroc Telecom Company's Q4 2023 revenue growth and margins, you can fetch the company data from the tools you have")
    # print(f"\n📈 INCOME STATEMENT ANALYSIS:\n{income_response.content}")
    
    # Balance Sheet Analyst  
    balance_analyst = financial_agents.create_balance_sheet_analyst()
    # balance_response =  balance_analyst.run("Analyze TAQA Morocco's current balance sheet structure and liquidity")
    # balance_analyst.print_response("Analyze the maroc telecom company's current balance sheet structure and liquidity")
    # print(f"\n🏦 BALANCE SHEET ANALYSIS:\n{balance_response.content}")
    
    # # Valuation Analyst
    valuation_analyst = financial_agents.create_valuation_analyst()
    # valuation_response = valuation_analyst.run("Value TAQA Morocco Company using EV/EBITDA multiples compared to Nareva Holding and Masen (Moroccan Agency for Sustainable Energy) ")
    # valuation_analyst.print_response("Value maroc telecom Company using EV/EBITDA multiples compared to other Inwi and Orange companies ")
    # print(f"\n💰 VALUATION ANALYSIS:\n{valuation_response.content}")

# Moroccan company example as per your documentation
# async def analyze_moroccan_company():
#     financial_agents = FinancialAnalysisAgents(api_key=os.getenv("XAI_API_KEY"))
#     chief_analyst = financial_agents.create_chief_financial_analyst()
    
#     moroccan_analysis = """
#     Analyze a hypothetical Moroccan agro-industrial company with:
#     - Annual Revenue: 50M MAD
#     - EBITDA: 8M MAD  
#     - Financial Debt: 10M MAD
#     - Cash: 3M MAD
#     - Industry EV/EBITDA multiple: 6x
    
#     Provide:
#     1. Income statement profitability analysis
#     2. Balance sheet health assessment
#     3. Company valuation using multiples method
#     4. Investment recommendation
#     """
    
#     print("🇲🇦 ANALYZING MOROCCAN COMPANY CASE STUDY...")
#     response =  chief_analyst.run(moroccan_analysis)
#     print(response.content)

# if __name__ == "__main__":
#     # Run the demonstrations
#     asyncio.run(demonstrate_agents())
    
    # Uncomment to run Moroccan company example
    # asyncio.run(analyze_moroccan_company())