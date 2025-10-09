from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import the Company Valuation agents
from Modules.CompanyValuation.CompanyValuation import agent
from Modules.CompanyValuation.CompanyValuationV2 import FinancialAnalysisAgents
from Modules.ClientOCR import client_ocr
from Modules.FallbackOCR import fallback_ocr

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('banking_investment_os.log'),
        logging.StreamHandler()
    ]
)

# Create logger for agent calls
agent_logger = logging.getLogger('banking_investment_os.agents')
api_logger = logging.getLogger('banking_investment_os.api')

# Initialize FastAPI app
app = FastAPI(
    title="Banking Investment OS API",
    description="AI-powered company valuation and financial analysis system",
    version="1.0.0"
)

# Add CORS middleware (configurable via env CORS_ALLOW_ORIGINS as comma-separated list)
cors_origins_env = os.getenv("CORS_ALLOW_ORIGINS", "")
if cors_origins_env.strip():
    allow_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
else:
    allow_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "https://investment-banking-ai-os.onrender.com:8080",
        "https://investment-banking-ai-os.onrender.com:10000",
        "https://investment-banking-ai-os.onrender.com:8000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    module: str
    agent: str
    custom_data: Optional[Dict[str, Any]] = None

class ResponseModel(BaseModel):
    success: bool
    response: str
    module: str
    agent: str
    error: Optional[str] = None

# Initialize the Company Valuation agents
api_logger.info("Initializing Banking Investment OS modules...")
api_logger.info("Setting up Company Valuation Module...")
agent_logger.info("Creating Financial Data Agent...")

# Initialize CompanyValuationV2 agents
xai_api_key = os.getenv("XAI_API_KEY")
if not xai_api_key:
    api_logger.warning("XAI_API_KEY not found in environment variables. CompanyValuationV2 agents will not be available.")
    financial_agents = None
else:
    financial_agents = FinancialAnalysisAgents(xai_api_key)
    api_logger.info("CompanyValuationV2 agents initialized successfully")

# Initialize OCR client
def initialize_ocr_client():
    """Initialize the OCR client if available"""
    try:
        # You'll need to import and configure your OCR client here
        # Example:
        # from your_ocr_client import Client
        # client = Client(api_key=os.getenv("OCR_API_KEY"))
        # client_ocr.set_client(client)
        # api_logger.info("OCR client initialized successfully")
        
        # For now, we'll just log that OCR is not configured
        api_logger.warning("OCR client not configured. Please set up your OCR client in initialize_ocr_client()")
        return False
    except Exception as e:
        api_logger.error(f"Failed to initialize OCR client: {e}")
        return False

# Initialize OCR
ocr_available = initialize_ocr_client()

# Agent mapping for easy access
AGENTS = {
    "company_valuation": {
        "financial_data_agent": agent,
        "income_statement_analyst": financial_agents.create_income_statement_analyst(),
        "balance_sheet_analyst": financial_agents.create_balance_sheet_analyst(),
        "valuation_analyst": financial_agents.create_valuation_analyst(),
        "chief_financial_analyst": financial_agents.create_chief_financial_analyst()
    }
}

# Add CompanyValuationV2 agents if available
# if financial_agents:
#     AGENTS["company_valuation_v2"] = {
#         "income_statement_analyst": financial_agents.create_income_statement_analyst(),
#         "balance_sheet_analyst": financial_agents.create_balance_sheet_analyst(),
#         "valuation_analyst": financial_agents.create_valuation_analyst(),
#         "chief_financial_analyst": financial_agents.create_chief_financial_analyst()
#     }

api_logger.info("All modules initialized successfully!")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Banking Investment OS API is running",
        "version": "1.0.0",
        "available_modules": list(AGENTS.keys())
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "All systems operational"}

# Get available modules and agents
@app.get("/modules")
async def get_modules():
    return {
        "modules": {
            module_name: list(agents.keys()) 
            for module_name, agents in AGENTS.items()
        }
    }

# Main query endpoint
@app.post("/query", response_model=ResponseModel)
async def query_agent(request: QueryRequest):
    start_time = datetime.now()
    request_id = f"{request.module}_{request.agent}_{start_time.strftime('%Y%m%d_%H%M%S')}"
    
    api_logger.info(f"[{request_id}] Received query request - Module: {request.module}, Agent: {request.agent}")
    agent_logger.info(f"[{request_id}] Query: {request.query[:100]}{'...' if len(request.query) > 100 else ''}")
    
    try:
        # Validate module and agent
        if request.module not in AGENTS:
            error_msg = f"Module '{request.module}' not found. Available modules: {list(AGENTS.keys())}"
            api_logger.error(f"[{request_id}] {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        if request.agent not in AGENTS[request.module]:
            error_msg = f"Agent '{request.agent}' not found in module '{request.module}'. Available agents: {list(AGENTS[request.module].keys())}"
            api_logger.error(f"[{request_id}] {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Get the agent
        agent_instance = AGENTS[request.module][request.agent]
        agent_logger.info(f"[{request_id}] Agent retrieved successfully: {agent_instance.name}")
        
        # Execute the query
        agent_logger.info(f"[{request_id}] Executing agent query...")
        execution_start = datetime.now()
        
        response = agent_instance.run(request.query)
        response_content = response.content if hasattr(response, 'content') else str(response)
        
        execution_time = (datetime.now() - execution_start).total_seconds()
        agent_logger.info(f"[{request_id}] Agent execution completed in {execution_time:.2f} seconds")
        agent_logger.info(f"[{request_id}] Response length: {len(response_content)} characters")
        
        total_time = (datetime.now() - start_time).total_seconds()
        api_logger.info(f"[{request_id}] Query completed successfully in {total_time:.2f} seconds")
        
        return ResponseModel(
            success=True,
            response=response_content,
            module=request.module,
            agent=request.agent
        )
        
    except HTTPException as e:
        total_time = (datetime.now() - start_time).total_seconds()
        api_logger.error(f"[{request_id}] HTTP error after {total_time:.2f} seconds: {e.detail}")
        return ResponseModel(
            success=False,
            response="",
            module=request.module,
            agent=request.agent,
            error=e.detail
        )
        
    except Exception as e:
        total_time = (datetime.now() - start_time).total_seconds()
        error_msg = str(e)
        api_logger.error(f"[{request_id}] Unexpected error after {total_time:.2f} seconds: {error_msg}")
        agent_logger.error(f"[{request_id}] Error details: {type(e).__name__}: {error_msg}")
        
        return ResponseModel(
            success=False,
            response="",
            module=request.module,
            agent=request.agent,
            error=error_msg
        )

# Company Valuation specific endpoints
@app.post("/company-valuation/financial-data")
async def financial_data_agent_query(request: QueryRequest):
    api_logger.info(f"Financial Data Agent endpoint called - Query: {request.query[:50]}...")
    request.module = "company_valuation"
    request.agent = "financial_data_agent"
    return await query_agent(request)

# Company Valuation V2 specific endpoints
@app.post("/company-valuation-v2/income-statement")
async def income_statement_analyst_query(request: QueryRequest):
    api_logger.info(f"Income Statement Analyst endpoint called - Query: {request.query[:50]}...")
    request.module = "company_valuation_v2"
    request.agent = "income_statement_analyst"
    return await query_agent(request)

@app.post("/company-valuation-v2/balance-sheet")
async def balance_sheet_analyst_query(request: QueryRequest):
    api_logger.info(f"Balance Sheet Analyst endpoint called - Query: {request.query[:50]}...")
    request.module = "company_valuation_v2"
    request.agent = "balance_sheet_analyst"
    return await query_agent(request)

@app.post("/company-valuation-v2/valuation")
async def valuation_analyst_query(request: QueryRequest):
    api_logger.info(f"Valuation Analyst endpoint called - Query: {request.query[:50]}...")
    request.module = "company_valuation_v2"
    request.agent = "valuation_analyst"
    return await query_agent(request)

@app.post("/company-valuation-v2/chief-analyst")
async def chief_financial_analyst_query(request: QueryRequest):
    api_logger.info(f"Chief Financial Analyst endpoint called - Query: {request.query[:50]}...")
    request.module = "company_valuation_v2"
    request.agent = "chief_financial_analyst"
    return await query_agent(request)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload files to the Backend/Inputs directory with OCR processing"""
    try:
        # Ensure the Inputs directory exists
        inputs_dir = Path("Inputs")
        inputs_dir.mkdir(exist_ok=True)
        
        uploaded_files = []
        
        for file in files:
            # Create a safe filename
            safe_filename = file.filename.replace(" ", "_").replace("(", "").replace(")", "")
            file_path = inputs_dir / safe_filename
            
            # Write the file
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Process with OCR if it's a PDF
            ocr_result = None
            if file_path.suffix.lower() == '.pdf':
                if ocr_available:
                    api_logger.info(f"Processing PDF with advanced OCR: {safe_filename}")
                    ocr_result = await client_ocr.process_uploaded_file(str(file_path))
                    
                    if ocr_result.get('success', False):
                        api_logger.info(f"Advanced OCR completed successfully for {safe_filename}")
                    else:
                        api_logger.warning(f"Advanced OCR failed for {safe_filename}: {ocr_result.get('error', 'Unknown error')}")
                else:
                    # Use fallback OCR with pypdf
                    api_logger.info(f"Processing PDF with fallback OCR (pypdf): {safe_filename}")
                    ocr_result = fallback_ocr.extract_text_from_pdf(str(file_path))
                    
                    if ocr_result.get('success', False):
                        # Save the extracted text
                        text_file_path = fallback_ocr.save_extracted_text(str(file_path), ocr_result)
                        if text_file_path:
                            ocr_result['metadata']['output_file'] = text_file_path
                        api_logger.info(f"Fallback OCR completed successfully for {safe_filename}")
                    else:
                        api_logger.warning(f"Fallback OCR failed for {safe_filename}: {ocr_result.get('error', 'Unknown error')}")
            
            uploaded_files.append({
                "filename": safe_filename,
                "original_name": file.filename,
                "size": len(content),
                "path": str(file_path),
                "ocr_success": ocr_result.get('success', False) if ocr_result else None,
                "extracted_text_length": len(ocr_result.get('text', '')) if ocr_result else 0,
                "ocr_metadata": ocr_result.get('metadata', {}) if ocr_result else {},
                "ocr_error": ocr_result.get('error') if ocr_result and not ocr_result.get('success', False) else None
            })
            
            api_logger.info(f"File uploaded: {safe_filename} ({len(content)} bytes)")
        
        return {
            "success": True,
            "message": f"Successfully uploaded {len(uploaded_files)} file(s) with OCR processing",
            "files": uploaded_files
        }
        
    except Exception as e:
        api_logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/images/{filename}")
async def get_image(filename: str):
    """Serve generated images from the Company Valuation module"""
    try:
        # Define the charts directory path
        charts_dir = Path("charts/")
        
        
        # Check if the charts directory exists
        if not charts_dir.exists():
            api_logger.error(f"Charts directory not found: {charts_dir}")
            raise HTTPException(status_code=404, detail="Charts directory not found")
        
        # Construct the full file path
        file_path = charts_dir / filename
        
        # Check if the file exists
        if not file_path.exists():
            api_logger.warning(f"Image file not found: {filename}")
            raise HTTPException(status_code=404, detail=f"Image '{filename}' not found")
        
        # Check if it's a valid image file
        valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        if file_path.suffix.lower() not in valid_extensions:
            api_logger.warning(f"Invalid file type requested: {filename}")
            raise HTTPException(status_code=400, detail=f"File '{filename}' is not a valid image format")
        
        # Log the successful image request
        api_logger.info(f"Serving image: {filename}")
        
        # Return the file using FileResponse
        return FileResponse(
            path=str(file_path),
            media_type=f"image/{file_path.suffix[1:].lower()}",
            filename=filename
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        api_logger.error(f"Error serving image '{filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error serving image: {str(e)}")

# Run the server
if __name__ == "__main__":
    api_logger.info("Starting Banking Investment OS FastAPI Server...")
    # Determine port from environment (Render provides PORT, default 10000)
    port = int(os.getenv("PORT", "10000"))
    api_logger.info(f"Binding on 0.0.0.0:{port}")
    api_logger.info(f"API docs at: http://localhost:{port}/docs (local) or via service URL on Render")

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
