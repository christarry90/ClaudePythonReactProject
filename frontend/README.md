# Frontend (React + TypeScript)

You build this during **Milestone 3**. It starts empty on purpose — you scaffold and write it yourself.

## Java mental model

Components ≈ reusable UI classes; props ≈ constructor args; TS interfaces ≈ Java interfaces/records.

## Scaffold (Milestone 3, with the tutor)

```bash
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

## Previewing it in the browser

**Local Windows setup:** open `http://localhost:5173` — done.

**Browser-based environment (`code.wakehub.org` / `code.home.wakehub.org`):** the dev server
runs inside the container, so `localhost:5173` means *your* laptop, not the container. Use the
port-forwarding proxy code-server already gives you instead — go directly to
`https://<the-domain-you're-on>/absproxy/5173/`.

Use `/absproxy/`, not the `/proxy/` path code-server's "Open in Browser" notification suggests —
`/proxy/` strips the path prefix before forwarding to the dev server, but Vite needs to see its
own base path in the incoming request or it redirect-loops. `/absproxy/` passes the path through
unchanged instead. Add this to `vite.config.ts` right after scaffolding, before your first
`npm run dev`:

```ts
export default defineConfig({
  plugins: [react()],
  base: '/absproxy/5173/',
  server: {
    host: true,
    allowedHosts: ['code.wakehub.org', 'code.home.wakehub.org'],
  },
})
```

**Milestone 4 tip:** point `fetch` calls straight at the backend — no Vite dev proxy needed here,
unlike the frontend-access problem above. That's because FastAPI doesn't care about a `base`
path the way Vite does, and in the browser-based environment the frontend
(`/absproxy/5173/...`) and backend (`/proxy/8000/...`) are both proxied through the *same*
origin (`code.wakehub.org`) — the browser sees that as same-origin, so CORS never even enters
the picture there.

```ts
// Local Windows setup
fetch('http://localhost:8000/tasks')

// Browser-based environment
fetch('/proxy/8000/tasks')
```

CORS only actually matters for the **local Windows setup**, where the frontend
(`localhost:5173`) and backend (`localhost:8000`) are genuinely different origins — see
`backend/README.md` for the `CORSMiddleware` you'll need there. Confirmed working end-to-end in
the browser-based environment: full add/toggle/delete round trip, verified after a page reload.
