from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from urllib.parse import parse_qs
import time

from pipeline.intent import extract_intent
from pipeline.schema import generate_schema
from pipeline.validator import validate_schema
from pipeline.repair import repair_schema


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AI APP BUILDER Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Manrope:wght@400;500;700&display=swap');

        :root {
            --bg: #fff9f0;
            --bg-alt: #ffe8c7;
            --surface: rgba(255, 255, 255, 0.88);
            --surface-strong: #ffffff;
            --ink: #1c1b1a;
            --muted: #68625b;
            --line: rgba(28, 27, 26, 0.14);
            --primary: #ff6b2d;
            --primary-ink: #451a06;
            --success: #1e8f5b;
            --warn: #bb6a00;
            --danger: #b00020;
            --shadow: 0 14px 40px rgba(82, 58, 25, 0.13);
            --radius-lg: 18px;
            --radius-md: 12px;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: 'Manrope', sans-serif;
            color: var(--ink);
            background:
                radial-gradient(circle at 8% 15%, rgba(255, 176, 76, 0.26), transparent 26%),
                radial-gradient(circle at 88% 82%, rgba(255, 130, 80, 0.24), transparent 30%),
                linear-gradient(160deg, var(--bg), var(--bg-alt));
            min-height: 100vh;
            padding: 24px;
        }

        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif;
            margin: 0;
            letter-spacing: 0.01em;
        }

        .shell {
            max-width: 1180px;
            margin: 0 auto;
            display: grid;
            gap: 18px;
        }

        .panel {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            backdrop-filter: blur(8px);
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 22px;
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: auto -90px -110px auto;
            width: 230px;
            height: 230px;
            background: linear-gradient(145deg, #ffd67a, #ff9357);
            border-radius: 35% 65% 70% 30% / 40% 50% 50% 60%;
            opacity: 0.32;
            animation: drift 8s ease-in-out infinite alternate;
            pointer-events: none;
        }

        @keyframes drift {
            from { transform: translateY(-6px) rotate(-5deg); }
            to { transform: translateY(8px) rotate(6deg); }
        }

        .title {
            font-size: clamp(1.6rem, 3vw, 2.2rem);
            margin-bottom: 6px;
        }

        .subtitle {
            margin: 0;
            color: var(--muted);
            max-width: 760px;
        }

        .input-grid {
            margin-top: 16px;
            display: grid;
            gap: 10px;
        }

        textarea {
            width: 100%;
            min-height: 102px;
            border: 1px solid var(--line);
            border-radius: var(--radius-md);
            padding: 12px;
            font: inherit;
            resize: vertical;
            background: var(--surface-strong);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(255, 107, 45, 0.18);
        }

        .actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }

        button {
            border: none;
            border-radius: 10px;
            padding: 10px 14px;
            font: 600 0.94rem 'Space Grotesk', sans-serif;
            cursor: pointer;
            transition: transform 0.16s ease, filter 0.16s ease;
        }

        button:hover { transform: translateY(-1px); filter: brightness(1.03); }
        button:disabled { cursor: wait; opacity: 0.75; }

        .btn-primary { background: var(--primary); color: #fff; }

        .btn-secondary {
            background: #f3e6d8;
            color: var(--ink);
            border: 1px solid var(--line);
        }

        .kpis {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 12px;
            padding: 16px;
        }

        .kpi {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 11px 12px;
            opacity: 0;
            transform: translateY(8px);
            animation: rise 0.45s forwards;
        }

        .kpi:nth-child(2) { animation-delay: 0.04s; }
        .kpi:nth-child(3) { animation-delay: 0.08s; }
        .kpi:nth-child(4) { animation-delay: 0.12s; }
        .kpi:nth-child(5) { animation-delay: 0.16s; }

        @keyframes rise { to { opacity: 1; transform: translateY(0); } }

        .kpi-label {
            color: var(--muted);
            font-size: 0.78rem;
            margin-bottom: 4px;
        }

        .kpi-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.86rem;
            border-radius: 999px;
            padding: 3px 9px;
            background: #fff5eb;
        }

        .status-success { color: var(--success); }
        .status-repaired { color: var(--warn); }
        .status-error { color: var(--danger); }

        .content {
            display: grid;
            gap: 16px;
            padding: 16px;
            grid-template-columns: 1.1fr 0.9fr;
        }

        .card {
            background: var(--surface-strong);
            border: 1px solid var(--line);
            border-radius: var(--radius-md);
            overflow: hidden;
        }

        .card-head {
            padding: 12px 14px;
            border-bottom: 1px solid var(--line);
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }

        .tabs { display: flex; flex-wrap: wrap; gap: 7px; }

        .tab {
            background: #f4ede2;
            color: var(--muted);
            border: 1px solid transparent;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 0.83rem;
        }

        .tab.active {
            color: var(--primary-ink);
            background: #ffe6d6;
            border-color: rgba(255, 107, 45, 0.34);
        }

        .viewer { display: none; }
        .viewer.active { display: block; }

        pre {
            margin: 0;
            padding: 14px;
            max-height: 440px;
            overflow: auto;
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            font-size: 0.82rem;
            line-height: 1.45;
            background: #fffdf9;
        }

        .list-wrap { max-height: 440px; overflow: auto; }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.88rem;
        }

        th, td {
            padding: 10px 12px;
            border-bottom: 1px solid var(--line);
            text-align: left;
            vertical-align: top;
        }

        th {
            color: var(--muted);
            font-weight: 600;
            background: #fff8ef;
            position: sticky;
            top: 0;
        }

        .empty {
            padding: 18px;
            color: var(--muted);
            font-size: 0.9rem;
        }

        .error {
            display: none;
            margin: 0 16px 16px;
            background: #fff0f3;
            color: #8c1029;
            border: 1px solid #ffc3cf;
            border-radius: 10px;
            padding: 10px 12px;
            font-size: 0.9rem;
        }

        .loading {
            display: none;
            align-items: center;
            gap: 8px;
            color: var(--muted);
            font-size: 0.9rem;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 999px;
            background: var(--primary);
            box-shadow: 0 0 0 0 rgba(255, 107, 45, 0.6);
            animation: pulse 1.2s infinite;
        }

        @keyframes pulse {
            70% { box-shadow: 0 0 0 10px rgba(255, 107, 45, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 107, 45, 0); }
        }

        @media (max-width: 980px) {
            .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .content { grid-template-columns: 1fr; }
        }

        @media (max-width: 640px) {
            body { padding: 12px; }
            .hero, .kpis, .content { padding: 12px; }
            .actions { flex-direction: column; }
            button { width: 100%; }
        }
    </style>
</head>
<body>
    <main class="shell">
        <section class="panel hero">
            <h1 class="title">AI APP BUILDER</h1>
            <p class="subtitle">Turn Your prompts into app architecture and inspect UI, API, and DB schema outputs with live metrics.</p>
            <div class="input-grid">
                <textarea id="prompt" placeholder="Describe your app...."></textarea>
                <div class="actions">
                    <button class="btn-primary" id="generateBtn" onclick="generate()">Generate Dashboard</button>
                    <button class="btn-secondary" onclick="clearDashboard()">Clear</button>
                    <button class="btn-secondary" onclick="copyJson()">Copy Schema JSON</button>
                    <button class="btn-secondary" onclick="downloadJson()">Download JSON</button>
                    <div class="loading" id="loading"><span class="dot"></span><span>Generating schema...</span></div>
                </div>
            </div>
        </section>

        <section class="panel kpis">
            <article class="kpi">
                <div class="kpi-label">Status</div>
                <div class="kpi-value"><span id="statusBadge" class="status-badge">idle</span></div>
            </article>
            <article class="kpi">
                <div class="kpi-label">Latency</div>
                <div class="kpi-value" id="latency">-</div>
            </article>
            <article class="kpi">
                <div class="kpi-label">UI Pages</div>
                <div class="kpi-value" id="uiPages">0</div>
            </article>
            <article class="kpi">
                <div class="kpi-label">API Endpoints</div>
                <div class="kpi-value" id="apiEndpoints">0</div>
            </article>
            <article class="kpi">
                <div class="kpi-label">DB Tables</div>
                <div class="kpi-value" id="dbTables">0</div>
            </article>
        </section>

        <section class="panel">
            <div class="error" id="error"></div>
            <div class="content">
                <article class="card">
                    <div class="card-head">
                        <h3>Schema Explorer</h3>
                        <div class="tabs" id="tabs">
                            <button class="tab active" data-target="fullViewer">Full</button>
                            <button class="tab" data-target="uiViewer">UI</button>
                            <button class="tab" data-target="apiViewer">API</button>
                            <button class="tab" data-target="dbViewer">DB</button>
                            <button class="tab" data-target="intentViewer">Intent</button>
                        </div>
                    </div>
                    <div class="viewer active" id="fullViewer"><pre id="fullJson">No schema generated yet.</pre></div>
                    <div class="viewer" id="uiViewer"><pre id="uiJson">No UI schema yet.</pre></div>
                    <div class="viewer" id="apiViewer"><pre id="apiJson">No API schema yet.</pre></div>
                    <div class="viewer" id="dbViewer"><pre id="dbJson">No DB schema yet.</pre></div>
                    <div class="viewer" id="intentViewer"><pre id="intentJson">No intent generated yet.</pre></div>
                </article>

                <article class="card">
                    <div class="card-head"><h3>API Endpoints</h3></div>
                    <div class="list-wrap" id="endpointWrap"><div class="empty">No endpoints found yet.</div></div>
                </article>

                <article class="card">
                    <div class="card-head"><h3>Database Tables</h3></div>
                    <div class="list-wrap" id="tableWrap"><div class="empty">No DB tables found yet.</div></div>
                </article>
            </div>
        </section>
    </main>

    <script>
        const state = { payload: null };

        function pretty(obj) {
            return JSON.stringify(obj ?? {}, null, 2);
        }

        function isObject(value) {
            return value && typeof value === "object" && !Array.isArray(value);
        }

        function asEntries(value) {
            if (Array.isArray(value)) {
                return value.map((item, idx) => [String(idx + 1), item]);
            }
            if (isObject(value)) {
                return Object.entries(value);
            }
            return [];
        }

        function setStatus(status, isError = false) {
            const badge = document.getElementById("statusBadge");
            badge.className = "status-badge " + (isError ? "status-error" : status === "success" ? "status-success" : status === "repaired" ? "status-repaired" : "");
            badge.textContent = status;
        }

        function renderEndpoints(apiSchema) {
            const wrap = document.getElementById("endpointWrap");
            const endpoints = asEntries(apiSchema?.endpoints);
            if (!endpoints.length) {
                wrap.innerHTML = '<div class="empty">No endpoints found yet.</div>';
                return 0;
            }

            const rows = endpoints.map(([name, cfg]) => {
                const method = (cfg?.method || "-").toString();
                const path = (cfg?.path || "-").toString();
                const desc = (cfg?.description || "-").toString();
                return `<tr><td>${name}</td><td>${method}</td><td>${path}</td><td>${desc}</td></tr>`;
            }).join("");

            wrap.innerHTML = `
                <table>
                    <thead><tr><th>Name</th><th>Method</th><th>Path</th><th>Description</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            `;
            return endpoints.length;
        }

        function renderTables(dbSchema) {
            const wrap = document.getElementById("tableWrap");
            const tables = asEntries(dbSchema?.tables);
            if (!tables.length) {
                wrap.innerHTML = '<div class="empty">No DB tables found yet.</div>';
                return 0;
            }

            const rows = tables.map(([name, cfg]) => {
                const columns = cfg?.columns ? Object.keys(cfg.columns).join(", ") : "-";
                return `<tr><td>${name}</td><td>${columns}</td></tr>`;
            }).join("");

            wrap.innerHTML = `
                <table>
                    <thead><tr><th>Table</th><th>Columns</th></tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            `;
            return tables.length;
        }

        function showError(message) {
            const el = document.getElementById("error");
            if (!message) {
                el.style.display = "none";
                el.textContent = "";
                return;
            }
            el.textContent = message;
            el.style.display = "block";
        }

        function setLoading(flag) {
            document.getElementById("loading").style.display = flag ? "inline-flex" : "none";
            document.getElementById("generateBtn").disabled = flag;
        }

        function render(payload) {
            state.payload = payload;
            const schema = payload?.final_schema || {};
            const uiSchema = schema?.ui_schema || {};
            const apiSchema = schema?.api_schema || {};
            const dbSchema = schema?.db_schema || {};

            document.getElementById("fullJson").textContent = pretty(schema);
            document.getElementById("uiJson").textContent = pretty(uiSchema);
            document.getElementById("apiJson").textContent = pretty(apiSchema);
            document.getElementById("dbJson").textContent = pretty(dbSchema);
            document.getElementById("intentJson").textContent = typeof payload?.intent === "string" ? payload.intent : pretty(payload?.intent || {});

            const pageCount = Object.keys(uiSchema?.pages || {}).length;
            const endpointCount = renderEndpoints(apiSchema);
            const tableCount = renderTables(dbSchema);

            document.getElementById("uiPages").textContent = String(pageCount);
            document.getElementById("apiEndpoints").textContent = String(endpointCount);
            document.getElementById("dbTables").textContent = String(tableCount);

            const latency = typeof payload?.latency === "number" ? `${(payload.latency * 1000).toFixed(0)} ms` : "-";
            document.getElementById("latency").textContent = latency;
            setStatus(payload?.status || "success");
        }

        async function generate() {
            const prompt = document.getElementById("prompt").value.trim();
            if (!prompt) {
                showError("Prompt is required.");
                setStatus("error", true);
                return;
            }

            showError("");
            setLoading(true);
            setStatus("generating");

            try {
                const res = await fetch("/generate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ prompt })
                });

                const data = await res.json();
                if (!res.ok || data.error) {
                    throw new Error(data.error || "Generation failed.");
                }

                render(data);
            } catch (err) {
                showError(err.message || "Something went wrong.");
                setStatus("error", true);
            } finally {
                setLoading(false);
            }
        }

        function clearDashboard() {
            document.getElementById("prompt").value = "";
            state.payload = null;
            document.getElementById("fullJson").textContent = "No schema generated yet.";
            document.getElementById("uiJson").textContent = "No UI schema yet.";
            document.getElementById("apiJson").textContent = "No API schema yet.";
            document.getElementById("dbJson").textContent = "No DB schema yet.";
            document.getElementById("intentJson").textContent = "No intent generated yet.";
            document.getElementById("latency").textContent = "-";
            document.getElementById("uiPages").textContent = "0";
            document.getElementById("apiEndpoints").textContent = "0";
            document.getElementById("dbTables").textContent = "0";
            document.getElementById("endpointWrap").innerHTML = '<div class="empty">No endpoints found yet.</div>';
            document.getElementById("tableWrap").innerHTML = '<div class="empty">No DB tables found yet.</div>';
            setStatus("idle");
            showError("");
        }

        async function copyJson() {
            if (!state.payload?.final_schema) {
                showError("Generate schema first to copy.");
                return;
            }
            await navigator.clipboard.writeText(pretty(state.payload.final_schema));
        }

        function downloadJson() {
            if (!state.payload?.final_schema) {
                showError("Generate schema first to download.");
                return;
            }
            const blob = new Blob([pretty(state.payload.final_schema)], { type: "application/json" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "generated_schema.json";
            a.click();
            URL.revokeObjectURL(url);
        }

        document.getElementById("tabs").addEventListener("click", (event) => {
            const tab = event.target.closest(".tab");
            if (!tab) return;

            const targetId = tab.dataset.target;
            document.querySelectorAll(".tab").forEach((btn) => btn.classList.remove("active"));
            document.querySelectorAll(".viewer").forEach((view) => view.classList.remove("active"));

            tab.classList.add("active");
            const target = document.getElementById(targetId);
            if (target) {
                target.classList.add("active");
            }
        });
    </script>
</body>
</html>
"""
@app.post("/generate")
async def generate_app(request: Request):
    start_time = time.time()

    content_type = request.headers.get("content-type", "")
    prompt = ""

    # Handle JSON or form
    if "application/json" in content_type:
        payload = await request.json()
        prompt = (payload or {}).get("prompt", "")
    else:
        raw_body = (await request.body()).decode("utf-8", errors="ignore")
        prompt = parse_qs(raw_body).get("prompt", [""])[0]

    prompt = str(prompt).strip()

    if not prompt:
        return JSONResponse({"error": "prompt is required"}, status_code=400)

    # 🔹 Stage 1: Intent
    print("🔹 Stage 1: Intent Extraction")
    intent = extract_intent(prompt)

    # 🔹 Stage 2: Schema
    print("🔹 Stage 2: Schema Generation")
    schema = generate_schema(intent)

    # 🔹 Stage 3: Validation
    print("🔹 Stage 3: Validation")
    valid_data, error = validate_schema(schema)

    # 🔧 Repair if needed
    if error:
        print("⚠️ Validation Failed → Repairing...")
        schema = repair_schema(schema, error)
        valid_data, error = validate_schema(schema)

    


    latency = time.time() - start_time

    # Logs
    print("✅ Intent:", intent)
    print("✅ Final Output:", valid_data)
   
    print("⏱ Latency:", latency)

    return {
        "intent": intent,
        "final_schema": valid_data,
        "latency": latency,
        "status": "success" if not error else "repaired",
        "error": error
    }
