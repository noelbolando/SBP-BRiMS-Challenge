# llm_agent_pipeline/runner.py

import os
import sys

from agent_controller import process_agent_logs

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner.py <tick_number>")
        sys.exit(1)

    tick = int(sys.argv[1])
    log_file = f"netlogo/llm_agent_logs/agents_tick_{tick}.json"
    process_agent_logs(log_file, "decisions")
