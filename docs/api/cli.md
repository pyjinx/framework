# CLI API (`pilot`)

PyJinx CLI uses a single command surface with Laravel-style grouped commands.

## Global behavior

- Command root: `pilot`
- Help: `pilot --help`
- Version: `pilot --version`
- Quiet mode: `pilot --quiet`

## Command groups and examples

### App lifecycle

```bash
pilot serve             # run application server (ASGI-first target)
pilot up
pilot down
pilot tinker
pilot about
```

### Scaffolding

```bash
pilot make:model User
pilot make:controller AuthController
pilot make:middleware VerifyCsrf
pilot make:command PurgeCache
pilot make:migration create_users_table
pilot make:request CreateUserRequest
pilot make:factory UserFactory
```

### Routing

```bash
pilot route:list
```

### Project initialization

```bash
pilot new my-project
```

### Database commands

```bash
pilot migrate
pilot migrate:status
pilot migrate:rollback
pilot db:seed
```

### Queue commands

```bash
pilot queue:work
pilot queue:retry
pilot queue:failed
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
