# Progress

The tutor (see `TUTOR_PROMPT.md`) reads this file at the start of every session to know where
you are, and updates it at the end of every session. You're welcome to edit it yourself too —
it's your progress, not a black box.

**Current milestone:** M6 — Containerize your app with Docker (complete)

**Current step:** Backend and frontend are both fully containerized. `backend/Dockerfile`
(`python:3.11-slim`, copy `requirements.txt` + install before copying source for layer caching,
`CMD` runs `uvicorn` without `--reload`) plus `backend/.dockerignore` (`.venv`, `__pycache__`).
`frontend/Dockerfile` is a multi-stage build: stage 1 (`node:20 AS build`) runs `npm ci` +
`npm run build`; stage 2 (`nginx:alpine`) copies the built `dist/` in via `COPY --from=build`,
plus a custom `frontend/nginx.conf` copied to `/etc/nginx/conf.d/default.conf` that reverse-proxies
`/proxy/8000/` to `http://backend:8000/` — needed because the frontend's `fetch` calls are
hardcoded to that code-server-specific dev-proxy path, which means nothing outside code-server.
Root `docker-compose.yml` defines `backend` (build `./backend`, port `8000:8000`) and `frontend`
(build `./frontend`, port `8080:80`, `depends_on: backend`) — service name `backend` doubles as
the DNS hostname nginx's `proxy_pass` resolves automatically inside the Compose network. Verified
end-to-end via `docker compose up`: `curl dind:8080/proxy/8000/tasks` round-trips through nginx to
the FastAPI backend and back. Flashcard checkpoint 4/4, no hints needed.

**M6 environment note:** the Docker-in-Docker sandbox starts/stops via Discord (`docker on` /
`docker off`), not a terminal `docker compose` command — see `ENVIRONMENT_LOG.md`. Also: her
shell's `DOCKER_HOST` points at the remote `dind` daemon, so published container ports are only
reachable via the `dind` hostname (e.g. `curl dind:8000/tasks`), **not** `localhost` — despite
what `TUTOR_PROMPT.md`'s M6 section currently says (stale, flagged in `ENVIRONMENT_LOG.md`).

**M5 recap:** In-app `/rosetta` panel (`react-markdown` + `remark-gfm`) + styling polish, and her
first push to her own GitHub repo (`christarry90/ClaudePythonReactProject`).

**Environment note:** Neither dev server is persistent across sessions and both have died
mid-session at least once this environment (memory pressure, not code issues — see
`ENVIRONMENT_LOG.md`). Start both at the top of each session:
- Backend: `cd backend && .venv/bin/uvicorn app:app --reload --host 0.0.0.0 --port 8000`
- Frontend: `cd frontend && npm run dev`
Frontend URL: `https://code.wakehub.org/absproxy/5173/` or `code.home.wakehub.org` (note
`/absproxy/`, not `/proxy/`). Frontend's `fetch` calls target the backend via
`/proxy/8000/...` (relative path — note `/proxy/`, not `/absproxy/`, since FastAPI's plain
route paths need the prefix stripped before it reaches them, unlike Vite).

**Next action:** M6 is complete. Next session: her choice — Capstone (working with Claude Code
at scale) or the SQLite/SQLAlchemy persistence stretch goal.

## Milestone checklist

- [x] M0 — Orientation & setup
- [x] M1 — Python syntax warm-up (no framework)
- [x] M2 — FastAPI backend (in-memory repository)
- [x] M3 — React + TypeScript frontend (complete: Task interface, TaskItem/TaskList
      components, props, list rendering w/ key, lifted state, toggle/add/delete all wired
      via callback props)
- [x] M4 — Wire frontend + backend (fetch, CORS, CRUD — GET on mount, POST/PUT/DELETE all
      round-trip through the real backend; id type mismatch (string vs int) caught and fixed)
- [x] M5 — In-app `/rosetta` panel (react-markdown + remark-gfm) + styling polish + pushed to
      her own GitHub repo (christarry90/ClaudePythonReactProject) for the first time
- [x] M6 — Containerize your app with Docker (backend + frontend Dockerfiles, multi-stage
      frontend build, nginx reverse-proxy config, docker-compose.yml, verified end-to-end)
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
2026-08-14 — M5 kickoff (paused for lunch mid-milestone): built the in-app /rosetta panel.
Backend: GET /readRosetta endpoint (new ReadFile Pydantic model, Path(__file__).parent.parent for
a cwd-independent path to ROSETTA.md — caught a response_model mismatch and a bad path along the
way). Frontend: chose react-markdown (her call, over hand-parsing the table) for Rosetta.tsx;
several early draft bugs caught (invalid `function X() =`, no return statement, JSX built inside
useEffect instead of returned from the component, `str` vs `string`, not unwrapping the
`{content}` response shape, referencing the setter/effect-fn instead of state in JSX, mismatched
import name vs JSX tag). Learned GFM tables need the remark-gfm plugin (core markdown spec doesn't
include table syntax) — installed it, wired in, confirmed table renders correctly in browser. Also
learned plain `tsc --noEmit` silently no-ops on this project due to project references; `tsc -b
--noEmit` is the real check. Toggle button in App.tsx switches between task view and rosetta view.
Next: general polish (button copy, styling), then push to GitHub for the first time.
2026-08-14 — M5 complete (resumed after lunch). Fixed the toggle button's static label with a
ternary. Added basic styling: rewrote App.css from scratch (old file was dead Vite boilerplate,
never imported — caught and fixed the missing `import './App.css'` too), caught a structural
bug where `.add-task-form`'s flex rule was on a wrapper div instead of the form element itself
so it never reached the input/button, and fixed an invalid `box-shadow: inset;` declaration.
Then walked through her first GitHub push live: gh auth login (device code flow), gh repo create,
added a second `mine` remote (this repo's `origin` is the public curriculum repo, not hers),
committed, pushed. Caught a commit-authored-with-wrong-email mistake after the fact; fixed via
amend --reset-author + force-push (safe, her own solo fresh repo). Confirmed live on GitHub:
christarry90/ClaudePythonReactProject. Next: her choice — Capstone or the SQLite/SQLAlchemy
stretch goal.
2026-08-17 — M6 complete (her choice over Capstone/stretch). Hit an environment blocker first:
the Docker-in-Docker sandbox's compose file isn't reachable from inside code-server at all
(flagged, then fixed by Jerrin mid-session — sandbox now starts via Discord `docker on`/`docker
off`). Built `backend/Dockerfile` (base image, WORKDIR, copy-then-install layering for cache
efficiency, RUN vs CMD distinction caught cleanly) and `backend/.dockerignore` after catching a
`.venv` bloat issue during the first build. Built `frontend/Dockerfile` as a multi-stage build
(Node build stage + nginx serve stage, `COPY --from=`) — caught a `COPY` multi-source trailing-
slash requirement, a wrong `COPY` destination, and a filename typo along the way. Diagnosed that
the frontend's hardcoded `/proxy/8000/` fetch paths (code-server-specific) wouldn't work outside
code-server, and fixed it with a `frontend/nginx.conf` reverse-proxying to the backend by Compose
service name — a real architecture problem, not scripted busywork. Wrote `docker-compose.yml`
(several iterations on YAML nesting/service-naming mixups: service name must match the nginx
proxy target, `container_name` vs. service-key confusion, absolute vs. relative build paths).
Hit and correctly diagnosed a second environment issue (published ports reachable via the `dind`
hostname, not `localhost`, due to the remote `DOCKER_HOST` — logged, not a real bug). Verified
the full stack end-to-end. Flashcard checkpoint 4/4 clean, no hints. Next: her choice — Capstone
or the SQLite/SQLAlchemy stretch goal.
