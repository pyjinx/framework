# Autonomous Laravel Parity Development Loop

## Mission

Continuously port `laravel/laravel` and `laravel/framework` into Python until
both parity trackers are completely implemented, source-reviewed, behaviorally
tested, and revalidated against the pinned Laravel 13.x baseline.

This loop is a development control record, not a claim that parity is already
complete.

## Authoritative trackers

The loop keeps both copies synchronized:

1. Canonical framework tracker:
   `port/framework/docs/LARAVEL_FEATURE_PARITY_TODO.md`
2. Runtime/application mirror:
   `port/pyjinx/framework/docs/LARAVEL_FEATURE_PARITY_TODO.md`

The canonical framework tracker is the source of truth. The runtime mirror MUST
be updated in the same change and MUST remain byte-equivalent unless an
explicit repository-layout decision records why it cannot be.

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
9. Keep framework source in `port/framework`; synchronize the runtime framework
   checkout at `port/pyjinx/framework` after every framework change.
10. Do not port `laravel/framework/tests/` as the current implementation test
    substitute. That exhaustive suite is the final acceptance phase only after
    both parity trackers are complete and revalidated.

## Loop

Repeat the following cycle until the exit gate is satisfied.

### 1. Select the next dependency-ready slice

- Read both parity trackers and the implementation plan.
- Choose the earliest incomplete item whose prerequisites are implemented.
- Prefer one cohesive Laravel namespace, contract, lifecycle, command group,
  or cross-component behavior slice.
- Record the slice as a task before editing.
- Do not skip a blocked prerequisite to work on a downstream feature.

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

- Copy/synchronize framework changes from `port/framework` to
  `port/pyjinx/framework`.
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

### 8. Continue automatically

After closing a slice:

- select the next dependency-ready incomplete item;
- repeat without restarting the project or redoing completed slices;
- preserve the pinned baseline and prior green evidence;
- stop only for a genuine external blocker, an authorized decision gate, or
  the final acceptance gate.

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
