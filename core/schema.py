from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class Step(BaseModel):
    action: str
    input: Dict[str, Any]

class Plan(BaseModel):
    steps: List[Step]

class ToolResult(BaseModel):
    tool: str
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class ExecutionResult(BaseModel):
    results: List[ToolResult]

class FinalResponse(BaseModel):
    status: str
    verified_output: Any
    issues: Optional[List[str]] = None
