from core.schema import FinalResponse, ExecutionResult

def verify_execution(execution: ExecutionResult) -> FinalResponse:
    issues = []
    verified_output = []

    for r in execution.results:
        if not r.success:
            issues.append(f"{r.tool} failed: {r.error}")
        else:
            verified_output.append({r.tool: r.data})

    status = "success" if not issues else "partial_success"

    return FinalResponse(
        status=status,
        verified_output=verified_output,
        issues=issues if issues else None
    )
