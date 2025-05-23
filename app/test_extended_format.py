"""Test script to verify agent generation with extended empire format."""

import asyncio
import json
from app.config import Settings
from app.models import ExtendedEmpireDescription
from app.main import convert_extended_to_standard
from app.claude_service import get_claude_suggestions

async def test_extended_format():
    """Test agent generation with extended empire format like the UI uses."""
    settings = Settings()
    
    # Create a test empire in extended format (like the UI sends)
    extended_empire = ExtendedEmpireDescription(
        empire_name_and_description="Strategic Cognition Empire - A system for building cognitive infrastructure in the AI era",
        ends=[
            "Establish durable, AI-literate democratic coalitions that can govern in contested information environments",
            "Build a new class of strategic cognition infrastructure that can operate across AI-native, hybrid, and legacy systems"
        ],
        means=[
            "Narrative warfare frameworks that map and counter adversarial information flows and psychographic persuasion tactics",
            "Empire modeling systems that synthesize relational game theory, scenario arcs, structural inference, and cognitive war diagnostics"
        ],
        principles=[
            "Narrative Determines Reality: Systems and societies are built on story before law or code",
            "Infrastructure Is Power: Whoever controls the epistemic or infrastructural layer of a system controls what is considered real within it"
        ],
        identity=[
            "I don't ask whether AI will replace us. I ask how we've already been replaced.",
            "My job isn't to predict the future. It's to help people remember how they've already been shaped by it.",
            "I build cognitive infrastructure for coalitions that don't realize they're already at war."
        ],
        resentments=[
            "Contempt for narrative manipulators and accelerationists who deploy cognitive weapons without care for the consequences"
        ],
        emotions=[
            "Sorrow for the loss of meaning and memory across digital public spheres",
            "Quiet rage at infrastructural erasure—the way powerful truths disappear if not structurally preserved"
        ]
    )
    
    # Convert to standard format
    standard_empire = convert_extended_to_standard(extended_empire)
    
    print("Extended Empire converted to Standard Format:")
    print(f"Empire Name: {standard_empire.empire_name}")
    print(f"Domains: {standard_empire.primary_focus_domains}")
    print(f"Goals: {len(standard_empire.main_goals)}")
    print(f"Resources: {len(standard_empire.available_resources)}")
    print(f"Principles: {len(standard_empire.core_principles)}")
    print(f"Challenges: {len(standard_empire.key_challenges)}")
    
    # Convert to JSON for prompt
    empire_json_str = standard_empire.model_dump_json()
    print(f"\nEmpire JSON length: {len(empire_json_str)} characters")
    
    # Load prompt and generate
    with open(settings.MASTER_PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    final_prompt = prompt_template.replace("{{empire_description_json}}", empire_json_str)
    print(f"Final prompt length: {len(final_prompt)} characters")
    
    # Call Claude
    print("\nCalling Claude API...")
    try:
        agent_specs = await get_claude_suggestions(
            empire_data=standard_empire,
            api_key=settings.CLAUDE_API_KEY,
            prompt_template_str=prompt_template
        )
        
        print(f"\nSuccess! Generated {len(agent_specs)} agents")
        
        # Print first agent as sample
        if agent_specs:
            print("\nFirst agent:")
            print(f"ID: {agent_specs[0].agent_id}")
            print(f"Name: {agent_specs[0].agent_name}")
            print(f"Domain: {agent_specs[0].primary_domain_category}")
            
    except Exception as e:
        print(f"\nError occurred: {type(e).__name__}: {e}")
        
        # Check if there's a saved problematic JSON
        import os
        json_files = [f for f in os.listdir('.') if f.endswith('.json') and f.startswith('tmp')]
        if json_files:
            print(f"\nFound {len(json_files)} debug JSON files")
            latest = max(json_files, key=lambda f: os.path.getmtime(f))
            print(f"Latest: {latest}")
            
            # Check file size
            size = os.path.getsize(latest)
            print(f"File size: {size} bytes")

if __name__ == "__main__":
    asyncio.run(test_extended_format())
