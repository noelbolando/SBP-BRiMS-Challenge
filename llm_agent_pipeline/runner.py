# llm_agent_pipeline/runner.py

import sys

from agent_controller import process_agent_logs

if __name__ == "__main__":
    tick = int(sys.argv[1])  # e.g., 1
    log_file = f"logs/agents_tick_{tick}.json"
    process_agent_logs(log_file, "decisions")
