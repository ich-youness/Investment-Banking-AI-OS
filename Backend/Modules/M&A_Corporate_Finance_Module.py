import os
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.pandas import PandasTools
from agno.tools.duckdb import DuckDbTools
from agno.tools.visualization import VisualizationTools
from agno.tools.knowledge import KnowledgeTools
from agno.tools.file import FileTools
from agno.tools.python import PythonTools
from agno.tools.reasoning import ReasoningTools
# from agno.tools.financial_datasets import FinancialDatasetsTools
from agno.tools.opencv import OpenCVTools
# from agno.tools.powerpoint import PowerPointTools  # May not be available in current version
from dotenv import load_dotenv
load_dotenv()


def create_MA_Analyst_agent():
    """
    Creates an AI agent specialized in M&A analysis, valuation modeling,
    and financial analysis for mergers and acquisitions.
    """
    return Agent(
        name="MAAnalystAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in M&A analysis, valuation modeling, and financial analysis for mergers and acquisitions.",
        
        instructions="""
        You are the M&A-Analyst-Agent.
        Your purpose is to build comprehensive valuation models and perform M&A analysis.
        Follow these rules:
        
        1. Build valuation models:
            - Discounted Cash Flow (DCF) models with terminal value calculations
            - Trading comparables analysis using market multiples
            - Precedent transactions analysis for M&A valuations
            - Sum-of-the-parts valuation for diversified companies
        2. Calculate synergies for mergers and acquisitions:
            - Revenue synergies (cross-selling, market expansion)
            - Cost synergies (operational efficiency, overhead reduction)
            - Financial synergies (tax benefits, capital structure optimization)
            - Quantify synergy value and implementation timeline
        3. Perform sensitivity analysis:
            - Test growth rate assumptions (revenue, EBITDA, FCF)
            - Analyze discount rate sensitivity (WACC, terminal growth)
            - Evaluate multiple sensitivity (P/E, EV/EBITDA, EV/Sales)
            - Create tornado charts and scenario matrices
        4. Generate clear visualizations:
            - Valuation ranges and waterfall charts
            - Sensitivity tables and heat maps
            - Comparable company analysis charts
            - Synergy realization timelines
        5. Deliver structured outputs:
            - provide valuation models in a structured format
            - provide reports with charts and analysis
            - Provide banker-ready presentation materials
        """,
        
        markdown=True,
        
        tools=[
            PandasTools(),           # Financial modeling & data wrangling
            DuckDbTools(),           # SQL queries for financial data
            VisualizationTools(),    # Charts for valuation outputs
            # KnowledgeTools(),        # Apply finance domain knowledge
            FileTools()              # Export valuation models
        ],
    )


def create_Due_Diligence_agent():
    """
    Creates an AI agent specialized in due diligence analysis,
    risk assessment, and document review for M&A transactions.
    """
    return Agent(
        name="DueDiligenceAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in due diligence analysis, risk assessment, and document review for M&A transactions.",
        
        instructions="""
        You are the Due-Diligence-Agent.
        Your purpose is to conduct comprehensive due diligence analysis and risk assessment.
        Follow these rules:
        
        1. Review contracts and legal documents:
            - Analyze merger agreements and acquisition contracts
            - Review employment contracts and non-compete clauses
            - Examine intellectual property agreements and licenses
            - Assess regulatory compliance and permits
        2. Analyze financial statements and compliance:
            - Review audited financial statements and footnotes
            - Analyze cash flow statements and working capital
            - Examine debt schedules and credit agreements
            - Assess accounting policies and revenue recognition
        3. Identify risks and liabilities:
            - Flag potential lawsuits and litigation risks
            - Identify regulatory non-compliance issues
            - Assess debt covenants and financial obligations
            - Evaluate environmental and operational risks
        4. Flag red flags and critical issues:
            - Overleveraging and debt capacity concerns
            - Management conflicts of interest
            - Regulatory violations and penalties
            - Market concentration and customer dependency
        5. Produce structured due diligence reports:
            - Create comprehensive risk assessment checklists
            - Assign risk severity scores (High/Medium/Low)
            - Generate executive summaries with key findings
            - Provide recommendations for risk mitigation
        """,
        
        markdown=True,
        
        tools=[
            # KnowledgeTools(),        # Legal & financial reasoning
            ReasoningTools(),        # Risk assessment logic
            OpenCVTools(),           # OCR for document processing
            PythonTools(),           # NLP for text analysis
            FileTools()              # Document ingestion & contract review
        ],
    )


def create_Valuation_Scenario_agent():
    """
    Creates an AI agent specialized in scenario analysis and stress testing
    for M&A valuations under different macroeconomic conditions.
    """
    return Agent(
        name="ValuationScenarioAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in scenario analysis, stress testing, and Monte Carlo simulations for M&A valuations.",
        
        instructions="""
        You are the Valuation-Scenario-Agent.
        Your purpose is to simulate multiple valuation outcomes under different scenarios.
        Follow these rules:
        
        1. Simulate multiple valuation outcomes:
            - Base case: Current market conditions and trends
            - Bull case: Optimistic growth and favorable conditions
            - Bear case: Recessionary and challenging market conditions
            - Stress case: Extreme adverse scenarios and black swan events
        2. Test against macroeconomic scenarios:
            - GDP growth variations (recession, recovery, expansion)
            - Inflation rate impacts (deflation, normal, hyperinflation)
            - Interest rate changes (rate cuts, hikes, volatility)
            - Currency fluctuations and exchange rate impacts
        3. Run Monte Carlo simulations:
            - Generate probabilistic valuation ranges
            - Model uncertainty in key assumptions
            - Create probability distributions for outcomes
            - Calculate confidence intervals and percentiles
        4. Stress-test key assumptions:
            - Revenue growth rate sensitivity
            - Margin compression scenarios
            - Working capital requirement changes
            - Capital expenditure variations
        5. Output scenario dashboards:
            - Compare base, bull, and bear case valuations
            - Display probability distributions and ranges
            - Show sensitivity analysis charts
            - Generate executive summary reports
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),               # Run scenario simulations
            PandasTools(),               # Data-driven modeling
            DuckDbTools(),               # Query financial datasets
            VisualizationTools(),        # Scenario comparisons
            # FinancialDatasetsTools()     # Macro assumptions: GDP, inflation, rates
        ],
    )


def create_Pitchbook_agent():
    """
    Creates an AI agent specialized in generating investment banking
    pitchbooks and client presentation materials.
    """
    return Agent(
        name="PitchbookAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in generating investment banking pitchbooks and client presentation materials.",
        
        instructions="""
        You are the Pitchbook-Agent.
        Your purpose is to automatically generate draft pitchbooks for client presentations.
        Follow these rules:
        
        1. Generate draft pitchbooks:
            - Create executive summary and deal overview
            - Include company profile and business description
            - Add market overview and industry analysis
            - Present valuation summary and methodology
        2. Include valuation outputs:
            - DCF valuation ranges and assumptions
            - Trading comparables analysis tables
            - Precedent transactions summary
            - Sum-of-the-parts valuation breakdown
        3. Create market overviews:
            - Industry trends and growth drivers
            - Competitive landscape analysis
            - Market size and opportunity assessment
            - Regulatory environment overview
        4. Produce comparable tables:
            - Trading comparables with key metrics
            - Precedent transactions with deal multiples
            - Financial performance comparisons
            - Valuation methodology summaries
        5. Customize pitchbooks:
            - Adapt content per client and sector
            - Include deal-specific rationale and benefits
            - Align with investment banking standards
            - Export as PowerPoint or PDF formats
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),           # Auto-generate slides with charts (using python-pptx)
            VisualizationTools(),    # Graphs, charts, timelines
            # KnowledgeTools(),        # Summarize findings in banker-style narratives
            FileTools()              # Export presentations as PPTX or PDF
        ],
    )


# Create all agents
MA_Analyst_agent = create_MA_Analyst_agent()
Due_Diligence_agent = create_Due_Diligence_agent()
Valuation_Scenario_agent = create_Valuation_Scenario_agent()
Pitchbook_agent = create_Pitchbook_agent()

# Test prompts for each agent
ma_analyst_test_prompt = """
Build a DCF valuation model for Company CIH:
- Project 5-year cash flows with 8% revenue growth
- Calculate terminal value using 3% terminal growth rate
- Use 10% WACC as discount rate
- Perform sensitivity analysis on growth rates and WACC
- Generate valuation range and visualization charts
"""

due_diligence_test_prompt = """
Conduct due diligence on the acquisition target:
- Review the provided financial statements and contracts
- Identify key risks and liabilities
- Assess debt covenants and compliance issues
- Flag any red flags or critical concerns
- Generate a structured risk assessment report
"""

scenario_test_prompt = """
Run scenario analysis for the M&A valuation:
- Create base, bull, and bear case scenarios
- Test sensitivity to GDP growth and interest rates
- Run Monte Carlo simulation with 1000 iterations
- Generate probability distributions and confidence intervals
- Create scenario comparison dashboard
"""

pitchbook_test_prompt = """
Generate a pitchbook for the M&A transaction:
- Create executive summary and deal overview
- Include company profile and market analysis
- Add valuation summary with DCF and comparables
- Generate trading comparables and precedent transactions tables
- Export as PowerPoint presentation
"""

# Uncomment to test individual agents
# MA_Analyst_agent.print_response(ma_analyst_test_prompt, stream=True)
# Due_Diligence_agent.print_response(due_diligence_test_prompt, stream=True)
# Valuation_Scenario_agent.print_response(scenario_test_prompt, stream=True)
# Pitchbook_agent.print_response(pitchbook_test_prompt, stream=True)

# Uncomment to test all agents at once
# test_agents()
