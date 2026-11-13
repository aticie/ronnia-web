import type { App } from "vue";
import type { Router } from "vue-router";
import * as Sentry from "@sentry/vue";
import { version } from "../package.json";

/// Configuration is injected at container start (`/sentry-config.js`), never
/// compiled in: the image is built once and the DSN, environment and sample
/// rates stay server-side settings. A missing or empty DSN disables Sentry.
type SentryRuntimeConfig = {
  dsn?: string;
  environment?: string;
  release?: string;
  tracesSampleRate?: number;
  replaysSessionSampleRate?: number;
  replaysOnErrorSampleRate?: number;
};

declare global {
  interface Window {
    __RONNIA_SENTRY__?: SentryRuntimeConfig;
  }
}

const rate = (value: unknown, fallback: number): number => {
  const parsed = typeof value === "string" ? Number(value) : value;
  return typeof parsed === "number" && Number.isFinite(parsed) && parsed >= 0 && parsed <= 1
    ? parsed
    : fallback;
};

export const initSentry = (app: App, router: Router): boolean => {
  const config = window.__RONNIA_SENTRY__;
  const dsn = config?.dsn?.trim();
  if (!dsn) {
    return false;
  }
  const build = config?.release;
  Sentry.init({
    app,
    dsn,
    environment: config?.environment || "production",
    release: `ronnia-web@${version}${build ? `+${build}` : ""}`,
    // v11 collects PII by opt-in; keep it minimal: no user identity, cookies,
    // query strings or bodies ever leave the browser.
    dataCollection: {
      userInfo: false,
      cookies: false,
      urlQueryParams: false,
      httpHeaders: false,
      httpBodies: [],
    },
    tracesSampleRate: rate(config?.tracesSampleRate, 0.1),
    integrations: [
      Sentry.browserTracingIntegration({ router }),
      Sentry.replayIntegration({ maskAllInputs: true }),
    ],
    tracePropagationTargets: ["/api", /^https:\/\/ronnia\.me\/api/],
    replaysSessionSampleRate: rate(config?.replaysSessionSampleRate, 0.1),
    replaysOnErrorSampleRate: rate(config?.replaysOnErrorSampleRate, 1.0),
    initialScope: { tags: { service: "web" } },
  });
  return true;
};
