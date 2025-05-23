"""Claude API service for generating agent suggestions."""

import json
from typing import List
import httpx
from fastapi import HTTPException
from app.models import EmpireDescriptionRequest, AgentSpecificationResponse


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
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4000,
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
            
            # Parse the JSON array from the text content
            agent_specs_data = json.loads(content_text)
            
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
