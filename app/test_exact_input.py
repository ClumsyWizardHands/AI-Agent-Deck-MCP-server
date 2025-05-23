"""Test with exact user input to reproduce the issue."""

import asyncio
import json
from app.config import Settings
from app.models import ExtendedEmpireDescription
from app.main import convert_extended_to_standard
from app.claude_service import get_claude_suggestions

async def test_exact_input():
    """Test with the exact input the user is entering."""
    settings = Settings()
    
    # Exact input from the user
    extended_empire = ExtendedEmpireDescription(
        empire_name_and_description="The Architect of Cognitive Coalitions\nBrett Horvath's empire centers around strategic foresight, cognitive infrastructure, and narrative weaponry for emergent coalitions navigating high-stakes informational conflict. Positioned at the nexus of governance, AI, media theory, and civilizational risk, Horvath's empire operates as both systems architect and field strategist, fusing deep epistemic insight with practical AI-era alliance building. He blends narrative hacking, empire modeling, and power diagnostics into infrastructure for cognitive sovereignty.",
        ends=[
            "Establish durable, AI-literate democratic coalitions that can govern in contested information environments."
        ],
        means=[
            "Empire modeling systems that synthesize relational game theory, scenario arcs, structural inference, and cognitive war diagnostics."
        ],
        principles=[
            "Narrative Determines Reality: Systems and societies are built on story before law or code."
        ],
        identity=[
            "I build cognitive infrastructure for coalitions that don't realize they're already at war."
        ],
        resentments=[
            "Resentment of AI naiveté among civil society allies—especially those who treat AI as neutral or merely technical."
        ],
        emotions=[
            "Sorrow for the loss of meaning and memory across digital public spheres"
        ]
    )
    
    # Convert to standard format
    standard_empire = convert_extended_to_standard(extended_empire)
    
    print("Converted Empire:")
    print(json.dumps(standard_empire.model_dump(), indent=2))
    
    # Call Claude
    print("\nCalling Claude API...")
    try:
        with open(settings.MASTER_PROMPT_PATH, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
            
        agent_specs = await get_claude_suggestions(
            empire_data=standard_empire,
            api_key=settings.CLAUDE_API_KEY,
            prompt_template_str=prompt_template
        )
        
        print(f"\nSuccess! Generated {len(agent_specs)} agents")
        
    except Exception as e:
        print(f"\nError occurred: {type(e).__name__}: {e}")
        
        # Check the latest saved JSON
        import os
        json_files = [f for f in os.listdir('.') if f.endswith('.json') and f.startswith('tmp')]
        if json_files:
            latest = max(json_files, key=lambda f: os.path.getmtime(f))
            print(f"\nChecking {latest}...")
            
            with open(latest, 'r') as f:
                content = f.read()
                print(f"File length: {len(content)} characters")
                print(f"Ends with ']': {content.strip().endswith(']')}")
                
                # Count opening and closing brackets
                open_brackets = content.count('[')
                close_brackets = content.count(']')
                open_braces = content.count('{')
                close_braces = content.count('}')
                
                print(f"Brackets: [ {open_brackets} ] {close_brackets}")
                print(f"Braces: {{ {open_braces} }} {close_braces}")

if __name__ == "__main__":
    asyncio.run(test_exact_input())
