import json
import re
from llm.gemini_llm import call_llm
from core.schema import Plan
from core.tool_registry import ToolRegistry

def _extract_city(text: str):
    """Simple but reliable city extractor"""
    cities = ["mumbai", "delhi", "pune", "bangalore", "chennai"]
    for city in cities:
        if city in text.lower():
            return city.capitalize()
    return None

def _extract_news_topic(text: str):
    """
    Extract topic AFTER words like 'news about', 'updates on', 'headlines for'
    """
    patterns = [
        r"news about (.+)",
        r"updates on (.+)",
        r"headlines about (.+)",
        r"recent news about (.+)",
        r"latest news about (.+)"
    ]

    for p in patterns:
        match = re.search(p, text.lower())
        if match:
            return match.group(1).strip()

    # Default fallback
    return "Artificial Intelligence"

def _rule_based_plan(user_task: str):
    """
    Local fallback planner (works even when Gemini quota is exhausted)
    """
    steps = []
    text = user_task.lower()

    city = _extract_city(text)
    topic = _extract_news_topic(text)

    if city:
        steps.append({
            "action": "weather_tool",
            "input": {"city": city}
        })

    if "news" in text:
        steps.append({
            "action": "news_tool",
            "input": {"query": topic}
        })

    # If nothing detected, still return a safe default
    if not steps:
        steps = [
            {"action": "weather_tool", "input": {"city": "Mumbai"}}
        ]

    return Plan(steps=steps)

def generate_plan(user_task: str) -> Plan:
    available_tools = ToolRegistry.list_tools()

    prompt = f"""
    You are a Planner Agent.

    Task: "{user_task}"

    Available tools: {available_tools}

    You must create MULTIPLE steps if the user asks for multiple things.

    Output ONLY valid JSON in this format:

    {{
      "steps": [
        {{"action": "tool_name", "input": {{"key": "value"}}}}
      ]
    }}
    """

    raw = call_llm(prompt)

    # If Gemini quota is exhausted → use local planner
    if raw == "LLM_QUOTA_EXHAUSTED":
        print("⚠️ Gemini quota exhausted — using rule-based planner")
        return _rule_based_plan(user_task)

    if raw.startswith("LLM_ERROR"):
        raise ValueError(raw)

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No JSON found in LLM response")

        plan_json = raw[start:end]
        plan_dict = json.loads(plan_json)

        # If LLM gives only one step but user clearly asked for two, fix it
        if len(plan_dict.get("steps", [])) == 1:
            print("⚠️ LLM missed some steps — enriching with rule-based planner")
            fallback_plan = _rule_based_plan(user_task)
            return fallback_plan

        return Plan(**plan_dict)

    except Exception as e:
        print(f"⚠️ Planner parsing failed — fallback used: {e}")
        return _rule_based_plan(user_task)
