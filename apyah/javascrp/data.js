const keys = []
const selectors = []
const ports = []

const sockets = []

function createPersistentSocket(selector, port, index) {{
  const ws = new WebSocket("ws://127.0.0.1:" + port);
  sockets[index] = ws;

  ws.onopen = () => {{
    ws.send("yes");
    sendStructuredData(selector, ws);
  }};

  ws.onclose = () => {{
    // Try reconnecting after 1 second
    setTimeout(() => createPersistentSocket(selector, port, index), 1000);
  }};

  ws.onerror = (err) => {{
    console.error("WebSocket error:", err);
    ws.close();
  }};

  ws.onmessage = (event) => {{
    // handle incoming messages if needed
  }};
}}

function sendStructuredData(selector, ws) {{
  const parent = document.querySelector(selector);
  if (!parent) {{
    console.error("Parent selector not found:", selector);
    return;
  }}

  const children = parent.children;
  const data = {};

  for (let i = 0; i < keys.length; i++) {{
    data[keys[i]] = i < children.length ? children[i].textContent : null;
  }}

  if (ws.readyState === WebSocket.OPEN) {{
    ws.send(JSON.stringify(data));
  }}
}}

// Send data every second on all open sockets
setInterval(() => {{
  for (let i = 0; i < selectors.length; i++) {{
    const portObj = ports[i];
    const ws = sockets[i];
    if (selectors[i] && portObj && portObj.enabled && ws && ws.readyState === WebSocket.OPEN) {{
      sendStructuredData(selectors[i], ws);
    }}
  }}
}}, 1000);

// Initial connections
for (let i = 0; i < selectors.length; i++) {{
  const portObj = ports[i];
  if (selectors[i] && portObj && portObj.enabled) {{
    createPersistentSocket(selectors[i], portObj.port, i);
  }}
}}
