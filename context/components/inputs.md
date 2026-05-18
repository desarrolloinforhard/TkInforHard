# Inputs

Componentes:

- `IHInput`
- `IHSearchInput`
- `IHTextArea`
- `IHCombobox`
- `IHDateInput`

Los inputs son compuestos: label, control y helper text cuando corresponde.

## Sistema visual

Los inputs usan una superficie `Canvas` redondeada para mantener consistencia visual con botones y navegacion:

- Radio `12`.
- Estados `normal`, `hover`, `focus`, `disabled` y `error`.
- Tokens propios para background, border y placeholder en light/dark.
- Placeholder gestionado por el componente, no por la pantalla consumidora.

## Ejemplos

```python
IHInput(
    label="Cliente",
    helper="Nombre fiscal o fantasia",
    placeholder="Ingrese un cliente",
)

field = IHInput(label="CUIT")
field.set_error("Formato invalido")
```

`IHSearchInput`, `IHDateInput`, `IHCombobox` e `IHTextArea` comparten la misma familia visual.
