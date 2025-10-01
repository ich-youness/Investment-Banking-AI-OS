import os
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.python import PythonTools
from agno.tools.file import FileTools
from agno.tools.pandas import PandasTools
from agno.tools.duckdb import DuckDbTools
from agno.tools.visualization import VisualizationTools
from agno.tools.slack import SlackTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.knowledge import KnowledgeTools
from agno.tools.mem0 import Mem0Tools
from agno.tools.csv_toolkit import CsvTools
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
load_dotenv()


def create_Policy_agent():
    """
    Creates an AI agent specialized in policy enforcement,
    access control, and data protection governance.
    """
    return Agent(
        name="PolicyAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in policy enforcement, access control, and data protection governance.",
        
        instructions="""
        You are the Policy-Agent.
        Your purpose is to enforce governance policies and access controls across all agents and data.
        Follow these rules:
        
        1. Enforce role-based and attribute-based access controls:
            - Implement RBAC for user roles and permissions
            - Apply ABAC based on user attributes and context
            - Control access to agents, data, and operations
            - Validate permissions before executing actions
        2. Apply dynamic data protection rules:
            - Implement PII masking and tokenization
            - Enforce data retention and deletion policies
            - Apply data classification and handling rules
            - Ensure compliance with privacy regulations
        3. Evaluate policies in real time:
            - Check policies before agent execution
            - Validate data access and modification requests
            - Enforce business rules and constraints
            - Prevent unauthorized operations
        4. Log all policy enforcement decisions:
            - Record policy evaluation results
            - Track access attempts and outcomes
            - Log policy violations and exceptions
            - Maintain audit trail for compliance
        5. Support exception approvals:
            - Handle policy override requests
            - Manage approval workflows for exceptions
            - Track exception approvals and justifications
            - Provide compliance evidence for audits
        6. Provide compliance evidence:
            - Generate policy compliance reports
            - Support regulator reporting requirements
            - Maintain evidence for audit trails
            - Enable compliance monitoring and reporting
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),             # Policy Engine (OPA or equivalent for RBAC & ABAC enforcement)
            FileTools(),               # Data Privacy Toolkit (PII masking, tokenization, retention rules)
            ReasoningTools(),          # Workflow Manager (approvals for sensitive operations)
            DuckDbTools(),             # Logging & Evidence Integration (links with Audit-Agent)
            KnowledgeTools()           # Policy knowledge base and rule management
        ],
    )


def create_Monitoring_agent():
    """
    Creates an AI agent specialized in system monitoring,
    anomaly detection, and operational health management.
    """
    return Agent(
        name="MonitoringAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in system monitoring, anomaly detection, and operational health management.",
        
        instructions="""
        You are the Monitoring-Agent.
        Your purpose is to continuously track system, model, and data health in real time.
        Follow these rules:
        
        1. Collect telemetry data:
            - Monitor latency, error rates, and throughput
            - Track feature drift and model performance
            - Collect system resource utilization metrics
            - Monitor data quality and integrity
        2. Detect anomalies and drift:
            - Identify outliers in system performance
            - Detect model drift and degradation
            - Flag data quality issues and inconsistencies
            - Alert on SLA violations and thresholds
        3. Provide monitoring dashboards:
            - Create real-time performance visualizations
            - Display system health and status indicators
            - Show trend analysis and historical data
            - Enable operational team oversight
        4. Run synthetic testing:
            - Validate pipelines and data flows
            - Test agent functionality and responses
            - Verify system integration and connectivity
            - Automate workload rebalancing
        5. Integrate with incident management:
            - Send alerts to PagerDuty, Slack, OpsGenie
            - Escalate critical issues automatically
            - Provide context and remediation guidance
            - Track incident resolution and follow-up
        6. Support automated responses:
            - Trigger retraining for model drift
            - Restart failed services and processes
            - Scale resources based on demand
            - Implement circuit breakers and failovers
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),             # Telemetry Collectors (latency, error rates, throughput, feature drift)
            PandasTools(),             # Anomaly Detection Models (for drift and outlier detection)
            VisualizationTools(),      # Dashboards & SLA Monitors (Grafana/Prometheus integrations)
            FileTools(),               # Synthetic Testing Suite (to validate pipelines and workloads)
            SlackTools()               # Incident Management Integration (PagerDuty, Slack, OpsGenie)
        ],
    )


def create_Audit_agent():
    """
    Creates an AI agent specialized in audit logging,
    compliance tracking, and regulatory reporting.
    """
    return Agent(
        name="AuditAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in audit logging, compliance tracking, and regulatory reporting.",
        
        instructions="""
        You are the Audit-Agent.
        Your purpose is to maintain comprehensive audit trails and support regulatory compliance.
        Follow these rules:
        
        1. Record all decisions and actions:
            - Log every agent decision and output
            - Track input data versions and sources
            - Record user actions and system events
            - Maintain complete audit trail
        2. Implement immutable logging:
            - Use append-only, tamper-proof storage
            - Ensure log integrity and authenticity
            - Prevent log modification or deletion
            - Support regulatory compliance requirements
        3. Track data provenance:
            - Record input data versions and sources
            - Track data lineage and transformations
            - Maintain data quality and integrity records
            - Support data governance requirements
        4. Generate regulator-ready packages:
            - Create comprehensive audit bundles
            - Include approvals and supporting documents
            - Format data for regulatory submission
            - Ensure compliance with reporting standards
        5. Correlate cross-agent events:
            - Reconstruct workflows from event logs
            - Link related actions and decisions
            - Support investigation and analysis
            - Enable end-to-end traceability
        6. Enforce retention and e-discovery:
            - Implement data retention policies
            - Support legal discovery processes
            - Manage data lifecycle and archiving
            - Ensure compliance with legal requirements
        """,
        
        markdown=True,
        
        tools=[
            FileTools(),               # Immutable Logging System (append-only, tamper-proof)
            DuckDbTools(),             # Provenance Tracker (records input data versions & sources)
            PythonTools(),             # Secure Storage (for regulator-ready audit bundles)
            ReasoningTools(),          # Workflow Correlator (rebuild cross-agent workflows)
            KnowledgeTools()           # E-Discovery Engine (retention & retrieval policies)
        ],
    )


def create_Explainability_agent():
    """
    Creates an AI agent specialized in model interpretability,
    decision explanation, and transparency reporting.
    """
    return Agent(
        name="ExplainabilityAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in model interpretability, decision explanation, and transparency reporting.",
        
        instructions="""
        You are the Explainability-Agent.
        Your purpose is to provide human-readable explanations for all AI-driven outputs and decisions.
        Follow these rules:
        
        1. Generate model interpretability:
            - Use SHAP, LIME, and counterfactual analysis
            - Create feature importance and attribution maps
            - Provide confidence bands and uncertainty measures
            - Explain model predictions and decisions
        2. Create natural language explanations:
            - Translate technical explanations into plain English
            - Generate user-friendly decision summaries
            - Provide context and reasoning for outputs
            - Ensure explanations are accessible to non-technical users
        3. Track feature provenance:
            - Link features to training data versions
            - Track data lineage and transformations
            - Maintain feature quality and integrity records
            - Support data governance requirements
        4. Enable scenario exploration:
            - Support "what-if" queries and sensitivity testing
            - Allow exploration of alternate outcomes
            - Provide scenario analysis and comparisons
            - Enable decision support and planning
        5. Attach explanation artifacts:
            - Include explanations with all outputs
            - Provide reasoning for risk flags and alerts
            - Document decision rationale and context
            - Support audit and compliance requirements
        6. Support multiple stakeholders:
            - Provide explanations for relationship managers
            - Generate reports for auditors and regulators
            - Enable client understanding and transparency
            - Support internal decision-making processes
        """,
        
        markdown=True,
        
        tools=[
            PythonTools(),             # Model Interpretability Libraries (SHAP, LIME, counterfactuals)
            KnowledgeTools(),          # Natural Language Generator (to translate technical explanations)
            DuckDbTools(),             # Feature Provenance Tracker (link features to training data versions)
            ReasoningTools(),          # Scenario Explorer (for "what-if" and sensitivity testing)
            VisualizationTools()       # Explanation visualization and reporting
        ],
    )


# Create all agents
Policy_agent = create_Policy_agent()
Monitoring_agent = create_Monitoring_agent()
Audit_agent = create_Audit_agent()
Explainability_agent = create_Explainability_agent()

# Test prompts for each agent
policy_test_prompt = """
Enforce access control for a sensitive financial operation:
- User requests access to client portfolio data
- Check RBAC permissions and data classification
- Apply PII masking for sensitive information
- Log the access decision and policy evaluation
- Generate compliance evidence for audit trail
"""

monitoring_test_prompt = """
Monitor system health and detect anomalies:
- Collect telemetry data from all agents
- Detect performance degradation and model drift
- Create monitoring dashboard with key metrics
- Run synthetic tests to validate system functionality
- Send alerts for critical issues to operations team
"""

audit_test_prompt = """
Generate comprehensive audit report:
- Collect all decision logs and data provenance
- Create immutable audit trail for regulatory compliance
- Correlate cross-agent events and workflows
- Generate regulator-ready audit package
- Ensure compliance with retention policies
"""

explainability_test_prompt = """
Explain a high-risk transaction flag:
- Analyze the decision factors and feature importance
- Generate human-readable explanation for the flag
- Provide "what-if" scenarios for different outcomes
- Link decision to underlying data and model features
- Create explanation report for compliance team
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
    
    print("Testing Policy-Agent...")
    Policy_agent.print_response(policy_test_prompt, stream=True)
    
    print("\nTesting Monitoring-Agent...")
    Monitoring_agent.print_response(monitoring_test_prompt, stream=True)
    
    print("\nTesting Audit-Agent...")
    Audit_agent.print_response(audit_test_prompt, stream=True)
    
    print("\nTesting Explainability-Agent...")
    Explainability_agent.print_response(explainability_test_prompt, stream=True)

# Uncomment to test individual agents
# Policy_agent.print_response(policy_test_prompt, stream=True)
# Monitoring_agent.print_response(monitoring_test_prompt, stream=True)
# Audit_agent.print_response(audit_test_prompt, stream=True)
# Explainability_agent.print_response(explainability_test_prompt, stream=True)

# Uncomment to test all agents at once
# test_agents()
