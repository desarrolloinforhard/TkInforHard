# Feedback

Componentes:

- `IHAlert`
- `IHLoading`
- `IHToast`
- `IHProgress`

Feedback debe ser claro, no invasivo y consistente con los variants semanticos.

## IHProgress

`IHProgress` soporta dos modos:

- `determinate`: barra con valor numerico.
- `indeterminate`: animacion continua para cargas.

Ejemplos:

```python
IHProgress(label="Carga", value=64)

loader = IHProgress(mode="indeterminate")
loader.start()
loader.stop()
```

Parametros:

- `label`
- `value`
- `maximum`
- `mode`
