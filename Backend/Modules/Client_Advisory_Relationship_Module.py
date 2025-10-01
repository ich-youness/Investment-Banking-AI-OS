import os
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.knowledge import KnowledgeTools
from agno.tools.file import FileTools
from agno.tools.python import PythonTools
from agno.tools.pandas import PandasTools
from agno.tools.duckdb import DuckDbTools
from agno.tools.visualization import VisualizationTools
# from agno.tools.email import EmailTools  # May not be available in current version
from agno.tools.slack import SlackTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.mem0 import Mem0Tools
from agno.tools.csv_toolkit import CsvTools
from dotenv import load_dotenv
load_dotenv()


def create_Dialogue_agent():
    """
    Creates an AI agent specialized in client dialogue management,
    secure communication, and CRM integration.
    """
    return Agent(
        name="DialogueAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in client dialogue management, secure communication, and CRM integration.",
        
        instructions="""
        You are the Dialogue-Agent.
        Your purpose is to handle authenticated client communications and provide intelligent responses.
        Follow these rules:
        
        1. Handle authenticated Q&A:
            - Process client questions about deals, reports, and portfolio performance
            - Verify client identity and authorization levels
            - Provide accurate and timely responses
            - Maintain professional and helpful tone
        2. Use Retrieval-Augmented Generation (RAG):
            - Fetch factual responses from internal knowledge bases
            - Access reports, models, and pitchbooks securely
            - Provide context-aware answers based on client history
            - Cite sources and provide references when appropriate
        3. Escalate to human relationship managers:
            - Identify complex queries requiring human expertise
            - Transfer conversations with full context and history
            - Provide handover summaries and recommended actions
            - Maintain seamless client experience during transitions
        4. Log all interactions in CRM:
            - Record conversation history and outcomes
            - Track client preferences and communication patterns
            - Maintain audit trails for compliance
            - Enable relationship managers to access conversation context
        5. Apply data masking and privacy protection:
            - Redact PII and sensitive data from responses
            - Ensure compliance with data protection regulations
            - Mask confidential information appropriately
            - Maintain client privacy and security
        6. Provide canned workflows:
            - Schedule meetings and appointments
            - Process valuation requests
            - Handle report downloads and sharing
            - Manage document access and permissions
        """,
        
        markdown=True,
        
        tools=[
            KnowledgeTools(),          # RAG over reports, models, pitchbooks
            FileTools(),               # CRM Integration (conversation logging)
            PythonTools(),             # Policy Masking Engine (PII & sensitive data redaction)
            Mem0Tools(),               # Secure Chat/Voice Interface (authenticated client comms)
            DuckDbTools()              # Client data and conversation storage
        ],
    )


def create_Advisor_agent():
    """
    Creates an AI agent specialized in financial advisory services,
    strategic recommendations, and client relationship management.
    """
    return Agent(
        name="AdvisorAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in financial advisory services, strategic recommendations, and client relationship management.",
        
        instructions="""
        You are the Advisor-Agent.
        Your purpose is to provide tailored strategic and financial recommendations to clients.
        Follow these rules:
        
        1. Provide strategic and financial recommendations:
            - Analyze client needs and objectives
            - Recommend issuance timing and M&A targets
            - Suggest refinancing strategies and capital structure optimization
            - Provide sector-specific insights and market opportunities
        2. Use financial modeling engine:
            - Build DCF models for valuation analysis
            - Create comparable company analysis (comps)
            - Develop refinancing models and scenarios
            - Perform sensitivity analysis and stress testing
        3. Benchmark client metrics:
            - Compare client performance against peer groups
            - Identify gaps and opportunities for improvement
            - Highlight competitive advantages and weaknesses
            - Provide market positioning insights
        4. Rank potential actions:
            - Evaluate options by impact, risk, and feasibility
            - Use scoring algorithms for objective assessment
            - Consider client constraints and preferences
            - Provide clear rationale for recommendations
        5. Produce execution plans:
            - Create step-by-step implementation guides
            - Define timelines and milestones
            - Identify required resources and dependencies
            - Provide risk mitigation strategies
        6. Adapt to client preferences:
            - Consider risk appetite and timeline constraints
            - Customize recommendations based on client profile
            - Learn from feedback and outcomes
            - Maintain personalized advisory approach
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),             # Financial Modeling Engine (DCF, comps, refinancing models)
            PandasTools(),             # Benchmarking Dataset (peer group metrics, market comparables)
            ReasoningTools(),          # Ranking & Scoring Algorithms (expected value vs risk)
            DuckDbTools(),             # Preference Manager (risk appetite, timeline constraints)
            KnowledgeTools()           # Client profile and preference management
        ],
    )


def create_Report_Generator_agent():
    """
    Creates an AI agent specialized in report generation,
    document assembly, and stakeholder communication.
    """
    return Agent(
        name="ReportGeneratorAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in report generation, document assembly, and stakeholder communication.",
        
        instructions="""
        You are the Report-Generator-Agent.
        Your purpose is to assemble and deliver comprehensive reports for various stakeholders.
        Follow these rules:
        
        1. Assemble executive summaries and reports:
            - Create performance dashboards with key metrics
            - Generate risk metrics and commentary
            - Compile market analysis and insights
            - Produce client-specific reports and presentations
        2. Use document assembly engine:
            - Generate PDF, PPTX, and XLSX exports
            - Maintain consistent formatting and branding
            - Include charts, tables, and visualizations
            - Ensure professional presentation quality
        3. Create visualizations and dashboards:
            - Design performance charts and risk dashboards
            - Generate interactive visualizations
            - Create executive summary graphics
            - Develop client-specific visual content
        4. Manage scheduling and delivery:
            - Send reports via email and CRM integration
            - Schedule automated report generation
            - Handle delivery confirmations and read receipts
            - Manage distribution lists and permissions
        5. Personalize reporting by role:
            - Customize content for CFO, board, and investors
            - Adapt detail level and focus areas
            - Include role-specific insights and recommendations
            - Maintain appropriate confidentiality levels
        6. Track audit logs and version control:
            - Maintain report history and version tracking
            - Log delivery and access events
            - Support compliance and audit requirements
            - Enable report revision and update management
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),             # Document Assembly Engine (PDF, PPTX, XLSX exports)
            VisualizationTools(),      # Visualization Tools (performance charts, risk dashboards)
            SlackTools(),              # Scheduling & Delivery System (notifications, CRM integration)
            FileTools(),               # Audit Logging & Version Control (report history tracking)
            PandasTools()              # Data processing and report generation
        ],
    )


def create_Opportunity_Detector_agent():
    """
    Creates an AI agent specialized in opportunity detection,
    market monitoring, and client relationship enhancement.
    """
    return Agent(
        name="OpportunityDetectorAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in opportunity detection, market monitoring, and client relationship enhancement.",
        
        instructions="""
        You are the Opportunity-Detector-Agent.
        Your purpose is to continuously monitor and detect opportunities for clients.
        Follow these rules:
        
        1. Monitor market events and client profiles:
            - Track corporate events, market news, and funding rounds
            - Monitor client preferences, sector exposure, and deal history
            - Analyze market trends and emerging opportunities
            - Identify potential strategic partnerships and acquisitions
        2. Match and score opportunities:
            - Evaluate fundraising opportunities and timing
            - Assess acquisition targets and strategic fit
            - Score opportunities by fit, probability, and expected value
            - Consider client constraints and strategic objectives
        3. Link opportunities with playbooks:
            - Connect opportunities with recommended next steps
            - Provide execution strategies and timelines
            - Include market intelligence and competitive analysis
            - Suggest relationship building and outreach strategies
        4. Send real-time alerts and notifications:
            - Generate immediate alerts for high-priority opportunities
            - Create CRM tasks for relationship manager follow-up
            - Provide context and background information
            - Enable quick response and engagement
        5. Learn from feedback and outcomes:
            - Track opportunity success rates and outcomes
            - Refine scoring algorithms based on results
            - Improve precision of opportunity signals
            - Adapt to changing market conditions and client needs
        6. Support relationship management:
            - Provide talking points and conversation starters
            - Suggest meeting topics and agenda items
            - Track client engagement and response patterns
            - Enable proactive relationship building
        """,
        
        markdown=True,
        
        tools=[
            DuckDuckGoTools(),         # Market Event Feeds (corporate events, market news, funding rounds)
            DuckDbTools(),             # Client Profile Database (preferences, sector exposure, deal history)
            PythonTools(),             # Scoring Engine (fit, probability, expected value)
            FileTools(),               # CRM Integration (alerts, auto-task creation for RMs)
            KnowledgeTools(),          # Opportunity matching and analysis
            ReasoningTools()           # Opportunity evaluation and ranking
        ],
    )


# Create all agents
Dialogue_agent = create_Dialogue_agent()
Advisor_agent = create_Advisor_agent()
Report_Generator_agent = create_Report_Generator_agent()
Opportunity_Detector_agent = create_Opportunity_Detector_agent()

# Test prompts for each agent
dialogue_test_prompt = """
Handle a client inquiry about their portfolio performance:
- Client asks about Q3 performance and upcoming opportunities
- Provide RAG-based response from their portfolio reports
- Check for any sensitive data that needs masking
- Log the conversation in CRM for relationship manager follow-up
- Suggest scheduling a meeting to discuss in detail
"""

advisor_test_prompt = """
Provide strategic recommendations for a tech client:
- Client is considering a $500M acquisition in the fintech sector
- Analyze the target using DCF and comparable company analysis
- Benchmark against peer group metrics and market trends
- Rank the opportunity by impact, risk, and feasibility
- Create execution plan with timeline and next steps
"""

report_generator_test_prompt = """
Generate a quarterly performance report for a private equity client:
- Create executive summary with key performance metrics
- Include risk dashboard and market commentary
- Generate visualizations for portfolio performance
- Customize content for board-level audience
- Schedule delivery via email and track read receipts
"""

opportunity_detector_test_prompt = """
Detect opportunities for a healthcare client:
- Monitor recent funding rounds and M&A activity in healthcare
- Match opportunities against client's sector focus and deal history
- Score potential targets by strategic fit and probability
- Generate alerts for high-priority opportunities
- Create CRM tasks for relationship manager follow-up
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
    
    print("Testing Dialogue-Agent...")
    Dialogue_agent.print_response(dialogue_test_prompt, stream=True)
    
    print("\nTesting Advisor-Agent...")
    Advisor_agent.print_response(advisor_test_prompt, stream=True)
    
    print("\nTesting Report-Generator-Agent...")
    Report_Generator_agent.print_response(report_generator_test_prompt, stream=True)
    
    print("\nTesting Opportunity-Detector-Agent...")
    Opportunity_Detector_agent.print_response(opportunity_detector_test_prompt, stream=True)

# Uncomment to test individual agents
# Dialogue_agent.print_response(dialogue_test_prompt, stream=True)
# Advisor_agent.print_response(advisor_test_prompt, stream=True)
# Report_Generator_agent.print_response(report_generator_test_prompt, stream=True)
# Opportunity_Detector_agent.print_response(opportunity_detector_test_prompt, stream=True)

# Uncomment to test all agents at once
# test_agents()
