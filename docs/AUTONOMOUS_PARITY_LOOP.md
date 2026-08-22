# Autonomous Laravel Parity Development Loop

## Mission

Continuously port `laravel/laravel` and `laravel/framework` into Python until
both parity trackers are completely implemented, source-reviewed, behaviorally
tested, and revalidated against the pinned Laravel 13.x baseline.

This loop is a development control record, not a claim that parity is already
complete.

## Executor requirement

This document defines the backlog, invariants, and resume protocol; Markdown
does not self-execute. A coordinator must invoke the loop and keep dispatching
implementation, verification, review, and delivery work.

In this environment, `/goal` is the coordinator invocation. Each invocation
can execute bounded slices and persist the next checkpoint, but it cannot
continue after the API response or start an unattended model process. An
external scheduler or orchestration runtime is required for unattended
execution. The absence of such a runtime MUST NOT be described as autonomous
background execution.

## Authoritative trackers

The loop keeps both copies synchronized:

1. Canonical framework tracker:
   `framework/docs/LARAVEL_FEATURE_PARITY_TODO.md`
2. Runtime/application mirror:
   `pyjinx/framework/docs/LARAVEL_FEATURE_PARITY_TODO.md`

The canonical framework tracker is the source of truth. The runtime mirror MUST
be updated in the same change and MUST remain byte-equivalent unless an
explicit repository-layout decision records why it cannot be.

## Complete backlog target

The loop target is **every checklist item in both parity trackers**:

- all 38 high-level Laravel feature categories;
- every detailed Database/Eloquent task;
- authentication, session, cookie, encryption, hashing, CSRF, and Sanctum;
- routing, HTTP, middleware, validation, configuration, foundation, events,
  container, support, logging, and views;
- every Artisan/console, scheduling, process, and operational task;
- cache, queues, mail, notifications, broadcasting, filesystem, Redis,
  translation, pagination, resources, HTTP client, image, concurrency, and
  extension namespaces;
- every `Illuminate.Contracts.*` namespace and promoted public contract;
- every acceptance, compatibility, deviation, and lifecycle evidence item.

The deferred `laravel/framework/tests/` port is not a shortcut or an omitted
backlog item. It is the final acceptance phase after all preceding tracker
items are complete and revalidated.

Execution is dependency-ordered because Laravel subsystems depend on one
another, but dependency ordering MUST NOT be interpreted as permission to stop
after one phase, one namespace, or one successful test run.

## Non-negotiable rules

1. Follow `software-engineering-handbook` for every non-trivial slice.
2. Preserve the Laravel 13.x source pins in `PROJECT_GOAL.md`.
3. Read the authoritative Laravel PHP source and API surface before coding.
4. Do not invent behavior, errors, ordering, lifecycle transitions, or APIs.
5. Translate Laravel implementation logic into Python; isolate only unavoidable
   PHP-runtime differences.
6. Every unavoidable deviation requires a durable rationale and behavioral
   evidence.
7. Use strict TDD: failing behavioral test, implementation, green test,
   refactor, and regression verification.
8. Do not mark a parity item complete from declarations or file presence.
9. Keep framework source in `framework`; synchronize the runtime framework
   checkout at `pyjinx/framework` after every framework change.
10. Do not port `laravel/framework/tests/` as the current implementation test
    substitute. That exhaustive suite is the final acceptance phase only after
    both parity trackers are complete and revalidated.
11. Do not stop at a phase boundary, successful component, or provisional
    checklist update. Continue to the next dependency-ready item until the
    final acceptance gate is reached or an explicit external blocker is
    recorded.

## Loop

Repeat the following cycle until the exit gate is satisfied.

### 1. Select the next dependency-ready slice

- Read both parity trackers and the implementation plan.
- Choose the earliest incomplete item whose prerequisites are implemented.
- Prefer one cohesive Laravel namespace, contract, lifecycle, command group,
  or cross-component behavior slice.
- Record the slice as a task before editing.
- Do not skip a blocked prerequisite to work on a downstream feature.
- If the next item is blocked, implement the earliest missing prerequisite or
  record the exact external blocker; do not silently skip the item.

### 2. Establish the source contract

For the selected slice:

- inventory every relevant Laravel class, public method, contract, option,
  event, error, and lifecycle transition;
- inspect `references/framework/` and `references/laravel/`;
- compare the Laravel API index;
- identify all current PyJinx callers and integration boundaries;
- write down inputs, outputs, side effects, ordering, failures, and known
  PHP-to-Python deviations.

### 3. Create behavioral evidence first

- Add focused failing tests for normal behavior, boundaries, errors, ordering,
  lifecycle transitions, and persistence where applicable.
- Add contract tests for every promoted public method.
- Add integration tests for cross-component effects.
- Preserve the Laravel scenario shape wherever Python permits.

### 4. Port the implementation

- Implement the Laravel behavior in the canonical framework source.
- Keep adapters thin and dependency details behind the existing boundary.
- Migrate every caller in scope.
- Remove obsolete parallel paths when the clean cutover is complete.
- Do not add speculative retries, fallbacks, abstractions, telemetry, or
  configuration outside the selected Laravel behavior.

### 5. Verify the changed surface

- Run focused tests first.
- Run the affected component suite.
- Run the full current PyJinx suite before delivery.
- Exercise the actual CLI, HTTP, database, or other runtime surface when the
  slice changes it.
- Record warnings, residual gaps, and quality-risk deltas.

### 6. Synchronize the split repository

- Copy/synchronize framework changes from `framework` to
  `pyjinx/framework`.
- Clear stale `__pycache__` files before rerunning runtime checks.
- Verify both framework copies resolve to the same source commit/content.
- Update both parity tracker files and relevant docs together.

### 7. Close the slice

A slice may be promoted only when it has:

- Laravel source/API mapping;
- implementation in the correct framework boundary;
- focused behavioral tests;
- affected integration/regression tests;
- synchronized framework copies;
- updated evidence and residual-gap notes in both trackers;
- clean repository state and an auditable commit.

If the complete Laravel surface is not implemented, keep the tracker item
partial or open. `[x]` means implementation presence only and is never release
completion evidence by itself.

### 8. Continue without stopping

After closing a slice:

- immediately select the next dependency-ready incomplete item;
- repeat without restarting the project or redoing completed slices;
- preserve the pinned baseline and prior green evidence;
- never treat a clean checkpoint, commit, or green suite as overall completion;
- stop only for a genuine external blocker, an authorized decision gate, or
  the final acceptance gate.

An API execution window may end operationally, but the durable checkpoint MUST
preserve the next action and the loop MUST resume there on the next invocation.

## Final acceptance gate

The loop MUST NOT begin the exhaustive Laravel test-suite port until all of the
following are true:

1. Every mapped item in both parity trackers is implemented.
2. Every tracker item has source-backed evidence.
3. Every promoted public method has a contract test.
4. Every lifecycle boundary has integration coverage.
5. Every intentional PHP-to-Python deviation is documented and tested.
6. Both trackers have been revalidated against the pinned Laravel 13.x source.
7. The revalidation result reports exact parity rather than provisional
   implementation presence.

Only then begin the final phase:

- port the complete `laravel/framework/tests/` suite;
- preserve every scenario, assertion, failure, lifecycle transition, and
  integration boundary;
- map PHPUnit/Pest helpers to PyJinx testing utilities without weakening
  assertions;
- separate intentional PHP-runtime differences from implementation failures;
- run the ported suite component-by-component and as a full framework suite.

The project is complete only when that final ported suite passes or every
remaining difference has an explicit, approved, technically unavoidable
runtime rationale with corresponding evidence.

## Resume checkpoint

At every pause, record in the parity trackers or a linked acceptance note:

- current Laravel source pin;
- completed slice and commit;
- focused and full-suite evidence;
- next dependency-ready slice;
- blocked items and the exact missing prerequisite;
- performance, code-smell, and memory-risk counts;
- outstanding PHP-to-Python deviations.
