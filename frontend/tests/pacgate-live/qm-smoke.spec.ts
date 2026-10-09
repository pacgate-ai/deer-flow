import { expect, test } from "@playwright/test";

/**
 * Phase A — QM web-ui smoke test against the LIVE running stack.
 *
 * Prereqs (already running):
 *   - QM web-ui at http://localhost:8182 (dev/cookie mode)
 *   - QM core at :8180
 *
 * QM is in dev mode: sign-in is a cookie-based POST /signin with a principal
 * email (no password). Verifies: dev sign-in works and the chat UI loads.
 */

const QM_URL = process.env.PACGATE_QM_URL ?? "http://localhost:8182";
const QM_PRINCIPAL = process.env.PACGATE_QM_PRINCIPAL ?? "admin@pacgate-law.com";

test.describe("QM live UI smoke", () => {
  test("dev sign-in and load the chat UI", async ({ page }) => {
    await page.goto(QM_URL);

    // Dev-mode sign-in form: a single "Principal" field + Continue
    await page.getByPlaceholder("you@org.com").fill(QM_PRINCIPAL);
    await page.getByRole("button", { name: /continue/i }).click();

    // Should show the dev-mode banner + chat input
    await expect(
      page.getByText(/dev mode.*signed in as/i),
    ).toBeVisible({ timeout: 30_000 });
    await expect(page.getByPlaceholder("Ask anything")).toBeVisible();
  });
});
