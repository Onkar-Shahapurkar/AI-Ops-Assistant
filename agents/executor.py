from core.schema import ExecutionResult, ToolResult
from core.tool_registry import ToolRegistry

def execute_plan(plan):
    results = []

    for step in plan.steps:
        tool_name = step.action
        params = step.input

        try:
            tool_cls = ToolRegistry.get(tool_name)
            tool = tool_cls()
            output = tool.run(**params)

            results.append(ToolResult(
                tool=tool_name,
                success=True,
                data=output
            ))

        except Exception as e:
            results.append(ToolResult(
                tool=tool_name,
                success=False,
                error=str(e)
            ))

    return ExecutionResult(results=results)
