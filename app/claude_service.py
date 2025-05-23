"""Claude API service for generating agent suggestions."""

import json
import logging
import re
from typing import List
import httpx
from fastapi import HTTPException
from app.models import EmpireDescriptionRequest, AgentSpecificationResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_claude_suggestions(
    empire_data: EmpireDescriptionRequest,
    api_key: str,
    prompt_template_str: str
) -> List[AgentSpecificationResponse]:
    """
    Get agent suggestions from Claude API based on empire description.
    
    Args:
        empire_data: The empire description request data
        api_key: Claude API key
        prompt_template_str: Prompt template with {{empire_description_json}} placeholder
        
    Returns:
        List of validated AgentSpecificationResponse objects
        
    Raises:
        HTTPException: For API errors, parsing errors, or validation errors
    """
    try:
        # Convert empire data to JSON string
        empire_json_str = empire_data.model_dump_json()
        
        # Replace placeholder in prompt template
        final_prompt = prompt_template_str.replace(
            "{{empire_description_json}}", 
            empire_json_str
        )
        
        # Construct Claude API request
        claude_payload = {
            "model": "claude-sonnet-4-20250514",  # Claude 4 Sonnet model
            "max_tokens": 20000,  # 20k tokens for complete responses
            "messages": [
                {"role": "user", "content": final_prompt}
            ]
        }
        
        claude_api_url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        # Make async request to Claude API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                claude_api_url,
                json=claude_payload,
                headers=headers,
                timeout=120.0  # 120 second timeout
            )
        
        # Check response status
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Claude API: {response.text}"
            )
        
        # Parse response
        try:
            response_json = response.json()
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to parse Claude API response as JSON: {str(e)}"
            )
        
        # Extract content from Claude's response structure
        # Claude Messages API returns: {"content": [{"type": "text", "text": "..."}], ...}
        try:
            if "content" not in response_json or not response_json["content"]:
                raise HTTPException(
                    status_code=502,
                    detail="Claude API response missing 'content' field"
                )
            
            # Get the text content from the first content item
            content_text = response_json["content"][0]["text"]
            
            # Log the raw content from Claude for debugging
            logger.info("=" * 80)
            logger.info("RAW CLAUDE RESPONSE:")
            logger.info(content_text[:1000] + "..." if len(content_text) > 1000 else content_text)
            logger.info("=" * 80)
            
            # Try to clean the response if it's wrapped in markdown or has extra text
            cleaned_text = content_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]  # Remove ```
            
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]  # Remove trailing ```
            
            cleaned_text = cleaned_text.strip()
            
            # Find the JSON array in the text (starts with [ and ends with ])
            start_idx = cleaned_text.find('[')
            end_idx = cleaned_text.rfind(']')
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                cleaned_text = cleaned_text[start_idx:end_idx + 1]
                logger.info("Extracted JSON from position %d to %d", start_idx, end_idx)
            
            # Try to parse the JSON array
            try:
                agent_specs_data = json.loads(cleaned_text)
            except json.JSONDecodeError as e:
                logger.error("Initial JSON parsing failed: %s", str(e))
                logger.error("Attempting to fix common JSON issues...")
                
                # Try to fix common JSON formatting issues
                fixed_text = cleaned_text
                
                # Fix missing commas between objects (common LLM error)
                # Pattern: } followed by whitespace/newlines and then {
                import re
                fixed_text = re.sub(r'}\s*\n\s*{', '},\n{', fixed_text)
                
                # Fix trailing commas before closing brackets
                fixed_text = re.sub(r',\s*\]', ']', fixed_text)
                fixed_text = re.sub(r',\s*\}', '}', fixed_text)
                
                # Log the specific error location
                if hasattr(e, 'lineno') and hasattr(e, 'colno'):
                    error_line = e.lineno
                    error_col = e.colno
                    lines = cleaned_text.split('\n')
                    if error_line <= len(lines):
                        logger.error("Error at line %d, column %d", error_line, error_col)
                        logger.error("Context around error:")
                        # Show 2 lines before and after
                        start_line = max(0, error_line - 3)
                        end_line = min(len(lines), error_line + 2)
                        for i in range(start_line, end_line):
                            prefix = ">>> " if i == error_line - 1 else "    "
                            logger.error("%s%d: %s", prefix, i + 1, lines[i][:200])
                
                # Try parsing the fixed text
                try:
                    agent_specs_data = json.loads(fixed_text)
                    logger.info("Successfully fixed JSON formatting issues")
                except json.JSONDecodeError as e2:
                    # Try one more fix - handle truncated JSON
                    logger.error("JSON parsing still failed after fixes: %s", str(e2))
                    logger.error("Attempting to fix truncated JSON...")
                    
                    # Check if it's likely truncated (missing closing brackets)
                    bracket_count = fixed_text.count('[') - fixed_text.count(']')
                    brace_count = fixed_text.count('{') - fixed_text.count('}')
                    
                    if bracket_count > 0 or brace_count > 0:
                        logger.info("Detected likely truncated JSON (bracket mismatch)")
                        # Try to close the JSON properly
                        truncated_fixed = fixed_text.rstrip()
                        
                        # Remove any incomplete entries at the end
                        # Look for the last complete object
                        last_complete_obj = truncated_fixed.rfind('},')
                        if last_complete_obj > 0:
                            truncated_fixed = truncated_fixed[:last_complete_obj + 1]
                        
                        # Close any open braces
                        while brace_count > 0:
                            truncated_fixed += '}'
                            brace_count -= 1
                        
                        # Close the array
                        if bracket_count > 0:
                            truncated_fixed += ']'
                        
                        try:
                            agent_specs_data = json.loads(truncated_fixed)
                            logger.info("Successfully parsed truncated JSON")
                        except json.JSONDecodeError:
                            # If still failing, save for debugging
                            import tempfile
                            import os
                            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', dir='.') as f:
                                f.write(cleaned_text)
                                logger.error("Saved problematic JSON to: %s", f.name)
                            
                            raise HTTPException(
                                status_code=502,
                                detail=f"Failed to parse agent specifications. Response appears truncated. Try with a simpler empire description."
                            )
                    else:
                        # Save the problematic JSON for debugging
                        import tempfile
                        import os
                        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', dir='.') as f:
                            f.write(cleaned_text)
                            logger.error("Saved problematic JSON to: %s", f.name)
                        
                        raise HTTPException(
                            status_code=502,
                            detail=f"Failed to parse agent specifications from Claude response: {str(e)}. Check logs for details."
                        )
            
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise HTTPException(
                status_code=502,
                detail=f"Failed to extract or parse agent specifications from Claude response: {str(e)}"
            )
        
        # Validate that we have a list
        if not isinstance(agent_specs_data, list):
            raise HTTPException(
                status_code=502,
                detail="Claude response did not contain a JSON array of agent specifications"
            )
        
        # Validate and convert each item to AgentSpecificationResponse
        validated_agents = []
        for idx, agent_data in enumerate(agent_specs_data):
            try:
                agent_spec = AgentSpecificationResponse(**agent_data)
                validated_agents.append(agent_spec)
            except Exception as e:
                raise HTTPException(
                    status_code=502,
                    detail=f"Failed to validate agent specification at index {idx}: {str(e)}"
                )
        
        return validated_agents
        
    except httpx.RequestError as e:
        # Network errors
        raise HTTPException(
            status_code=503,
            detail=f"Network error when calling Claude API: {str(e)}"
        )
    except httpx.TimeoutException:
        # Timeout errors
        raise HTTPException(
            status_code=504,
            detail="Request to Claude API timed out after 120 seconds"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error in Claude service: {str(e)}"
        )
