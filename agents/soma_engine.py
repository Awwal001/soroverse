import os
from uagents import Agent, Protocol
from uagents_core.contrib.protocols.chat import chat_protocol_spec

soma_engine = Agent(
    name="SOMA Engine", 
    seed=os.getenv("SOMA_ENGINE_SEED", "soma_secret_002"),
    port=8002,
    mailbox=True
)

chat_proto = Protocol(spec=chat_protocol_spec)
soma_engine.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🧠 Starting SOMA Engine Agent...")
    soma_engine.run()
