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

**Next action:** M3 core content is done (see session log). Two options for next session, her
choice: (a) build optional extra UI polish — an "add task" form and a delete button — before
M4, or (b) skip straight to M4 (wiring fetch calls to the real FastAPI backend) and let
add/delete emerge naturally as real CRUD endpoints get wired up. Either way: remind her the Vite
dev server isn't persistent across sessions (`npm run dev` from `frontend/`), URL is
`https://code.wakehub.org/absproxy/5173/` or `code.home.wakehub.org` (note `/absproxy/`, not
`/proxy/`). The `backend/app.py` regeneration decision from 2026-08-12 was resolved (walkthrough
done, confirmed it matches her memory of M2) — no longer an open item.

## Milestone checklist

- [x] M0 — Orientation & setup
- [x] M1 — Python syntax warm-up (no framework)
- [x] M2 — FastAPI backend (in-memory repository)
- [x] M3 — React + TypeScript frontend (core done: Task interface, TaskItem/TaskList
      components, props, list rendering w/ key, lifted state + callback toggle; optional
      add/delete UI polish not yet built)
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
2026-08-12 — Resumed session: confirmed dev server renders (base path fixed to /absproxy/5173/
last session), flagged the backend/app.py regeneration issue to Chris (decision still open, not
yet answered). Restarted the Vite dev server (not persistent across sessions) and gave her the
link twice. Session paused before opening main.tsx — no M3 app code written yet. Next: recap the
backend/app.py decision + restart Vite server + link, then actually open main.tsx/App.tsx.
2026-08-12 — M3 core complete. Resolved the backend/app.py walkthrough (matched her memory of
M2, no retype needed). Toured main.tsx (JSX, non-null assertion) and the default App.tsx
(useState re-render model, boolean-in-JSX gotcha). Built Task interface, TaskItem and TaskList
components (props, .map() list rendering, key prop), wired sample data into App.tsx, then lifted
state up: useState in App, handleToggle threaded down as a callback prop through TaskList to
TaskItem's button, closure/scoping bug caught along the way. Confirmed working live in browser
(toggle button flips completed state). Flashcard checkpoint 6/6 (one needed a directional
clarify: closures were framed backwards but the concept was there). Next: her choice — optional
add-task/delete UI polish, or skip straight to M4 (wiring fetch calls to the real backend).
