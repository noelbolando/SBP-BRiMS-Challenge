# llm_agent_pipeline/process_tick_data.py

import os
import json
from pathlib import Path

# --- Config ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENT_LOG_DIR = PROJECT_ROOT / "netlogo" / "llm_agent_logs"
DECISION_DIR = PROJECT_ROOT / "llm_agent_pipeline" / "decisions"
DECISION_DIR.mkdir(parents=True, exist_ok=True)

def get_latest_tick_file():
    files = sorted(AGENT_LOG_DIR.glob("agents_tick_*.json"), key=os.path.getmtime, reverse=True)
    return files[0] if files else None

def build_prompt(agent):
    """Create a deterministic prompt based on agent's state and surroundings."""
    return f"""
You are an agent in a disease simulation.
Your current state is: {agent['state']}
You are {'wearing a mask' if agent['masked'] else 'not wearing a mask'}.
You are {'at home' if agent['home'] else 'outside'}.
Your current position is: (x={agent['x']}, y={agent['y']})
It is currently tick {agent['tick']}.

Decide your next move. You may choose to:
- MOVE_FORWARD
- ROTATE_LEFT
- ROTATE_RIGHT
- STAY

Respond ONLY with your decision in all caps (e.g., "MOVE_FORWARD").
    """.strip()

def process_tick_data():
    tick_file = get_latest_tick_file()
    if not tick_file:
        print("No agent log files found.")
        return

    with open(tick_file, "r") as f:
        agent_data = json.load(f)

    decisions = []
    for agent in agent_data:
        agent_id = agent["unique_id"]
        prompt = build_prompt(agent)
        decisions.append({
            "agent_id": agent_id,
            "tick": agent["tick"],
            "prompt": prompt,
            "decision": None  # To be filled after querying LLM
        })

    output_file = DECISION_DIR / f"decisions_tick_{agent_data[0]['tick']}.json"
    with open(output_file, "w") as f:
        json.dump(decisions, f, indent=2)

    print(f"✅ Prompts written to: {output_file}")

if __name__ == "__main__":
    process_tick_data()
