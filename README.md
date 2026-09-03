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
| `bep-delivery-engineering` | Compatibility, migrations, releases, rollback, and reproducibility |
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
