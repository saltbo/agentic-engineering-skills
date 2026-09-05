# Agentic Engineering Skills

Focused engineering skills for coding agents. Each skill has a narrow trigger
boundary so a small task does not load an entire engineering handbook.

All skills in this engineering suite use the `bep-` namespace so their source
is recognizable in catalogs, prompts, and cross-skill references.

## Install

Inspect the skills available in the repository:

```bash
npx skills add saltbo/agentic-engineering-skills --list
```

Select skills and target agents interactively:

```bash
npx skills add saltbo/agentic-engineering-skills
```

Install every skill globally for Codex without prompts:

```bash
npx skills add saltbo/agentic-engineering-skills \
  --skill '*' \
  --agent codex \
  --global \
  --yes
```

Install only one skill globally:

```bash
npx skills add saltbo/agentic-engineering-skills \
  --skill bep-software-testing \
  --agent codex \
  --global \
  --yes
```

If the `skills` CLI is installed globally, use `skills` in place of
`npx skills` in the commands above.

## Skills

| Skill | Use it for |
| --- | --- |
| `bep-backend-engineering` | Backend ownership, dependency direction, persistence, messaging, and service lifecycle |
| `bep-frontend-engineering` | Feature boundaries, browser state, rendering, accessibility, security, and performance |
| `bep-http-engineering` | End-to-end HTTP lifecycle and protocol semantics |
| `bep-software-debugging` | Reproducible defect, regression, and performance diagnosis |
| `bep-software-testing` | Test-layer selection and automated test design |
| `bep-verification-gates` | Proof inventories, coverage governance, and blocking CI policy |
| `bep-production-verification` | Safe verification against deployed environments |
| `bep-delivery-engineering` | Compatibility, migrations, deployment, rollback, and release acceptance |
| `bep-engineering-review` | Outcome, risk, contract, and implementation review |
| `bep-best-openapi-design` | Resource-oriented REST and OpenAPI contract design |
| `bep-best-engineering-practice` | Explicit comprehensive audit across applicable disciplines |

## Invocation Model

Specialist skills may be selected automatically when their narrow description
matches the task. Their supporting references are loaded only for the affected
boundary.

`bep-best-engineering-practice` is intentionally explicit-only. It is an umbrella
audit for requests that genuinely need multiple disciplines, not a router for
ordinary coding work.

## Project Baseline

These skills encode BEP engineering preferences. For a new project, apply the
preferences directly. For an existing project, preserve its working architecture,
supported contracts, API version placement, and test tooling. Improve the affected
boundary without turning a local change into an unrelated migration. A preference
difference is not automatically a correctness or security defect.

Descriptions identify actual tasks, not broad technology keywords. Running an
existing test does not need the testing skill; editing an HTTP header does not
need resource modeling; a local implementation does not trigger deployment.
Optional specialist skills are not prerequisites to independent work.

## Testing And Acceptance

Use a test pyramid: many fast Unit tests for rules, focused Integration tests for
real boundaries, and a small set of critical E2E journeys. Prove a behavior's full
matrix once at its cheapest sufficient layer; higher layers prove distinct wiring
or runtime risks. The pyramid is not a fixed ratio. Formal coverage thresholds,
proof inventories, and CI adapters belong to governance work, not every test edit.

Implementation requires local acceptance with the smallest meaningful checks and
an exercise of the changed behavior. Fix failures caused by the change and rerun
affected checks. A missing environment is an acceptance limitation, never a pass.

An authorized deployment uses `bep-delivery-engineering` and continues through
`bep-production-verification` for post-deployment regression. Prefer an explicitly
selected production-safe E2E subset sharing assertions with local E2E. When a
small fixture or runner change enables that subset, implement and validate it
locally. Otherwise complete bounded manual regression of affected flows and
relevant critical journeys, and report the concrete automation gap. Deployment
success and regression success are separate results.

No additional release skill is required: delivery owns the release lifecycle,
production verification owns the live checks, and testing owns reusable E2E design.

## Repository Checks

Run the path checker's behavioral regression tests:

```bash
python3 -B -m unittest discover -s tests -v
```

For a new API, the path helper defaults to the BEP profile. Use `--profile existing`
when preserving an existing contract; this mode checks path structure and does not
prove resource semantics or conformance to that project's conventions:

```bash
python3 skills/bep-best-openapi-design/scripts/check_resource_paths.py \
  --profile bep '/orders/{orderId}'
python3 skills/bep-best-openapi-design/scripts/check_resource_paths.py \
  --profile existing '/v1/orders/{orderId}'
```

Both profiles support `--file` with one path per line. See
[behavioral evaluation cases](docs/skill-behavior-evaluation.md) for reviewing skill
selection and scope on realistic tasks.
