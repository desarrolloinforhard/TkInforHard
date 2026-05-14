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

