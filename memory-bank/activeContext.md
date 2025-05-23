# Active Context: Agent Swarm MCP Server

## Current Focus
**JSON Parsing Error Resolution** - Fixed Claude response parsing issues with enhanced error handling

## Recent Decisions

### Framework Selection (Session: 5/23/2025)
- **Decision**: Chose FastAPI as the web framework
- **Rationale**: Modern async support, automatic API documentation, excellent type hint integration
- **Impact**: Sets foundation for high-performance agent coordination

### Project Structure (Session: 5/23/2025)
- **Decision**: Standard Python project layout with dedicated directories
- **Structure**: 
  - `app/` for application code
  - `prompts/` for prompt templates
  - `memory-bank/` for project context
  - `venv/` for virtual environment
- **Rationale**: Clear separation of concerns, follows Python best practices

### Dependency Selection (Session: 5/23/2025)
- **Core Dependencies**: fastapi, uvicorn[standard], pydantic, httpx
- **Rationale**: Minimal but comprehensive stack for MCP server functionality
- **Future Extensions**: Ready for database, caching, and monitoring additions

## Current Work Items

### Completed This Session (5/23/2025 - Part 3)
17. ✅ Added debug logging to Claude service
    - Logs raw Claude responses for troubleshooting
    - Helps identify formatting issues
18. ✅ Improved master prompt clarity
    - Added explicit instructions about JSON-only output
    - No markdown formatting allowed
    - Must start with [ and end with ]
    - Multiple reminders about output format
19. ✅ Added response cleaning logic
    - Automatically removes markdown code blocks
    - Extracts JSON array from mixed text
    - Handles common formatting issues from LLMs
20. ✅ Enhanced JSON parsing with automatic repair (5/23/2025 - Part 4)
    - Added regex-based fixes for missing commas between objects
    - Fixes pattern: `} {` → `}, {`
    - Removes trailing commas: `,]` → `]` and `,}` → `}`
    - Added detailed error diagnostics showing exact line/column
    - Saves problematic JSON to temporary file for debugging
    - Multiple fix attempts before failing

### Completed Earlier This Session
1. ✅ Project directory structure created
2. ✅ Python virtual environment set up
3. ✅ Core dependencies installed and verified
4. ✅ Basic FastAPI application with starter endpoints
5. ✅ Health check endpoint implemented
6. ✅ MCP protocol placeholder endpoint created
7. ✅ Comprehensive README documentation
8. ✅ Memory bank established with full context
9. ✅ Configuration management with Pydantic BaseSettings (5/23/2025)
   - Added pydantic-settings dependency
   - Created app/config.py with Settings class
   - CLAUDE_API_KEY and MASTER_PROMPT_PATH configured
10. ✅ Master prompt template created (5/23/2025)
    - Created prompts/master_prompt.txt
    - Contains AI Agent Swarm Architect instructions
    - Uses {{empire_description_json}} placeholder for dynamic content
11. ✅ Claude API service implemented (5/23/2025)
    - Created app/claude_service.py
    - Async function get_claude_suggestions() with Claude 4 Sonnet integration
    - Comprehensive error handling for network, parsing, and validation errors
    - Uses claude-sonnet-4-20250514 model
12. ✅ API endpoint integrated with Claude service (5/23/2025)
    - Modified /suggest-agents endpoint in app/main.py
    - Loads master prompt from file system
    - Calls Claude service with empire data and API key
    - Returns AI-generated agent specifications
13. ✅ Empire Builder UI created
    - Built clean HTML/CSS/JavaScript interface
    - Dynamic form fields with add/remove functionality
    - Auto-expanding textareas
    - Psychological/strategic empire format:
      - Empire Name & Description
      - Ends (what you seek to make real)
      - Means (tools and capacities)
      - Principles (deep structural drivers)
      - Identity (stories that shape actions)
      - Resentments (what haunts or drives)
      - Emotions (strategic emotional patterns)
14. ✅ Extended Empire Model implemented
    - Created ExtendedEmpireDescription model
    - Converter function maps to standard format
    - Intelligent domain detection from content
    - Preserves psychological/strategic richness
15. ✅ New API endpoint /suggest-agents-extended
    - Accepts extended empire format
    - Converts to standard format automatically
    - Uses existing Claude integration
    - No changes needed to master prompt
16. ✅ Static file serving configured
    - Fixed path issues for CSS and JavaScript
    - Proper routing for UI assets
    - Empire Builder accessible at /empire-builder

### Immediate Next Steps
1. **Testing**: Test the enhanced JSON parsing with various empire descriptions
2. **Monitor Logs**: Watch server console for detailed error diagnostics
3. **Iterate on Prompt**: If Claude continues to produce malformed JSON, may need to further refine the master prompt
4. **Agent Suggestion Logic Enhancement**: Replace placeholder logic with AI/ML-based analysis
5. **MCP Protocol Implementation**: Define actual MCP protocol handlers
6. **Agent Registration**: Create endpoints for agent registration and discovery
7. **Message Routing**: Implement agent-to-agent message routing
8. **Authentication**: Add security layer for production use
9. **Logging**: Implement structured logging for debugging

### Outstanding Questions
- **MCP Specification**: Need to research exact MCP protocol requirements
- **Agent State Management**: How to handle persistent agent state
- **Scaling Strategy**: How to handle multiple agent instances
- **Security Model**: Authentication and authorization approach

## Context for Next Session
- **Server Status**: Running with enhanced JSON parsing and error handling
- **Command to Run**: `cd agent_swarm_mcp_server; venv\Scripts\python -m app.main`
- **Verified Endpoints**: `/` (root), `/health` (health check), `/mcp` (placeholder), `/empire-builder` (UI), `/suggest-agents-extended` (API)
- **Documentation**: Available at `/docs` and `/redoc` when server is running
- **Memory Bank**: Complete context established for future development
- **JSON Parsing**: Enhanced with automatic repair for common LLM formatting issues

## Recent JSON Parsing Enhancements (5/23/2025 - Part 4)
- **Problem**: Claude generating JSON with missing comma delimiters
- **Solution**: Added regex-based automatic fixes for common JSON issues
- **Debug Features**: 
  - Logs exact error location (line/column)
  - Shows context around error
  - Saves problematic JSON to temp file
- **Fix Patterns**:
  - Missing commas: `} {` → `}, {`
  - Trailing commas: `,]` → `]` and `,}` → `}`
- **Testing**: Server now running, ready for testing with empire descriptions
