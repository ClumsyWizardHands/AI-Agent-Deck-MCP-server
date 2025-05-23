from pydantic import BaseModel, Field
from typing import Optional, List

class EmpireDescriptionRequest(BaseModel):
    """
    Pydantic model for empire description request.
    Used to capture comprehensive information about an organization/empire
    for generating agent specifications.
    """
    empire_name: str = Field(..., description="Name of the empire/organization")
    primary_focus_domains: list[str] = Field(
        ..., 
        min_length=1, 
        description="Primary focus domains (must contain at least one item)"
    )
    main_goals: list[str] = Field(
        ..., 
        min_length=1, 
        description="Main goals of the empire (must contain at least one item)"
    )
    available_resources: list[str] = Field(
        ..., 
        description="Available resources for the empire"
    )
    core_principles: list[str] = Field(
        ..., 
        description="Core principles guiding the empire"
    )
    key_challenges: list[str] = Field(
        ..., 
        min_length=1, 
        description="Key challenges faced by the empire (must contain at least one element)"
    )
    resentments: Optional[list[str]] = Field(
        None,
        description="Unmet needs, grievances, perceived injustices that influence behavior"
    )
    emotions: Optional[list[str]] = Field(
        None,
        description="Emotional states that influence decisions"
    )
    operational_style: Optional[str] = Field(
        None, 
        description="Operational style of the empire"
    )
    key_processes_or_workflows: Optional[list[str]] = Field(
        None, 
        description="Key processes or workflows used by the empire"
    )
    desired_agent_capabilities: Optional[list[str]] = Field(
        None, 
        description="Desired capabilities for agents"
    )


class AgentSpecificationResponse(BaseModel):
    """
    Pydantic model for agent specification response.
    Contains detailed specifications for an AI agent tailored to empire needs.
    """
    agent_id: str = Field(..., description="Unique identifier for the agent")
    agent_name: str = Field(..., description="Name of the agent")
    agent_purpose_and_tasks: str = Field(
        ..., 
        description="Purpose and tasks the agent will perform"
    )
    linked_empire_need_or_component: str = Field(
        ..., 
        description="Specific empire need or component this agent addresses"
    )
    suggested_technical_approach: str = Field(
        ..., 
        description="Suggested technical approach for implementing the agent"
    )
    estimated_complexity_to_build: str = Field(
        ..., 
        description="Estimated complexity level to build this agent"
    )
    key_data_inputs: list[str] = Field(
        ..., 
        description="Key data inputs required by the agent"
    )
    key_data_outputs_or_actions: list[str] = Field(
        ..., 
        description="Key data outputs or actions the agent will produce"
    )
    potential_dependencies_or_integrations: Optional[list[str]] = Field(
        None, 
        description="Potential dependencies or integrations needed"
    )


class ExtendedEmpireDescription(BaseModel):
    """
    Extended empire description model with psychological and strategic dimensions.
    Captures a richer, more nuanced view of an empire including emotional and identity aspects.
    """
    empire_name_and_description: str = Field(
        ..., 
        description="Full empire name and comprehensive description"
    )
    ends: List[str] = Field(
        ..., 
        min_items=1,
        description="What the empire seeks to make real"
    )
    means: List[str] = Field(
        ..., 
        min_items=1,
        description="Tools and capacities at the empire's disposal"
    )
    principles: List[str] = Field(
        ..., 
        min_items=1,
        description="Deep structural drivers of behavior"
    )
    identity: List[str] = Field(
        ..., 
        min_items=1,
        description="Stories that shape the empire's actions"
    )
    resentments: List[str] = Field(
        ..., 
        min_items=1,
        description="What haunts or drives the empire"
    )
    emotions: List[str] = Field(
        ..., 
        min_items=1,
        description="Strategic emotional patterns"
    )
