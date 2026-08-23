# PyJinx CLI Reference (`pyjinx`)

This document is the concrete user-facing documentation for the CLI parity surface required by the framework roadmap and PRD.

## CLI entrypoint

- Primary command: `pyjinx`
- Optional local fallback: `python -m pyjinx`
- Global options:
  - `--help` / `-h` Show command help
  - `--version` / `-v` Show framework version
  - `--quiet` / `-q` Suppress non-error output

## Command groups and contracts

### App lifecycle

| Command | Purpose | Exit code | Notes |
|---|---|---:|---|
| `loom serve` | Start the app process | `0` on successful boot; non-zero on bootstrap/startup error | ASGI-first runtime entry |
| `loom up` | Mark app online | `0` | Maintenance mode control |
| `loom down` | Mark app maintenance/disabled | `0` | Maintenance response behavior defined in router/config |
| `loom tinker` | Interactive shell-like helper | `0` | Safe read-only helpers by default |
| `loom about` | Show environment/runtime summary | `0` | Useful for diagnostics |

### Scaffolding (`make:*`)

| Command | Purpose |
|---|---|
| `loom make:model <Name>` | Generate model scaffold |
| `loom make:controller <Name>` | Generate controller scaffold |
| `loom make:middleware <Name>` | Generate middleware class |
| `loom make:command <Name>` | Generate custom command |
| `loom make:migration <name>` | Generate migration stub |
| `loom make:request <Name>` | Generate request validation class |
| `loom make:factory <Name>` | Generate factory stub |

### Routing and routes inspection

| Command | Purpose |
|---|---|
| `loom route:list` | Print registered routes |

### Project bootstrap

| Command | Purpose |
|---|---|
| `pyjinx new <project>` | Create a new starter application skeleton |

### Database / migration

| Command | Purpose |
|---|---|
| `loom migrate` | Run pending migrations |
| `loom migrate:status [--pending]` | Show every migration or only pending migrations; reports when none are pending |
| `loom migrate:rollback` | Roll back last migration batch |
| `loom db:seed` | Run seed data commands |

### Queue and worker (future adjacent package support)

| Command | Purpose |
|---|---|
| `loom queue:work` | Process queue jobs |
| `loom queue:retry` | Retry failed jobs |
| `loom queue:failed` | Inspect failed jobs |

## Generator behavior contract

- Commands are deterministic and produce predictable files from versioned stubs.
- Generated file path and namespace are derived from configured project/app namespace.
- `--force` (or equivalent command option) overwrites existing files.
- `--dry-run` prints target path and content preview without writing.
- Missing required args/invalid stubs fail with actionable error and non-zero exit code.

## Error handling convention

- Invalid command: non-zero exit code + short usage message.
- Validation failures: non-zero exit code and structured error payload where feasible.
- Execution failures: surfaced with command identity and root cause classification.

## Versioned CLI surface policy

- The command set is versioned with the framework major/minor.
- Backward-incompatible command behavior changes require migration notes and release notes.
- No hidden compatibility mode for commands.

## See also

- [PRD](./PRD.md)
- [Roadmap](./ROADMAP.md)
- [Implementation Plan](./IMPLEMENTATION_PLAN.md)