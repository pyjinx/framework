# Validation API

PyJinx ships Laravel-like validation primitives under `Illuminate.Validation`.

## 1) Rule-based validation

Create validator instance through the container service:

```python
validator = app.make("validator").make(
    data={"email": "user@example.com"},
    rules={"email": ["required", "email"]}
)

result = validator.validate()
```

The validator returns `ValidationResponse`:

- `result.validated()` (validated data)
- `result.errors()` (error map)

## 2) Using `ValidationResponse`

A successful validation includes normalized keys and errors list.

```python
if result.is_failed:
    return {"errors": result.errors}

clean_data = result.validated_data
```

## 3) Built-in rules

Rules live in `Illuminate.Validation.rules` and include:

- `required`, `nullable`, `numeric`, `integer`, `min`, `max`, `email`, `size`, and many others.

Rules are resolved dynamically through `RulesMapper`.

## 4) Form request integration

`Illuminate.Foundation.Http.FormRequest` exists as a dedicated request base class for future form-request-specific validation. Use controllers to call validator before dispatching domain logic.

## 5) API docs status

- Rule DSL and `Validator` are present and operational in core.
- Some edge-case validation semantics should be tightened in v1 hardening pass (type coercion, nested payloads, consistent error messages).

See also: [Architecture plan](../IMPLEMENTATION_PLAN.md) and [CLI docs](./cli.md).