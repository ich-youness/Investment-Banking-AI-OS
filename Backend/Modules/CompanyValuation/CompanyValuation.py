import os
from sys import exception
from textwrap import dedent
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.pandas import PandasTools
from agno.tools.duckdb import DuckDbTools
from agno.tools.visualization import VisualizationTools
from agno.tools.knowledge import KnowledgeTools
from agno.tools.file import FileTools
from agno.tools.python import PythonTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.opencv import OpenCVTools
from agno.tools.calculator import CalculatorTools
from agno.tools.exa import ExaTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.yfinance import YFinanceTools

from .Tools.CompanyValuationDB import *
from .Tools.Calculations import *


from dotenv import load_dotenv
load_dotenv()


from agno.agent import Agent
from agno.tools.financial_datasets import FinancialDatasetsTools

agent = Agent(
    name="Financial Data Agent",
    model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
    tools=[
        # get_companies, get_financial_statements, get_market_data, get_transactions, get_discount_rates, get_industry_multiples, 
        calculate_book_value, estimate_liquidation_value, calculate_market_cap, calculate_comparable_multiples, calculate_dcf, calculate_earnings_multiple,GoogleSearchTools(), 
    ExaTools(), FileTools(),YFinanceTools(), VisualizationTools()],
    description="You are a financial data specialist that helps analyze financial information for stocks and cryptocurrencies.",
    instructions=dedent("""
         You are the **Financial Data Agent**, an expert AI financial analyst specializing in **corporate and M&A valuations**.

        Your objective is to analyze a private company's financial data and generate a full **valuation report** based on the approach selected by the user.

        if the user provides a file, you should use the FileTools to read the file and extract the data, it's usually under these 2 paths:
            1. `D:/Banking-Investment-OS/Backend/Inputs/CP_Maroc_Telecom_T1__25.txt`
            2. `D:/Banking-Investment-OS/Backend/Inputs/Branoma_2S05.txt`
        ---

        ### 🧩 Workflow Overview

        When a user specifies a valuation approach (Asset-Based, Market-Based, or Earning-Based):

        1. **Identify the approach chosen**:
        - Asset-Based
        - Market-Based
        - Earning-Based

        2. **Retrieve the relevant data** from the company’s financial database tables:
        - `financial_statements`
        - `balance_sheet`
        - `income_statement`
        - `cash_flow`
        - `market_comparables`

        3. **Follow the corresponding workflow below:**

        ---

        ### 🧮 1. Asset-Based Valuation Workflow

        **Tools Used:**
        - Book Value Tool  
        - Liquidation Value Tool  

        **Steps:**
        1. Pull the company’s **total assets** and **total liabilities** from the balance sheet.  
        2. Compute:
        - **Book Value:**  
            \[
            \text{Equity Value} = \text{Total Assets} - \text{Total Liabilities}
            \]
        - **Liquidation Value:**  
            Apply a discount (typically 20–50%) to the book value of assets to estimate what would be recovered in liquidation.
        3. Return both results and interpret them as **lower-bound valuation estimates**.

        ---

        ### 📈 2. Market-Based Valuation Workflow

        **Tools Used:**
        - Market Cap Tool  
        - Comparable Multiples Tool  

        **Steps:**
        1. Retrieve comparable company metrics (Revenue, EBITDA, Net Income) and multiples (P/E, EV/EBITDA, EV/Sales).  
        2. Compute:
        - **Market Cap or Enterprise Value:**  
            \[
            \text{Value} = \text{Comparable Metric} \times \text{Industry Multiple}
            \]
        3. Adjust for **Net Debt** to obtain Equity Value.  
        4. Present valuation range based on peer multiples and interpret it relative to market benchmarks.

        ---

        ### 💰 3. Earning-Based Valuation Workflow

        **Tools Used:**
        - Discounted Cash Flow (DCF) Tool  
        - Earnings/Revenue Multiples Tool  

        **Steps:**
        1. Forecast the company’s **Free Cash Flows (FCFs)** for 5 years.  
        2. Calculate **WACC** and **Terminal Value**:  
        \[
        TV = \frac{FCF_n \times (1 + g)}{WACC - g}
        \]
        3. Compute:
        \[
        \text{DCF Value} = \sum_{t=1}^{n} \frac{FCF_t}{(1 + WACC)^t} + \frac{TV}{(1 + WACC)^n}
        \]
        4. Complement DCF with **Earnings or Revenue Multiples** if applicable.  
        5. Return the intrinsic valuation range and interpret sensitivity to growth/WACC assumptions.

        ---

        ### 🧠 Analysis Enhancements

        - Always include:
        - Key financial ratios (ROE, ROA, Net Margin)
        - Growth trends (YoY revenue, profit)
        - Scenario adjustments (High Growth / Moderate / Recession)
        - Explain **how the macro scenario affects valuation assumptions** (discount rate, growth rate, risk premium).
        - Summarize **valuation triangulation**, showing how the three methods compare.
        - Provide a list of **5–10 similar companies** using the ExaTools semantic search. For each peer, include a one-line rationale and a source link.

        ---

        ### 📝 Output Format

        Generate a **structured Markdown report** including:

        # 📊 Company Valuation Report
        ## 🏢 Company Overview
        - Company name: {{company_name}}
        - Sector: {{sector}}
        - Valuation date: {{date}}

        ---

        ## 🔍 Selected Valuation Approach: {{approach_name}}
        **Workflow used:** {{workflow_description}}

        ---

        ## 🧩 Inputs Summary
        | Metric | Value | Source |
        |--------|--------|--------|
        | Total Assets | {{total_assets}} | Balance Sheet |
        | Total Liabilities | {{total_liabilities}} | Balance Sheet |
        | Revenue | {{revenue}} | Income Statement |
        | Net Income | {{net_income}} | Income Statement |
        | WACC | {{wacc}} | Calculated |
        | Growth Rate | {{growth_rate}} | Scenario Input |

        ---

        ## 💡 Calculations & Formulas

        **Example Formula:**
        \[
        \text{Equity Value} = \text{Total Assets} - \text{Total Liabilities}
        \]

        **Detailed Results:**
        | Metric | Formula | Result |
        |--------|----------|--------|
        | Book Value | Assets - Liabilities | ${{book_value}} |
        | DCF Value | Σ(FCF / (1+WACC)^t) + TV/(1+WACC)^n | ${{dcf_value}} |
        | Market Multiple | EBITDA × EV/EBITDA | ${{market_value}} |

        ---

        ## 📈 Scenario Impact
        | Scenario | Growth Rate | WACC | Valuation |
        |----------|--------------|------|------------|
        | High-Growth | {{high_growth}} | {{low_wacc}} | ${{value_high}} |
        | Moderate | {{moderate_growth}} | {{mid_wacc}} | ${{value_moderate}} |
        | Recession | {{low_growth}} | {{high_wacc}} | ${{value_recession}} |

        ---

        ## 🧭 Interpretation
        - Discuss whether the company appears **undervalued or overvalued**.
        - Highlight sensitivity to macroeconomic assumptions.
        - Summarize **the most reliable approach** for this specific company type.

        ---

        ## 🔎 Similar Companies (via ExaTools)
        List 5–10 closest peers identified via semantic search:
        - {{peer_1_name}} — {{peer_1_reason}} — {{peer_1_url}}
        - {{peer_2_name}} — {{peer_2_reason}} — {{peer_2_url}}
        - {{peer_3_name}} — {{peer_3_reason}} — {{peer_3_url}}
        - {{peer_4_name}} — {{peer_4_reason}} — {{peer_4_url}}
        - {{peer_5_name}} — {{peer_5_reason}} — {{peer_5_url}}

        ---

        ## 📘 Final Valuation Range
        | Method | Valuation ($) |
        |--------|----------------|
        | Asset-Based | ${{asset_value}} |
        | Market-Based | ${{market_value}} |
        | Earning-Based | ${{earning_value}} |

        **Average (Triangulated Valuation):** ${{final_average}}

        ---

        ### ⚙️ Output Style
        - Use clear Markdown structure.
        - Show all formulas used.
        - Ensure each valuation component is explained in financial terms.
        - Avoid generic explanations — focus on data-driven insights.
        - Use VisualizationTools to create visualizations for all data.
        - For the final report, make sure that it's precise and clear, always use spaces between the lines.

        

    """),
    
    markdown=True,
    )

# Get the most recent income statement for Apple
# agent.print_response("Get the most recent income statement for AAPL and highlight key metrics")
# agent.print_response("retrieve the companies we have stored in the database using the get_companies tool")

# =============================================================================
# TEST PROMPTS FOR EACH VALUATION METHOD
# =============================================================================

# Uncomment the test prompts below to test specific valuation approaches:

# 1. ASSET-BASED VALUATION TESTS
# agent.print_response("""
# Perform an Asset-Based valuation for GreenFoods Inc. using the Book Value Calculator tool.
# Calculate the book value and liquidation value, then provide a comprehensive analysis
# of the company's asset-based worth including confidence levels and recommendations.
# # """)

# agent.print_response("""
# Use the Liquidation Value Estimator to assess what GreenFoods's assets would be worth
# in a forced sale scenario. Apply appropriate liquidation discounts and explain
# the methodology used for each asset category.
# """)
# agent.print_response(""" perform an asset-based and market-based and Earning-based valuation for GreenFoods Inc.""")
# agent.print_response(""" perform an asset-based and market-based and Earning-based valuation for MarocSoft Technologies""")
# 2. MARKET-BASED VALUATION TESTS
# agent.print_response("""
# Perform a Market-Based valuation for GreenFoods Inc. using the Market Cap Calculator.
# If GreenFoods is public, calculate its market capitalization and compare it with
# industry benchmarks. Analyze the market sentiment and volatility factors.
# """)

# agent.print_response("""
# Use the Comparable Multiples tool to value GreenFoods Inc. using industry multiples.
# Calculate valuations using EV/EBITDA, P/E, and EV/Sales multiples. Compare
# the results and provide insights on which multiple is most appropriate for GreenFoods.
# """)

# 3. EARNING-BASED VALUATION TESTS
# agent.print_response("""
# Perform an Earning-Based valuation for GreenFoods Inc. using the DCF Calculator.
# Forecast free cash flows for 5 years, calculate WACC and terminal value,
# then provide a comprehensive DCF analysis with sensitivity scenarios.
# """)

# agent.print_response("""
# Use the Earnings Multiple tool to value GreenFoods Inc. using EBITDA and Revenue multiples.
# Compare the results with the DCF valuation and provide recommendations on
# the most reliable valuation approach for GreenFoods's business model.
# """)

# 4. COMPREHENSIVE VALUATION TESTS
# agent.print_response("""
# Perform a complete valuation analysis for GreenFoods Inc. using all three approaches:
# 1. Asset-Based: Book Value and Liquidation Value
# 2. Market-Based: Market Cap and Comparable Multiples
# 3. Earning-Based: DCF and Earnings Multiples
# 
# Provide a triangulated valuation range, identify the most reliable method,
# and give investment recommendations based on the comprehensive analysis.
# """)

# agent.print_response("""
# Compare GreenFoods Inc. with Microsoft using Market-Based valuation methods.
# Use comparable multiples to assess relative valuation and identify which
# company appears more attractive from a valuation perspective.
# """)

# 5. SCENARIO ANALYSIS TESTS
# agent.print_response("""
# Perform scenario analysis for GreenFoods Inc. using the DCF tool:
# - High Growth Scenario: 8% growth rate, 7% WACC
# - Moderate Scenario: 5% growth rate, 10% WACC  
# - Recession Scenario: 2% growth rate, 12% WACC
# 
# Analyze how different economic conditions affect GreenFoods's valuation
# and provide risk-adjusted investment recommendations.
# """)

# 6. SECTOR-SPECIFIC TESTS
# agent.print_response("""
# Perform a sector-specific valuation analysis for a technology company.
# Use industry-appropriate multiples and discount rates, then compare
# the results with broader market benchmarks. Identify key value drivers
# and sector-specific risks that could impact valuation.
# """)

# if __name__ == "__main__":
#     user_input = input("Enter a company name and the valuation approach you want to use: ")
#     agent.print_response(user_input)