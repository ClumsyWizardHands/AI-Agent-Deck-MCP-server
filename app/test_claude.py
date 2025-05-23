"""Test script to verify Claude API connection and response limits."""

import asyncio
import json
from app.config import Settings
import httpx

async def test_claude_connection():
    """Test basic Claude API connection and response."""
    settings = Settings()
    
    # Simple test prompt that should generate a long response
    test_prompt = """Generate a JSON array with exactly 5 simple test objects. Each object should have:
- id (string)
- name (string)
- description (string - make this about 50 words)

Start with [ and end with ]. No other text."""
    
    claude_payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 20000,
        "messages": [
            {"role": "user", "content": test_prompt}
        ]
    }
    
    claude_api_url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": settings.CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    
    print("Testing Claude API connection...")
    print(f"Model: {claude_payload['model']}")
    print(f"Max tokens: {claude_payload['max_tokens']}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                claude_api_url,
                json=claude_payload,
                headers=headers,
                timeout=30.0
            )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            
            # Print response metadata
            if "usage" in response_json:
                print(f"Tokens used: {response_json['usage']}")
            
            # Extract and print content
            if "content" in response_json and response_json["content"]:
                content = response_json["content"][0]["text"]
                print(f"Response length: {len(content)} characters")
                print("Response content:")
                print("-" * 80)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("-" * 80)
                
                # Try to parse as JSON
                try:
                    parsed = json.loads(content)
                    print(f"Successfully parsed JSON with {len(parsed)} items")
                except json.JSONDecodeError as e:
                    print(f"JSON parsing failed: {e}")
            else:
                print("No content in response")
                print(f"Full response: {response_json}")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_claude_connection())
