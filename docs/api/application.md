# Application, Kernel, and Lifecycle

## 1) Core application object

The central object is `Illuminate/Foundation/Application.py` (`app`). It owns:

- service container bindings
- provider registration and booting
- kernel selection
- config/environment access
- request and command handlers

Common entrypoints:

```python
app = Application.configure(base_path="...").with_routing().with_middleware().with_exceptions().create()
response = app.handle_request(request)
result = app.handle_command(input)
```

## 2) Bootstrap pipeline

At runtime, bootstrap executes bootstrappers in order:

1. `LoadEnvironmentVariables`
2. `LoadConfiguration`
3. `HandleExceptions`
4. `RegisterFacades`
5. `RegisterProviders`
6. `BootProviders`

This is orchestrated by both the HTTP and console kernels.

## 3) HTTP vs Console kernels

- **HTTP kernel**: `Illuminate.Foundation.Http.Kernel`
  - `handle(request)` -> runs middleware and route dispatch
- **Console kernel**: `Illuminate.Foundation.Console.Kernel`
  - `handle(input, output)` -> parses/dispatches CLI commands

Both kernels call bootstrap once and keep the application in an initialized state for the process lifetime.

## 4) Providers lifecycle

A provider follows this lifecycle:

1. register time
2. boot time (after all providers are registered)

A provider is registered by either:

- default framework registration (`Application._register_base_providers()`),
- explicit call to `app.register(provider_class)`,
- config-driven providers from `config`.

## 5) Container and service registration points

- Register binding:
  - `app.bind(key, resolver)`
  - `app.singleton(key, resolver)`
  - `app.instance(key, value)`
- Resolve:
  - `app.make(key)`
  - `app.get_instance(key)`

Use this when your services need dependency-injected construction.

## 6) Hooks and extension points

- `bootstraping` / `bootstrapped` app events are dispatched during kernel init.
- Commander bootstrappers can subscribe via console dispatcher/listeners.
- Existing support for command/listener registration is in `ServiceProvider` and dispatcher contracts.

## 7) Errors and termination

- Runtime init errors bubble through the active kernel and can be caught in host integration.
- `app.terminate()` is called during lifecycle end:
  - HTTP kernel termination receives request/response
  - Console kernel termination runs command callbacks