import os
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.pandas import PandasTools
from agno.tools.duckdb import DuckDbTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.financial_datasets import FinancialDatasetsTools
from agno.tools.visualization import VisualizationTools
from agno.tools.file import FileTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.exa import ExaTools
from agno.tools.knowledge import KnowledgeTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.python import PythonTools
from agno.tools.postgres import PostgresTools
from dotenv import load_dotenv
load_dotenv()


def create_Capital_Markets_agent():
    """
    Creates an AI agent specialized in capital markets operations,
    deal structuring, and pricing for IPOs, bonds, and equity offerings.
    """
    return Agent(
        name="CapitalMarketsAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in capital markets operations, deal structuring, and pricing for IPOs, bonds, and equity offerings.",
        
        instructions="""
        You are the Capital-Markets-Agent.
        Your purpose is to design deal structures and calculate pricing for capital markets transactions.
        Follow these rules:
        
        1. Design deal structures:
            - IPO structures with primary and secondary offerings
            - Bond offerings with various maturities and coupon structures
            - Equity offerings including follow-ons and rights issues
            - Convertible bonds and hybrid instruments
        2. Calculate offering price ranges:
            - Use comparable company analysis for IPOs
            - Apply bookrunner benchmarks and market multiples
            - Consider sector-specific valuation metrics
            - Factor in market conditions and investor appetite
        3. Model financial metrics:
            - Cost of capital calculations (WACC, cost of equity)
            - Coupon rate determination for bonds
            - Dilution effects for equity offerings
            - Yield curve analysis for fixed income
        4. Simulate deal structures:
            - Test different demand scenarios (high, medium, low)
            - Model pricing under various market conditions
            - Analyze impact of deal size on pricing
            - Consider regulatory and market constraints
        5. Output structured reports:
            - Generate term sheets with key deal terms
            - Create pricing models and sensitivity analysis
            - Provide internal review materials
            - Export Excel models for further analysis
        """,
        
        markdown=True,
        
        tools=[
            PandasTools(),               # Financial modeling & pricing models
            DuckDbTools(),               # SQL queries for financial data
            YFinanceTools(),             # Market comparables, benchmarks
            FinancialDatasetsTools(),    # Financial market data
            VisualizationTools(),        # Deal structures, yield curves
            FileTools()                  # Term sheets, pricing models export
        ],
    )


def create_Investor_Sentiment_agent():
    """
    Creates an AI agent specialized in analyzing investor sentiment
    from various sources including news, social media, and research reports.
    """
    return Agent(
        name="InvestorSentimentAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in analyzing investor sentiment from news, social media, and research reports.",
        
        instructions="""
        You are the Investor-Sentiment-Agent.
        Your purpose is to analyze market sentiment and investor mood from various data sources.
        Follow these rules:
        
        1. Scrape and analyze market sentiment:
            - Monitor financial news from major outlets (Reuters, Bloomberg, CNBC)
            - Track social media sentiment (Twitter, LinkedIn, Reddit finance communities)
            - Analyze research reports from investment banks and analysts
            - Monitor earnings calls and management commentary
        2. Score sentiment toward specific targets:
            - Companies (individual stock sentiment)
            - Sectors (technology, healthcare, energy, etc.)
            - Asset classes (equities, bonds, commodities)
            - Market themes (ESG, AI, inflation, etc.)
        3. Correlate sentiment with historical data:
            - Compare sentiment scores with stock price movements
            - Analyze correlation with trading volumes
            - Track sentiment leading indicators for market direction
            - Identify sentiment-driven investment opportunities
        4. Deliver sentiment insights:
            - Create sentiment dashboards with trend analysis
            - Generate alerts for significant sentiment shifts
            - Provide sentiment scores for specific companies/sectors
            - Anticipate IPO/bond reception based on sentiment
        5. Support capital markets decisions:
            - Help time IPOs and bond offerings
            - Assess market receptiveness to new issues
            - Identify potential investor concerns or red flags
            - Provide sentiment context for pricing decisions
        """,
        
        markdown=True,
        
        tools=[
            DuckDuckGoTools(),           # Financial news and web data
            ExaTools(),                  # Advanced web search and content analysis
            KnowledgeTools(),            # Sentiment scoring logic
            ReasoningTools(),            # Interpret investor mood from text data
            VisualizationTools()        # Trend dashboards
        ],
    )


def create_Bookbuilding_agent():
    """
    Creates an AI agent specialized in bookbuilding simulations,
    allocation strategies, and demand modeling for capital markets transactions.
    """
    return Agent(
        name="BookbuildingAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in bookbuilding simulations, allocation strategies, and demand modeling for capital markets transactions.",
        
        instructions="""
        You are the Bookbuilding-Agent.
        Your purpose is to simulate investor demand and optimize allocation strategies for capital markets transactions.
        Follow these rules:
        
        1. Simulate investor demand:
            - Model demand curves for IPOs and bond offerings
            - Simulate different investor types (institutional, retail, strategic)
            - Account for market conditions and timing factors
            - Consider sector-specific demand patterns
        2. Model allocation strategies:
            - Pro-rata allocation based on order size
            - Discretionary allocation considering investor quality
            - Tiered allocation with different rules per investor tier
            - Hybrid approaches combining multiple strategies
        3. Optimize allocations:
            - Maximize investor satisfaction and long-term relationships
            - Balance issuer proceeds with market stability
            - Consider aftermarket performance implications
            - Account for regulatory requirements and constraints
        4. Analyze demand vs. price relationships:
            - Create demand curves at different price points
            - Model price elasticity and sensitivity
            - Test pricing strategies under various scenarios
            - Optimize pricing for maximum proceeds
        5. Produce allocation reports:
            - Generate allocation heatmaps by investor type
            - Create demand vs. price curve visualizations
            - Provide allocation strategy recommendations
            - Export structured reports for syndicate desks
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),               # Auction & allocation simulations
            PandasTools(),               # Demand curve modeling
            VisualizationTools(),        # Allocation heatmaps, demand curves
            PostgresTools()              # Store simulated investor demand datasets
        ],
    )


# Create all agents
Capital_Markets_agent = create_Capital_Markets_agent()
Investor_Sentiment_agent = create_Investor_Sentiment_agent()
Bookbuilding_agent = create_Bookbuilding_agent()

# Test prompts for each agent
capital_markets_test_prompt = """
Design a deal structure for a tech company IPO:
- Company: TechCorp, $500M revenue, 15% growth rate
- Seeking to raise $200M in primary offering
- Use comparable tech companies for pricing
- Calculate offering price range and dilution effects
- Generate term sheet and pricing model
"""

sentiment_test_prompt = """
Analyze investor sentiment for the technology sector:
- Scrape recent news and social media mentions
- Score sentiment for major tech companies (Apple, Microsoft, Google)
- Identify key themes driving sentiment (AI, regulation, earnings)
- Create sentiment dashboard with trend analysis
- Assess market receptiveness for tech IPOs
"""

bookbuilding_test_prompt = """
Simulate bookbuilding for a $100M bond offering:
- Model demand from institutional and retail investors
- Test different allocation strategies (pro-rata vs discretionary)
- Create demand vs. price curves at various coupon rates
- Optimize allocation to maximize proceeds and investor satisfaction
- Generate allocation heatmap and strategy recommendations
"""

def test_agents():
    """
    Test function to run all agents with their respective test prompts.
    Make sure XAI_API_KEY is set before calling this function.
    """
    if not os.getenv("XAI_API_KEY"):
        print("ERROR: XAI_API_KEY environment variable not set!")
        print("Please set it in your .env file or environment variables")
        return
    
    print("Testing Capital-Markets-Agent...")
    Capital_Markets_agent.print_response(capital_markets_test_prompt, stream=True)
    
    print("\nTesting Investor-Sentiment-Agent...")
    Investor_Sentiment_agent.print_response(sentiment_test_prompt, stream=True)
    
    print("\nTesting Bookbuilding-Agent...")
    Bookbuilding_agent.print_response(bookbuilding_test_prompt, stream=True)

# Uncomment to test individual agents
# Capital_Markets_agent.print_response(capital_markets_test_prompt, stream=True)
# Investor_Sentiment_agent.print_response(sentiment_test_prompt, stream=True)
# Bookbuilding_agent.print_response(bookbuilding_test_prompt, stream=True)

# Uncomment to test all agents at once
# test_agents()
