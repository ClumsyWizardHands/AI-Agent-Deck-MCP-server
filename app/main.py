from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
from typing import Dict, Any, List, Optional
from .models import EmpireDescriptionRequest, AgentSpecificationResponse
from .claude_service import get_claude_suggestions
from .config import settings

app = FastAPI(
    title="Agent Swarm MCP Server",
    description="A FastAPI-based MCP (Model Context Protocol) server for agent swarm operations",
    version="1.0.0"
)

# Configure CORS middleware
# NOTE: In production, replace "*" with your actual frontend domain(s)
# e.g., allow_origins=["https://your-frontend-domain.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request/response structures
class HealthResponse(BaseModel):
    status: str
    message: str

class MCPRequest(BaseModel):
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class MCPResponse(BaseModel):
    id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

# Basic health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        message="Agent Swarm MCP Server is running"
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Agent Swarm MCP Server",
        "docs": "/docs",
        "health": "/health"
    }

# MCP protocol endpoint (placeholder for future implementation)
@app.post("/mcp", response_model=MCPResponse)
async def mcp_handler(request: MCPRequest):
    # Placeholder for MCP protocol implementation
    return MCPResponse(
        id=request.id,
        result={"message": "MCP endpoint ready for implementation"}
    )

# Agent suggestion endpoint
@app.post("/suggest-agents", response_model=List[AgentSpecificationResponse])
async def suggest_agents_endpoint(empire_input: EmpireDescriptionRequest):
    try:
        with open(settings.MASTER_PROMPT_PATH, 'r') as f:
            prompt_template_str = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Master prompt file not found.")

    # Convert Pydantic model to JSON string for injection
    # empire_data_json_str = empire_input.model_dump_json() # Pydantic v2+
    # For Pydantic v1, it might be empire_input.json()

    agent_specs = await get_claude_suggestions(
        empire_data=empire_input,
        api_key=settings.CLAUDE_API_KEY,
        prompt_template_str=prompt_template_str
    )
    return agent_specs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
