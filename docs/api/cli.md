# CLI API (`pyjinx`)

PyJinx CLI uses a single command surface with Laravel-style grouped commands.

## Global behavior

- Command root: `pyjinx`
- Help: `pyjinx --help`
- Version: `pyjinx --version`
- Quiet mode: `pyjinx --quiet`

## Command groups and examples

### App lifecycle

```bash
pyjinx serve             # run application server (ASGI-first target)
pyjinx up
pyjinx down
pyjinx tinker
pyjinx about
```

### Scaffolding

```bash
pyjinx make:model User
pyjinx make:controller AuthController
pyjinx make:middleware VerifyCsrf
pyjinx make:command PurgeCache
pyjinx make:migration create_users_table
pyjinx make:request CreateUserRequest
pyjinx make:factory UserFactory
```

### Routing

```bash
pyjinx route:list
```

### Project initialization

```bash
pyjinx new my-project
```

### Database commands

```bash
pyjinx migrate
pyjinx migrate:status
pyjinx migrate:rollback
pyjinx db:seed
```

### Queue commands

```bash
pyjinx queue:work
pyjinx queue:retry
pyjinx queue:failed
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
