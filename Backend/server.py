from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import the Company Valuation agent
from Modules.CompanyValuation.CompanyValuation import agent

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],
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

# Initialize the Company Valuation agent
api_logger.info("Initializing Banking Investment OS modules...")
api_logger.info("Setting up Company Valuation Module...")
agent_logger.info("Creating Financial Data Agent...")

# Agent mapping for easy access
AGENTS = {
    "company_valuation": {
        "financial_data_agent": agent
    }
}

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

@app.get("/images/{filename}")
async def get_image(filename: str):
    """Serve generated images from the Company Valuation module"""
    # This would need to be implemented based on where images are stored
    # For now, return a placeholder
    return {"message": f"Image {filename} not found. This endpoint needs to be implemented."}

# Run the server
if __name__ == "__main__":
    api_logger.info("Starting Banking Investment OS FastAPI Server...")
    api_logger.info("Server will be available at: http://localhost:8000")
    api_logger.info("API Documentation: http://localhost:8000/docs")
    api_logger.info("Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
