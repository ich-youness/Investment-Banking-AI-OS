import os
from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.duckduckgo import DuckDuckGoTools  # Example for web data
from agno.tools.yfinance import YFinanceTools 
from agno.tools.csv_toolkit import CsvTools
from agno.tools.financial_datasets import FinancialDatasetsTools
from agno.tools.opencv import OpenCVTools
from agno.tools.file import FileTools
from agno.tools.python import PythonTools
from agno.tools.knowledge import KnowledgeTools
from agno.tools.reasoning import ReasoningTools
# from agno.tools.custom_api import CustomAPITools  # May not be available in current version
from agno.tools.pandas import PandasTools
from agno.tools.duckdb import DuckDbTools
from agno.tools.visualization import VisualizationTools


def create_Ingest_agent(): 
    """
    Creates an AI agent that ingests raw data from multiple sources 
    (CSV, Excel, APIs, databases, and websites), normalizes formats, 
    and prepares it for further processing. 
    """
    return Agent(
        name="IngestAgent", 
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in ingesting financial and business data from multiple sources and preparing it for downstream analysis.", 
        
        instructions="""
        You are the Ingest-Agent. 
        Your purpose is to fetch, load, and standardize data from different input sources. 
        Follow these rules:
        
        1. Identify the type of input (CSV, Excel, API, SQL database, or Web page).
        2. Use the correct tool for ingestion:
            - CSV/Excel → use CSV or Pandas toolkits.
            - API data → use Custom API toolkit (provide endpoint + params).
            - Databases → use SQL, DuckDb, or Postgres depending on connection.
            - Web pages → use Firecrawl or Website toolkit.
        3. Validate the ingested data:
            - Ensure the file is readable and not corrupted.
            - Standardize column names and data types where possible.
        4. Provide a summary of ingested data:
            - Number of rows & columns.
            - Key fields or headers.
            - Any missing or inconsistent values detected.
        5. Save or pass the clean structured data to the next pipeline step. 
        """, 
        
        markdown=True,
        
        tools=[
            DuckDuckGoTools(),        # For fetching data from the web
            YFinanceTools(),          # For stock & market data
            FinancialDatasetsTools(), # For macro & sector data
            CsvTools(),               # Work with CSV files
            PandasTools(),            # Data manipulation
            DuckDbTools(),            # Run SQL queries on local datasets
            FileTools()               # Read/write local files
        ],
    )


def create_OCR_agent():
    """
    Creates an AI agent that processes scanned documents and images
    using OCR technology to extract machine-readable text.
    """
    return Agent(
        name="OCRAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in optical character recognition (OCR) for processing scanned financial documents, contracts, and reports.",
        
        instructions="""
        You are the OCR-Agent.
        Your purpose is to process scanned documents and images to extract machine-readable text.
        Follow these rules:
        
        1. Accept scanned PDFs, contracts, or financial reports as input.
        2. Preprocess images for optimal OCR:
            - Remove noise and artifacts
            - Align and deskew documents
            - Enhance contrast and clarity
            - Convert to appropriate format (grayscale/binary)
        3. Apply OCR processing:
            - Use OpenCV for image preprocessing
            - Integrate with Tesseract or other OCR engines via Python
            - Handle multiple languages if needed
            - Process both text and tables
        4. Post-process extracted text:
            - Clean and format the output
            - Preserve document structure where possible
            - Handle special characters and formatting
        5. Pass structured text output to NLP-Extractor-Agent for further processing.
        """,
        
        markdown=True,
        
        tools=[
            OpenCVTools(),    # Document preprocessing, image cleaning
            FileTools(),      # Handle scanned documents
            PythonTools()     # Custom OCR pipelines, Tesseract integration
        ],
    )


def create_NLP_Extractor_agent():
    """
    Creates an AI agent that extracts key information from text using
    natural language processing techniques.
    """
    return Agent(
        name="NLPExtractorAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in extracting entities, financial metrics, and structured information from text using NLP techniques.",
        
        instructions="""
        You are the NLP-Extractor-Agent.
        Your purpose is to extract key elements and structured information from text.
        Follow these rules:
        
        1. Take OCR text and extract key elements:
            - Entities (companies, people, locations, dates)
            - Financial amounts and currencies
            - Dates and time periods
            - Legal clauses and obligations
        2. Identify financial metrics:
            - Revenue, EBITDA, profit margins
            - Assets, liabilities, equity
            - Cash flow statements
            - Financial covenants and ratios
        3. Tag legal/contractual obligations:
            - Termination clauses
            - Penalties and fees
            - Risk factors
            - Compliance requirements
        4. Use structured extraction:
            - Apply named entity recognition (NER)
            - Use reasoning tools for logical structure
            - Use Python tools for custom API calls if needed
        5. Output structured JSON format for Feature-Agent processing.
        """,
        
        markdown=True,
        
        tools=[
            KnowledgeTools(),     # Extract entities from text
            ReasoningTools(),     # Structure extracted insights logically
            PythonTools()         # Custom API calls and NER processing
        ],
    )


def create_Feature_agent():
    """
    Creates an AI agent that transforms raw data into model-ready features
    through feature engineering and data preprocessing.
    """
    return Agent(
        name="FeatureAgent",
        model=xAI(id="grok-3-mini", api_key=os.getenv("XAI_API_KEY")),
        description="An agent specialized in feature engineering and data transformation to prepare clean, model-ready datasets.",
        
        instructions="""
        You are the Feature-Agent.
        Your purpose is to transform raw ingested and extracted data into model-ready features.
        Follow these rules:
        
        1. Transform raw data into features:
            - Apply feature engineering techniques
            - Create derived variables and ratios
            - Generate time-series features
            - Build categorical encodings
        2. Standardize formats:
            - Currency normalization (convert to common base currency)
            - Date alignment and timezone handling
            - Unit standardization across datasets
            - Format consistency checks
        3. Handle data quality issues:
            - Detect and handle missing values
            - Identify and treat outliers
            - Remove duplicates and inconsistencies
            - Validate data integrity
        4. Generate insights and visualizations:
            - Statistical summaries and distributions
            - Feature correlation analysis
            - Data quality reports
            - Visualization charts and graphs
        5. Provide cleaned dataset for modeling in other modules.
        """,
        
        markdown=True,
        
        tools=[
            PandasTools(),           # Feature engineering & transformations
            DuckDbTools(),           # Query and clean datasets
            VisualizationTools()     # Show feature distributions
        ],
    )


# Create all agents
Ingest_agent = create_Ingest_agent()
OCR_agent = create_OCR_agent()
NLP_Extractor_agent = create_NLP_Extractor_agent()
Feature_agent = create_Feature_agent()

# Test prompts for each agent
ingest_test_prompt = """
Ingest the data from a CSV file named 'transactions.csv', 
summarize its contents (rows, columns, headers), 
and check if there are any missing values.
"""

ocr_test_prompt = """
Process the scanned PDF document 'financial_report.pdf',
extract all text content, and prepare it for NLP analysis.
"""

nlp_test_prompt = """
Extract key financial entities and metrics from the provided text:
- Company names and financial amounts
- Revenue, EBITDA, and profit figures
- Important dates and contractual terms
Output the results in structured JSON format.
"""

feature_test_prompt = """
Transform the ingested financial data into model-ready features:
- Normalize currency values to USD
- Create financial ratios and derived metrics
- Handle missing values and outliers
- Generate statistical summaries and visualizations
"""

# Uncomment to test individual agents
# Ingest_agent.print_response(ingest_test_prompt, stream=True)
# OCR_agent.print_response(ocr_test_prompt, stream=True)
# NLP_Extractor_agent.print_response(nlp_test_prompt, stream=True)
# Feature_agent.print_response(feature_test_prompt, stream=True)

 