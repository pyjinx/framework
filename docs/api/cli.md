# CLI API (`loom`)

PyJinx CLI uses a single `loom` command surface with Laravel-style grouped
commands. The same executable is used by PyJinx and the future Veyra line.

## Global behavior

- Command root: `loom`
- Help: `loom --help`
- Version: `loom --version`
- Quiet mode: `loom --quiet`

## Command groups and examples

### App lifecycle

```bash
loom serve             # run application server (ASGI-first target)
loom up
loom down
loom tinker
loom about

### Scaffolding

```bash
loom make:model User
loom make:controller AuthController
loom make:middleware VerifyCsrf
loom make:command PurgeCache
loom make:migration create_users_table
loom make:request CreateUserRequest
loom make:factory UserFactory
```

### Routing

```bash
loom route:list
```

### Project initialization

```bash
pyjinx new my-project
```

### Database commands

```bash
loom migrate
loom migrate:status
loom migrate:status --pending
loom migrate:rollback
loom db:seed
```

### Queue commands

```bash
loom queue:work
loom queue:retry
loom queue:failed
```

## Console kernel behavior

Console input is represented by `Illuminate.Foundation.Console.Input.ArgvInput` and executed through:

- `Console Kernel.handle(input, output)`
- `application.handle_command(input)`

Existing commands implemented currently:

- `list`
- `help`

Additional commands are part of the v1.0 CLI parity workstream.

For exact command contract, exit codes, overwrite/dry-run behavior, see [CLI_REFERENCE](../CLI_REFERENCE.md).
