# Component Architecture

Los componentes se organizan por dominio: buttons, cards, inputs, feedback, navigation, data y display.

Cada componente debe:

- Heredar de `ttk.Frame`, `ttk.Button`, `ttk.Label` u otro widget ttk compatible.
- Encapsular detalles de `ttkbootstrap`.
- Exponer una API semantica y estable.
- Aceptar parametros modernos como `variant`, `outline`, `size`, `label`, `helper` o `items`.
- No requerir que la app final conozca estilos internos.
- Preferir componentes especializados cuando el patron de interaccion lo justifica. Ejemplo: usar `IHImageGridTable` para imagenes/iconos en grilla en lugar de forzar `Treeview` o `Tableview`.

Ejemplo:

```python
IHButton(text="Guardar", variant="success", outline=False)
```

Para pantallas pesadas o modulos con muchos widgets, el controller debe usar `IHRenderHost` como contenedor de contenido para evitar que el usuario vea el render parcial.
