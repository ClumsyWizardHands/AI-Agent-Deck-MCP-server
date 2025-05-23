# Technical Context: Agent Swarm MCP Server

## Development Environment

### Operating System
- **Primary**: Windows 11 (current development environment)
- **Target**: Cross-platform (Windows, Linux, macOS)
- **Deployment**: Linux containers preferred for production

### Python Environment
- **Version**: Python 3.12 (current)
- **Minimum**: Python 3.7+ (FastAPI requirement)
- **Virtual Environment**: `venv` (included in project)
- **Package Manager**: pip with requirements.txt

## Languages & Frameworks

### Primary Language: Python
- **Rationale**: Excellent async support, rich ecosystem, FastAPI integration
- **Version**: 3.12.x (latest stable)
- **Style**: Type hints throughout, async/await patterns

### Core Framework: FastAPI
- **Version**: Latest stable (0.115.12 as installed)
- **Features Used**: 
  - Automatic API documentation
  - Pydantic integration
  - Async request handling
  - Dependency injection system

### Key Dependencies
- **fastapi**: Web framework and API server
- **uvicorn[standard]**: ASGI server with full features
- **pydantic**: Data validation and serialization (2.11.5)
- **httpx**: Async HTTP client for external calls (0.28.1)

## Tooling Stack

### Development Server
- **Local**: uvicorn with auto-reload
- **Command**: `python app/main.py` or `uvicorn app.main:app --reload`
- **Port**: 8000 (default)
- **Host**: 0.0.0.0 (accepts external connections)

### API Documentation
- **Swagger UI**: Auto-generated at `/docs`
- **ReDoc**: Alternative docs at `/redoc`
- **OpenAPI**: JSON schema at `/openapi.json`

### Project Structure Tools
- **Virtual Environment**: `venv/` directory
- **Dependencies**: `requirements.txt`
- **Documentation**: `README.md`
- **Memory Bank**: `memory-bank/` for project context

## Development Constraints

### Environment Constraints
- **Windows Commands**: No bash/shell scripting, use Windows cmd syntax
- **Path Separators**: Use backslashes for Windows paths
- **Process Management**: Use `taskkill` for stopping servers

### Performance Constraints
- **Async Required**: All I/O operations must be non-blocking
- **Memory Efficiency**: Consider memory usage for agent state management
- **Network Latency**: Optimize for low-latency agent communication

### Security Constraints
- **Input Validation**: All inputs validated via Pydantic models
- **Authentication**: Placeholder for future implementation
- **CORS**: Configure for cross-origin requests if needed
- **Environment Variables**: Use for sensitive configuration

## Deployment Considerations

### Local Development
- **Command**: `agent_swarm_mcp_server\venv\Scripts\python agent_swarm_mcp_server\app\main.py`
- **URL**: http://localhost:8000
- **Auto-reload**: Available with uvicorn --reload flag

### Production Readiness
- **ASGI Server**: Uvicorn with Gunicorn for production
- **Process Management**: systemd or Docker containers
- **Logging**: Structured logging for monitoring
- **Configuration**: Environment-based settings

### Future Enhancements
- **Containerization**: Docker support for easy deployment
- **Database**: Consider async database integration
- **Caching**: Redis for agent state caching
- **Monitoring**: Prometheus metrics integration
