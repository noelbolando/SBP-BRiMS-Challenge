import json
import os
import sys
import requests

def llm(prompt: str) -> str:
    """LLM caller."""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip().lower()

def build_prompt(agent: dict) -> str:
    """Prompt builder."""
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

Based on your current state, you must make a few decisions based on the following guidelines:
- You must move unless you're at home sick and symptomatically infectious.
- Symptomatically infected agents must stay home.
- Recovered agents must return to the community once they are no longer infectious.
- You must practice social distancing (put on a mask) if you are in a densely populated area such that you have 4 or more neighbors.
- Social distancing (mask wearing) is not required if you have less than 4 neighbors.

Decide your next combination of actions: "move" or "stay"; "mask on" or "mask off".
Respond with either combination of those two actions.
Keep your answers short and concise.
""".strip()

def process_agent_logs(log_path: str, out_dir: str):
    """Send agent states to LLM and process decisions."""
    with open(log_path, "r") as f:
        agents = json.load(f)

    decisions = []
    for agent in agents:
        prompt = build_prompt(agent)
        action = llm(prompt)
        decision = {
            "unique_id": agent["unique_id"],
            "tick": agent["tick"],
            "action": action,
        }
        decisions.append(decision)

    tick = agents[0]["tick"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"decisions_tick_{tick}.json")
    with open(out_path, "w") as f:
        json.dump(decisions, f, indent=2)

    print(f"Saved decisions for tick {tick} to {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python llm_agent_runner.py <tick_number>")
        sys.exit(1)

    tick = int(sys.argv[1])
    log_file = f"netlogo/llm_agent_logs/agents_tick_{tick}.json"
    process_agent_logs(log_file, "decisions")
