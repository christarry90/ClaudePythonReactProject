# Progress

The tutor (see `TUTOR_PROMPT.md`) reads this file at the start of every session to know where
you are, and updates it at the end of every session. You're welcome to edit it yourself too —
it's your progress, not a black box.

**Current milestone:** Stretch — Postgres + SQLAlchemy persistence — **complete**. Resuming
NEXT_STEPS Path A2 (Tags) frontend next, see below.

**Current step:** Stretch complete end-to-end. Step 3 (`backend/postgres_task_repository.py`)
finished: `add`/`get`/`list`/`update`/`delete` all written and verified live against real
Postgres (caught: invalid `from db import db.X` import syntax → `import db`; bare module-level
functions with `self` but no class → wrapped in `PostgresTaskRepository`; `Task(id=db_task.title,
...)` bug → `db_task.id`; `list`'s `.append(id=..., ...)` bug → `.append(Task(...))`; `update`
initially clobbered unset fields with `None` → fixed with `task_update.model_dump
(exclude_unset=True)` + `setattr` loop, same pattern as the in-memory repo). Step 4 (DI wiring
swap): changed `_repository = TaskRepository()` to `PostgresTaskRepository()` in `app.py` — hit a
real circular import (`app.py` importing `postgres_task_repository` at the top, which imports
`Task`/`TaskCreate`/`TaskUpdate` back from `app` before those classes existed yet); fixed by
moving that one import down to just above the `_repository = ...` line, still module-level, just
positioned after `Task`/`TaskCreate`/`TaskUpdate` are defined — her own correct diagnosis once
prompted to think about *timing* rather than "wrap it in a function." Verified live: `/tasks`
returns the real Postgres rows over HTTP, create round-trips too — zero other route/service code
touched, confirming the M2 abstraction boundary holds. Step 5 (persistence proof): created a task
via HTTP, `db off` in Discord → `/tasks` correctly 500s, `db on` → task confirmed still there.
Step 6: committed (`app.py` + `postgres_task_repository.py`, her own commit message) and pushed
to `mine` — the `gh auth setup-git` fix from the earlier GitHub-push session held up cleanly.

**A2 (Tags) recap:** Backend fully complete and verified live over HTTP — data layer
(`Tag`/`TagCreate`/`TagUpdate`, `TagRepository`, `TaskTagRepository`), `TaskService`/`TagService`
composition with tag hydration (`_hydrate_tasks` helper, her own unprompted DRY extraction), and
all `/tags` CRUD + attach/detach routes (`POST`/`DELETE /tasks/{task_id}/tags/{tag_id}`, her own
route-shape design). Notable bugs caught along the way: the missing-`self.`-on-method-call gotcha
recurred three times across two sessions (flag proactively next time rather than waiting for a
fourth); a real conceptual bug treating "no tags yet" as a 404 instead of a normal empty state;
a route-collision bug where attach/detach were both first registered as `@app.post` on the
identical path. Only the frontend remains (`Tag` type, nested `tags: Tag[]` on `Task`,
`TaskItem.tsx` rendering, attach/detach UI — NEXT_STEPS.md's "list of lists," harder than M3–M4)
— resume after the Postgres stretch completes. Whether `Tag` deletion should cascade/clean up
`TaskTagRepository` entries is still open (correctly placed at the service layer, not implemented,
not blocking frontend work).

**M6 recap:** Backend and frontend fully containerized (`backend/Dockerfile`, `frontend/Dockerfile`
multi-stage build, `frontend/nginx.conf` reverse-proxying `/proxy/8000/` to `backend:8000`,
root `docker-compose.yml`). Verified end-to-end via `docker compose up`. Flashcard 4/4.

**Capstone recap:** Delegated the `priority` field (Task model, backend + frontend) to a
subagent with a scoped, self-contained prompt; it caught a real bug (`TaskRepository.add()`
silently dropping `task_create.priority`) rather than overstepping its "don't touch
TaskRepository" instruction, and she fixed the one-line omission herself. Created the repo's
first `CLAUDE.md` entry (`/absproxy/` vs `/proxy/` Vite gotcha). Covered permission-mode
calibration (reversibility + blast radius, not "how scary it looks") using the real M5
force-push-to-her-own-repo example.

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

**Next action:** Resume NEXT_STEPS Path A2 (Tags) — backend is fully done and verified live over
HTTP (models, all three repositories, TaskService/TagService composition + hydration, all `/tags`
+ attach/detach routes). Only the frontend remains: `Tag` type in `types.ts`, nested `tags: Tag[]`
on `Task`, render tags in `TaskItem.tsx`, and UI to attach/detach a tag from a task (fetch calls to
`POST`/`DELETE /tasks/{task_id}/tags/{tag_id}`) — the harder React state shape NEXT_STEPS.md
flagged ("a list of lists"). Note: the frontend currently fetches against the in-memory-repository
era backend, now Postgres-backed — no frontend changes needed for that, just worth a mention that
data now persists across backend restarts. Course milestones + Capstone + the Postgres stretch are
all now fully done — after A2, `NEXT_STEPS.md`'s other paths (A1 auth, A3 deploy, B portfolio
polish, C interview prep, D Docker/K8s) are open any time.

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
- [x] Capstone — Working with Claude Code at scale (delegated a subagent to add a `priority`
      field end-to-end, created first `CLAUDE.md` entry, covered permission-mode calibration)
- [x] Stretch — Postgres + SQLAlchemy persistence (real Postgres-backed `TaskRepository`,
      DI-swapped in with zero route/service changes, persistence proven via `db off`/`db on`)

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
2026-08-18 — Capstone complete (her choice). Part 1 (subagents): delegated adding a `priority`
field across backend + frontend to a general-purpose subagent, with a scoped, self-contained
prompt (exact file paths, exact type, explicit "verify this assumption" instruction). Subagent
caught a real bug I'd told it not to fix — TaskRepository.add() built Task by named fields and
silently dropped task_create.priority — flagged it instead of overstepping scope; she fixed the
one-line omission herself and correctly explained why add() needed it but update() didn't
(explicit field construction vs. generic model_dump(exclude_unset=True)). Verified live in
browser, then committed locally. Part 2 (CLAUDE.md): created the repo's first CLAUDE.md entry
(the /absproxy/ vs /proxy/ Vite gotcha) — first draft was correct but missing the "where"
(vite.config.ts), self-corrected on one nudge. Part 3 (permission modes): she initially
misremembered PROGRESS.md edits as a confirm-point (they're not — routine local edits are
auto-mode); correctly named the M5 git push. Walked through the actual distinction (reversibility
+ blast radius, not "how scary it looks") using the real M5 force-push-to-her-own-repo example
and the branch-protection hook that hard-blocks origin/main but allows her mine remote. Course
milestones are now fully complete. Next: her choice, any time — NEXT_STEPS.md menu (app
extension, portfolio polish, interview prep, Docker volumes/K8s primer) or the SQLite/SQLAlchemy
stretch goal.
2026-08-18 (cont'd) — Started NEXT_STEPS Path A2 (Tags, many-to-many), her pick from Path A after
choosing it over auth/deploy. Correctly reasoned unaided that Tags (not Projects) was the harder
option because there's no join table in a plain dict-backed repository, and correctly mapped JPA's
`@ManyToMany` (auto-generated join table, hydrated objects) to what we'd have to hand-roll instead.
Correctly placed the join table in its own `TaskTagRepository`, not bolted onto `TaskRepository`/
`TagRepository`. Built `Tag`/`TagCreate`/`TagUpdate` models and `TagRepository` (mirrored
`TaskRepository` cleanly, one naming nudge: renamed `Tag.title` to `.name`). `TaskTagRepository`
took more iterations: missed `self` on `add_tag` initially (fixed), then the same `self` omission
recurred on `remove_tag`/`get_tags_for_task` right after (fixed again — flagging this as a pattern
to watch for next session, not just a one-off), plus a real logic bug in `remove_tag` (`del
self._task_tags[task_id]` deleted the whole task's tag set instead of removing one tag via
`.discard(tag_id)` — walked through a concrete trace to find it, then fixed correctly). Added a
new ROSETTA.md row (many-to-many / hand-rolled join table vs `@ManyToMany`). Backend imports
clean; stopped before the harder part (TaskService composition across three repositories, /tags
routes, frontend). Next: resume mid-feature — see "Current step" above.
2026-08-19 — Resumed Path A2 (Tags) same-day, before lunch. Added `tags: list[Tag] = []` to Task
(caught + fixed a class-definition-order bug: Task referenced Tag before its definition, same
category as last session's TagUpdate forward-reference bug). Composed TaskService across all
three repositories (constructor + module-level singletons), extracted a private `_hydrate_tasks`
helper on her own initiative to avoid duplicating hydration logic across get_task/list_tasks —
good unprompted DRY instinct. Caught several bugs: the missing-`self.`-on-method-call gotcha
recurred a third time (across two sessions now — proactively flag this pattern next session
rather than waiting for it); an undefined `task_id` reference inside `_hydrate_tasks` (should've
been `task.id`); a real conceptual bug treating "no tags yet" (`None` from `get_tags_for_task`) as
a 404 instead of a normal empty state, which would've broken fetching any untagged task; and a
list_tasks reassignment-doesn't-mutate bug, which she fixed herself correctly and unprompted with
a `new_list` accumulator. Verified hydration end-to-end via a live Python smoke test (tagged task
→ nested Tag object, list_tasks hydrates all, untagged task → `tags: []`). Paused for lunch before
building /tags routes.
2026-08-19 (cont'd) — Resumed after lunch, finished the entire backend for Tags. Built TagService
(one bug: get_tag referenced a nonexistent self.tag_create instead of self._tag_repository) plus
its DI wiring. She independently designed the attach/detach route shape (POST/DELETE
/tasks/{task_id}/tags/{tag_id}) and correctly reasoned attach/detach belongs on TaskService, not
TagService, since it's the only service with all three repositories. Wrote attach_tag/detach_tag
(one bug: called a nonexistent TaskTagRepository.detach_tag instead of the real remove_tag) and
all /tags CRUD + attach/detach routes (one real bug, not style: both attach and detach were first
registered as @app.post on the identical path — a route collision, not just a nitpick — fixed to
@app.delete for detach). Verified the whole feature live over HTTP with uvicorn + curl: attach
returns a hydrated nested Tag object, detach clears it, get_task independently confirms
persistence, attaching a nonexistent tag 404s cleanly. Backend for Path A2 is fully complete.
Next: frontend — Tag type, nested tags on Task, TaskItem rendering, attach/detach UI.
2026-08-20 — Pushed 27 local commits to her `mine` GitHub remote (christarry90/
ClaudePythonReactProject) — clean fast-forward, nothing diverged. Hit and fixed a real auth
issue along the way (logged to ENVIRONMENT_LOG.md): gh auth login alone wasn't sufficient, since
~/.gitconfig never existed and GIT_ASKPASS pointed at a dead VS Code IPC socket — fixed via `gh
auth setup-git` plus unsetting GIT_ASKPASS for the push. She asked about a new curriculum commit
(PR #15, already merged into main) that replaced the SQLite stretch milestone with Postgres +
SQLAlchemy — walked her through TUTOR_PROMPT.md Section 13's new content. She chose to switch
over to the Postgres stretch now, pausing Path A2 (Tags) with only its frontend remaining.
Completed Postgres Steps 1–2 in full (raw psql CREATE TABLE/\d/INSERT...RETURNING with real bugs
caught — INT(1) is MySQL syntax not Postgres, and an uppercase/lowercase priority-value
mismatch both self-corrected; SQLAlchemy Base/Task model + engine/session in new backend/db.py,
verified connecting live; backend/.env created only after confirming .gitignore excludes it,
unprompted good instinct, with two self-corrected bugs — a typo and a missing password). Started
Step 3 (backend/postgres_task_repository.py) — add()/get() begun but left with real uncorrected
bugs when she paused for lunch + a team meeting.
2026-08-20 (cont'd) — Resumed after lunch + team meeting, finished the Postgres stretch end to
end. Step 3: fixed all four bugs left in postgres_task_repository.py from before lunch (invalid
`from db import db.X` import syntax, missing class wrapper around bare `add`/`get` functions,
`Task(id=db_task.title, ...)` → `.id`, empty `get()` stub), then wrote `list`/`update`/`delete`
from scratch against the in-memory `TaskRepository`'s interface as the reference shape — caught a
`.append(id=..., ...)` bug (list.append takes one positional item, not kwargs) and, in `update`,
correctly reasoned through why unconditionally assigning all three fields from `TaskUpdate` would
null out fields the caller didn't set, fixing it with the same `model_dump(exclude_unset=True)`
pattern as the in-memory repo. All five methods verified live against real Postgres. Step 4: DI
wiring swap in app.py surfaced a genuine circular import (app.py importing
postgres_task_repository at module top, which imports Task/TaskCreate/TaskUpdate back from app
before those classes existed) — she correctly diagnosed it as a timing problem once prompted, not
a "wrap in a function" problem, and moved the import below the Task/TaskCreate/TaskUpdate
definitions. Verified live over HTTP with zero route/service code changes — the M2 abstraction
boundary held. Step 5: persistence proven live (create via HTTP → db off → 500 confirmed → db on
→ task confirmed still present, contrasted against in-memory data which dies on a mere restart).
Step 6: committed and pushed to mine — the earlier gh auth setup-git fix held up. Postgres +
SQLAlchemy stretch is now fully complete. Next: resume NEXT_STEPS Path A2 (Tags) frontend — Tag
type, nested tags on Task, TaskItem rendering, attach/detach UI.
