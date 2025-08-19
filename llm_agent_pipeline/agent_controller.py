# llm_agent_pipeline/agent_controller.py

import json
import os

from llm_utils import llm #
from prompt_templates import build_prompt

def process_agent_logs(log_path: str, out_dir: str):
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

    # Write out all decisions
    tick = agents[0]["tick"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"decisions_tick_{tick}.json")
    with open(out_path, "w") as f:
        json.dump(decisions, f, indent=2)

    print(f"Saved decisions for tick {tick} to {out_path}")