import os
from uagents import Agent, Protocol
from uagents_core.contrib.protocols.chat import chat_protocol_spec

psn_connect = Agent(
    name="PSN Connect",
    seed=os.getenv("PSN_CONNECT_SEED", "psn_secret_004"),
    port=8004,
    mailbox=True
)

chat_proto = Protocol(spec=chat_protocol_spec)
psn_connect.include(chat_proto, publish_manifest=True)

if __name__ == "__main__":
    print("🤝 Starting PSN Connect Agent...")
    psn_connect.run()
