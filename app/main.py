from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import json
import re
import os
from typing import Dict, Any, List, Optional
from .models import EmpireDescriptionRequest, AgentSpecificationResponse, ExtendedEmpireDescription
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

# Get the directory where this file is located
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
static_dir = os.path.join(parent_dir, "static")

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

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
        "health": "/health",
        "empire_builder": "/empire-builder"
    }

# empire Builder UI endpoint
@app.get("/empire-builder")
async def empire_builder():
    html_path = os.path.join(static_dir, "empire-builder.html")
    return FileResponse(html_path)

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

# Converter function from extended to standard format
def convert_extended_to_standard(extended: ExtendedEmpireDescription) -> EmpireDescriptionRequest:
    """
    Convert ExtendedEmpireDescription to EmpireDescriptionRequest.
    Maps the psychological/strategic dimensions to the standard format.
    """
    # Extract empire name from the first line or until first period/newline
    empire_text = extended.empire_name_and_description.strip()
    empire_name_match = re.match(r'^([^.\n]+)', empire_text)
    empire_name = empire_name_match.group(1).strip() if empire_name_match else "Unknown empire"
    
    # Detect primary focus domains from content
    # You could enhance this with more sophisticated keyword detection
    domain_keywords = {
        "governance": ["governance", "democratic", "political", "policy"],
        "technology": ["AI", "tech", "digital", "software", "algorithm"],
        "strategy": ["strategic", "foresight", "planning", "warfare"],
        "narrative": ["narrative", "story", "discourse", "media"],
        "cognitive": ["cognitive", "epistemic", "knowledge", "intelligence"],
        "security": ["security", "defense", "protection", "risk"]
    }
    
    detected_domains = set()
    full_text = (empire_text + " " + 
                 " ".join(extended.ends) + " " + 
                 " ".join(extended.means) + " " + 
                 " ".join(extended.principles))
    
    for domain, keywords in domain_keywords.items():
        if any(keyword.lower() in full_text.lower() for keyword in keywords):
            detected_domains.add(domain)
    
    # If no domains detected, add a default
    if not detected_domains:
        detected_domains.add("general")
    
    # Combine identity statements into operational style
    operational_style = empire_text + "\n\nIdentity:\n" + "\n".join(extended.identity)
    
    # Keep resentments and emotions separate
    # For now, keep key_challenges empty or you could add other challenges if needed
    key_challenges = []
    
    return EmpireDescriptionRequest(
        empire_name=empire_name,
        primary_focus_domains=list(detected_domains),
        main_goals=extended.ends,
        available_resources=extended.means,
        core_principles=extended.principles,
        key_challenges=key_challenges if key_challenges else ["No specific challenges identified"],
        resentments=extended.resentments,
        emotions=extended.emotions,
        operational_style=operational_style
    )

# Extended agent suggestion endpoint
@app.post("/suggest-agents-extended", response_model=List[AgentSpecificationResponse])
async def suggest_agents_extended_endpoint(extended_empire: ExtendedEmpireDescription):
    """
    Accept empire description in extended format with psychological/strategic dimensions.
    Directly passes to Claude without conversion for more focused agent generation.
    """
    # Log the incoming request for debugging
    print("=" * 80)
    print("INCOMING REQUEST FROM UI:")
    print(f"empire Name: {extended_empire.empire_name_and_description[:100]}...")
    print(f"Ends: {len(extended_empire.ends)} items")
    print(f"Means: {len(extended_empire.means)} items")
    print(f"Principles: {len(extended_empire.principles)} items")
    print(f"Identity: {len(extended_empire.identity)} items")
    print(f"Resentments: {len(extended_empire.resentments)} items")
    print(f"Emotions: {len(extended_empire.emotions)} items")
    print("=" * 80)
    
    # Load prompt template
    try:
        with open(settings.MASTER_PROMPT_PATH, 'r') as f:
            prompt_template_str = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Master prompt file not found.")
    
    # Pass extended empire directly to Claude (no conversion)
    agent_specs = await get_claude_suggestions(
        empire_data=extended_empire,
        api_key=settings.CLAUDE_API_KEY,
        prompt_template_str=prompt_template_str
    )
    
    print(f"Successfully generated {len(agent_specs)} agents")
    return agent_specs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
