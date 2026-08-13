# Progress

The tutor (see `TUTOR_PROMPT.md`) reads this file at the start of every session to know where
you are, and updates it at the end of every session. You're welcome to edit it yourself too —
it's your progress, not a black box.

**Current milestone:** M4 — Wire frontend + backend (complete)

**Current step:** Frontend is fully wired to the real FastAPI backend — no more local-only
`useState` data. `useEffect` fetches tasks from the backend on mount; add/toggle/delete all make
real `POST`/`PUT`/`DELETE` calls and update state from the server's response. CORS configured on
the backend (`CORSMiddleware`, `allow_origins=["*"]`, no credentials). Fixed a real type bug along
the way: `Task.id` was typed `string` in the frontend but the backend's Pydantic model uses
`int` — corrected to `number` across `types.ts`, `App.tsx`, `TaskList.tsx`, `TaskItem.tsx`;
`tsc --noEmit` clean. Full round trip (add/toggle/delete, then page reload) confirmed working —
tasks persist server-side now, not just in React state.

**Environment note:** Neither dev server is persistent across sessions and both have died
mid-session at least once this environment (memory pressure, not code issues — see
`ENVIRONMENT_LOG.md`). Start both at the top of each session:
- Backend: `cd backend && .venv/bin/uvicorn app:app --reload --host 0.0.0.0 --port 8000`
- Frontend: `cd frontend && npm run dev`
Frontend URL: `https://code.wakehub.org/absproxy/5173/` or `code.home.wakehub.org` (note
`/absproxy/`, not `/proxy/`). Frontend's `fetch` calls target the backend via
`/proxy/8000/...` (relative path — note `/proxy/`, not `/absproxy/`, since FastAPI's plain
route paths need the prefix stripped before it reaches them, unlike Vite).

**Next action:** M4 is complete. Next session: M5 — build the in-app `/rosetta` panel (rendering
`ROSETTA.md`'s content in the app itself), general polish, then push to GitHub.

## Milestone checklist

- [x] M0 — Orientation & setup
- [x] M1 — Python syntax warm-up (no framework)
- [x] M2 — FastAPI backend (in-memory repository)
- [x] M3 — React + TypeScript frontend (complete: Task interface, TaskItem/TaskList
      components, props, list rendering w/ key, lifted state, toggle/add/delete all wired
      via callback props)
- [x] M4 — Wire frontend + backend (fetch, CORS, CRUD — GET on mount, POST/PUT/DELETE all
      round-trip through the real backend; id type mismatch (string vs int) caught and fixed)
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
2026-08-13 — M3 optional polish: built AddTaskForm (local input state, controlled input,
preventDefault, crypto.randomUUID() for new ids) and a delete button, both wired via the same
lifted-state + callback-prop pattern (handleAddTask/handleDelete in App, threaded through
TaskList to TaskItem). Introduced the functional-updater setState form
(`setTasks((prev) => ...)`) as the safer default over reading state directly from closure. All
three CRUD-like actions (toggle/add/delete) confirmed working live in browser. M3 fully complete.
Next: M4 — wire fetch calls to the real FastAPI backend.
2026-08-13 — M4 complete. Covered CORS (browser-enforced, not server-level) and fixed it on the
backend with CORSMiddleware (caught a missing import and an invalid allow_origins=["*"] +
allow_credentials=True combo along the way). Covered useEffect for mount-time fetching (empty
dep array, async-inner-function pattern since the effect callback itself can't be async). Wired
GET (load on mount), POST (add), PUT (toggle), and DELETE (delete) end-to-end against the real
FastAPI backend, replacing all local-only state mutation — each took a few iterations to land
(wrong HTTP verb, url template-literal quoting, request body shape, using the response to update
state instead of the stale local computation). Caught a real type bug: Task.id was declared
string in TS but the backend returns int; fixed across all four frontend files, tsc clean. Backend
process died mid-session from environment memory pressure (twice) — restarted, not a code issue.
Full round trip incl. page reload confirmed working (tasks persist server-side). Next: M5 — build
the in-app /rosetta panel, polish, push to GitHub.
