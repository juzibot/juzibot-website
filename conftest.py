"""Root pytest + Hypothesis configuration for the website-redesign test harness.

This file registers the Hypothesis settings profiles used by every
property-based test in the spec. The key guarantee required by the design
(Testing Strategy: "each property test runs a minimum of 100 iterations") is
enforced here centrally so individual tests do not need to repeat it.

Profiles
--------
- ``ci``  (default, loaded automatically): ``max_examples = 100`` so every
  property runs at least the required minimum of 100 iterations per property.
- ``dev``: a faster local profile (still >= 100) for quick iteration.
- ``thorough``: a heavier profile for deeper exploration before release.

Select a non-default profile with the environment variable
``HYPOTHESIS_PROFILE`` (e.g. ``HYPOTHESIS_PROFILE=thorough pytest``).

Property tagging convention
---------------------------
Every property-based test MUST carry a comment tag in the exact format::

    # Feature: website-redesign, Property {n}: {property_text}

where ``{n}`` is the Correctness Property number from design.md (1-29) and
``{property_text}`` is the property's one-line statement. The tag links the
test back to the design property it validates and sits alongside the
``**Validates: Requirements X.Y**`` annotation.
"""

import os

from hypothesis import HealthCheck, settings

# Minimum iterations per property mandated by the design's Testing Strategy.
MIN_EXAMPLES = 100

settings.register_profile(
    "ci",
    max_examples=MIN_EXAMPLES,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)

settings.register_profile(
    "dev",
    max_examples=MIN_EXAMPLES,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)

settings.register_profile(
    "thorough",
    max_examples=500,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)

# Default to the "ci" profile (>= 100 examples) unless the caller overrides it.
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "ci"))
