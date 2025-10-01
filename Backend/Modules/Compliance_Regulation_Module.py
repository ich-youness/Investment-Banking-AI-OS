import os
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.opencv import OpenCVTools
from agno.tools.neo4j import Neo4jTools
from agno.tools.python import PythonTools
from agno.tools.pandas import PandasTools
from agno.tools.file import FileTools
from agno.tools.knowledge import KnowledgeTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.visualization import VisualizationTools
from agno.tools.duckdb import DuckDbTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.website import WebsiteTools
from dotenv import load_dotenv
load_dotenv()


def create_KYC_agent():
    """
    Creates an AI agent specialized in Know Your Customer (KYC) processes,
    identity verification, and beneficial ownership mapping.
    """
    return Agent(
        name="KYCAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in Know Your Customer (KYC) processes, identity verification, and beneficial ownership mapping.",
        
        instructions="""
        You are the KYC-Agent.
        Your purpose is to parse identity documents, verify client information, and map corporate structures.
        Follow these rules:
        
        1. Parse identity documents:
            - Extract data from passports, driver's licenses, and national IDs
            - Process corporate filings and registration documents
            - Verify document authenticity and detect forgeries
            - Extract key information (name, DOB, address, ID numbers)
        2. Verify client information:
            - Cross-reference extracted data with external databases
            - Validate identity against government records
            - Check for duplicate or suspicious identities
            - Verify address and contact information
        3. Build beneficial ownership graphs:
            - Map complex corporate structures and ownership chains
            - Identify ultimate beneficial owners (UBOs)
            - Track ownership percentages and control relationships
            - Detect shell companies and nominee structures
        4. Run KYC checks and risk scoring:
            - Apply rule-based risk scoring algorithms
            - Integrate ML models for enhanced risk assessment
            - Flag cases requiring enhanced due diligence (EDD)
            - Generate risk profiles and recommendations
        5. Maintain KYC records:
            - Store verified information in secure databases
            - Set up periodic re-screening workflows
            - Track document expiration dates
            - Maintain audit trails for compliance
        6. Integrate with compliance teams:
            - Route high-risk cases for manual review
            - Provide case management system integration
            - Generate reports for compliance officers
            - Support escalation workflows
        """,
        
        markdown=True,
        
        tools=[
            OpenCVTools(),             # OCR & Document Parsers (Passport, ID, Corporate Filings)
            Neo4jTools(),              # Graph Databases for ownership mapping
            PythonTools(),             # Risk Scoring Engine (rule-based + ML models)
            FileTools(),               # Case Management System Integration
            KnowledgeTools()           # Document verification and validation
        ],
    )


def create_AML_agent():
    """
    Creates an AI agent specialized in Anti-Money Laundering (AML) monitoring,
    suspicious activity detection, and investigation support.
    """
    return Agent(
        name="AMLAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in Anti-Money Laundering (AML) monitoring, suspicious activity detection, and investigation support.",
        
        instructions="""
        You are the AML-Agent.
        Your purpose is to monitor transactions for money-laundering activities and support investigations.
        Follow these rules:
        
        1. Monitor client transactions:
            - Process real-time and batch transaction data
            - Analyze transaction patterns and behaviors
            - Track cross-border and high-value transactions
            - Monitor for unusual timing and frequency patterns
        2. Detect suspicious activities:
            - Apply rule-based detection for known typologies
            - Use ML models for anomaly detection
            - Identify structuring and layering patterns
            - Detect suspicious behavior indicators
        3. Generate and prioritize alerts:
            - Create Suspicious Activity Reports (SARs)
            - Apply risk scoring to prioritize alerts
            - Categorize alerts by typology and severity
            - Generate alert summaries and recommendations
        4. Link related alerts into cases:
            - Identify connections between related alerts
            - Build investigation timelines and narratives
            - Map entity relationships and networks
            - Provide analyst tools for case investigation
        5. Support investigation workflows:
            - Generate investigation dashboards
            - Provide entity linking and timeline visualization
            - Support compliance team workflows
            - Enable case collaboration and documentation
        6. Export regulator-ready reports:
            - Generate SARs for regulatory submission
            - Create compliance reports and summaries
            - Maintain audit trails for regulatory review
            - Support regulatory examination processes
        """,
        
        markdown=True,
        
        tools=[
            DuckDbTools(),             # Transaction Monitoring Systems (real-time & batch)
            PythonTools(),             # Machine Learning Models (anomaly detection, suspicious behavior)
            ReasoningTools(),          # Rule Engines (structuring, layering, typology patterns)
            VisualizationTools(),      # Investigation Dashboards (entity linking, timeline visualization)
            PandasTools()              # Data analysis and reporting
        ],
    )


def create_Sanction_Screener_agent():
    """
    Creates an AI agent specialized in sanction screening,
    blacklist monitoring, and prohibited entity detection.
    """
    return Agent(
        name="SanctionScreenerAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in sanction screening, blacklist monitoring, and prohibited entity detection.",
        
        instructions="""
        You are the Sanction-Screener-Agent.
        Your purpose is to screen counterparties against global sanction lists and prevent prohibited activities.
        Follow these rules:
        
        1. Maintain global sanction databases:
            - Continuously update OFAC, UN, EU, and domestic sanction lists
            - Monitor regulatory updates and changes
            - Integrate multiple data sources and formats
            - Ensure data quality and completeness
        2. Screen counterparties and entities:
            - Apply fuzzy-matching algorithms to reduce false positives
            - Use alias resolution and name variations
            - Check against multiple sanction lists simultaneously
            - Support batch and real-time screening processes
        3. Escalate high-risk matches:
            - Automatically flag potential matches for review
            - Apply confidence scoring to match results
            - Route high-risk matches to compliance teams
            - Implement quarantine systems for blocked entities
        4. Block prohibited activities:
            - Prevent transactions with sanctioned entities
            - Implement real-time blocking mechanisms
            - Support manual override processes with approval
            - Maintain blocking decision audit trails
        5. Provide provenance logging:
            - Log all screening decisions and results
            - Maintain audit trails for regulatory reporting
            - Track screening history and changes
            - Support regulatory examination processes
        6. Integrate with workflows:
            - Connect with onboarding processes
            - Integrate with transaction monitoring
            - Support ongoing monitoring and re-screening
            - Enable exception handling and appeals
        """,
        
        markdown=True,
        
        tools=[
            DuckDbTools(),             # Sanction Databases (OFAC, UN, EU, Domestic Lists)
            PythonTools(),             # Fuzzy Matching & Alias Resolution Algorithms
            FileTools(),               # Case Escalation & Quarantine System
            KnowledgeTools(),          # Logging & Audit Trail Framework
            PandasTools()              # Data processing and analysis
        ],
    )


def create_Regulation_agent():
    """
    Creates an AI agent specialized in regulatory monitoring,
    compliance mapping, and policy management.
    """
    return Agent(
        name="RegulationAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in regulatory monitoring, compliance mapping, and policy management.",
        
        instructions="""
        You are the Regulation-Agent.
        Your purpose is to monitor regulatory changes, map compliance requirements, and support policy updates.
        Follow these rules:
        
        1. Parse regulatory texts:
            - Monitor regulatory feeds and official publications
            - Extract laws, guidelines, and compliance bulletins
            - Process regulatory updates and amendments
            - Support multiple jurisdictions and languages
        2. Extract compliance requirements:
            - Use NLP models for clause extraction
            - Interpret legal text and requirements
            - Identify applicable rules and obligations
            - Categorize requirements by business function
        3. Map regulations to internal policies:
            - Map external rules to internal checklists
            - Update policy frameworks and procedures
            - Identify gaps and compliance requirements
            - Support cross-border compliance implications
        4. Generate alerts and notifications:
            - Push alerts when new rules affect workflows
            - Notify compliance officers of critical changes
            - Prioritize updates by impact and urgency
            - Support subscription-based alerting
        5. Support jurisdiction-specific compliance:
            - Handle multi-jurisdictional requirements
            - Manage conflicting regulatory obligations
            - Support cross-border compliance frameworks
            - Enable regional compliance variations
        6. Maintain audit trails:
            - Track regulatory interpretations and updates
            - Document policy change decisions
            - Support regulatory examination processes
            - Generate compliance reporting and summaries
        """,
        
        markdown=True,
        
        tools=[
            DuckDuckGoTools(),         # Regulatory Feed Parsers (laws, guidelines, compliance bulletins)
            WebsiteTools(),            # Web scraping for regulatory content
            PythonTools(),             # NLP Models (clause extraction, legal text interpretation)
            KnowledgeTools(),          # Policy Mapping Engine (map external rules → internal policies)
            FileTools(),               # Alerting System (change notifications to compliance officers)
            ReasoningTools()           # Legal text analysis and interpretation
        ],
    )


# Create all agents
KYC_agent = create_KYC_agent()
AML_agent = create_AML_agent()
Sanction_Screener_agent = create_Sanction_Screener_agent()
Regulation_agent = create_Regulation_agent()

# Test prompts for each agent
kyc_test_prompt = """
Process KYC for a new corporate client:
- Extract information from uploaded passport and corporate registration documents
- Map the corporate ownership structure and identify beneficial owners
- Run risk scoring and determine if enhanced due diligence is required
- Generate KYC report with recommendations
- Set up periodic re-screening workflow
"""

aml_test_prompt = """
Analyze suspicious transaction patterns:
- Monitor recent transactions for structuring and layering patterns
- Apply ML models to detect anomalous behavior
- Generate SARs for high-risk transactions
- Link related alerts into investigation cases
- Create investigation dashboard with timeline visualization
"""

sanction_test_prompt = """
Screen counterparties against sanction lists:
- Update global sanction databases (OFAC, UN, EU)
- Screen new client against all applicable lists
- Apply fuzzy matching to reduce false positives
- Escalate high-risk matches for manual review
- Generate screening report with audit trail
"""

regulation_test_prompt = """
Monitor regulatory changes:
- Parse new regulatory texts and extract compliance requirements
- Map new rules to internal policies and procedures
- Identify affected business functions and workflows
- Generate alerts for compliance officers
- Update compliance checklists and documentation
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
    
    print("Testing KYC-Agent...")
    KYC_agent.print_response(kyc_test_prompt, stream=True)
    
    print("\nTesting AML-Agent...")
    AML_agent.print_response(aml_test_prompt, stream=True)
    
    print("\nTesting Sanction-Screener-Agent...")
    Sanction_Screener_agent.print_response(sanction_test_prompt, stream=True)
    
    print("\nTesting Regulation-Agent...")
    Regulation_agent.print_response(regulation_test_prompt, stream=True)

# Uncomment to test individual agents
# KYC_agent.print_response(kyc_test_prompt, stream=True)
# AML_agent.print_response(aml_test_prompt, stream=True)
# Sanction_Screener_agent.print_response(sanction_test_prompt, stream=True)
# Regulation_agent.print_response(regulation_test_prompt, stream=True)

# Uncomment to test all agents at once
# test_agents()
