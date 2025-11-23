import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from langchain.agents import create_agent
from utils.model_util import model

agent = create_agent(model=model)

INDEX_HTML = """<!doctype html>
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
        es.addEventListener('tool', e => { tools.textContent = '工具调用: ' + e.data; });
        es.onerror = () => { es && es.close(); };
      };
    </script>
  </body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode("utf-8"))
            return

        if parsed.path == "/api/stream":
            qs = parse_qs(parsed.query)
            q = qs.get("q", ["李白有哪些作品"])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("X-Accel-Buffering", "no")
            self.end_headers()
            last = ""
            try:
                for chunk in agent.stream({
                    "messages": [{"role": "user", "content": q}]
                }, stream_mode="values"):
                    latest = chunk["messages"][-1]
                    c = latest.content
                    if c:
                        if isinstance(c, list):
                            c = "".join([str(x) for x in c])
                        new = c[len(last):]
                        if new:
                            msg = f"data: {new}\n\n".encode("utf-8")
                            self.wfile.write(msg)
                            self.wfile.flush()
                            last = c
                    elif getattr(latest, "tool_calls", None):
                        names = [tc["name"] for tc in latest.tool_calls]
                        msg = f"event: tool\ndata: {names}\n\n".encode("utf-8")
                        self.wfile.write(msg)
                        self.wfile.flush()
            except BrokenPipeError:
                pass
            return

        self.send_response(404)
        self.end_headers()


def run(host="127.0.0.1", port=8000):
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"Running on http://{host}:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    run()