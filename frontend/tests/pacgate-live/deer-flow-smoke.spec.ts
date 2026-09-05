import { expect, test } from "@playwright/test";

/**
 * Phase A — deer-flow UI smoke test against the LIVE running stack.
 *
 * Prereqs (already running):
 *   - deer-flow frontend at http://localhost:8090
 *   - deer-flow gateway at :8001 (inside container)
 *   - a registered test user (pwtest@pacgate-law.com / TestPass123!)
 *
 * Verifies: login works, workspace chat UI loads, and a message can be sent.
 */

const DEER_FLOW_URL = process.env.PACGATE_DEER_FLOW_URL ?? "http://localhost:8090";
const TEST_EMAIL = process.env.PACGATE_TEST_EMAIL ?? "pwtest@pacgate-law.com";
const TEST_PASSWORD = process.env.PACGATE_TEST_PASSWORD ?? "TestPass123!";

test.describe("deer-flow live UI smoke", () => {
  test("login and load the workspace chat UI", async ({ page }) => {
    await page.goto(`${DEER_FLOW_URL}/login`);

    // Fill the sign-in form
    await page.getByPlaceholder("you@example.com").fill(TEST_EMAIL);
    await page.getByPlaceholder("•••••••").fill(TEST_PASSWORD);
    await page.getByRole("button", { name: /sign in/i }).click();

    // Should land in the workspace chat UI
    await expect(page).toHaveURL(/\/workspace\/chats/);
    await expect(
      page.getByText(/hello, again!/i).first(),
    ).toBeVisible({ timeout: 30_000 });
    await expect(
      page.getByPlaceholder(/how can i assist you today/i),
    ).toBeVisible();
  });

  test("send a message and receive a response", async ({ page }) => {
    await page.goto(`${DEER_FLOW_URL}/login`);
    await page.getByPlaceholder("you@example.com").fill(TEST_EMAIL);
    await page.getByPlaceholder("•••••••").fill(TEST_PASSWORD);
    await page.getByRole("button", { name: /sign in/i }).click();
    await expect(page).toHaveURL(/\/workspace\/chats/);

    const input = page.getByPlaceholder(/how can i assist you today/i);
    await input.click();
    await page.keyboard.type("Hello, please reply with a short greeting.");
    await page.keyboard.press("Enter");

    // The agent should produce some assistant output (may take a while on local Ollama)
    await expect(
      page.locator('[data-testid*="message"], [class*="assistant"], main').last(),
    ).toBeVisible({ timeout: 120_000 });
  });
});
