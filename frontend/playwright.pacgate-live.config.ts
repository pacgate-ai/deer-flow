import { defineConfig, devices } from "@playwright/test";

/**
 * PacGate-Law live-stack smoke tests.
 *
 * Targets the ALREADY-RUNNING production stack (no webServer is started):
 *   - deer-flow frontend : http://localhost:8090  (Next.js, real gateway :8001)
 *   - QM web-ui          : http://localhost:8182  (dev/cookie mode)
 *
 * These are UI smoke tests (Phase A) + tool-call verification (Phase B).
 * They do NOT mock the backend — they drive the real running services.
 */
export default defineConfig({
  testDir: "./tests/pacgate-live",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: process.env.CI ? "github" : "html",
  timeout: 120_000,

  use: {
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },

  projects: [
    {
      name: "msedge",
      use: { ...devices["Desktop Edge"], channel: "msedge" },
    },
  ],
});
