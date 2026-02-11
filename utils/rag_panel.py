import streamlit.components.v1 as components

def rag_panel():
    components.html("""
<script>

function mountChatbot() {

const parentDoc = window.parent?.document || document;

// prevent duplicate injection
if (parentDoc.getElementById("ai-fab")) return;

// ---------- STYLE ----------

const style = parentDoc.createElement("style");
style.innerHTML = `
#ai-fab {
  position: fixed;
  bottom: 25px;
  right: 25px;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #6366f1;
  color: white;
  font-size: 28px;
  border: none;
  cursor: pointer;
  z-index: 999999;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
}

#ai-chat {
  display: none;
  position: fixed;
  bottom: 110px;
  right: 25px;
  width: 380px;
  height: 520px;
  background: #0b1220;
  border-radius: 14px;
  padding: 14px;
  color: white;
  font-family: sans-serif;
  z-index: 999999;
  box-shadow: 0 20px 60px rgba(0,0,0,0.7);
  overflow-y: auto;
}

#ai-log {
  height: 360px;
  overflow-y: auto;
  margin-bottom: 8px;
  font-size: 14px;
}

#ai-chat textarea {
  width: 100%;
  height: 70px;
  border-radius: 8px;
  border: none;
  padding: 8px;
}

#ai-chat button {
  width: 100%;
  margin-top: 8px;
  padding: 10px;
  border-radius: 8px;
  background: #6366f1;
  border: none;
  color: white;
  cursor: pointer;
}

.msg-user { color: #a5b4fc; margin: 6px 0; }
.msg-ai { color: #e5e7eb; margin: 6px 0; }
`;

parentDoc.head.appendChild(style);

// ---------- FAB ----------

const fab = parentDoc.createElement("button");
fab.id = "ai-fab";
fab.innerHTML = "💬";

// ---------- CHAT PANEL ----------

const chat = parentDoc.createElement("div");
chat.id = "ai-chat";

chat.innerHTML = `
<h3>AI Assistant</h3>
<div id="ai-log"></div>
<textarea id="ai-input" placeholder="Ask something..."></textarea>
<button id="ai-send">Send</button>
`;

// toggle chat
fab.onclick = () => {
  chat.style.display = chat.style.display === "none" ? "block" : "none";
};

parentDoc.body.appendChild(fab);
parentDoc.body.appendChild(chat);

// ---------- EVENTS ----------

const log = parentDoc.getElementById("ai-log");
const input = parentDoc.getElementById("ai-input");
const send = parentDoc.getElementById("ai-send");

send.onclick = async () => {

const q = input.value.trim();
if (!q) return;

log.innerHTML += `<div class="msg-user">You: ${q}</div>`;
input.value = "";

try {

const res = await fetch("http://127.0.0.1:8000/ask", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({question: q})
});

const data = await res.json();

const formatted = data.answer
  .replace(/\\n/g, "<br>")
  .replace(/(\\d+\\.)/g, "<br><b>$1</b> ");

log.innerHTML += `<div class="msg-ai"><b>AI:</b><br>${formatted}</div>`;

} catch (err) {

log.innerHTML += `<div class="msg-ai">⚠️ API error. Is backend running?</div>`;
console.error(err);

}

log.scrollTop = log.scrollHeight;

};

}

// retry injection after Streamlit hydration
setTimeout(mountChatbot, 400);

</script>
""", height=0)
