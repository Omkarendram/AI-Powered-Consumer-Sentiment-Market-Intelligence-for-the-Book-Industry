# import streamlit.components.v1 as components

# def rag_panel():
#     components.html("""
# <script>

# function mountChatbot() {

# const parentDoc = window.parent?.document || document;

# // prevent duplicate injection
# if (parentDoc.getElementById("ai-fab")) return;

# // ---------- STYLE ----------

# const style = parentDoc.createElement("style");
# style.innerHTML = `
# #ai-fab {
#   position: fixed;
#   bottom: 25px;
#   right: 25px;
#   width: 64px;
#   height: 64px;
#   border-radius: 50%;
#   background: #6366f1;
#   color: white;
#   font-size: 28px;
#   border: none;
#   cursor: pointer;
#   z-index: 999999;
#   box-shadow: 0 10px 30px rgba(0,0,0,0.6);
# }

# #ai-chat {
#   display: none;
#   position: fixed;
#   bottom: 110px;
#   right: 25px;
#   width: 380px;
#   height: 520px;
#   background: #0b1220;
#   border-radius: 14px;
#   padding: 14px;
#   color: white;
#   font-family: sans-serif;
#   z-index: 999999;
#   box-shadow: 0 20px 60px rgba(0,0,0,0.7);
#   overflow-y: auto;
# }

# #ai-log {
#   height: 360px;
#   overflow-y: auto;
#   margin-bottom: 8px;
#   font-size: 14px;
# }

# #ai-chat textarea {
#   width: 100%;
#   height: 70px;
#   border-radius: 8px;
#   border: none;
#   padding: 8px;
# }

# #ai-chat button {
#   width: 100%;
#   margin-top: 8px;
#   padding: 10px;
#   border-radius: 8px;
#   background: #6366f1;
#   border: none;
#   color: white;
#   cursor: pointer;
# }

# .msg-user { color: #a5b4fc; margin: 6px 0; }
# .msg-ai { color: #e5e7eb; margin: 6px 0; }
# `;

# parentDoc.head.appendChild(style);

# // ---------- FAB ----------

# const fab = parentDoc.createElement("button");
# fab.id = "ai-fab";
# fab.innerHTML = "💬";

# // ---------- CHAT PANEL ----------

# const chat = parentDoc.createElement("div");
# chat.id = "ai-chat";

# chat.innerHTML = `
# <h3>AI Assistant</h3>
# <div id="ai-log"></div>
# <textarea id="ai-input" placeholder="Ask something..."></textarea>
# <button id="ai-send">Send</button>
# `;

# // toggle chat
# fab.onclick = () => {
#   chat.style.display = chat.style.display === "none" ? "block" : "none";
# };

# parentDoc.body.appendChild(fab);
# parentDoc.body.appendChild(chat);

# // ---------- EVENTS ----------

# const log = parentDoc.getElementById("ai-log");
# const input = parentDoc.getElementById("ai-input");
# const send = parentDoc.getElementById("ai-send");

# send.onclick = async () => {

# const q = input.value.trim();
# if (!q) return;

# log.innerHTML += `<div class="msg-user">You: ${q}</div>`;
# input.value = "";

# try {

# const res = await fetch("http://127.0.0.1:8000/ask", {
#   method: "POST",
#   headers: {"Content-Type": "application/json"},
#   body: JSON.stringify({question: q})
# });

# const data = await res.json();

# const formatted = data.answer
#   .replace(/\\n/g, "<br>")
#   .replace(/(\\d+\\.)/g, "<br><b>$1</b> ");

# log.innerHTML += `<div class="msg-ai"><b>AI:</b><br>${formatted}</div>`;

# } catch (err) {

# log.innerHTML += `<div class="msg-ai">⚠️ API error. Is backend running?</div>`;
# console.error(err);

# }

# log.scrollTop = log.scrollHeight;

# };

# }

# // retry injection after Streamlit hydration
# setTimeout(mountChatbot, 400);

# </script>
import streamlit as st
import streamlit.components.v1 as components
import threading
import time
import requests

_server_thread = None


def _ensure_server():
        """Start a local FastAPI uvicorn server in background if it's not running."""
        global _server_thread
        # quick health check
        try:
                r = requests.get("http://127.0.0.1:8001/", timeout=0.5)
                if r.status_code == 200:
                        return
        except Exception:
                pass

        if _server_thread and _server_thread.is_alive():
                return

        def run_uvicorn():
                import uvicorn
                from rag import api

                uvicorn.run(api.app, host="127.0.0.1", port=8001, log_level="warning")

        t = threading.Thread(target=run_uvicorn, daemon=True)
        t.start()

        # wait for server to become ready (best-effort)
        for _ in range(20):
                try:
                        r = requests.get("http://127.0.0.1:8001/", timeout=0.5)
                        if r.status_code == 200:
                                break
                except Exception:
                        time.sleep(0.2)

        _server_thread = t


def rag_panel():
        """Inject a floating chat FAB and panel into the Streamlit page.

        This function ensures an internal FastAPI server is started and points
        the UI to it so messages are served by `rag.api.ask` which calls
        `rag.rag_app.answer_query`.
        """

        # ensure backend is running
        try:
                _ensure_server()
        except Exception:
                pass

        html = r"""
<script>
function mountChatbot() {
    const parentDoc = window.parent?.document || document;
    if (parentDoc.getElementById("ai-fab")) return;
    const style = parentDoc.createElement("style");
    style.innerHTML = `
        #ai-fab { position: fixed; bottom: 25px; right: 25px; width: 64px; height: 64px; border-radius: 50%; background: #6366f1; color: white; font-size: 28px; border: none; cursor: pointer; z-index: 999999; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        #ai-chat { display: none; position: fixed; bottom: 110px; right: 25px; width: 380px; max-height: 520px; background: #0b1220; border-radius: 14px; padding: 14px; color: white; font-family: sans-serif; z-index: 999999; box-shadow: 0 20px 60px rgba(0,0,0,0.7); overflow-y: auto; }
        #ai-log { height: 320px; overflow-y: auto; margin-bottom: 8px; font-size: 14px; }
        #ai-chat textarea { width: 100%; height: 70px; border-radius: 8px; border: none; padding: 8px; resize: none; }
        #ai-chat button { width: 100%; margin-top: 8px; padding: 10px; border-radius: 8px; background: #6366f1; border: none; color: white; cursor: pointer; }
        .msg-user { color: #a5b4fc; margin: 6px 0; }
        .msg-ai { color: #e5e7eb; margin: 6px 0; }
    `;
    parentDoc.head.appendChild(style);
    const fab = parentDoc.createElement("button");
    fab.id = "ai-fab"; fab.title = "Open AI Assistant"; fab.innerHTML = "💬";
    const chat = parentDoc.createElement("div"); chat.id = "ai-chat";
    chat.innerHTML = `<h3>AI Assistant</h3><div id="ai-log"></div><textarea id="ai-input" placeholder="Ask something..."></textarea><button id="ai-send">Send</button>`;
    fab.onclick = () => { chat.style.display = chat.style.display === "none" ? "block" : "none"; };
    parentDoc.body.appendChild(fab); parentDoc.body.appendChild(chat);
    const log = parentDoc.getElementById("ai-log"); const input = parentDoc.getElementById("ai-input"); const send = parentDoc.getElementById("ai-send");
        // disable send until backend healthy
        let backendReady = false;
        async function checkBackend() {
                try {
                        const r = await fetch('http://127.0.0.1:8001/');
                        backendReady = r.ok;
                        send.disabled = !backendReady;
                        send.style.opacity = backendReady ? 1 : 0.6;
                        return backendReady;
                } catch (e) {
                        send.disabled = true;
                        send.style.opacity = 0.6;
                        return false;
                }
        }

        // poll backend until ready (best-effort)
        checkBackend();
        setInterval(checkBackend, 2000);

        send.onclick = async () => {
                const q = input.value.trim();
                if (!q) return;
                log.innerHTML += `<div class="msg-user"><b>You:</b> ${q}</div>`;
                input.value = "";

                try {
                        const res = await fetch("http://127.0.0.1:8001/ask", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({question: q}) });

                        let bodyText = await res.text();
                        let answer = null;

                        try {
                                const parsed = JSON.parse(bodyText || '{}');
                                answer = parsed.answer || null;
                        } catch (e) {
                                answer = bodyText || null;
                        }

                        if (!res.ok) {
                                const msg = answer || 'Unknown backend error';
                                log.innerHTML += `<div class="msg-ai">⚠️ Backend: ${msg}</div>`;
                        } else {
                                const formatted = (answer || 'No answer').replace(/\n/g, "<br>");
                                log.innerHTML += `<div class="msg-ai"><b>AI:</b><br>${formatted}</div>`;
                        }

                } catch (err) {
                        log.innerHTML += `<div class="msg-ai">⚠️ Network error. Is backend running?</div>`;
                        console.error(err);
                }

                log.scrollTop = log.scrollHeight;
        };
}
setTimeout(mountChatbot, 400);
</script>
"""

        components.html(html, height=0)
