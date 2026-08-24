# Next Steps — Beyond the Course

You've built a working full-stack app end to end (M0–M5), and picked up the Capstone and/or the
Postgres stretch goal. What's below isn't a new milestone — it's a menu. **Pick whichever path is
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
  foreign keys if you did the Postgres stretch, nested Pydantic models, and a genuinely harder React
  state problem (a list of lists, not a flat list).
- **Rough scope:** a few evenings — bigger than one new field, smaller than auth.
- **Pick this if:** you want more reps on data modeling, or want the frontend state logic to get
  meaningfully harder than M3–M4.

### A3: Deploy it publicly
- **Already got a head start:** if you did M6, you already have `backend/Dockerfile`,
  `frontend/Dockerfile`, and a `docker-compose.yml` that runs both together — this path reuses
  them as-is. You're adding the real Traefik/Cloudflare wiring on top, not starting over.
- **What:** get the app live on a real URL. **Recommended route: the homelab** — containerize the
  backend and frontend (a `Dockerfile` each, frontend served as a static build via nginx), add it
  to a `docker-compose.yml` the same way every other service here works, and expose it through the
  homelab's existing Cloudflare tunnel + Traefik setup — the same pattern that's serving *this
  very environment* to you right now. No new accounts, no new platform to learn from scratch.
  (Alternative if you'd rather not touch shared infra: Railway/Render/Fly.io for the backend,
  Vercel/Netlify for the frontend — one-click PaaS deploys, simpler but a new account and a
  platform-specific config format each.)
- **What it teaches:** writing a production `Dockerfile` (not just running one someone else
  wrote), environment config for prod vs. dev, CORS in a *real* cross-origin deployment (it was a
  no-op in this browser-based environment — see `backend/README.md`) — and, on the homelab route
  specifically, actual reverse-proxy + DNS routing (a Traefik router/service entry and a
  Cloudflare hostname), which is closer to how a real company runs production than a PaaS "click
  deploy" button is.
- **Rough scope:** about a day, mostly config and troubleshooting once the app itself is
  containerized (which is small).
- **Heads up if you go the homelab route:** this touches shared host infrastructure other
  services depend on — loop in Jerrin before exposing anything publicly, same as anyone else
  adding a service to that network. The tutor here can help you write the `Dockerfile`s and
  compose config, but the actual Traefik/Cloudflare wiring on the shared host is a "get sign-off
  first" step, not something to do solo mid-lesson.
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

## Path D — Docker Advanced + a taste of Kubernetes

Builds on M6 — do this after you've got the Dockerfiles/compose file working there. Two
independent pieces; do one or both, in any order.

### D1: Volumes / persistence
- **What:** add a named volume (or bind mount) to the `docker-compose.yml` from M6 so data
  survives `docker compose down` / `up`.
  - If you did the Postgres stretch goal: you've already seen a database container with a
    persisted volume (the sandbox's own `postgres` sidecar) — this is the same idea, but on a
    container you add to your own app's `docker-compose.yml` from M6. A natural follow-on from
    there, if you want it: Alembic migrations, now that you have a real Postgres instance of your
    own to point them at — the Stretch milestone deliberately stopped at
    `Base.metadata.create_all()` and left schema migrations for here.
  - If not: a minimal, self-contained demo still teaches the concept — write a file inside the
    running container, recreate the container, and watch the file disappear; add a volume,
    recreate again, and watch it survive this time.
- **What it teaches:** volumes vs. bind mounts vs. the container's own throwaway filesystem. You
  already lived inside a bind mount for this entire course — this environment's `code-server`
  container has your repo mounted in from the host the whole time — this exercise is that same
  idea, made explicit and hands-on.

### D2: Kubernetes — awareness, not hands-on here
- **What:** a short conceptual mapping session with the tutor, same predict-then-reveal style as
  the rest of the course, not a new milestone:
  - **Pod** ≈ roughly one compose service's running instance.
  - **Deployment** ≈ replica count + rollout management — genuinely new; `docker-compose` doesn't
    really have an equivalent, since it doesn't manage replicas or rolling updates.
  - **Service** ≈ stable networking/load-balancing across replicas — compose's default network
    gives you a weaker version of this for a single instance.
  - **ConfigMap / Secret** ≈ externalized `.env` values.
  - **`kubectl`** ≈ the `docker` CLI's cluster-scale counterpart.
- **Why not on the homelab:** the homelab is already memory-tight (this course fought that limit
  more than once around M2–M4), and a real cluster control plane is a much bigger addition than
  the isolated Docker sandbox M6 gave you — and more importantly, cluster-admin-equivalent access
  is a materially bigger ask than anything else in this course. Not happening on shared infra.
- **If you want to actually try it:** do it on your own laptop via `minikube` — not in this
  environment, since `minikube` needs to run directly on your machine's OS, not inside a
  container inside a container. If you want a guide, ask **local** Claude Code (running directly
  on your laptop, not this browser tab) to walk you through installing `minikube` and deploying
  this same app to it. This is a fully self-directed side quest — `PROGRESS.md` and
  `TUTOR_PROMPT.md` won't track it, and that's fine.

## Path E — AWS Cloud Fundamentals + Kubernetes

A separate repo, not part of this one — cloud infrastructure is different enough content (and a
different audience moment) that it got its own curriculum rather than another bullet here.

- **What:** hands-on AWS fundamentals (S3, DynamoDB, SQS/SNS, IAM, Lambda, EventBridge, Step
  Functions, API Gateway, CloudFormation) against a free local AWS emulator (floci) running in
  the same homelab sandbox you already use — plus a capstone deploying this very Todo app to both
  Lambda and ECS. Wraps up with a Kubernetes primer and deploying the app to a local `minikube`
  cluster on your own machine.
- **What it teaches:** the managed-service equivalents of infra patterns you already know from a
  backend-dev career (a queue, a relational DB, secrets config, container orchestration) — this
  time AWS-shaped — plus real serverless-vs-containers tradeoffs from deploying the same app two
  different ways.
- **Rough scope:** comparable to this whole course, milestone by milestone — not a single
  evening's detour.
- **Getting started:** clone `github.com/jerrinss5/aws-cloud-fundamentals`, open it in this same
  code-server environment (it's a separate top-level folder — `~/aws-fundamentals`, alongside
  this repo's `~/project`), and say "start the tutor" the same way you did here. `aws on`/`aws
  off` toggles the AWS sandbox via Discord, same pattern as `db on`/`db off`.
- **Pick this if:** you want to round out the infra/ops side of your skill set beyond app code —
  this is genuinely new territory (AWS, and separately Kubernetes), not more reps on things
  you've already built.

## Coming back to this later

If you pick a path from here, treat it the same way the core course worked: predict-then-reveal,
you write every line, and — if you're back in this environment — `PROGRESS.md` and
`TUTOR_PROMPT.md` still apply. Just tell the tutor which path (A1/A2/A3/B/C/D/E) you're starting,
so it can adjust its Socratic questions to match — the further you get from the guided
milestones, the more the tutor should lean on "how would you approach this" rather than a fixed
lesson plan.
