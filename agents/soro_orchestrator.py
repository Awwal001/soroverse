import os
from uagents import Agent

soro_orchestrator = Agent(
    name="SORO Orchestrator",
    seed=os.getenv("SORO_ORCHESTRATOR_SEED", "soro_secret_003"), 
    port=8003,
    mailbox=True
)

if __name__ == "__main__":
    print("💫 Starting SORO Orchestrator Agent...")
    soro_orchestrator.run()
