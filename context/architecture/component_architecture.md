# Component Architecture

Los componentes se organizan por dominio: buttons, cards, inputs, feedback, navigation, data y display.

Cada componente debe:

- Heredar de `ttk.Frame`, `ttk.Button`, `ttk.Label` u otro widget ttk compatible.
- Encapsular detalles de `ttkbootstrap`.
- Exponer una API semantica y estable.
- Aceptar parametros modernos como `variant`, `outline`, `size`, `label`, `helper` o `items`.
- No requerir que la app final conozca estilos internos.

Ejemplo:

```python
IHButton(text="Guardar", variant="success", outline=False)
```

