# Dependency Injection Container

The container (`Illuminate/Container/Container.py`) provides object graph construction for services.

## 1) Registering services

### Bind transient

```python
app.bind("cache.client", lambda: RedisClient())
```

### Bind singleton

```python
app.singleton("db", lambda app: Database(app.make("config")))
```

### Register existing instance

```python
app.instance("mailer", Mailer(api_key="..."))
```

## 2) Resolving services

```python
redis = app.make("cache.client")
```

If a key is unresolved, container raises an exception in current implementation. Explicitly register all framework contracts you use from command code and providers.

## 3) Constructor injection behavior

Container resolves callables by function signature:

- positional and keyword arguments are mapped from available container bindings
- context parameters are allowed during `resolve` calls that pass explicit dependency values

## 4) Aliasing

```python
app.alias(MyService, "my_service")
app.alias("my_service", MyService)
```

The container can resolve by alias chains for facade and service lookups.

## 5) Service providers and DI

Service providers are the primary integration point to wire dependencies:

```python
class MyProvider(ServiceProvider):
    def register(self):
        self.app.singleton("audit", lambda app: AuditService())

    def boot(self):
        pass
```

## 6) Useful patterns

- Keep bindings close to the provider that owns them.
- Avoid registering global mutable state at module import time; register inside provider `register`.
- Prefer explicit interface-key contracts (`"mail"`, `"cache"`) instead of hard class imports across many modules.

## 7) Known current constraints

- Some container defaults are currently mutable in constructor signatures; behavior is planned to be hardened.
- Service provider duplicate registration is filtered via loaded-provider map, but extension patterns should remain idempotent.