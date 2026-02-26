import asyncio, json, base64
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from playwright.async_api import async_playwright

app = FastAPI(title="Aether-TMA Runtime")
app.mount("/static", StaticFiles(directory="static"), name="static")

sessions = {}

@app.post("/launch")
async def launch(url: str, init_data: str, session_id: str):
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=True)
    context = await browser.new_context(viewport={'width': 375, 'height': 667})
    
    # Инжект моста
    with open("bridge.js", "r") as f:
        js_bridge = f.read().replace("__INIT_DATA__", init_data)
    
    await context.add_init_script(js_bridge)
    page = await context.new_page()
    await page.goto(url)
    
    sessions[session_id] = {"page": page, "browser": browser, "context": context}
    return {"status": "running"}

@app.get("/state/{session_id}")
async def get_state(session_id: str):
    if session_id not in sessions: raise HTTPException(404)
    page = sessions[session_id]["page"]
    elements = await page.evaluate("""() => {
        return Array.from(document.querySelectorAll('[data-agent-id]')).map(el => ({
            id: el.getAttribute('data-agent-id'),
            text: el.innerText,
            tag: el.tagName,
            disabled: el.disabled || false,
            visible: el.offsetWidth > 0
        }));
    }""")
    return {"elements": elements, "url": page.url}

@app.websocket("/ws/monitor/{session_id}")
async def monitor(websocket: WebSocket, session_id: str):
    await websocket.accept()
    page = sessions[session_id]["page"]
    while True:
        try:
            screenshot = await page.screenshot(type="jpeg", quality=40)
            await websocket.send_json({
                "image": base64.b64encode(screenshot).decode('utf-8')
            })
            await asyncio.sleep(0.5)
        except: break
