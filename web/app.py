from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, HTMLResponse
import json
from langchain.agents import create_agent
from utils.model_util import model

app = FastAPI()

agent = create_agent(model=model)

def sse(q: str):
    last = ""
    for chunk in agent.stream({
        "messages": [{"role": "user", "content": q}]
    }, stream_mode="values"):
        latest = chunk["messages"][-1]
        c = latest.content
        if isinstance(c, list):
            c = "".join([x.get("text", "") if isinstance(x, dict) else str(x) for x in c])
        c = c or ""
        if c:
            new = c[len(last):] if c.startswith(last) else c
            if new:
                yield f"data: {new}\n\n"
                yield f"event: full\ndata: {json.dumps({"text": c}, ensure_ascii=False)}\n\n"
                last = c
        elif getattr(latest, "tool_calls", None):
            names = [tc["name"] for tc in latest.tool_calls]
            yield f"event: tool\ndata: {json.dumps(names, ensure_ascii=False)}\n\n"
    yield "event: done\ndata: done\n\n"

@app.get("/")
def index():
    return HTMLResponse(
        """
        <!doctype html>
        <html>
        <head>
          <meta charset=\"utf-8\">
          <title>Agent Stream</title>
          <style>
            body{font-family:system-ui,Arial,sans-serif;margin:24px}
            #box{display:flex;gap:8px;margin-bottom:12px}
            input{flex:1;padding:8px;font-size:14px}
            button{padding:8px 12px;font-size:14px}
            pre{white-space:pre-wrap;border:1px solid #ddd;padding:12px;min-height:160px}
            #tools{color:#666;margin-top:8px}
          </style>
        </head>
        <body>
          <div id=\"box\">
            <input id=\"q\" placeholder=\"输入问题\" value=\"李白有哪些作品\">
            <button id=\"start\">开始</button>
          </div>
          <pre id=\"out\"></pre>
          <div id=\"tools\"></div>
          <script>
            let es;
            const q = document.getElementById('q');
            const out = document.getElementById('out');
            const tools = document.getElementById('tools');
            document.getElementById('start').onclick = () => {
              if (es) es.close();
              out.textContent = '';
              tools.textContent = '';
              const url = '/api/stream?q=' + encodeURIComponent(q.value || '');
              es = new EventSource(url);
              es.onmessage = e => { out.textContent += e.data; };
              es.addEventListener('full', e => { try { const o = JSON.parse(e.data); out.textContent = o.text || out.textContent; } catch {} });
              es.addEventListener('tool', e => { tools.textContent = '工具调用: ' + e.data; });
              es.addEventListener('done', () => { /* no-op */ });
              es.onerror = () => { es && es.close(); };
            };
          </script>
        </body>
        </html>
        """
    )

@app.get("/api/stream")
def api_stream(q: str = Query("李白有哪些作品")):
    return StreamingResponse(
        sse(q),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)