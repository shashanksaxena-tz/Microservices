from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import json
import uuid
from pathlib import Path
from datetime import datetime
from jinja2 import Template
import os

app = FastAPI(title="MCP Creator Service", description="Model Context Protocol API Creator")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MCP_DIR = Path(os.getenv("UPLOAD_DIR", "/uploads")) / "mcp"
MCP_DIR.mkdir(parents=True, exist_ok=True)


class Field_Model(BaseModel):
    name: str
    type: str  # string, integer, float, boolean, date, etc.
    required: bool = True
    description: Optional[str] = None


class MCPResource(BaseModel):
    name: str = Field(..., description="Resource name (e.g., 'user', 'product')")
    description: str = Field(..., description="Description of the resource")
    fields: List[Field_Model] = Field(..., description="Fields of the resource")
    enable_create: bool = Field(default=True)
    enable_read: bool = Field(default=True)
    enable_update: bool = Field(default=True)
    enable_delete: bool = Field(default=True)
    enable_list: bool = Field(default=True)


class MCPProject(BaseModel):
    project_name: str = Field(..., description="Name of the API project")
    description: str = Field(..., description="Project description")
    base_path: str = Field(default="/api/v1", description="API base path")
    resources: List[MCPResource] = Field(..., description="Resources to create")


# In-memory storage
mcp_projects: Dict[str, Dict] = {}


def generate_fastapi_code(project: MCPProject) -> str:
    """Generate FastAPI code for CRUD operations."""
    
    template = '''from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

app = FastAPI(title="{{ project_name }}", description="{{ description }}")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
storage: Dict[str, Dict[str, Any]] = {}

{% for resource in resources %}
# {{ resource.name | title }} Models
class {{ resource.name | title }}Base(BaseModel):
    {% for field in resource.fields %}
    {{ field.name }}: {{ field.type | python_type }}{{ " = None" if not field.required else "" }}  # {{ field.description or "" }}
    {% endfor %}

class {{ resource.name | title }}Create({{ resource.name | title }}Base):
    pass

class {{ resource.name | title }}Update(BaseModel):
    {% for field in resource.fields %}
    {{ field.name }}: Optional[{{ field.type | python_type }}] = None
    {% endfor %}

class {{ resource.name | title }}Response({{ resource.name | title }}Base):
    id: str
    created_at: str
    updated_at: str

# {{ resource.name | title }} storage
{{ resource.name }}_storage: Dict[str, Dict] = {}

{% if resource.enable_create %}
@app.post("{{ base_path }}/{{ resource.name }}", response_model={{ resource.name | title }}Response)
async def create_{{ resource.name }}({{ resource.name }}: {{ resource.name | title }}Create):
    """Create a new {{ resource.name }}."""
    {{ resource.name }}_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    {{ resource.name }}_data = {
        "id": {{ resource.name }}_id,
        **{{ resource.name }}.dict(),
        "created_at": now,
        "updated_at": now
    }
    
    {{ resource.name }}_storage[{{ resource.name }}_id] = {{ resource.name }}_data
    return {{ resource.name }}_data
{% endif %}

{% if resource.enable_read %}
@app.get("{{ base_path }}/{{ resource.name }}/{{"{"}}{{ resource.name }}_id{{"}"}}", response_model={{ resource.name | title }}Response)
async def get_{{ resource.name }}({{ resource.name }}_id: str):
    """Get {{ resource.name }} by ID."""
    if {{ resource.name }}_id not in {{ resource.name }}_storage:
        raise HTTPException(status_code=404, detail="{{ resource.name | title }} not found")
    return {{ resource.name }}_storage[{{ resource.name }}_id]
{% endif %}

{% if resource.enable_list %}
@app.get("{{ base_path }}/{{ resource.name }}", response_model=List[{{ resource.name | title }}Response])
async def list_{{ resource.name }}s(skip: int = 0, limit: int = 100):
    """List all {{ resource.name }}s."""
    items = list({{ resource.name }}_storage.values())
    return items[skip:skip + limit]
{% endif %}

{% if resource.enable_update %}
@app.put("{{ base_path }}/{{ resource.name }}/{{"{"}}{{ resource.name }}_id{{"}"}}", response_model={{ resource.name | title }}Response)
async def update_{{ resource.name }}({{ resource.name }}_id: str, {{ resource.name }}_update: {{ resource.name | title }}Update):
    """Update {{ resource.name }}."""
    if {{ resource.name }}_id not in {{ resource.name }}_storage:
        raise HTTPException(status_code=404, detail="{{ resource.name | title }} not found")
    
    {{ resource.name }}_data = {{ resource.name }}_storage[{{ resource.name }}_id]
    update_data = {{ resource.name }}_update.dict(exclude_unset=True)
    
    {{ resource.name }}_data.update(update_data)
    {{ resource.name }}_data["updated_at"] = datetime.utcnow().isoformat()
    
    {{ resource.name }}_storage[{{ resource.name }}_id] = {{ resource.name }}_data
    return {{ resource.name }}_data
{% endif %}

{% if resource.enable_delete %}
@app.delete("{{ base_path }}/{{ resource.name }}/{{"{"}}{{ resource.name }}_id{{"}"}}") 
async def delete_{{ resource.name }}({{ resource.name }}_id: str):
    """Delete {{ resource.name }}."""
    if {{ resource.name }}_id not in {{ resource.name }}_storage:
        raise HTTPException(status_code=404, detail="{{ resource.name | title }} not found")
    
    del {{ resource.name }}_storage[{{ resource.name }}_id]
    return {"message": "{{ resource.name | title }} deleted successfully"}
{% endif %}

{% endfor %}

@app.get("/")
async def root():
    return {
        "service": "{{ project_name }}",
        "version": "1.0.0",
        "resources": {{ resources | map(attribute='name') | list | tojson }}
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
'''
    
    def python_type_filter(field_type: str) -> str:
        """Convert field type to Python type."""
        type_map = {
            "string": "str",
            "integer": "int",
            "float": "float",
            "boolean": "bool",
            "date": "str",
            "datetime": "str",
            "email": "str",
            "url": "str"
        }
        return type_map.get(field_type.lower(), "str")
    
    # Add filter to environment instead of globals if possible, or use environment
    from jinja2 import Environment
    env = Environment()
    env.filters['python_type'] = python_type_filter
    jinja_template = env.from_string(template)
    
    return jinja_template.render(
        project_name=project.project_name,
        description=project.description,
        base_path=project.base_path,
        resources=[r.dict() for r in project.resources]
    )


def generate_docker_files(project: MCPProject) -> Dict[str, str]:
    """Generate Dockerfile and requirements.txt."""
    
    dockerfile = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
'''
    
    requirements = '''fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
python-multipart==0.0.6
'''
    
    return {
        "Dockerfile": dockerfile,
        "requirements.txt": requirements
    }


@app.get("/")
async def root():
    return {
        "service": "MCP Creator Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/mcp/create")
async def create_mcp_project(project: MCPProject):
    """Create a new MCP (Model Context Protocol) CRUD API project."""
    project_id = str(uuid.uuid4())
    
    # Generate code
    api_code = generate_fastapi_code(project)
    docker_files = generate_docker_files(project)
    
    # Create project directory
    project_dir = MCP_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Save files
    (project_dir / "main.py").write_text(api_code)
    (project_dir / "Dockerfile").write_text(docker_files["Dockerfile"])
    (project_dir / "requirements.txt").write_text(docker_files["requirements.txt"])
    
    # Save project metadata
    metadata = {
        "project_id": project_id,
        "project_name": project.project_name,
        "description": project.description,
        "base_path": project.base_path,
        "resources": [r.dict() for r in project.resources],
        "created_at": datetime.utcnow().isoformat()
    }
    
    (project_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    
    # Store in memory
    mcp_projects[project_id] = metadata
    
    return {
        "project_id": project_id,
        "project_name": project.project_name,
        "description": project.description,
        "files_generated": ["main.py", "Dockerfile", "requirements.txt", "metadata.json"],
        "download_url": f"/mcp/download/{project_id}",
        "metadata": metadata
    }


@app.get("/mcp/list")
async def list_mcp_projects():
    """List all created MCP projects."""
    return {
        "projects": [
            {
                "project_id": pid,
                "project_name": data["project_name"],
                "description": data["description"],
                "created_at": data["created_at"]
            }
            for pid, data in mcp_projects.items()
        ],
        "total": len(mcp_projects)
    }


@app.get("/mcp/{project_id}")
async def get_mcp_project(project_id: str):
    """Get MCP project details."""
    if project_id not in mcp_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_dir = MCP_DIR / project_id
    
    # Read generated files
    files = {}
    for file in ["main.py", "Dockerfile", "requirements.txt"]:
        file_path = project_dir / file
        if file_path.exists():
            files[file] = file_path.read_text()
    
    return {
        "project_id": project_id,
        "metadata": mcp_projects[project_id],
        "files": files
    }


@app.get("/mcp/code/{project_id}")
async def get_generated_code(project_id: str):
    """Get generated code for a project."""
    project_dir = MCP_DIR / project_id
    main_file = project_dir / "main.py"
    
    if not main_file.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project_id,
        "code": main_file.read_text()
    }


@app.delete("/mcp/{project_id}")
async def delete_mcp_project(project_id: str):
    """Delete an MCP project."""
    if project_id not in mcp_projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Remove from storage
    del mcp_projects[project_id]
    
    return {"message": "Project deleted successfully"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mcp-creator"}
