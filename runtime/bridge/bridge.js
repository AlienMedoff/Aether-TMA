/**
 * Aether Bridge v2.0
 * Injected into the Telegram Mini App to provide bi-directional communication with the Runtime.
 */
(function() {
    const RUNTIME_URL = "http://localhost:8000";
    const WS_URL = "ws://localhost:8000/observe";

    console.log("🌌 Aether Bridge: Initialized and Injecting Observability");

    /**
     * Captures essential DOM elements and metadata to send to the Runtime.
     * This allows the LLM to 'see' the current state of the UI.
     */
    async function syncUIState() {
        const state = {
            url: window.location.href,
            elements: Array.from(document.querySelectorAll('button, a, input, [role="button"]')).map(el => ({
                id: el.id || 'unnamed',
                tag: el.tagName,
                text: el.innerText || el.value || '',
                visible: el.getBoundingClientRect().height > 0,
                rect: el.getBoundingClientRect()
            })),
            viewport: {
                height: window.innerHeight,
                width: window.innerWidth,
                safeAreaBottom: getComputedStyle(document.documentElement).getPropertyValue('--tg-viewport-height') // TMA specific
            },
            timestamp: Date.now()
        };

        // Dispatch state to Runtime via POST (can be upgraded to dedicated WS)
        await fetch(`${RUNTIME_URL}/control`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: "SYNC_STATE", data: state})
        }).catch(() => {});
    }

    // Global Aether object for command execution
    window.Aether = {
        execute: (cmd) => {
            console.log("Aether executing command:", cmd);
            if (cmd.action === "CLICK") {
                const element = document.querySelector(cmd.selector);
                if (element) element.click();
            }
        },
        sync: syncUIState
    };

    // Periodic UI synchronization every 2 seconds to maintain agent grounding
    setInterval(syncUIState, 2000);
})();
