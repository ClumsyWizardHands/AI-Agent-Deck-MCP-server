"""Test script to verify agent generation with actual prompt."""

import asyncio
import json
from app.config import Settings
from app.models import EmpireDescriptionRequest
import httpx

async def test_agent_generation():
    """Test agent generation with a sample empire description."""
    settings = Settings()
    
    # Load the actual prompt template
    with open(settings.MASTER_PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    # Create a simple test empire
    test_empire = EmpireDescriptionRequest(
        empire_name="Test Empire",
        primary_focus_domains=["technology", "governance"],
        main_goals=["Build AI literacy", "Establish democratic coalitions"],
        available_resources=["AI expertise", "Community networks"],
        core_principles=["Transparency", "Democratic participation"],
        key_challenges=["AI skepticism", "Information overload"],
        operational_style="Collaborative and educational",
        key_processes_or_workflows=["Education", "Coalition building"],
        desired_agent_capabilities=["Teaching", "Analysis", "Communication"]
    )
    
    # Convert to JSON and insert into prompt
    empire_json_str = test_empire.model_dump_json()
    final_prompt = prompt_template.replace("{{empire_description_json}}", empire_json_str)
    
    print(f"Prompt length: {len(final_prompt)} characters")
    
    claude_payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 20000,
        "messages": [
            {"role": "user", "content": final_prompt}
        ]
    }
    
    claude_api_url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": settings.CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    print("Testing agent generation with actual prompt...")
    print(f"Model: {claude_payload['model']}")
    print(f"Max tokens: {claude_payload['max_tokens']}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                claude_api_url,
                json=claude_payload,
                headers=headers,
                timeout=120.0
            )
        
        print(f"\nResponse status: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            
            # Print response metadata
            if "usage" in response_json:
                print(f"Tokens used: {response_json['usage']}")
            
            # Extract content
            if "content" in response_json and response_json["content"]:
                content = response_json["content"][0]["text"]
                print(f"Response length: {len(content)} characters")
                
                # Check if response looks truncated
                if not content.strip().endswith(']'):
                    print("WARNING: Response doesn't end with ']' - may be truncated!")
                
                # Find JSON boundaries
                start_idx = content.find('[')
                end_idx = content.rfind(']')
                
                if start_idx != -1 and end_idx != -1:
                    json_content = content[start_idx:end_idx + 1]
                    print(f"JSON content length: {len(json_content)} characters")
                    
                    # Try to parse
                    try:
                        agents = json.loads(json_content)
                        print(f"Successfully parsed {len(agents)} agents")
                        
                        # Print first agent as sample
                        if agents:
                            print("\nFirst agent sample:")
                            print(json.dumps(agents[0], indent=2)[:500] + "...")
                    except json.JSONDecodeError as e:
                        print(f"JSON parsing failed: {e}")
                        print(f"Error at position {e.pos}")
                        
                        # Save problematic JSON
                        with open("test_problematic.json", "w") as f:
                            f.write(json_content)
                        print("Saved problematic JSON to test_problematic.json")
                else:
                    print("Could not find JSON array boundaries")
                    
            else:
                print("No content in response")
                
        else:
            print(f"Error response: {response.text[:500]}")
            
    except Exception as e:
        print(f"Exception occurred: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_agent_generation())
