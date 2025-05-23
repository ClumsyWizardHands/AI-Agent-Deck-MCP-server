"""Test with comprehensive multi-field empire description."""

import asyncio
import json
from app.config import Settings
from app.models import ExtendedEmpireDescription
from app.main import convert_extended_to_standard
from app.claude_service import get_claude_suggestions

async def test_comprehensive():
    """Test with a comprehensive empire description with multiple entries per field."""
    settings = Settings()
    
    # Create a comprehensive empire with multiple entries in each field
    extended_empire = ExtendedEmpireDescription(
        empire_name_and_description="The Architect of Cognitive Coalitions\nBrett Horvath's empire centers around strategic foresight, cognitive infrastructure, and narrative weaponry for emergent coalitions navigating high-stakes informational conflict. Positioned at the nexus of governance, AI, media theory, and civilizational risk, Horvath's empire operates as both systems architect and field strategist, fusing deep epistemic insight with practical AI-era alliance building. He blends narrative hacking, empire modeling, and power diagnostics into infrastructure for cognitive sovereignty.",
        
        ends=[
            "Establish durable, AI-literate democratic coalitions that can govern in contested information environments",
            "Build a new class of strategic cognition infrastructure that can operate across AI-native, hybrid, and legacy systems",
            "Create narrative immune systems that protect democratic discourse from weaponized disinformation",
            "Develop anticipatory governance frameworks for emerging AI capabilities and risks",
            "Foster cognitive sovereignty for individuals and communities in the attention economy"
        ],
        
        means=[
            "Empire modeling systems that synthesize relational game theory, scenario arcs, structural inference, and cognitive war diagnostics",
            "Narrative warfare frameworks that map and counter adversarial information flows and psychographic persuasion tactics",
            "AI literacy curricula designed for civil society organizations and democratic institutions",
            "Strategic foresight methodologies adapted for high-uncertainty, high-stakes environments",
            "Coalition-building protocols that bridge technical and non-technical stakeholder groups",
            "Cognitive infrastructure toolkits for resilient decision-making under information warfare conditions"
        ],
        
        principles=[
            "Narrative Determines Reality: Systems and societies are built on story before law or code",
            "Infrastructure Is Power: Whoever controls the epistemic or infrastructural layer of a system controls what is considered real within it",
            "Coalitions Over Solutions: In contested environments, the quality of alliances matters more than technical optimality",
            "Memory Is Resistance: Preserving institutional and cultural memory is a form of cognitive defense",
            "Strategic Empathy: Understanding adversarial worldviews without adopting them is essential for effective counter-strategy"
        ],
        
        identity=[
            "I build cognitive infrastructure for coalitions that don't realize they're already at war",
            "I don't ask whether AI will replace us. I ask how we've already been replaced",
            "My job isn't to predict the future. It's to help people remember how they've already been shaped by it",
            "I architect systems that make democracy antifragile to information warfare",
            "I translate between the languages of power: technical, political, narrative, and strategic"
        ],
        
        resentments=[
            "Contempt for narrative manipulators and accelerationists who deploy cognitive weapons without care for the consequences",
            "Frustration with technologists who treat political and social dynamics as edge cases rather than core constraints",
            "Anger at the systematic dismantling of public sense-making infrastructure",
            "Resentment of AI naiveté among civil society allies—especially those who treat AI as neutral or merely technical",
            "Disdain for strategic actors who exploit democratic openness while operating from authoritarian safe havens"
        ],
        
        emotions=[
            "Sorrow for the loss of meaning and memory across digital public spheres",
            "Quiet rage at infrastructural erasure—the way powerful truths disappear if not structurally preserved",
            "Deep concern for the cognitive health of democratic coalitions under sustained information attack",
            "Cautious hope that new forms of collective intelligence can emerge from current chaos",
            "Fierce protectiveness toward the communities and institutions working to preserve human agency"
        ]
    )
    
    # Print empire details
    print("Extended Empire Description:")
    print(f"Empire: {extended_empire.empire_name_and_description[:100]}...")
    print(f"Ends: {len(extended_empire.ends)}")
    print(f"Means: {len(extended_empire.means)}")
    print(f"Principles: {len(extended_empire.principles)}")
    print(f"Identity: {len(extended_empire.identity)}")
    print(f"Resentments: {len(extended_empire.resentments)}")
    print(f"Emotions: {len(extended_empire.emotions)}")
    
    # Convert to JSON for prompt
    empire_json_str = extended_empire.model_dump_json()
    print(f"\nEmpire JSON length: {len(empire_json_str)} characters")
    
    # Load prompt and generate
    with open(settings.MASTER_PROMPT_PATH, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
    
    final_prompt = prompt_template.replace("{{empire_description_json}}", empire_json_str)
    print(f"Final prompt length: {len(final_prompt)} characters")
    
    # Call Claude
    print("\nCalling Claude API with comprehensive empire...")
    try:
        agent_specs = await get_claude_suggestions(
            empire_data=extended_empire,
            api_key=settings.CLAUDE_API_KEY,
            prompt_template_str=prompt_template
        )
        
        print(f"\nSuccess! Generated {len(agent_specs)} agents")
        
        # Print each agent card
        print("\n" + "="*80)
        print("AGENT CARDS:")
        print("="*80)
        
        for i, agent in enumerate(agent_specs, 1):
            print(f"\n--- Agent {i}/{len(agent_specs)} ---")
            print(f"ID: {agent.agent_id}")
            print(f"Name: {agent.agent_name}")
            print(f"Complexity: {agent.estimated_complexity_to_build}")
            print(f"\nPurpose: {agent.agent_purpose_and_tasks}")
            print(f"\nLinked to: {agent.linked_empire_need_or_component}")
            print(f"\nTechnical Approach: {agent.suggested_technical_approach}")
            print(f"\nInputs: {', '.join(agent.key_data_inputs)}")
            print(f"Outputs: {', '.join(agent.key_data_outputs_or_actions)}")
            if agent.potential_dependencies_or_integrations:
                print(f"Dependencies: {', '.join(agent.potential_dependencies_or_integrations)}")
        
        print("\n" + "="*80)
        print(f"TOTAL AGENTS GENERATED: {len(agent_specs)}")
        print("="*80)
            
    except Exception as e:
        print(f"\nError occurred: {type(e).__name__}: {e}")
        
        # Check if there's a saved problematic JSON
        import os
        json_files = [f for f in os.listdir('.') if f.endswith('.json') and f.startswith('tmp')]
        if json_files:
            latest = max(json_files, key=lambda f: os.path.getmtime(f))
            with open(latest, 'r') as f:
                content = f.read()
            print(f"\nProblematic JSON saved to: {latest}")
            print(f"File size: {len(content)} bytes")
            print(f"Last 100 chars: ...{content[-100:]}")

if __name__ == "__main__":
    asyncio.run(test_comprehensive())
