# Tables

Componentes:

- `IHTable`
- `IHFilterBar`
- `IHPagination`
- `IHEmptyState`
- `RoundedTableview`

`IHTable` envuelve `Treeview` y expone `load(rows)` para reemplazar datos sin filtrar logica de negocio dentro del componente.

## IHTable

`IHTable` soporta filas simples con tuplas y filas dict con tags de color.

Parametros relevantes:

- `columns`: columnas visibles.
- `rows`: datos iniciales.
- `row_tag_key`: clave usada como tag cuando las filas son dict.

Metodos:

- `load(rows)`: reemplaza los datos.
- `set_tag_color(tag, background, fg=None)`: define colores custom para tags.

Ejemplo:

```python
IHTable(
    columns=("Fecha", "Estado", "Monto"),
    rows=[
        {"Fecha": "2026-05-18", "Estado": "approved", "Monto": "$100", "semaforo": "green"},
    ],
    row_tag_key="semaforo",
)
```

Tags default:

- `green`
- `yellow`
- `red`

## IHFilterBar

`IHFilterBar` tiene dos modos.

Modo simple:

```python
IHFilterBar(on_search=buscar, on_refresh=actualizar)
```

Modo declarativo:

```python
IHFilterBar(fields=[
    {"type": "date", "key": "desde", "label": "Desde"},
    {"type": "date", "key": "hasta", "label": "Hasta"},
    {"type": "combo", "key": "estado", "label": "Estado", "values": ["(Todos)", "approved"]},
    {"type": "button", "key": "generar", "label": "Generar", "variant": "primary"},
])
```

Metodos:

- `get_values()`
- `set_state(key, state)`
- `update_combo(key, values)`

## RoundedTableview

`RoundedTableview` extiende `ttkbootstrap.tableview.Tableview` y reemplaza la paginacion por una barra redondeada con botones `IHButton`.

Parametros extra:

- `pagination_fill`
- `pagination_outer_bg`
- `pagination_text_fg`
- `pagination_radius`

Metodo:

- `apply_theme(fill, outer_bg=None, fg=None)`

Se usa para reportes con muchas filas, paginacion y estilo corporativo.
