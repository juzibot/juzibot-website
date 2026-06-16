"""Smoke checks that the Python test harness itself is configured correctly.

These are NOT design Correctness Property tests (those are authored in later
spec tasks). They only verify that the harness scaffolding works: that the
Hypothesis profile enforcing the >= 100 iterations minimum is active and that
Hypothesis runs at all.
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

# Minimum iterations per property mandated by the design's Testing Strategy.
MIN_EXAMPLES = 100


@pytest.mark.unit
def test_active_profile_enforces_minimum_iterations():
    """The loaded Hypothesis profile must run at least 100 examples per property."""
    assert settings().max_examples >= MIN_EXAMPLES


@pytest.mark.unit
def test_hypothesis_runs():
    """Hypothesis can drive a trivial property end-to-end under this harness."""
    counter = {"n": 0}

    @given(st.integers())
    def _prop(x):
        counter["n"] += 1
        assert x + 0 == x

    _prop()
    assert counter["n"] >= 1
