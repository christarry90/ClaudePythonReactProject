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
port-forwarding proxy code-server already gives you instead — either click the "Open in Browser"
notification it pops up when it detects the port, or go directly to
`https://<the-domain-you're-on>/proxy/5173/`.

For that proxy URL to actually render the app (not a blank page or a "This host is not allowed"
error), add this to `vite.config.ts` right after scaffolding, before your first `npm run dev`:

```ts
export default defineConfig({
  plugins: [react()],
  base: '/proxy/5173/',
  server: {
    host: true,
    allowedHosts: ['code.wakehub.org', 'code.home.wakehub.org'],
  },
})
```

**Milestone 4 tip:** when you wire up the backend, point `fetch` calls at a relative path
(`/api/...`) and add a dev proxy instead of hitting `http://localhost:8000` directly — it avoids
CORS entirely and you never have to expose a second port:

```ts
server: {
  host: true,
  allowedHosts: ['code.wakehub.org', 'code.home.wakehub.org'],
  proxy: { '/api': 'http://localhost:8000' },
},
```
