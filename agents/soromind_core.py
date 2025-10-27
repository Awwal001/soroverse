import os
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import chat_protocol_spec

soromind = Agent(
    name="SoroMind Core",
    seed=os.getenv("SOROMIND_SEED", "soromind_secret_001"),
    port=8001,
    mailbox=True
)

chat_proto = Protocol(spec=chat_protocol_spec)
soromind.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🚀 Starting SoroMind Core Agent...")
    soromind.run()
