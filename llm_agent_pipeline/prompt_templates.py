# llm_agent_pipeline/prompt_template.py

def build_prompt(agent: dict) -> str:
    return f"""
You are an autonomous agent in a pandemic simulation.

Your current state:
- Unique ID: {agent["unique_id"]}
- Health State: {agent["state"]}
- Masked: {"Yes" if agent["masked"] else "No"}
- At Home: {"Yes" if agent["home"] else "No"}
- Position: ({agent["x"]}, {agent["y"]})
- Current Tick: {agent["tick"]}

Rules:
- You must move unless you're at home and sick.
- Symptomatic infected agents (IS) must stay home.
- Recovered agents can leave home.
- Masked agents reduce infection risk.
- Your goal is to minimize infections and recover safely.

Decide your next action: "move", "stay", or "seek-mask".
Respond ONLY with one of those actions.
"""