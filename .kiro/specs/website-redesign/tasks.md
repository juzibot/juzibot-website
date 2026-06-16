# Implementation Plan: Website Redesign (句子互动 / JuziBot)

## Overview

This plan rebuilds the JuziBot static site's design system, information architecture, layout, and interactions while preserving 100% of content and every asset byte-for-byte. Work is expressed through a rewritten `assets/style.css` token/component system, rewritten markup in `build_pages.py` snippets and per-page bodies, rewritten hand-edited root pages, and a new `verify_site.py` harness that machine-checks preservation and structural guarantees against a captured baseline.

Implementation languages (from the design): **CSS** for the design system, **Python** (with Hypothesis) for the build pipeline and structural/preservation property tests, and **JavaScript** (with fast-check + Playwright) for responsive/interaction property tests.

## Tasks

- [x] 1. Capture baseline and scaffold the test harness
  - [x] 1.1 Build the baseline snapshot generator
    - Create `baseline_snapshot.py` that captures the pre-redesign site into three reference sets: per-page content strings, asset files with size+checksum, and internal link targets
    - Tag/archive the current site (`pre-redesign`) and persist the snapshot to a stable location the verifier can read
    - _Requirements: 2.1, 2.5, 1.2, 1.5_

  - [x] 1.2 Scaffold the verification and test harness configuration
    - Set up the Python test harness (pytest + Hypothesis) with a minimum of 100 iterations per property and the tag format `Feature: website-redesign, Property {n}`
    - Set up the JavaScript harness (Node + fast-check + Playwright) for layout-measurement property tests
    - _Requirements: 9.2_

- [x] 2. Rebuild the Design System token layer in `assets/style.css`
  - [x] 2.1 Implement the `:root` design-token system
    - Define named tokens across all six categories (color, typography, spacing, radius, shadow, elevation), a light near-white background, a minimum content padding token ≥ 16px, ≤ 3 accent color tokens, and `var(--token, <fallback>)` fallbacks at every critical reference
    - _Requirements: 3.1, 3.2, 3.4, 3.6, 3.7_

  - [ ]* 2.2 Write property test for token category coverage
    - **Property 25: Design-token category coverage**
    - **Validates: Requirements 3.1**

  - [ ]* 2.3 Write property test for light-theme token values
    - **Property 26: Light-theme token values**
    - **Validates: Requirements 3.2**

  - [ ]* 2.4 Write property test for accent palette limit
    - **Property 27: Accent palette limit**
    - **Validates: Requirements 3.4**

  - [ ]* 2.5 Write property test for token fallbacks
    - **Property 28: Token fallbacks prevent unstyled rendering**
    - **Validates: Requirements 3.6, 3.7**

  - [ ]* 2.6 Write property test for body-copy contrast
    - **Property 29: Body-copy contrast**
    - **Validates: Requirements 11.5**

- [x] 3. Rebuild the Design System component layer in `assets/style.css`
  - [x] 3.1 Implement base reset, layout primitives, and canonical components
    - Implement base/reset, layout primitives, and exactly one canonical token set for card, button, and shadow treatments with no page-local overrides; restrict gradients to accent-only usage ≤ 30% of the viewport
    - _Requirements: 3.3, 3.5, 10.1, 10.5_

  - [x] 3.2 Implement structured-component, navigation, and responsive styles
    - Style the structured components (cards, lists, feature grid, timeline, comparison table, data display, tag categories, FAQ accordion), the nav/dropdowns/burger, footer, announcement marquee, floating panel, and modal; add responsive overrides for 320–1920px breakpoints and reduced-motion fallbacks
    - _Requirements: 5.4, 6.1, 6.2, 6.3, 6.4, 10.5_

- [x] 4. Checkpoint - design system review
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Rebuild shared snippet functions in `build_pages.py`
  - [x] 5.1 Rewrite shared regions, page shell, and inline behaviors
    - Rewrite `nav_html`, `footer_html`, `announcement_html`, `contact_module`, and `page_layout` to emit the new markup with semantic landmarks (one `main`, plus `header`/`nav`/`footer`), `zh-CN` lang, bounded unique title/description, and shared-region path-prefix-only variance; implement the dependency-free inline JS for dropdown reveal (hover + focus), burger toggle, contact modal (open/close/overlay/Escape + scroll restore), floating-panel scroll threshold, marquee duplication, and the demo `fit()` scaling
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 8.3, 8.5, 10.2, 10.4, 11.3, 11.4, 2.4_

  - [x] 5.2 Rewrite the structured-component snippet functions
    - Rewrite `feat_grid`, `kpi_row`, `split_section`, `block`, `cta_band`/`cta_section` and add new shared snippets (`feature_list`, `comparison_table`, `timeline`, `faq_accordion`, `tag_categories`) as single reusable functions with image text-alternative handling (non-empty alt for informative assets, empty alt for decorative)
    - _Requirements: 5.1, 5.4, 8.5, 11.1, 11.2_

- [ ] 6. Rebuild generated page bodies in `build_pages.py`
  - [x] 6.1 Rebuild the 7 product page bodies
    - Recompose miaodong, shouhu, canmou, dongxing, miaohui, cli, and zhizao from shared structured components with a new module order, re-presenting any >60-word block in a structured format and retaining every preserved string, metric, and product name
    - _Requirements: 4.1, 5.1, 5.2, 5.3, 8.1, 8.2, 8.4_

  - [ ] 6.2 Rebuild AI-employee and enterprise bodies and builder error handling
    - Recompose the 6 AI-employee pages (sales, marketing, service, government, finance, hr) and `enterprise.html` with rebuilt module order and structured components; wrap each page write and content lookup so a failure halts, reports the failing page + reason, and leaves already-written pages intact
    - _Requirements: 4.1, 5.1, 5.2, 5.3, 8.1, 8.2, 8.4, 8.6_

  - [ ] 6.3 Write unit test for builder error handling
    - Inject a write/lookup failure and assert the builder halts, reports the failing page and reason, and leaves prior pages intact
    - _Requirements: 8.6_

- [x] 7. Rebuild hand-edited root pages
  - [x] 7.1 Rebuild `index.html`
    - Rebuild the home page DOM module order and grid using the rebuilt design system, embedding the same shared nav/footer/announcement/contact/floating markup and preserving all content
    - _Requirements: 4.1, 4.2, 5.1, 5.2, 8.3_

  - [x] 7.2 Rebuild `about.html` and `fde.html`
    - Rebuild both pages with new module order and structured components, shared regions, preserved content, and bounded unique metadata
    - _Requirements: 4.1, 5.1, 5.2, 8.3, 10.2, 10.3_

  - [x] 7.3 Rebuild `industries.html` and `careers/index.html`
    - Rebuild both pages with new module order and structured components, shared regions (path-prefix adjusted), preserved content, and preserved career figure assets
    - _Requirements: 4.1, 5.1, 5.2, 8.3, 1.1_

- [ ] 8. Checkpoint - run the builder and review output
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement `verify_site.py` content/structure verification
  - [ ] 9.1 Implement content-preservation comparison
    - Compare Build_Output against the baseline snapshot for content completeness and report any missing string; detect any text in preserved blocks absent from the baseline content set
    - _Requirements: 2.1, 2.2, 2.3, 2.5, 5.2, 5.3, 8.4_

  - [ ]* 9.2 Write property test for content preservation
    - **Property 1: Content preservation**
    - **Validates: Requirements 2.1, 2.2, 2.3, 5.2, 8.4**

  - [ ]* 9.3 Write property test for no fabricated copy in preserved blocks
    - **Property 2: No fabricated copy in preserved blocks**
    - **Validates: Requirements 5.3**

  - [ ] 9.4 Implement asset, link, and structure extraction
    - Implement asset-integrity checks (byte/size/checksum equality, reference resolution, path-set equality), internal link resolution, ancillary-file retention, legacy redirect resolution, and extraction of dropdown links, DOM module order, metadata, semantic landmarks, document language, stylesheet reference, and shared-region normalization
    - _Requirements: 1.1, 1.2, 1.4, 1.5, 1.6, 4.5, 9.4, 9.5, 8.2_

  - [ ]* 9.5 Write property test for asset integrity
    - **Property 3: Asset integrity**
    - **Validates: Requirements 1.1, 1.2, 1.4, 1.5**

  - [ ]* 9.6 Write property test for internal link integrity
    - **Property 8: Internal link integrity**
    - **Validates: Requirements 4.5**

  - [ ]* 9.7 Write property test for retained ancillary files
    - **Property 24: Retained ancillary files exist**
    - **Validates: Requirements 9.5**

  - [ ]* 9.8 Write property test for legacy URL redirects
    - **Property 23: Legacy URLs redirect to home**
    - **Validates: Requirements 2.6, 9.4**

  - [ ]* 9.9 Write property test for dropdown structure and resolution
    - **Property 7: Dropdown structure and resolution**
    - **Validates: Requirements 4.3, 7.6**

  - [ ]* 9.10 Write property test for page reachability
    - **Property 9: Page reachability**
    - **Validates: Requirements 4.2**

  - [ ]* 9.11 Write property test for rebuilt module order
    - **Property 10: Module order rebuilt**
    - **Validates: Requirements 4.1**

  - [ ]* 9.12 Write property test for structured long-form copy
    - **Property 11: Long-form copy is structured**
    - **Validates: Requirements 5.1**

  - [ ]* 9.13 Write property test for component consistency
    - **Property 13: Component consistency**
    - **Validates: Requirements 3.5, 5.4, 10.1, 10.5**

  - [ ]* 9.14 Write property test for image text-alternative correctness
    - **Property 14: Image text-alternative correctness**
    - **Validates: Requirements 11.1, 11.2**

  - [ ]* 9.15 Write property test for accessible control names
    - **Property 15: Accessible names for controls**
    - **Validates: Requirements 11.3**

  - [ ]* 9.16 Write property test for metadata bounds and uniqueness
    - **Property 16: Page metadata bounds and uniqueness**
    - **Validates: Requirements 10.2, 10.3**

  - [ ]* 9.17 Write property test for semantic landmarks
    - **Property 17: Semantic landmarks**
    - **Validates: Requirements 10.4**

  - [ ]* 9.18 Write property test for document language
    - **Property 18: Document language**
    - **Validates: Requirements 2.4**

  - [ ]* 9.19 Write property test for full page-set generation
    - **Property 19: Builder produces the full page set**
    - **Validates: Requirements 8.1**

  - [ ]* 9.20 Write property test for rebuilt design-system reference
    - **Property 20: Generated pages reference the rebuilt design system**
    - **Validates: Requirements 8.2**

  - [ ]* 9.21 Write property test for shared-region equality modulo prefix
    - **Property 21: Shared regions equal modulo path prefix**
    - **Validates: Requirements 8.3, 8.5**

  - [ ]* 9.22 Write property test for server-runtime-free rendering
    - **Property 22: Pages render without a server runtime**
    - **Validates: Requirements 9.2**

- [ ] 10. Responsive and interaction tests
  - [ ]* 10.1 Write property test for aspect-ratio preservation across widths
    - **Property 4: Aspect-ratio preservation across widths**
    - **Validates: Requirements 1.3, 6.5**

  - [ ]* 10.2 Write property test for no horizontal overflow across widths
    - **Property 5: No horizontal overflow across widths**
    - **Validates: Requirements 6.1, 6.4, 7.8**

  - [ ]* 10.3 Write property test for navigation breakpoint visibility
    - **Property 6: Navigation breakpoint visibility**
    - **Validates: Requirements 6.2, 6.3**

  - [ ]* 10.4 Write property test for floating-panel scroll threshold
    - **Property 12: Floating-panel scroll threshold**
    - **Validates: Requirements 7.4, 7.5**

  - [ ]* 10.5 Write unit tests for contact modal interactions
    - Modal opens on each trigger; closes via X, overlay click, and Escape, restoring prior scroll position
    - _Requirements: 7.2, 7.3, 11.4_

  - [ ]* 10.6 Write unit test for burger toggle round-trip
    - Activate shows links, activate again hides them
    - _Requirements: 7.7_

  - [ ]* 10.7 Write unit test for announcement marquee message presence
    - Assert the marquee contains every message string and is duplicated for a seamless loop
    - _Requirements: 7.1_

  - [ ]* 10.8 Write unit test for internal link target content
    - Activating an internal link reaches a page containing the expected preserved content
    - _Requirements: 4.4_

- [ ] 11. Deployment integration and smoke tests
  - [ ]* 11.1 Write integration test for deploy-script logic
    - Verify `stage` checkout, conditional `build_pages.py` re-run, publish reachability, and failure-leaves-site-unchanged behavior
    - _Requirements: 9.3, 9.6_

  - [ ]* 11.2 Write smoke test for static-config compatibility
    - Assert `deploy.yml` is unchanged, no server runtime is introduced, and the site remains a static multi-page site
    - _Requirements: 9.1_

- [ ] 12. Final checkpoint - ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional test tasks and can be skipped for a faster MVP.
- Each task references specific requirements (or a property number) for traceability.
- Property tests validate the universal correctness properties from the design; unit and integration tests cover specific interaction scenarios and error paths.
- Purely visual concerns (gradient feel, premium aesthetic, continuous marquee animation, render-timing performance, full WCAG AA conformance) are handled by lint/snapshot/manual review per the design's Testing Strategy and are intentionally not coding tasks here.
- All edits to `assets/style.css`, `build_pages.py`, and `verify_site.py` are sequenced into separate waves to avoid concurrent writes to the same file.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1"] },
    { "id": 2, "tasks": ["2.2", "2.3", "2.4", "2.5", "2.6", "3.1"] },
    { "id": 3, "tasks": ["3.2"] },
    { "id": 4, "tasks": ["5.1"] },
    { "id": 5, "tasks": ["5.2"] },
    { "id": 6, "tasks": ["6.1", "7.1", "7.2", "7.3"] },
    { "id": 7, "tasks": ["6.2"] },
    { "id": 8, "tasks": ["6.3", "9.1", "10.1", "10.2", "10.3", "10.4", "10.5", "10.6", "10.7", "10.8", "11.1", "11.2"] },
    { "id": 9, "tasks": ["9.2", "9.3", "9.4"] },
    { "id": 10, "tasks": ["9.5", "9.6", "9.7", "9.8", "9.9", "9.10", "9.11", "9.12", "9.13", "9.14", "9.15", "9.16", "9.17", "9.18", "9.19", "9.20", "9.21", "9.22"] }
  ]
}
```
