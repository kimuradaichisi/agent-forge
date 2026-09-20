# Task examples

## Cheap exploration

```text
Find every call site of OrderService.save and return path + symbol + one-line purpose. Use the cheapest suitable worker. Do not redesign anything.
```

## Tiny edit

```text
Change the timeout from 30 to 45 only in config/app.yaml and run the config validation command. Escalate if the value is derived elsewhere.
```

## Parent reasoning

```text
We need to split ordering and settlement ownership across modules. Compare boundary options and migration risks.
```
