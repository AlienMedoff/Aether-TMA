# 🌌 Aether-TMA: Universal Agentic Runtime

> **Stop building brittle scrapers. Start giving your LLMs reliable hands and eyes.**

**Aether-TMA** is a vendor-agnostic high-performance runtime designed to connect any LLM (GPT-4, Claude, Gemini, Llama) directly to **Telegram Mini Apps** and complex web interfaces. It transforms raw UI into a programmable, observable environment for autonomous agents.

---

## 🏛 Architecture

```text
       [ YOUR LLM ] (GPT-4 / Claude / Gemini / Llama)
             |
             | [ JSON Control Protocol v2.0 ]
             v
    ___________________________
   |    Aether-TMA Runtime     |  <-- FastAPI Engine
   |---------------------------|
   | [Control] [State] [Memory]|  <-- Redis Persistence
   |___________________________|
             |
             | [ Injected Bridge.js ]
             v
    [ Telegram Mini App / UI ]    <-- Isolated Chromium Sandbox
             |
             +---> [ Live Observability ] (WebSockets Stream)
