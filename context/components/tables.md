# Tables

Componentes:

- `IHTable`
- `IHImageGridTable`
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

## IHImageGridTable

`IHImageGridTable` es una tabla visual paginada para imagenes, iconos, miniaturas, productos, adjuntos o cualquier dataset donde el primer contacto del usuario debe ser visual y no textual.

Usar cuando:

- Hay que mostrar muchos iconos o miniaturas.
- La UI debe parecer una galeria o browser visual.
- Crear muchos botones/widgets causa parpadeo o render progresivo visible.
- Se necesita paginacion y seleccion de items.

No usar cuando:

- El dato principal es texto tabular.
- Se necesitan columnas, ordenamiento textual o celdas editables. Para eso usar `IHTable` o `ttkbootstrap.tableview.Tableview`.

API principal:

```python
IHImageGridTable(
    master,
    items=data,
    rows=8,
    columns=10,
    cell_size=50,
    image_factory=make_image,
    image_key_getter=lambda item: item["id"],
    label_getter=lambda item: item["name"],
    on_select=handle_select,
    show_labels=False,
    renderer="canvas",
    cache_images=True,
)
```

Argumentos importantes:

- `items`: lista de datos fuente.
- `rows` y `columns`: tamano de pagina. El componente limita por defecto hasta 10x10.
- `image_factory(item, size=None)`: callback que devuelve `PhotoImage` para cada item.
- `image_key_getter(item)`: clave estable para cachear imagenes. Debe incluir todo lo que cambie el render, por ejemplo provider, estilo, nombre, tamano y color.
- `label_getter(item)`: texto opcional si `show_labels=True`.
- `on_select(item)`: callback al seleccionar.
- `renderer="canvas"`: modo recomendado para muchos items. Reutiliza celdas en Canvas.
- `cache_images=True`: evita regenerar imagenes al volver a una pagina.

Ejemplo:

```python
def make_swatch(item, size=None):
    image_size = int(size or 48)
    image = tk.PhotoImage(width=image_size, height=image_size)
    image.put(item["color"], to=(0, 0, image_size, image_size))
    return image

grid = IHImageGridTable(
    parent,
    items=colors,
    rows=2,
    columns=5,
    image_factory=make_swatch,
    image_key_getter=lambda item: item["name"],
    on_select=lambda item: print(item["name"]),
    renderer="canvas",
)
```

Notas de diseno:

- Los tiles no deben verse como botones pesados. Deben parecer celdas visuales: fondo suave, hover sutil y borde de seleccion claro.
- En dark mode, el color de los iconos de la grilla debe priorizar legibilidad. El color elegido por el usuario puede aplicarse al preview, no necesariamente a toda la grilla.
- Mantener el nombre y los detalles en un panel lateral o inferior, no debajo de cada icono salvo que el dataset lo requiera.

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