# Next Steps — Beyond the Course

You've built a working full-stack app end to end (M0–M5), and picked up the Capstone and/or the
SQLite stretch goal. What's below isn't a new milestone — it's a menu. **Pick whichever path is
useful to you right now, skip the rest, or come back to any of them later.** Nothing here is
sequential and nothing here is required.

## Path A — Extend your Todo app

Three independent options. Each builds on the app you already have — no new project to start
from scratch. Pick one, or do more than one, in any order.

### A1: Add authentication
- **What:** user accounts, login, and scoping tasks to the signed-in user.
- **What it teaches:** FastAPI security dependencies (`OAuth2PasswordBearer`, JWTs), password
  hashing (`passlib`/`bcrypt`), protecting routes with `Depends(get_current_user)` — this is the
  closest Python equivalent to Spring Security you'll touch.
- **Rough scope:** a weekend project, bigger than anything in the core course.
- **Pick this if:** security/auth is what you most want to be strong on for the job market.

### A2: Add a second resource with relationships
- **What:** e.g. "Projects" that own many "Tasks" (one-to-many), or "Tags" on tasks
  (many-to-many).
- **What it teaches:** relational modeling inside the repository pattern you already built,
  foreign keys if you did the SQLite stretch, nested Pydantic models, and a genuinely harder React
  state problem (a list of lists, not a flat list).
- **Rough scope:** a few evenings — bigger than one new field, smaller than auth.
- **Pick this if:** you want more reps on data modeling, or want the frontend state logic to get
  meaningfully harder than M3–M4.

### A3: Deploy it publicly
- **What:** get the app live on a real URL — Railway/Render/Fly.io for the backend,
  Vercel/Netlify for the frontend (or self-host, if you want to see how the homelab side of this
  works).
- **What it teaches:** environment config for prod vs. dev, CORS in a *real* cross-origin
  deployment (it was a no-op in this browser-based environment — see `backend/README.md`), and a
  build/deploy pipeline — genuinely new territory next to a Spring Boot deploy.
- **Rough scope:** about a day, mostly config and troubleshooting rather than new code.
- **Pick this if:** you want a live demo link for your resume/LinkedIn, not just a GitHub repo.

## Path B — Portfolio polish

Not a project — a checklist for the repo you already have. An afternoon, any time, doesn't
depend on Path A.

- [ ] Add 2–3 screenshots (or a short screen recording) near the top of your repo's `README.md`
  so someone can see what it does without cloning it.
- [ ] Add a "What I built / what I learned" section — the Java→Python/TS correlations you made
  are exactly the kind of specific, technical detail that stands out in a portfolio README over
  generic "built a todo app" copy.
- [ ] Add a few tests (backend: `pytest` for the service/repository layer; frontend: a component
  test or two) — even a small suite signals more than a big one added late.
- [ ] If you did A3, link the live demo at the very top.
- [ ] Re-read your own commit history (`git log --oneline`) and make sure the messages read like
  something you'd want an interviewer to see.

## Path C — Interview prep, using Claude as a practice partner

Not a one-time task — a skill worth keeping after the course ends. This repo *is* the project
you'll bring up in interviews, so practicing on it directly is the point. Sample prompts to run
against Claude:

- *"Quiz me on FastAPI dependency injection like a technical interviewer would — one question at
  a time, don't give the answer away."*
- *"Here's a diff from my Todo app: [paste]. Review it like an interviewer would in a code-review
  round — ask me to defend the design choices, don't just praise it."*
- *"Compare Python's dict-based repository pattern against a Java `JpaRepository`, the way I'd
  need to explain it out loud if asked to walk through this project."*
- *"Give me a mock 'walk me through a project you built' interview question about this app, then
  interrupt me if I'm being vague or hand-wavy."*

## Coming back to this later

If you pick a path from here, treat it the same way the core course worked: predict-then-reveal,
you write every line, and — if you're back in this environment — `PROGRESS.md` and
`TUTOR_PROMPT.md` still apply. Just tell the tutor which path (A1/A2/A3/B/C) you're starting, so
it can adjust its Socratic questions to match — the further you get from the guided milestones,
the more the tutor should lean on "how would you approach this" rather than a fixed lesson plan.
