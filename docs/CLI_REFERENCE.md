# PyJinx CLI Reference (`pilot`)

This document is the concrete user-facing documentation for the CLI parity surface required by the framework roadmap and PRD.

## CLI entrypoint

- Primary command: `pilot`
- Optional local fallback: `python -m pyjinx`
- Global options:
  - `--help` / `-h` Show command help
  - `--version` / `-v` Show framework version
  - `--quiet` / `-q` Suppress non-error output

## Command groups and contracts

### App lifecycle

| Command | Purpose | Exit code | Notes |
|---|---|---:|---|
| `pilot serve` | Start the app process | `0` on successful boot; non-zero on bootstrap/startup error | ASGI-first runtime entry |
| `pilot up` | Mark app online | `0` | Maintenance mode control |
| `pilot down` | Mark app maintenance/disabled | `0` | Maintenance response behavior defined in router/config |
| `pilot tinker` | Interactive shell-like helper | `0` | Safe read-only helpers by default |
| `pilot about` | Show environment/runtime summary | `0` | Useful for diagnostics |

### Scaffolding (`make:*`)

| Command | Purpose |
|---|---|
| `pilot make:model <Name>` | Generate model scaffold |
| `pilot make:controller <Name>` | Generate controller scaffold |
| `pilot make:middleware <Name>` | Generate middleware class |
| `pilot make:command <Name>` | Generate custom command |
| `pilot make:migration <name>` | Generate migration stub |
| `pilot make:request <Name>` | Generate request validation class |
| `pilot make:factory <Name>` | Generate factory stub |

### Routing and routes inspection

| Command | Purpose |
|---|---|
| `pilot route:list` | Print registered routes |

### Project bootstrap

| Command | Purpose |
|---|---|
| `pilot new <project>` | Create a new starter application skeleton |

### Database / migration

| Command | Purpose |
|---|---|
| `pilot migrate` | Run pending migrations |
| `pilot migrate:status` | Show migration state |
| `pilot migrate:rollback` | Roll back last migration batch |
| `pilot db:seed` | Run seed data commands |

### Queue and worker (future adjacent package support)

| Command | Purpose |
|---|---|
| `pilot queue:work` | Process queue jobs |
| `pilot queue:retry` | Retry failed jobs |
| `pilot queue:failed` | Inspect failed jobs |

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