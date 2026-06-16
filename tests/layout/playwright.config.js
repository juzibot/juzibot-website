// @ts-check
import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright configuration for the website-redesign layout-measurement
 * property tests (design Properties 4, 5, 6, 12).
 *
 * The site is static, so tests are served straight from the repository root
 * (two levels up from this directory) as plain files. Property generators
 * (fast-check) drive viewport widths in [320, 1920] and scroll offsets; this
 * config provides the headless browser those tests measure layout in.
 *
 * Property tag convention (mirrors the Python harness):
 *   // Feature: website-redesign, Property {n}: {property_text}
 *   // Validates: Requirements X.Y
 */
export default defineConfig({
  testDir: "./specs",
  testMatch: "**/*.spec.{js,mjs}",
  // Each fast-check property runs >= 100 iterations internally (numRuns),
  // so the per-test timeout is generous to accommodate many browser layouts.
  timeout: 120_000,
  fullyParallel: true,
  reporter: [["list"]],
  use: {
    headless: true,
    // Static site served from the repository root.
    baseURL: "http://127.0.0.1:8000",
    trace: "retain-on-failure",
  },
  // Serve the static site for the duration of the test run.
  webServer: {
    command: "python -m http.server 8000",
    cwd: "../..",
    url: "http://127.0.0.1:8000",
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
