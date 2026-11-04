# Ronnia dashboard

This is the standalone [aticie/ronnia-web](https://github.com/aticie/ronnia-web) Vue dashboard for the [Ronnia Rust backend](https://github.com/aticie/ronnia). The integration retains this repository's appearance, settings controls, community links, and live-stream cards from commit `ec0ff76ef8e3b06c873f5213c71a0901ef6514f9`. That snapshot did not include a LICENSE file; this integration does not assign a new license to the existing source.

## Local Compose

Deploy the backend first from the root of `aticie/ronnia`, following that repository's README. Its Compose project runs only the Rust backend, published on loopback port `${BIND_PORT:-8080}`, and creates the shared Docker network `${RONNIA_NETWORK:-ronnia}`. Configure the backend with `PUBLIC_ORIGIN=http://localhost:3000`, `API_ORIGIN=http://localhost:8080`, and `COOKIE_SECURE=false` for local HTTP. Provider credentials and session data stay in the backend; do not copy its `.env` into this repository.

Then, from this repository root:

```sh
docker compose up --build -d
```

This standalone Compose project runs only the Nginx dashboard at `http://localhost:3000`. It publishes `${WEB_PORT:-3000}` on loopback and joins the backend-created external Docker network `${RONNIA_NETWORK:-ronnia}`. Nginx proxies `/api` directly to the backend service through `API_UPSTREAM=http://ronnia:${BIND_PORT:-8080}`; it does not route through the host's loopback port. If you choose another backend port, pass the same `BIND_PORT` here and in the backend project:

```sh
BIND_PORT=8081 WEB_PORT=3001 docker compose up --build -d
```

With those example ports, set the backend's `PUBLIC_ORIGIN=http://localhost:3001` and `API_ORIGIN=http://localhost:8081`. The API origin and OAuth callbacks point directly to the backend, not to the dashboard's `/api` proxy. For an existing configured deployment, retain its current API origin, port, provider callback registrations, and secrets; these local defaults do not require changing them.

Both Compose projects must use the same `RONNIA_NETWORK` and `BIND_PORT` values; start the backend before the dashboard so the external network and `ronnia` service are available. `API_UPSTREAM` is an optional server-only override for an existing backend reachable from the dashboard container, for example `API_UPSTREAM=http://other-backend:8080 docker compose up --build -d`. It is never compiled into browser JavaScript. The shared network keeps backend traffic inside Docker while the host-published backend port remains loopback-only.

For an HTTPS backend, set `API_UPSTREAM=https://api.new.ronnia.me` (without a trailing slash). Nginx sends the upstream host in `Host` and enables TLS SNI; its default [`proxy_ssl_name $proxy_host`](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_ssl_name) selects the upstream hostname for SNI, without a non-default port. The browser's `Origin`, `Referer`, and cookies are preserved, so keep `PUBLIC_ORIGIN` set to the dashboard origin; the backend validates those configured origins, not the forwarded `Host`. `/api/` is still stripped and `/api/internal/` remains blocked.

The browser contract is fixed and public:

- Axios uses `/api` with browser credentials enabled, initialized before routing.
- Login links are `/api/oauth2/osu-login` and `/api/oauth2/twitch-login`.
- Nginx strips `/api` and forwards to the Rust API. No backend URL or secret is compiled into the JavaScript, and no frontend `.env` file is required.
- Provider callback URLs remain the directly published Rust endpoints (for example, `http://localhost:8080/oauth2/osu-redirect` and `http://localhost:8080/oauth2/twitch-redirect`). Keep the existing provider registrations. The API redirects back to `PUBLIC_ORIGIN` after a callback.
- Use `localhost` consistently, not a mixture of `localhost` and `127.0.0.1`: host-only HttpOnly cookies are shared across localhost ports. Local HTTP requires backend `COOKIE_SECURE=false`.
- The backend `PUBLIC_ORIGIN` must be the dashboard origin for browser Origin/Referer checks. Logout and account deletion follow the backend's 303 response; the browser processes cleared cookies and Pinia/router are reset only on success.

No client code reads cookies, stores OAuth tokens, or receives provider secrets. Do not put backend secrets in `VITE_*` variables, which are public bundle inputs.

## Frontend development

Use Node 24 and npm. From this directory:

```sh
npm ci --ignore-scripts
npm run dev
```

The dev server listens on `http://localhost:3000` with a same-origin `/api` proxy. Its backend defaults to `http://127.0.0.1:8080`; `BIND_PORT` changes that port (for example, `BIND_PORT=8081 npm run dev`). For a different API host, set the server-only `API_PROXY_TARGET`, for example `API_PROXY_TARGET=http://api-host:8080 npm run dev`. These values are read from the shell, not from the backend repository's `.env`, and are not exposed as Vite client variables. The dev proxy preserves the browser Origin/Referer. Keep the backend `PUBLIC_ORIGIN=http://localhost:3000` for local development.

```sh
npm run build
```

Build runs the real Vue/TypeScript check (`vue-tsc --noEmit`) before Vite creates `dist/`. Tooling uses Vite 7, Vue plugin 6, TypeScript 5.9, and vue-tsc 3; there is no Node runtime in the Compose frontend container. `npm run preview` serves build output only; it does not replace the configured API reverse proxy.

## Continuous integration

The GitHub Actions build uses Node 24, installs the lockfile with `npm ci --ignore-scripts`, audits dependencies with `npm audit --audit-level=high`, runs the Vue/TypeScript and Vite production build, then builds the standalone Docker image. To run the same checks from this repository root:

```sh
npm ci --ignore-scripts
npm audit --audit-level=high
npm run build
docker build -t ronnia-web:local .
docker compose config
```

### Split deployment verification (2026-11-04)

The frontend lockfile install, dependency audit (zero vulnerabilities), Vue/TypeScript check, production build, and Docker image build passed. A real isolated two-project Compose run then used the Rust backend built from `aticie/ronnia` and `ronnia-web:split-check`, a fresh SQLite volume, synthetic provider credentials, and the unique shared network `ronnia-split-proof-20261104`. The backend ran `serve --api-only` with `BOT_ENABLED=false`; backend and dashboard were published only on loopback ports 28857 and 23857. No provider login was attempted and no real environment file or deployment was used.

Managed Chromium opened `http://localhost:23857/login` at 1440×1000 and rendered **Ronnia Dashboard**, both provider buttons, community links, and **No Ronnia streamers are live right now.** The actual same-origin proxy returned:

- `GET /api/ready`: HTTP 200, `{"status":"ready"}`.
- `GET /api/user/me`: HTTP 200, JSON `null`.
- `GET /api/internal/`: HTTP 404 from Nginx, not forwarded to the internal API.
- Provider link targets: `/api/oauth2/twitch-login` and `/api/oauth2/osu-login`.

Browser network access was restricted to localhost; external font stylesheets were intentionally blocked, so the rendered proof used fallback fonts. OAuth authorization and authenticated settings mutations were not exercised against real providers. Both isolated Compose projects, their shared network, and the disposable database volume were removed after the run.

## Migration status banner

The app shell requests the public, same-origin `GET /api/migration/status` once on load. The request is fire-and-forget: an unavailable endpoint, a non-2xx response, or an unexpected payload is treated as inactive and never blocks login or settings.

When the response is `{"active":true,"cutoffAt":null}` or has a cutoff, a non-dismissible `[data-testid="migration-banner"]` with `role="status"` appears above both `/login` and `/settings`. It explains that accounts and settings use the new dashboard, asks users to log in and re-authorize Twitch bot access, links to `/settings`, and includes an RFC 3339 `cutoffAt` as a localized date and time in the viewer's timezone. The banner is not hidden in `localStorage`; `active:false` or a failed status request leaves it absent.

## Registration and account settings

An anonymous `/api/user/me` response is JSON `null`, so both provider buttons are shown. Either provider can be first. After the first callback, the API returns `{ "signup": "osu" }` or `{ "signup": "twitch" }`; only the missing provider is displayed. After both callbacks, the complete nine-field user response leads to `/settings`. Reloading `/settings` waits for the current user instead of incorrectly ejecting a valid session.

For older accounts without `twitchBotAuthorized`, settings show a **Re-authorize Twitch** link. Consent must be renewed as the displayed, already-linked Twitch identity; the existing osu! account and settings are retained.

Settings autosave after 1.5 seconds, or use **Save Changes**. The POST contains all seven effective fields (`enable`, `echo`, `sub-only`, `points-only`, `test`, `cooldown`, `sr`), with boolean toggles and `sr` upper `-1` representing unlimited. Exclusions load from the server and use its normalized login after successful mutations; failed requests do not change the list. The live-stream endpoint is requested with `limit=100`.

Manual and automatic settings saves share one serialized writer. Edits made during a request are coalesced into the newest complete snapshot and sent after that request finishes, preventing older requests from overwriting newer changes. Success is shown only after the queue drains. If a write fails, the form stays intact with a visible error and **Save Changes** can retry immediately.

API failures remain visible through inline status/errors and the existing toaster. A 401 clears the cached session and returns to login without an automatic refetch loop; **Retry loading account** explicitly retries. Account mutations do not clear local state or claim success on other HTTP/network errors.

### Browser integration workflow

- Start at `/login`; locate `a[href="/api/oauth2/osu-login"]` and `a[href="/api/oauth2/twitch-login"]`. Repeat registration with both provider orders in separate clean browser contexts. A pending signup shows exactly the other link, then the completed account opens `/settings`.
- Reload `/settings` with a valid session. Profile text and avatars should remain visible. Toggle inputs have IDs matching the setting names, including `#sub-only` and `#points-only`. **Save Changes** submits the full settings object; drag the right star-rating thumb to its maximum to submit unlimited `-1`.
- Exclusions input: `input[aria-label="Twitch user to exclude"]`; add button: `button[aria-label="Add excluded user"]`; remove button: `button[aria-label="Remove LOGIN from excluded users"]`. Invalid/failed mutations show `[role="alert"]` and keep the list unchanged.
- An account whose `twitchBotAuthorized` is false shows `a[href="/api/oauth2/twitch-login"]` with **Re-authorize Twitch** text on settings.
- **Logout** and **Delete Account** are ordinary button text selectors. Successful requests clear state and return to `/login`. Expire a session before a settings/exclusion request to check the visible session-expired login message and lack of repeated `/user/me` calls.
- At desktop widths above 1024px, the login page includes live-stream cards or a visible empty/error status. Error toasts use `[role="status"]`; persistent fetch/mutation errors use `[role="alert"]`.
- With migration enabled, reload `/login` and `/settings` and locate `[data-testid="migration-banner"][role="status"]`, text **Ronnia is migrating** / **re-authorize Twitch bot access**, the localized **Migration cutoff** when configured (or no cutoff line), and `a[href="/settings"]` labelled **Open settings**. With migration disabled, or with the status endpoint failing, no migration banner renders and the page still loads.
