from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json
import yaml
import uuid
from pathlib import Path
from datetime import datetime

app = FastAPI(title="Agent Creator Service", description="Create and manage AI agents")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AGENTS_DIR = Path("/uploads/agents")
AGENTS_DIR.mkdir(parents=True, exist_ok=True)


class Tool(BaseModel):
    name: str
    description: str
    parameters: Optional[Dict] = {}


class Agent(BaseModel):
    name: str = Field(..., description="Name of the agent")
    description: str = Field(..., description="Description of what the agent does")
    system_prompt: str = Field(..., description="System prompt for the agent")
    model: str = Field(default="gpt-4", description="AI model to use")
    temperature: float = Field(default=0.7, ge=0, le=2)
    tools: List[Tool] = Field(default=[], description="Tools available to the agent")
    capabilities: List[str] = Field(default=[], description="Agent capabilities")


class AgentResponse(BaseModel):
    agent_id: str
    name: str
    description: str
    created_at: str
    config: Dict


# In-memory storage (in production, use a database)
agents_store: Dict[str, Dict] = {}


def generate_agent_config(agent: Agent) -> Dict:
    """Generate agent configuration."""
    return {
        "name": agent.name,
        "description": agent.description,
        "model": agent.model,
        "temperature": agent.temperature,
        "system_prompt": agent.system_prompt,
        "tools": [tool.dict() for tool in agent.tools],
        "capabilities": agent.capabilities,
        "created_at": datetime.utcnow().isoformat()
    }


def save_agent_config(agent_id: str, config: Dict):
    """Save agent configuration to file."""
    # Save as JSON
    json_path = AGENTS_DIR / f"{agent_id}.json"
    with open(json_path, "w") as f:
        json.dump(config, f, indent=2)
    
    # Save as YAML
    yaml_path = AGENTS_DIR / f"{agent_id}.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


@app.get("/")
async def root():
    return {
        "service": "Agent Creator Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/agents/create", response_model=AgentResponse)
async def create_agent(agent: Agent):
    """Create a new agent configuration."""
    agent_id = str(uuid.uuid4())
    
    # Generate configuration
    config = generate_agent_config(agent)
    
    # Store agent
    agents_store[agent_id] = {
        "id": agent_id,
        "config": config
    }
    
    # Save to file
    save_agent_config(agent_id, config)
    
    return AgentResponse(
        agent_id=agent_id,
        name=agent.name,
        description=agent.description,
        created_at=config["created_at"],
        config=config
    )


@app.get("/agents/list")
async def list_agents():
    """List all created agents."""
    return {
        "agents": [
            {
                "agent_id": agent_id,
                "name": data["config"]["name"],
                "description": data["config"]["description"],
                "created_at": data["config"]["created_at"]
            }
            for agent_id, data in agents_store.items()
        ],
        "total": len(agents_store)
    }


@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent configuration."""
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agents_store[agent_id]


@app.put("/agents/{agent_id}")
async def update_agent(agent_id: str, agent: Agent):
    """Update agent configuration."""
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Generate new configuration
    config = generate_agent_config(agent)
    
    # Update store
    agents_store[agent_id]["config"] = config
    
    # Save to file
    save_agent_config(agent_id, config)
    
    return {
        "agent_id": agent_id,
        "config": config,
        "message": "Agent updated successfully"
    }


@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent."""
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Remove from store
    del agents_store[agent_id]
    
    # Delete files
    json_path = AGENTS_DIR / f"{agent_id}.json"
    yaml_path = AGENTS_DIR / f"{agent_id}.yaml"
    
    if json_path.exists():
        json_path.unlink()
    if yaml_path.exists():
        yaml_path.unlink()
    
    return {"message": "Agent deleted successfully"}


@app.get("/agents/templates/list")
async def list_templates():
    """List available agent templates."""
    templates = [
        {
            "id": "customer-support",
            "name": "Customer Support Agent",
            "description": "An agent designed to handle customer support queries",
            "capabilities": ["text-understanding", "response-generation", "sentiment-analysis"]
        },
        {
            "id": "data-analyst",
            "name": "Data Analyst Agent",
            "description": "An agent that can analyze data and generate insights",
            "capabilities": ["data-analysis", "visualization", "reporting"]
        },
        {
            "id": "code-reviewer",
            "name": "Code Reviewer Agent",
            "description": "An agent that reviews code and provides feedback",
            "capabilities": ["code-analysis", "best-practices", "security-check"]
        }
    ]
    
    return {"templates": templates}


@app.post("/agents/templates/{template_id}")
async def create_from_template(template_id: str):
    """Create an agent from a template."""
    templates = {
        "customer-support": Agent(
            name="Customer Support Agent",
            description="Handles customer support queries with empathy and efficiency",
            system_prompt="You are a helpful customer support agent. Be empathetic, clear, and solution-oriented.",
            model="gpt-4",
            temperature=0.7,
            capabilities=["text-understanding", "response-generation", "sentiment-analysis"]
        ),
        "data-analyst": Agent(
            name="Data Analyst Agent",
            description="Analyzes data and generates actionable insights",
            system_prompt="You are a data analyst. Analyze data carefully and provide clear, actionable insights.",
            model="gpt-4",
            temperature=0.5,
            capabilities=["data-analysis", "visualization", "reporting"]
        ),
        "code-reviewer": Agent(
            name="Code Reviewer Agent",
            description="Reviews code for quality, security, and best practices",
            system_prompt="You are a code reviewer. Review code for quality, security, and adherence to best practices.",
            model="gpt-4",
            temperature=0.3,
            capabilities=["code-analysis", "best-practices", "security-check"]
        )
    }
    
    if template_id not in templates:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return await create_agent(templates[template_id])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "agent-creator"}
