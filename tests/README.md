# Test harness — website-redesign

This directory holds the automated checks that enforce the redesign's
preservation and structural guarantees. There are two harnesses, one per
language, matching the design's Testing Strategy.

## 1. Python harness (pytest + Hypothesis)

Drives the structural / preservation / metadata / token property tests and the
example-based unit/integration tests against the Build_Output and the captured
baseline snapshot (via `verify_site.py`).

### Layout

```
tests/
  structural/   # property tests over build output, content, assets, metadata, tokens
  unit/         # example-based unit + integration/smoke tests
```

(Root files `pytest.ini`, `conftest.py`, and `requirements-dev.txt` configure
this harness.)

### Setup

```bash
python -m pip install -r requirements-dev.txt
```

### Running

```bash
pytest                 # default "ci" profile: >= 100 examples per property
HYPOTHESIS_PROFILE=thorough pytest   # heavier exploration (500 examples)
```

### Iteration count

`conftest.py` registers Hypothesis settings profiles and loads `ci` by default,
which sets `max_examples = 100`. This satisfies the design requirement that
**each property test runs a minimum of 100 iterations per property**. Individual
tests therefore do not need to set `@settings(max_examples=...)` themselves.

### Property tag format (required)

Every property-based test MUST carry a comment in this exact format directly
above the test, linking it to the design Correctness Property it validates:

```python
# Feature: website-redesign, Property 1: Content preservation — for any content
# string present in the baseline site, that exact character sequence appears in
# the redesigned site on the corresponding page.
# Validates: Requirements 2.1, 2.2, 2.3, 5.2, 8.4
@pytest.mark.property
def test_content_preservation(...):
    ...
```

- `{n}` is the property number from `design.md` (Properties 1–29).
- `{property_text}` is the property's one-line statement.
- Keep the `Validates: Requirements ...` line alongside the tag.

### Markers

- `@pytest.mark.property` — a Hypothesis property test for a design property.
- `@pytest.mark.unit` — an example-based unit test (specific scenario / error path).
- `@pytest.mark.integration` — a deploy / static-config integration or smoke test.

## 2. JavaScript harness (Node + fast-check + Playwright)

Drives the responsive / interaction property tests that require real layout
measurement in a headless browser (design Properties 4, 5, 6, 12). It lives in
its own self-contained package so its Node dependencies stay isolated.

### Layout

```
tests/layout/
  package.json          # fast-check + Playwright dev dependencies + scripts
  playwright.config.js  # headless browser + responsive viewport projects
  specs/                # layout-measurement property tests (added in later tasks)
```

See `tests/layout/README.md` for setup and run instructions.

## Property → test mapping

One property-based test per Correctness Property (design Properties 1–29).
Properties whose space is a fixed finite set are still implemented as a single
property test quantifying over that set. The actual property/unit tests are
authored in later spec tasks; this directory is the scaffolding only.
