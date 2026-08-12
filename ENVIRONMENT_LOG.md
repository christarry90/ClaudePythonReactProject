# Environment Log

Local-only, never committed (see `.gitignore`) — infrastructure/environment fixes made outside a
teaching session. The tutor reads this at the start of every session (see `TUTOR_PROMPT.md`
Section 8). Newest entries at the top.

---

**2026-08-11 — M4 dev-proxy pattern pre-verified.** Before Chris reaches M4, the
`fetch`-through-Vite-proxy-to-FastAPI pattern documented in `frontend/README.md` was tested
end-to-end against a throwaway config (not her real files): full CRUD through
`code-server → /absproxy/5173/ → Vite proxy (with rewrite) → uvicorn`. Confirmed working. If it
doesn't work when she gets there, something changed — it's not a first-principles problem.

**2026-08-11 — Chris's M2 backend (`backend/app.py`) was lost and reconstructed.** It was never
committed (uncommitted work had no safety net at the time), and was wiped by a container
recreate — exact mechanism unconfirmed, `.bash_history` and VS Code local history were both
empty by the time this was investigated. Rebuilt from `PROGRESS.md`'s session log to match the
original architecture (Task Pydantic model, TaskRepository, TaskService w/ constructor DI, the
Depends()-per-request-vs-singleton-repository lesson, full CRUD, 404 handling). Verified with a
live CRUD smoke test. She did not retype it — see the note in `PROGRESS.md` for the tutor.

**2026-08-11 — Local-only auto-commit safety net added.** `discord-bot` now runs
`git add -A && git commit` (local only, never pushed) on every `done` and on idle auto-stop, to
prevent a repeat of the above. Discord reports "Locally committed your work" / "Saved a local
snapshot" on success.

**2026-08-11 — discord-bot's git operations were running as root, silently breaking her file
permissions.** Every file a merged PR touched (`.gitignore`, `backend/README.md`,
`frontend/README.md`, `TUTOR_PROMPT.md`) ended up root-owned and read-only for the `coder` user
(uid 1000) after a `git pull`, because discord-bot had no `USER` directive. Fixed: discord-bot
now runs as uid 1000, git config moved from `--global` to `--system` (a bare numeric UID has no
resolvable `$HOME`). Existing root-owned files/dirs were chowned back. If you ever see a
"permission denied" saving a file that was recently touched by a merged PR, this is the
likely cause — check `ls -la` ownership before assuming it's a code problem.

**2026-08-11 — Vite dev server: use `/absproxy/<port>/`, not `/proxy/<port>/`.**
code-server's `/proxy/<port>/` strips the path prefix before forwarding to the app; Vite's
`base` config needs to still see that prefix, so it redirect-loops
(`/proxy/5173/proxy/5173/...`). `/absproxy/<port>/` passes the path through unchanged, which is
what Vite needs — this is a documented code-server + Vite interaction, not specific to this
homelab (see coder/code-server#7603). `frontend/vite.config.ts` uses
`base: '/absproxy/5173/'` and `allowedHosts` covering both `code.wakehub.org` and
`code.home.wakehub.org`.

**2026-08-11 — code-server memory limit raised 2G → 3G, core dumps disabled.** A Vite dev
server crash produced a 1.1GB core dump — VS Code + the TS language server + Vite together
exceeded the old 2G container limit. Host (`.54`) is itself memory-constrained (full media
stack), so 3G was a deliberate moderate choice, not maxed out. `ulimits.core: 0` added so a
future crash fails cleanly in logs instead of writing a multi-GB file into the project
directory.

**2026-08-10/11 — `~/.claude.json` and `~/.bash_history` do NOT survive a `code-server`
container recreate.** Only three paths are bind-mounted: `~/.claude/`, `~/project/`, and
`~/.local/share/code-server`. `~/.claude.json` is now also bind-mounted (fixed), so Claude Code
login/project state persists. `~/.bash_history` is still NOT persisted — expect it to be empty
after any container recreate.

**2026-08-09/10 — `code-server`'s network can be dropped by Docker while the container sits
stopped for long stretches** (exact trigger unconfirmed), leaving a stale network reference that
makes `/start` 404. `docker-control`'s `/start` now self-heals this automatically (detects the
missing network, recreates it, retries) — should be invisible going forward, but if `ready`
silently fails, check `docker logs docker-control` for a `NotFound` network error.
