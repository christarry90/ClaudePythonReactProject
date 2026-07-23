# Windows Setup — From Zero to Learning

For a Windows 10/11 laptop, starting with nothing installed. You do **three things by hand** to
get Claude Code running; after that you paste one bootstrap prompt and Claude Code installs and
verifies the rest for you.

## What gets installed

| Tool | What it's for | Java analogy |
|---|---|---|
| **Node.js** | Runs Claude Code and the React frontend tooling | The JVM for the JavaScript world |
| **Claude Code** | Your AI tutor + coding assistant | — |
| **Git** | Clones this repo, tracks your work | Same Git you use for Java |
| **Python 3.12** | The backend language | Like installing a JDK |

You need a **Claude account** (Pro, Max, or API) to sign in to Claude Code.

---

## Part A — Do these 3 steps by hand

### Step 1 — Open PowerShell
Press **Start**, type **PowerShell**, open **Windows PowerShell**.

### Step 2 — Install Node.js
```powershell
winget install --id OpenJS.NodeJS.LTS -e
```
Then **close and reopen PowerShell** (so the PATH updates) and confirm:
```powershell
node --version
```
You should see `v20.x` or newer.

> `winget` is Windows' built-in package manager — think `apt` or Homebrew, but shipped with Windows.

### Step 3 — Install Claude Code and sign in
```powershell
npm install -g @anthropic-ai/claude-code
claude
```
The first run of `claude` opens your browser to log in. Sign in with your Claude account. Once
you're back at the prompt, Claude Code is ready.

---

## Part B — Let Claude Code do the rest

### Step 4 — Make a folder and launch Claude Code in it
```powershell
mkdir $HOME\dev
cd $HOME\dev
claude
```

### Step 5 — Paste this bootstrap prompt into Claude Code

Copy everything in the box and paste it into the Claude Code prompt:

```
You are helping me set up a Windows laptop for a full-stack learning project. I'm an
experienced Java developer, new to Python and React. Work through the steps below. Show me
each command before you run it, and briefly explain each tool in Java terms. Ask before any
install. Do the ENVIRONMENT SETUP ONLY — do not start the learning milestones until the very
last step.

1. Report what's already installed and the versions: git --version, python --version,
   node --version, npm --version.

2. For anything missing, install it with winget (ask me first):
   - Git:      winget install --id Git.Git -e
   - Python:   winget install --id Python.Python.3.12 -e
   If a PATH change is needed, tell me to close and reopen the terminal, then re-verify.

3. Clone my learning repo, unless we're already inside it:
   git clone https://github.com/jerrinss5/java-to-fullstack
   then cd into java-to-fullstack.

4. Get the Python backend ready (run from the backend/ folder). Use the venv's python
   directly so no PowerShell execution-policy issues get in the way:
   - python -m venv .venv
   - .venv\Scripts\python.exe -m pip install --upgrade pip
   - .venv\Scripts\python.exe -m pip install -r requirements.txt
   - verify with: .venv\Scripts\python.exe -m uvicorn --version
   Explain that a venv is an isolated dependency scope, like a single module's classpath in
   Java — it keeps this project's packages separate from the rest of the system.

5. Confirm the frontend toolchain is ready: node --version (must be v18+) and npm --version.
   Do NOT scaffold the React app yet — I'll do that with the tutor in Milestone 3.

6. When everything above is green, read TUTOR_PROMPT.md and start the tutor from PROGRESS.md
   (Milestone 0). Greet me, confirm my environment is set up, and begin.
```

That's it. Claude Code will verify/install everything, then hand you off to the tutor for
Milestone 0.

---

## If something goes wrong

- **`winget` not found:** Update "App Installer" from the Microsoft Store, or install Node,
  Git, and Python manually from their official websites.
- **`claude` not found after npm install:** Close and reopen PowerShell so PATH refreshes.
- **PowerShell blocks a script (`Activate.ps1`):** You don't need to activate the venv — the
  bootstrap prompt calls `.venv\Scripts\python.exe` directly, which sidesteps it. If you ever
  want activation, run once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- **Stuck on anything:** just tell Claude Code the exact error message — it can diagnose and fix
  from there.
