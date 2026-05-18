# Navigation

Componentes:

- `IHSidebar`
- `IHTopbar`
- `IHMenuItem`
- `IHBreadcrumb`
- `IHDrawerMenu`

La navegacion prioriza aplicaciones empresariales: sidebar persistente, topbar compacta y breadcrumbs de contexto.

`IHMenuItem` replica el patron del sidebar de referencia como componente formal:

- Canvas compuesto.
- `158 x 46`.
- Radio `14`.
- Texto `Segoe UI 10 bold`.
- Fondo normal, hover y activo centralizados en tokens.
- Soporte para teclado e icono opcional.

`IHDrawerMenu` agrega un panel lateral flotante con apertura/cierre animado:

- `side="left" | "right"`.
- `open()`, `close()` y `toggle()`.
- `create_toggle_button()` para generar un disparador listo.
- `add_item()` para agregar `IHMenuItem`.
- `add_widget()` para componer controles arbitrarios dentro del menu.

Ejemplo:

```python
drawer = IHDrawerMenu(root, title="Herramientas", side="right", width=300)
drawer.add_item("Cambios", command=show_changes)
drawer.add_item("Local", command=show_local)
drawer.create_toggle_button(root, text="Menu").pack()
```
