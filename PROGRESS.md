# Progress

The tutor (see `TUTOR_PROMPT.md`) reads this file at the start of every session to know where
you are, and updates it at the end of every session. You're welcome to edit it yourself too —
it's your progress, not a black box.

**Current milestone:** M3 — React + TypeScript frontend (in progress)

**Current step:** Vite scaffold complete (`frontend/` has a working `react-ts` project),
dev server confirmed rendering in the browser. Two separate issues fixed in
`frontend/vite.config.ts`: `server.host: true` + `server.allowedHosts:
['code.wakehub.org', 'code.home.wakehub.org']` (Vite's host-header protection, covering both
URLs this environment is reachable on), and `base: '/absproxy/5173/'` — **not** `/proxy/5173/`,
which redirect-loops for Vite specifically (code-server's `/proxy/` strips the path prefix
before forwarding, but Vite needs to see it; `/absproxy/` passes it through unchanged). The
earlier blank page was actually the code-server container running out of memory (VS Code +
TypeScript + the dev server exceeded its old 2G limit), fixed infrastructure-side (more memory
headroom). No further action needed on either — both confirmed fixed and verified working.

**Last session covered:** M0, M1, and all of M2 (see earlier log entries — full CRUD FastAPI
backend, complete).

**Heads up for the tutor:** the original `backend/app.py` was lost to an infrastructure issue
(container recreate wiped an unpersisted path) before it was ever committed. It's been
reconstructed to match this file's session log exactly — same architecture (Task Pydantic
model, TaskRepository, TaskService with constructor DI, the Depends()-per-request-vs-singleton-
repository pattern), same endpoints, verified with a live CRUD smoke test. It was NOT retyped by
Chris. Don't assume she has fresh muscle memory of it — when M4 needs the backend, do a quick
verbal walkthrough of `backend/app.py` together first (2-3 minutes, not a full re-teach) so she
can confirm it matches what she remembers building, before wiring the frontend to it.

**Next action:** Start the real M3 content: tour
`main.tsx`/`App.tsx`/`index.html` and connect them to the Spring Boot "bootstrap" mental model,
then start building components, props, state, and a `Task` TypeScript interface — no backend
calls yet (that's M4).

## Milestone checklist

- [x] M0 — Orientation & setup
- [x] M1 — Python syntax warm-up (no framework)
- [x] M2 — FastAPI backend (in-memory repository)
- [ ] M3 — React + TypeScript frontend (scaffolded, dev server confirmed working, app code not started)
- [ ] M4 — Wire frontend + backend (fetch, CORS, CRUD)
- [ ] M5 — In-app `/rosetta` panel + polish + push to GitHub
- [ ] Capstone — Working with Claude Code at scale
- [ ] Stretch — SQLite + SQLAlchemy persistence

## Session log

The tutor appends a one-line, dated entry here at the end of every session (e.g.
`2026-07-22 — Covered M0 setup; confirmed Python/Node installed; next: M1 variables & functions.`).

2026-08-10 — Covered M0 setup (toolchain confirmed) and all of M1 (list, dict, set,
comprehensions, self/__init__, truthiness); flashcard checkpoint 5/5.
2026-08-10 — M2 kickoff: Task Pydantic model, route param binding rules, hand-wrote
TaskRepository (fixed a router/repository layering mixup along the way); next: TaskService +
Depends() DI, then wire the router.
2026-08-10 — M2 continued: built TaskService (DI via constructor), worked through the
Depends()-per-request singleton gotcha, wired POST /tasks and GET /tasks/{id} end-to-end
including HTTPException 404 handling; next: list/update/delete endpoints, then M2 wrap-up.
2026-08-10 — M2 complete: list/update/delete endpoints wired end-to-end (repository, service,
router); flashcard checkpoint 6/6; next: M3, scaffold the Vite/React/TS frontend.
2026-08-11 — M3 kickoff: scaffolded Vite/React/TS in frontend/. Spent the session on dev-server
proxy config (host, allowedHosts, base path for this code-server environment's /proxy/<port>/
routing) rather than app code; server confirmed correct via curl but browser still showed a
blank page (likely stale cache, unconfirmed). Next: confirm the page actually loads, then start
touring main.tsx/App.tsx and building components.
2026-08-11 — Infra recovery: backend/app.py was lost (uncommitted, wiped by a container
recreate) and has been reconstructed to match this log's description of M2 (Task model,
TaskRepository, TaskService, full CRUD, Depends() DI). Verified working via CRUD smoke test.
Chris did not retype it — tutor should walk through it with her briefly before M4 builds on it.
