# Buttons

Componentes:

- `IHButton`
- `IHIconButton`
- `IHToggleButton`

Ejemplo:

```python
IHButton(text="Guardar", variant="success")
IHButton(text="Cancelar", variant="secondary", outline=True)
IHIconButton(icon="⚙", text="Configurar")
IHToggleButton(text="Activo")
```

Los botones encapsulan `ttkbootstrap` mediante `variant`, `outline`, `rounded` y `size`.

## Decision tecnica

`IHButton` usa `Canvas` internamente para dibujar bordes redondeados reales. Esta decision evita depender de las limitaciones visuales de `ttk.Button`, que no garantiza radius consistente entre themes y sistemas.

Reglas para botones:

- Mantener API semantica: `text`, `variant`, `outline`, `rounded`, `size`, `command`.
- Dibujar fill, borde, hover y pressed desde tokens.
- No hardcodear colores dentro de pantallas consumidoras.
- Los botones derivados deben extender `IHButton`, no `ttk.Button`.
