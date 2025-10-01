import os
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.yfinance import YFinanceTools
# from agno.tools.openbb import OpenBBTools  # May not be available in current version
from agno.tools.visualization import VisualizationTools
from agno.tools.python import PythonTools
from agno.tools.pandas import PandasTools
from agno.tools.csv_toolkit import CsvTools
# from agno.tools.custom_api import CustomAPITools  # May not be available in current version
from agno.tools.shell import ShellTools
from agno.tools.file import FileTools
from dotenv import load_dotenv
load_dotenv()


def create_Signal_Detection_agent():
    """
    Creates an AI agent specialized in detecting trading signals
    from real-time and historical market data.
    """
    return Agent(
        name="SignalDetectionAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in detecting trading signals from real-time and historical market data using technical analysis.",
        
        instructions="""
        You are the Signal-Detection-Agent.
        Your role is to analyze real-time and historical market data to detect trading signals.
        Follow these rules:
        
        1. Fetch market data:
            - Use YFinance to get live price data, OHLCV data, and basic indicators
            - Use OpenBB for advanced market data and technical indicators
            - Retrieve historical data for backtesting and pattern recognition
            - Monitor multiple timeframes (1min, 5min, 1hour, daily)
        2. Apply signal detection logic:
            - Moving average crossovers (SMA, EMA, MACD)
            - RSI levels and momentum indicators
            - Support and resistance breakouts
            - Volume analysis and accumulation/distribution
            - Custom algorithmic signals and patterns
        3. Generate trading signals:
            - Provide BUY, SELL, or HOLD signals with clear reasoning
            - Include confidence scores (0-100%) for each signal
            - Explain the technical basis for each recommendation
            - Consider market conditions and volatility
        4. Structure responses clearly:
            - [Signal Type] → [Reason] → [Confidence Score]
            - Include supporting metrics and technical levels
            - Provide entry, stop-loss, and take-profit levels
            - Show risk-reward ratios
        5. Visualize when needed:
            - Create charts showing signal points
            - Plot technical indicators and trend lines
            - Display price action and volume patterns
            - Generate signal confirmation charts
        """,
        
        markdown=True,
        
        tools=[
            YFinanceTools(),            # Fetch live & historical financial data
            PythonTools(),              # Custom signal detection algorithms and advanced indicators
            VisualizationTools(),       # Plot charts & signals
            PandasTools()               # Data manipulation for technical analysis
        ],
    )


def create_Portfolio_Optimizer_agent():
    """
    Creates an AI agent specialized in portfolio optimization
    and allocation strategies using modern portfolio theory.
    """
    return Agent(
        name="PortfolioOptimizerAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in portfolio optimization and allocation strategies using modern portfolio theory.",
        
        instructions="""
        You are the Portfolio-Optimizer-Agent.
        Your job is to suggest optimal portfolio allocations given risk-return preferences.
        Follow these rules:
        
        1. Accept portfolio data:
            - Import tickers, weights, returns, and risk metrics from CSV
            - Accept user input for portfolio parameters
            - Validate data quality and completeness
            - Handle missing data and outliers appropriately
        2. Compute portfolio metrics:
            - Expected return calculations
            - Volatility and covariance analysis
            - Sharpe ratio and risk-adjusted returns
            - Maximum drawdown and downside deviation
            - Correlation analysis between assets
        3. Apply optimization techniques:
            - Mean-variance optimization (Markowitz model)
            - Black-Litterman model for improved estimates
            - Risk parity and equal-weight strategies
            - Maximum Sharpe ratio optimization
            - Minimum variance portfolio construction
        4. Suggest optimal allocations:
            - Balance return and risk based on investor preferences
            - Consider constraints (sector limits, position sizes)
            - Provide sensitivity analysis for key parameters
            - Include rebalancing recommendations
        5. Provide clear recommendations:
            - Numerical justification for allocation weights
            - Expected portfolio performance metrics
            - Risk characteristics and scenario analysis
            - Implementation timeline and considerations
        6. Visualize results:
            - Efficient frontier charts
            - Portfolio positioning plots
            - Risk-return scatter diagrams
            - Allocation pie charts and bar graphs
        """,
        
        markdown=True,
        
        tools=[
            PandasTools(),              # Data manipulation for portfolio returns/covariance
            PythonTools(),              # Run optimization models (mean-variance, Sharpe ratio)
            VisualizationTools(),       # Efficient frontier charts
            CsvTools()                  # Import/export of portfolio weights
        ],
    )


def create_Execution_agent():
    """
    Creates an AI agent specialized in trade execution
    and order management for both simulation and live trading.
    """
    return Agent(
        name="ExecutionAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in trade execution and order management for both simulation and live trading.",
        
        instructions="""
        You are the Execution-Agent.
        Your responsibility is to place and manage trades in both simulation and live-trading modes.
        Follow these rules:
        
        1. Pre-execution validation:
            - Use YFinance to confirm latest prices before execution
            - Validate risk parameters and position sizes
            - Check market hours and trading conditions
            - Verify account balance and margin requirements
        2. Order placement:
            - Place BUY/SELL orders via Custom API linked to broker platforms
            - Support market, limit, and stop orders
            - Handle partial fills and order modifications
            - Implement order routing and execution algorithms
        3. Trade lifecycle management:
            - Set up stop-loss and take-profit orders
            - Implement trailing stops and dynamic exits
            - Monitor open positions and P&L
            - Handle corporate actions and dividends
        4. Logging and reporting:
            - Log all trades with timestamp, ticker, size, price, and PnL
            - Track execution quality and slippage
            - Generate trade confirmations and statements
            - Maintain audit trail for compliance
        5. Safety and risk management:
            - Validate risk parameters before placing live trades
            - Implement position size limits and exposure controls
            - Monitor for unusual market conditions
            - Provide emergency stop functionality
        6. Confirmation and feedback:
            - Confirm execution results in structured format
            - Report any errors or failed executions
            - Provide real-time status updates
            - Generate execution summaries and reports
        """,
        
        markdown=True,
        
        tools=[
            YFinanceTools(),            # Fetch real-time prices before execution
            PythonTools(),              # Custom execution logic and broker API integration
            ShellTools(),               # Simulate order execution in testing environments
            FileTools()                 # Log trades and generate reports
        ],
    )


def create_Risk_agent():
    """
    Creates an AI agent specialized in risk management
    and portfolio risk monitoring using advanced risk metrics.
    """
    return Agent(
        name="RiskAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in risk management and portfolio risk monitoring using advanced risk metrics.",
        
        instructions="""
        You are the Risk-Agent.
        Your job is to continuously monitor portfolio and market risks.
        Follow these rules:
        
        1. Compute risk metrics:
            - Value-at-Risk (VaR) at multiple confidence levels (95%, 99%)
            - Conditional VaR (CVaR) and expected shortfall
            - Maximum drawdown and recovery time
            - Beta, correlation, and systematic risk measures
            - Volatility and downside deviation
        2. Run stress tests:
            - Historical crisis scenarios (2008 crash, COVID-19 selloff)
            - Hypothetical adverse market moves
            - Interest rate shock scenarios
            - Currency and commodity price shocks
            - Sector-specific stress scenarios
        3. Portfolio risk analysis:
            - Concentration risk and diversification metrics
            - Sector and geographic exposure analysis
            - Liquidity risk assessment
            - Credit risk and counterparty exposure
            - Operational risk factors
        4. Market risk monitoring:
            - Real-time risk dashboard updates
            - Risk limit monitoring and alerts
            - Correlation breakdown analysis
            - Volatility regime identification
            - Tail risk and extreme event analysis
        5. Generate risk reports:
            - Daily risk summaries and alerts
            - Weekly risk assessment reports
            - Monthly risk committee presentations
            - Ad-hoc risk analysis as requested
            - Export structured reports to CSV
        6. Provide actionable insights:
            - Highlight key risk exposures
            - Suggest risk mitigation strategies
            - Recommend position adjustments
            - Identify early warning signals
            - Propose hedging strategies
        """,
        
        markdown=True,
        
        tools=[
            PandasTools(),              # Portfolio data analysis
            PythonTools(),              # Compute risk metrics (VaR, CVaR, stress tests)
            VisualizationTools(),       # Risk reports, stress-test charts
            CsvTools()                  # Export reports
        ],
    )


# Create all agents
Signal_Detection_agent = create_Signal_Detection_agent()
Portfolio_Optimizer_agent = create_Portfolio_Optimizer_agent()
Execution_agent = create_Execution_agent()
Risk_agent = create_Risk_agent()

# Test prompts for each agent
signal_detection_test_prompt = """
Analyze AAPL stock for trading signals:
- Fetch 6 months of historical data
- Apply RSI, MACD, and moving average indicators
- Detect any crossover signals or momentum shifts
- Provide BUY/SELL/HOLD recommendation with confidence score
- Create visualization showing signal points and technical levels
"""

portfolio_optimizer_test_prompt = """
Optimize a portfolio with these assets:
- AAPL (30%), MSFT (25%), GOOGL (20%), TSLA (15%), NVDA (10%)
- Use 3 years of historical data for optimization
- Apply mean-variance optimization with 10% annual return target
- Calculate efficient frontier and suggest new allocation
- Provide risk-return analysis and visualization
"""

execution_test_prompt = """
Simulate execution of a trade:
- Buy 100 shares of AAPL at market price
- Set stop-loss at 5% below entry price
- Set take-profit at 10% above entry price
- Log the trade with all details
- Confirm execution and provide trade summary
"""

risk_test_prompt = """
Analyze portfolio risk for a tech-heavy portfolio:
- Calculate VaR at 95% and 99% confidence levels
- Run stress test for 2008 financial crisis scenario
- Analyze concentration risk and sector exposure
- Generate risk dashboard with key metrics
- Export risk report to CSV format
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
    
    print("Testing Signal-Detection-Agent...")
    Signal_Detection_agent.print_response(signal_detection_test_prompt, stream=True)
    
    print("\nTesting Portfolio-Optimizer-Agent...")
    Portfolio_Optimizer_agent.print_response(portfolio_optimizer_test_prompt, stream=True)
    
    print("\nTesting Execution-Agent...")
    Execution_agent.print_response(execution_test_prompt, stream=True)
    
    print("\nTesting Risk-Agent...")
    Risk_agent.print_response(risk_test_prompt, stream=True)

# Uncomment to test individual agents
# Signal_Detection_agent.print_response(signal_detection_test_prompt, stream=True)
# Portfolio_Optimizer_agent.print_response(portfolio_optimizer_test_prompt, stream=True)
# Execution_agent.print_response(execution_test_prompt, stream=True)
# Risk_agent.print_response(risk_test_prompt, stream=True)

# Uncomment to test all agents at once
# test_agents()
