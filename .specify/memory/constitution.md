<!--
Sync Impact Report

- Version change: unspecified → 1.0.0
- Modified principles: Template placeholders → Concrete principles
- Added sections: "Quality Gates & Tooling", "Development Workflow & Quality Gates"
- Removed sections: Reduced principle placeholders to four concrete principles
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md (Constitution Check gates added)
	- ✅ .specify/templates/spec-template.md (Non-functional requirements prompts added)
	- ✅ .specify/templates/tasks-template.md (Tests marked mandatory; cross-cutting tasks updated)
- Follow-up TODOs:
	- None (Ratified date set to 2025-10-11)
-->

# pygmrt Constitution

## Core Principles

### I. Code Quality (Non‑Negotiable)

- All changes MUST pass automated linting and formatting using the project’s standard tools.
- Static analysis and type checking (where supported by the language) MUST be enabled at a strict level
	in CI for changed code and public APIs.
- Public-facing functions, classes, endpoints, and CLI commands MUST include clear, up-to-date
	documentation (docstrings/help text) describing purpose, inputs, outputs, and error modes.
- Complexity MUST be kept within agreed thresholds (e.g., cyclomatic complexity, function length) as
	enforced by CI. Any exception requires an inline justification and a plan to reduce complexity.
- Every behavior change MUST undergo peer review; self-approval is not allowed for non-trivial changes.

Rationale: Consistent, readable, and analyzable code reduces defects, accelerates onboarding, and
keeps maintenance costs predictable.

### II. Testing Standards

- Tests are MANDATORY for all new code and for any bug fix (include a regression test that fails before
	the fix).
- Minimum coverage target: 80% lines and 100% of critical paths identified in the spec/plan; coverage
	must not decrease on changed files.
- Test pyramid MUST be followed where applicable: unit tests first, integration tests for public
	contracts, and end-to-end tests when user journeys are introduced.
- Tests MUST be deterministic and stable; flaky tests are not allowed in mainline. Repeated-run
	stability checks may be used to verify.
- CI MUST block merges on failing tests, coverage regressions, or missing tests for new behavior.

Rationale: Reliable tests enable refactoring, prevent regressions, and serve as executable
documentation for behavior.

### III. User Experience Consistency

- All user-facing surfaces (CLI, API responses, UI if applicable) MUST be consistent in naming,
	structure, and error handling. Provide actionable error messages with machine-readable codes where
	appropriate.
- Accessibility and usability guidelines MUST be followed for visual interfaces; for CLI/API, provide
	clear help/usage and stable, documented contracts.
- Breaking changes to user-facing behavior MUST follow a deprecation policy documented in the
	spec/plan, including migration notes.
- Copy, messages, and interface patterns SHOULD reuse established project conventions; when none exist,
	create them in docs and reference them.

Rationale: Consistency builds user trust, reduces support burden, and simplifies integration.

### IV. Performance Requirements

- Each feature MUST define measurable performance budgets in the plan/spec (latency, throughput,
	memory/CPU, startup time, or frame rate as applicable).
- Changes MUST be validated against these budgets before merge; where automated benchmarks are
	feasible, include them in CI. Otherwise, provide manual measurements with methodology.
- Absent explicit budgets, changes MUST avoid >20% regression on established baselines for critical
	paths and MUST document any trade-offs.
- Performance fixes SHOULD include tests or checks that prevent future regressions where practical.

Rationale: Clear budgets prevent silent degradations and make performance a first-class, testable
requirement.

## Quality Gates & Tooling

- Lint/format pass is REQUIRED on all changes.
- Static analysis and type checks (when supported) MUST pass.
- Tests MUST run green with coverage targets met; include required unit/integration tests.
- Documentation for public interfaces MUST be updated with behavior or contract changes.
- Performance budgets MUST be defined per feature and verified with evidence prior to merge.

## Development Workflow & Quality Gates

- All work originates from a spec/plan that lists acceptance criteria, performance budgets, and testing
	strategy aligned with this constitution.
- Pull requests MUST include: linked spec/plan, test results, coverage report, and (when applicable)
	performance evidence.
- No direct commits to main for behavior changes; use PRs with peer review.
- Exceptions to any gate require an explicit, time-bounded waiver documented in the plan with owner and
	remediation steps.

## Governance

- This constitution supersedes informal practices. Conflicts MUST be resolved in favor of this
	document.
- Amendments occur via PR that includes a Sync Impact Report at the top of this file and updates to
	dependent templates/docs. Approval by at least one maintainer is REQUIRED.
- Versioning policy:
	- MAJOR: Backward-incompatible rule changes or removals.
	- MINOR: New principle/section or materially expanded guidance.
	- PATCH: Clarifications and wording that do not change intent.
- Compliance is reviewed during PRs and in periodic audits; unresolved violations MUST be tracked with
	owners and due dates.

**Version**: 1.0.0 | **Ratified**: 2025-10-11 | **Last Amended**: 2025-10-11