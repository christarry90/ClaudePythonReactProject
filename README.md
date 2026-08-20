# Java → Full-Stack: Python/FastAPI + React/TypeScript

A guided, hands-on path for a Java backend developer to gain confidence in Python/FastAPI and
React/TypeScript — by building a small Todo/Task board app, one milestone at a time, with an
AI tutor that remembers where you left off.

## Who it's for

An **experienced Java backend developer**, not a programming beginner. This is not a "learn to
code" course — it assumes you already know how to design systems, model data, write tests, and
reason about layered architecture, dependency injection, and REST APIs.

The goal is **syntax fluency and full-stack mental models**, built by continuously correlating
new material back to the Java you already know: "Java has X — Python/TypeScript has Y." If
you're looking for an intro-to-programming course, this isn't it. If you're a Java dev who wants
to stop feeling slow in Python and React, this is exactly it.

## How it works

1. Either paste [`TUTOR_PROMPT.md`](TUTOR_PROMPT.md) into a Claude conversation, or open this
   repo in **Claude Code** and say "start the tutor" — Claude Code can read and write
   `PROGRESS.md` and `ROSETTA.md` directly, which makes it the smoother option.
2. The tutor is **Socratic**: for every new concept, it asks "How would you do this in Java?"
   before showing you the Python or React/TypeScript equivalent, side by side.
3. The tutor is **stateful**: it reads [`PROGRESS.md`](PROGRESS.md) at the start of every
   session so you can pick up exactly where you left off, and updates it at the end.
4. The tutor is **forgiving on syntax and strict on concepts** — "grade concepts, not
   semicolons." A missing colon or misplaced brace isn't the point; whether you've correctly
   mapped the Java pattern to its Python/TS equivalent is.
5. **You write every line.** The tutor guides and reviews; it never hands you finished code you
   didn't type yourself.

## The four learning aids

- **Inline comparison tables** — Java vs. Python/TS shown side by side as each concept is
  introduced.
- **[`ROSETTA.md`](ROSETTA.md)** — a growing Java ↔ Python ↔ TypeScript cheat-sheet, gaining a
  new row after every lesson.
- **Flashcard checkpoints** — a quick recall round at the end of each milestone: "Java has X —
  what's the Python/TS equivalent?"
- **The in-app `/rosetta` panel** — in Milestone 5, `ROSETTA.md` gets rendered live inside the
  app itself, turning your cheat-sheet into a feature of the product you built.

## Milestone arc

- **M0 — Orientation & setup.** Confirm your environment, read the backend/frontend READMEs,
  set expectations.
- **M1 — Python syntax warm-up (no framework).** Core Python: variables, functions, control
  flow, comprehensions, collections, classes.
- **M2 — FastAPI backend (in-memory repository).** Build the Task API with Pydantic models, a
  service layer, and a `dict`-backed repository.
- **M3 — React + TypeScript frontend.** Scaffold with Vite, build components, props, state, and
  typed interfaces for the Task shape.
- **M4 — Wire frontend + backend.** `fetch`, CORS, and full CRUD from the UI against the FastAPI
  backend.
- **M5 — In-app `/rosetta` panel + polish + push to GitHub.** Render `ROSETTA.md` live in the
  app, polish the app, and publish the repo.
- **M6 — Containerize your app with Docker.** Write Dockerfiles for the backend and frontend,
  then a `docker-compose.yml` running both together, inside an isolated sandbox.
- **Capstone — Working with Claude Code at scale.** A short exercise in delegating work to
  subagents and using project memory (`CLAUDE.md`), using the app you just built as the example.
- **Stretch — Postgres + SQLAlchemy persistence.** Swap the in-memory repository for a real
  Postgres server without changing its interface.

## After the course

Once the milestones (and Capstone/stretch) are done, [`NEXT_STEPS.md`](NEXT_STEPS.md) is a menu
of optional, parallel paths — extending the app, polishing the portfolio, interview prep with
Claude, and going deeper on Docker plus a Kubernetes-awareness primer. Pick whichever is useful;
none of it is required or sequential.

## Working with Claude

Alongside the curriculum, [`WORKING_WITH_CLAUDE.md`](WORKING_WITH_CLAUDE.md) is a running
companion guide to working with Claude and Claude Code well — context management, effective
prompting, debugging, code review as a habit, and plan mode. The tutor points you to it at
natural moments; you can also just read it whenever.

## Quickstart

**On Windows, starting from a fresh laptop?** Follow [`SETUP_WINDOWS.md`](SETUP_WINDOWS.md) — it
installs Node, Claude Code, Git, and Python, and hands you off to the tutor.

Otherwise:

```bash
git clone https://github.com/jerrinss5/java-to-fullstack
cd java-to-fullstack
```

Then either:

- **Open the repo in Claude Code** and say: `start the tutor`, or
- **Paste [`TUTOR_PROMPT.md`](TUTOR_PROMPT.md)** into a Claude conversation, and paste the
  contents of `PROGRESS.md` (and `ROSETTA.md`, once it has rows) back when the tutor asks for
  them.

## Tech stack

- **Backend:** FastAPI + Pydantic, in-memory dict repository to start; Postgres via SQLAlchemy is
  an optional stretch milestone once the core app works.
- **Frontend:** React + TypeScript + Vite.

## Repo map

```
.
├── README.md          # you are here
├── SETUP_WINDOWS.md    # zero-to-running setup for a Windows laptop
├── WORKING_WITH_CLAUDE.md  # companion guide: context mgmt, prompting, debugging, plan mode
├── TUTOR_PROMPT.md     # the tutor prompt — paste into Claude or run via Claude Code
├── PROGRESS.md         # stateful session tracker: milestone, next step, session log
├── ROSETTA.md          # growing Java ↔ Python ↔ TypeScript cheat-sheet
├── NEXT_STEPS.md       # optional, parallel paths after the course: extend, polish, interview prep
├── backend/            # FastAPI app — built during M2 (starts empty on purpose)
└── frontend/           # React + TypeScript app — built during M3 (starts empty on purpose)
```
