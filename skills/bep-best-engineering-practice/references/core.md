# Audit Scope And BEP Preferences

Compare requested outcomes, authorized scope, and supported behavior first.
For a new project, use BEP ownership, contract, testing, and delivery preferences.
For an existing project, inspect established conventions and distinguish defects
from style differences. Do not require modernization, new BDD tooling, or a new
coverage protocol merely because this audit is comprehensive.

Inspect the relevant boundaries for concrete risks: ownership and dependencies;
error propagation; concurrency and state; authentication and authorization;
supported contracts and data migrations; test-layer sufficiency; local acceptance;
and, only for a deployment task, live regression and recovery.

Keep general coding guidance out of a second mandatory handbook. Specialist
references own detailed rules. Formal thresholds and proof inventories apply only
to adopted governance or the policy work requested in this audit.

For new products, BEP favors lightweight domain behavior specifications, a test
pyramid, and clear local acceptance commands. Existing products keep their native
specification/test conventions unless the task includes changing them. Pure
libraries do not need product BDD merely to fit this preference.

Scale review depth to concrete risk. Independently examine requested-outcome
correctness and engineering risks; use independent reviewers when required by
project policy and authorized. Missing optional reviewer capability is a reported
limitation, not an automatically invented release gate.

For each finding, record evidence and separate severity from scope. Correct
in-scope blocking findings when fixes are authorized, rerun affected local checks,
and report out-of-scope findings without expanding the work. Scope searches to
the suspected pattern; repository-wide correction requires that scope in the task.
Completion means the requested outcome and applicable acceptance are satisfied,
not that all possible architecture preferences have been imposed.

The feedback-loop, vertical-slice, deep-module, seam, behavior-testing, diagnosis,
and two-axis review ideas were adapted from Matt Pocock's MIT-licensed
[skills](https://github.com/mattpocock/skills) repository, copyright 2026 Matt Pocock.
The BEP choices reflect this repository owner's preferences.
