# Layout-measurement harness (Node + fast-check + Playwright)

Self-contained Node package for the responsive / interaction property tests
that need real layout measurement in a headless browser. It covers the design's
Correctness Properties that cannot be checked from static HTML alone:

- **Property 4** — aspect-ratio preservation across viewport widths (320–1920px)
- **Property 5** — no horizontal overflow across viewport widths
- **Property 6** — navigation breakpoint visibility (burger vs. desktop links)
- **Property 12** — floating-panel scroll threshold (200px)

## Setup

```bash
cd tests/layout
npm install
npm run install:browsers   # downloads the Chromium build Playwright drives
```

> If `npm install` or the browser download cannot reach the network in your
> environment, run them later — the configuration files here are complete and
> the commands above are the only setup required.

## Running

```bash
cd tests/layout
npm test                   # serves the static site and runs the layout properties
```

`playwright.config.js` starts a static file server (`python -m http.server`)
rooted at the repository top level, so pages are exercised exactly as they are
served in production (no bundler, no runtime).

## Writing property tests

- Use **fast-check** for generators (viewport widths as integers in `[320, 1920]`,
  scroll offsets partitioned around the 200px threshold) — do not hand-roll
  random generation.
- Use **Playwright** to apply the generated viewport / scroll state and measure
  the resulting layout.
- Run **at least 100 iterations** per property via fast-check's `numRuns` option
  (`fc.assert(fc.property(...), { numRuns: 100 })`).
- Tag every property test with the shared convention:

  ```js
  // Feature: website-redesign, Property 5: No horizontal overflow across widths —
  // for any viewport width in [320, 1920], no page produces a horizontal scrollbar.
  // Validates: Requirements 6.1, 6.4, 7.8
  ```

Place test files under `specs/` named `*.spec.js`. They are added in later spec
tasks; this directory is scaffolding only.
