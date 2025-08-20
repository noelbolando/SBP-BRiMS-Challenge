# llm_agent_pipeline/prompt_template.py

def build_prompt(agent: dict) -> str:
    return f"""
You are an autonomous agent in an infectious disease outbreak. 

Please evaluate your current state:
- Unique ID: {agent["unique_id"]}
- Disease State: {agent["state"]}
- Masked: {"Yes" if agent["masked"] else "No"}
- At Home: {"Yes" if agent["home"] else "No"}
- Position: ({agent["x"]}, {agent["y"]})
- Current Tick: {agent["tick"]}

Where your disease state can be described with the following:
- "S" = susceptible to the infectious disease
- "IA" = infected asymptomatic
- "IS" = infected symptomatic
- "R" = recovered

Based on your current state, you must make a few decisions based on the following guidlines:
- You must move unless you're at home sick and symptomatically infectious.
- Symptomatically infected agents must stay home.
- Recovered agents must return to the community once they are no longer infectious. 
- You must practice social distancing (put on a mask) if you are in a densely populated area such that you have 4 or more neighbors.
- Social distancing (mask wearing) is not required if you have less than 4 neighbors.

Decide your next combination of actions: "move" or "stay"; "mask on" or "mask off".
Respond with either combination of those two actions. 
Keep your answers short and concise.
"""