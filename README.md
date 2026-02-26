## 🏛 Architecture

Your LLM (GPT-4/Claude/Llama)
       |
       | [ JSON Control Protocol ]
       v
+-----------------------------+
|      Aether-TMA Runtime     |  <-- FastAPI Engine
|-----------------------------|
| [State] [Memory] [Control]  |  <-- Redis Persistence
+-----------------------------+
       |
       | [ Playwright + Bridge.js ]
       v
[ Telegram Mini App / Web UI ]   <-- Isolated Sandbox
       |
       +---> [ Live Monitor ]    <-- WebSockets (Real-time Vision)# Aether-TMA
Aether-TMA is a universal Agentic Runtime that turns any UI (Telegram Mini Apps, Web) into a programmable environment for AI. It provides LLMs with "eyes and hands" via isolated Playwright containers, persistent memory, and an observability bridge. Designed for autonomous agents where APIs don't exist. UI is the new API. 🌌🚀
