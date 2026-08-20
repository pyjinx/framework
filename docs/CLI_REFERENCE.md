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
| `pyjinx serve` | Start the app process | `0` on successful boot; non-zero on bootstrap/startup error | ASGI-first runtime entry |
| `pyjinx up` | Mark app online | `0` | Maintenance mode control |
| `pyjinx down` | Mark app maintenance/disabled | `0` | Maintenance response behavior defined in router/config |
| `pyjinx tinker` | Interactive shell-like helper | `0` | Safe read-only helpers by default |
| `pyjinx about` | Show environment/runtime summary | `0` | Useful for diagnostics |

### Scaffolding (`make:*`)

| Command | Purpose |
|---|---|
| `pyjinx make:model <Name>` | Generate model scaffold |
| `pyjinx make:controller <Name>` | Generate controller scaffold |
| `pyjinx make:middleware <Name>` | Generate middleware class |
| `pyjinx make:command <Name>` | Generate custom command |
| `pyjinx make:migration <name>` | Generate migration stub |
| `pyjinx make:request <Name>` | Generate request validation class |
| `pyjinx make:factory <Name>` | Generate factory stub |

### Routing and routes inspection

| Command | Purpose |
|---|---|
| `pyjinx route:list` | Print registered routes |

### Project bootstrap

| Command | Purpose |
|---|---|
| `pyjinx new <project>` | Create a new starter application skeleton |

### Database / migration

| Command | Purpose |
|---|---|
| `pyjinx migrate` | Run pending migrations |
| `pyjinx migrate:status` | Show migration state |
| `pyjinx migrate:rollback` | Roll back last migration batch |
| `pyjinx db:seed` | Run seed data commands |

### Queue and worker (future adjacent package support)

| Command | Purpose |
|---|---|
| `pyjinx queue:work` | Process queue jobs |
| `pyjinx queue:retry` | Retry failed jobs |
| `pyjinx queue:failed` | Inspect failed jobs |

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