# Configuration and Environment

## 1) Configuration repository

The container binds a `config` service from `Illuminate.Config.Repository`.

- `app.make("config")` resolves repository
- `config.get("key")` reads nested keys with dot notation
- `config.set("key", value)` writes runtime values

Example:

```python
config = app.make("config")
app_url = config.get("app.url")
config.set("app.debug", True)
```

## 2) Configuration files

Framework bootstrap loads `.py` files from configured config path (`config` directory by default).

## 3) Environment variables

Environment loading reads:

1. base `.env`
2. `.env.<APP_ENV>` when APP_ENV exists

Use `dotenv` variables directly where needed; `APP_ENV` influences loaded config state in bootstrap.

## 4) Runtime env conventions

- Keep secrets in `.env` files.
- Never log secret values.
- Restrict config caching/serialization to explicit implementation points when added in CLI phase.

## 5) Recommended production settings

- set `APP_ENV=production`
- set `APP_DEBUG=false`
- keep DB credentials in environment and avoid hardcoding defaults

See [Getting started](./getting-started.md) for bootstrap example using `Application.configure(...).