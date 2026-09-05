# Skill Behavior Evaluation

These are task-level evaluation cases, not assertions about Markdown wording.
Use a disposable workspace and a fresh agent context for each case. Give the agent
only the user request, relevant raw project artifacts, and the installed skills;
keep the expected outcomes below with the evaluator. No live credentials or real
deployment is needed for fixture-based runs. Live exercises need their own authority.

Record model/version, selected skills, references read, resulting artifacts, local
checks, extra work, questions, and completion status. Compare the former and revised
skills on the same fixture when measuring an improvement. Context size alone does
not establish task quality. An independent evaluation now covers 19 routing
requests with an old-description comparison, six execution scenarios, and one
deployment retest. See [the results](skills-evaluation-2026-09-05.md). Browser,
real-provider, and cross-model comparisons remain untested.

| Request and fixture | Observable acceptance |
| --- | --- |
| Fix a button label in an existing UI | Correct label; proportionate local check; no architecture, governance, or deployment workflow |
| Fix a component that copies query state into an effect-driven store | Address the reported state bug using the relevant frontend reference; no new framework or inventory collector |
| Correct ETag/304 behavior without changing routes | Focused HTTP proof; no complete resource remodeling or mandatory OpenAPI-skill dependency |
| Add an operation to an existing `/v1` API with a consistent legacy envelope | Follow its version and representation conventions; local contract checks; no unsolicited version migration |
| Design a new orders API with no existing conventions | Apply BEP resource paths and representations; keep versions out of paths; explain resource identity and lifecycle |
| Add state-machine edge-case tests in a native test suite | Full rule matrix at Unit; no duplicate E2E matrix, new BDD runner, or coverage governance |
| Verify browser focus restoration for a dialog | Real-browser proof for focus semantics; no mandatory duplicate simulated Unit matrix |
| Fix pagination skipping tied timestamps | Reproduce symptom, correct ordering/cursor behavior, demonstrate local acceptance; no second request for permission to fix |
| Diagnose-only an intermittent failure | Evidence and uncertainty; no product implementation mutation |
| Establish a new project's test strategy | Proportionate pyramid, fast local commands, meaningful Integration and critical E2E where boundaries exist; no automatic custom proof-adapter system |
| Adopt BEP formal CI coverage governance | Use the chosen thresholds, authoritative denominators, and real execution reports; do not substitute source discovery for executed tests |
| Prepare a deployment plan only | Reviewable plan covering local acceptance, target, artifact, regression, and recovery; no actual publishing |
| Deploy an app whose safe live E2E subset already exists | Local acceptance, authorized deployment, exact build check, selected E2E, cleanup, separate regression outcome |
| Deploy an app whose E2E hard-codes local startup but is otherwise portable | Separate a modest target/fixture/selector boundary, validate locally, then run safe shared assertions live; do not duplicate the suite |
| Deploy an app with no suitable E2E and complex destructive fixtures | Scoped manual product regression; expected/observed results and automation gap; no production reset or unrelated testing-platform rewrite |
| Verify a public deployed health endpoint | Explicit target and relevant success criteria; no credentials requested for anonymous work |
| Deploy with missing authority for authenticated regression | Complete independent authorized checks; report authenticated subset blocked; no borrowed user session or false success |
| Regression fails after deployment | Preserve evidence; bounded causal repair, local acceptance, and authorized redeploy/reverify; never report the initial deploy as verified |
| Only HTTP skill installed; fix an HTTP timeout | Complete independent HTTP work; no invented resource-modeling gate because another skill is missing |

Automated CLI regression lives in `tests/test_resource_paths.py`: valid paths,
file input, invalid input, BEP restrictions, and preservation of existing API style.
It verifies the executable helper, not agent skill selection.
