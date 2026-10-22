# Multi-Agent Code Analyzer — Prototype Setup Guide

This is the working prototype for your research project: **A Multi-Agent AI
System for Intelligent Code Review, Bug Detection, and Performance Analysis**.

It has 5 agents:
1. **Code Review Agent** — quality, readability, best practices
2. **Bug Detection Agent** — syntax, logical, runtime bugs
3. **Complexity Analysis Agent** — time & space complexity (Big-O)
4. **Performance Optimization Agent** — selective, justified efficiency suggestions
5. **Validation Agent** — cross-checks the other 4 agents' findings and gives an overall confidence score

Stack: **FastAPI** (backend) + **React + Vite + Tailwind** (frontend) + **Google Gemini API**.
No PostgreSQL / login for this prototype (deferred, as decided).

Everything below assumes **Windows**, with **Python and Node.js already installed**,
using **VS Code**'s terminal (PowerShell). Follow the steps in order — don't skip any.

---

## Part 1 — Get a Gemini API key (free)

1. Go to **https://aistudio.google.com/app/apikey** in your browser.
2. Sign in with your Google account.
3. Click **"Create API key"**.
4. Choose "Create API key in new project" if asked.
5. Copy the key that appears (starts with `AIza...`). Keep this tab open — you'll paste it in Part 3.

⚠️ **Never share this key, commit it to GitHub, or paste it into frontend code.** It only ever goes in the backend's `.env` file, which is already excluded from being shared.

---

## Part 2 — Open the project in VS Code

1. Unzip the project folder you downloaded (`multi-agent-code-analyzer`) somewhere easy to find, e.g. `C:\Users\<you>\Projects\`.
2. Open VS Code.
3. `File → Open Folder` → select the unzipped `multi-agent-code-analyzer` folder.
4. Open a terminal inside VS Code: `Terminal → New Terminal` (it opens PowerShell by default on Windows).

---

## Part 3 — Backend setup (FastAPI + Gemini)

All commands below are typed into the VS Code terminal, one at a time.

### 3.1 Create the virtual environment

```powershell
cd backend
python -m venv venv
```

This creates a `venv` folder inside `backend/` — your project's isolated Python environment.

### 3.2 Activate the virtual environment

```powershell
venv\Scripts\activate
```

Your terminal prompt should now start with `(venv)`. **You must do this every time**
you open a new terminal to work on the backend.

> If PowerShell blocks this with a "running scripts is disabled" error, run this once:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then try activating again.

### 3.3 Install backend dependencies

```powershell
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, the Gemini SDK, and everything else needed.

### 3.4 Add your Gemini API key

1. In the `backend` folder, find the file `.env.example`.
2. Make a copy of it in the same folder and rename the copy to `.env` (exactly that — a file named `.env`, no `.example`).
3. Open `.env` and replace `your_gemini_api_key_here` with the key you copied in Part 1:
   ```
   GEMINI_API_KEY=AIza...your_real_key...
   GEMINI_MODEL=gemini-2.5-flash
   ```
4. Save the file.

> If `gemini-2.5-flash` ever stops working (model names change over time), open
> https://aistudio.google.com , check the current available model names, and
> update `GEMINI_MODEL` in `.env` accordingly.

### 3.5 Run the backend server

```powershell
uvicorn app.main:app --reload --port 8000
```

You should see output ending in something like `Uvicorn running on http://127.0.0.1:8000`.
Leave this terminal running. Open `http://localhost:8000` in a browser — you should
see `{"status":"ok", ...}`. That confirms the backend works.

**Keep this terminal open and running** while you use the app.

---

## Part 4 — Frontend setup (React)

Open a **second** VS Code terminal (`Terminal → New Terminal` again — don't close the backend one).

### 4.1 Install frontend dependencies

```powershell
cd frontend
npm install
```

This may take a minute or two the first time.

### 4.2 Run the frontend

```powershell
npm run dev
```

You'll see a local URL, typically `http://localhost:5173`. Open that in your browser.

---

## Part 5 — Use the prototype

1. With both servers running (backend on :8000, frontend on :5173), open `http://localhost:5173`.
2. Paste Python code into the text box, or switch to "Upload .py" and choose a file.
3. Click **Analyze code**.
4. Wait a few seconds — the 4 analysis agents run in parallel, then the Validation Agent
   cross-checks their output. You'll see a structured report with all 5 agents' findings,
   severity/verdict badges, and response-time numbers (useful for your Review 2 evaluation section).

Try it first with a small, obviously imperfect function, e.g.:

```python
def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i != j and lst[i] == lst[j] and lst[i] not in duplicates:
                duplicates.append(lst[i])
    return duplicates
```

This has an O(n²) nested loop the Performance and Complexity agents should both flag —
good for checking that the agents agree with each other (which is exactly what your
Validation Agent is meant to check).

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Could not reach the backend" in the browser | Make sure the `uvicorn` terminal is still running and shows no errors |
| `GEMINI_API_KEY is not configured` in the report | Check `backend/.env` exists (not `.env.example`) and has your real key, then restart `uvicorn` |
| `ModuleNotFoundError` when running uvicorn | You forgot to activate the venv (`venv\Scripts\activate`) or run `pip install -r requirements.txt` |
| Agent result shows a JSON parse error occasionally | Gemini sometimes returns malformed JSON; the code already retries automatically — just re-run the analysis |
| Blank page on localhost:5173 | Check the frontend terminal for errors; make sure `npm install` finished without errors |

---

## What's deliberately NOT in this prototype (by design, for Review 2 scope)

- PostgreSQL / persistent history of past analyses
- Login / authentication (JWT)
- Multi-language support (Python only, as scoped)
- Deployment / hosting

These are listed in your proposal as later/"if time permits" items — this prototype is
the minimum viable Review 2 demo: paste or upload code → 5-agent analysis → structured report.

---

## Where each project decision lives in the code (for your report/demo)

- **Orchestration layer** → `backend/app/orchestrator.py`
- **Each specialized agent's prompt** → `backend/app/agents/*.py`
- **Validation Agent (consistency + confidence check)** → `backend/app/agents/validation_agent.py`
- **Response-time measurement** → returned in every report under `"timing"`
- **API endpoint (paste + upload)** → `backend/app/main.py`
