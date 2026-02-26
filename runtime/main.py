from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import redis
import json

app = FastAPI(title="Aether-TMA Runtime")

# Enable CORS for communication with Telegram Mini Apps and external LLMs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redis connection (assumes redis container is named 'redis' in docker-compose)
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

@app.post("/control")
async def control_agent(command: dict):
    """
    Entry point for JSON Control Protocol v2.0.
    Stores commands from LLM in Redis for the Bridge to execute.
    """
    r.set("last_command", json.dumps(command))
    return {"status": "dispatched", "command": command}

@app.websocket("/observe")
async def websocket_endpoint(websocket: WebSocket):
    """
    Live stream of the UI state. 
    Provides the agent with 'eyes' by streaming DOM snapshots from Redis.
    """
    await websocket.accept()
    try:
        while True:
            # Fetch the latest UI snapshot provided by Bridge.js
            ui_state = r.get("ui_state") or "{}"
            await websocket.send_text(ui_state)
    except WebSocketDisconnect:
        print("Agent observability client disconnected")
