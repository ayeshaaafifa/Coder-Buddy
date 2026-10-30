from pydantic import BaseModel, Field
from typing import List, Optional

class File(BaseModel):
    file_path: str
    purpose: str

class Plan(BaseModel):
    app_name: str
    description: str
    tech_stack: str
    features: List[str]
    files: List[File]

class ImplementationTask(BaseModel):
    file_path: str
    task_description: str

class TaskPlan(BaseModel):
    implementation_steps: List[ImplementationTask]
    class Config:
        extra = "allow"
