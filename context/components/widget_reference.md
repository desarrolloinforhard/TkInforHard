# Widget Reference

Referencia rapida de componentes publicos de TkInforHard.

Import base:

```python
from TkInforHard.widgets import *
from TkInforHard.layout import *
```

## Buttons

### `IHButton`

Boton de accion canvas con bordes redondeados.

Parametros:

| Parametro | Tipo | Default | Uso |
| --- | --- | --- | --- |
| `text` | `str` | `""` | Texto visible |
| `variant` | `str` | `"primary"` | `primary`, `secondary`, `success`, `info`, `warning`, `danger` |
| `outline` | `bool` | `False` | Boton outline |
| `rounded` | `bool` | `True` | Habilita radio |
| `size` | `str` | `"md"` | `sm`, `md`, `lg` |
| `command` | callable | `None` | Accion al click |
| `min_width` | `int` | automatico | Ancho minimo |
| `radius` | `int` | token | Radio manual |
| `state` | `str` | `"normal"` | `normal` o `disabled` |

Metodos:

- `invoke()`
- `set_text(text)`

```python
IHButton(text="Guardar", variant="success", command=save)
IHButton(text="Cancelar", variant="secondary", outline=True)
```

### `IHIconButton`

Boton compacto para acciones con icono o texto corto.

Parametros adicionales:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `icon` | `str` | `""` |
| `tooltip` | `str | None` | `None` |

```python
IHIconButton(icon="?", text="Ayuda", variant="secondary", outline=True)
```

### `IHToggleButton`

Boton de dos estados respaldado por `BooleanVar`.

Parametros adicionales:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `variable` | `tk.BooleanVar | None` | nueva variable |
| `command` | callable | `None` |

```python
IHToggleButton(text="Activo", command=lambda value: print(value))
```

## Cards

### `IHCard`

Superficie redondeada componible.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str | None` | `None` |
| `subtitle` | `str | None` | `None` |
| `padding` | `int` | `16` |
| `variant` | `str` | `"default"` |
| `interactive` | `bool` | `False` |
| `command` | callable | `None` |

Variantes:

- `default`
- `outlined`
- `elevated`

Metodos:

- `add(child, **pack_options)`

```python
card = IHCard(title="Resumen", subtitle="Hoy", variant="outlined")
```

### `IHMetricCard`

Card para KPI.

Parametros adicionales:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str` | `""` |
| `value` | `str` | `""` |
| `delta` | `str | None` | `None` |

```python
IHMetricCard(title="Ventas", value="$ 1.240.000", delta="+12%", variant="elevated")
```

### `IHInfoCard`

Card para texto explicativo o resumen.

Parametros adicionales:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str` | `""` |
| `body` | `str` | `""` |
| `action` | widget | `None` |

```python
IHInfoCard(title="Operacion", body="Resumen compacto")
```

## Inputs

### `IHInput`

Input de una linea con superficie canvas.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `label` | `str | None` | `None` |
| `helper` | `str | None` | `None` |
| `placeholder` | `str | None` | `None` |
| `variable` | `tk.StringVar | None` | nueva variable |
| `state` | `str` | `"normal"` |

Metodos:

- `get()`
- `set(value)`
- `set_error(message=None)`
- `clear_error()`

```python
field = IHInput(label="Cliente", placeholder="Ingrese un cliente")
field.set_error("Campo requerido")
```

### `IHSearchInput`

Especializacion de `IHInput`.

Parametro adicional:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `placeholder` | `str` | `"Buscar..."` |

### `IHDateInput`

Especializacion de `IHInput`.

Parametros default:

- `label="Fecha"`
- `placeholder="YYYY-MM-DD"`

### `IHCombobox`

Combobox etiquetado con superficie visual compartida.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `label` | `str | None` | `None` |
| `values` | iterable | `()` |
| `variable` | `tk.StringVar | None` | nueva variable |

Metodos:

- `get()`
- `set(value)`

### `IHTextArea`

Entrada multilinea.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `label` | `str | None` | `None` |
| `height` | `int` | `5` |

Metodos:

- `get()`
- `set(value)`

## Navigation

### `IHSidebar`

Sidebar fija para navegacion principal.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str` | `"TkInforHard"` |
| `items` | `list[tuple[str, callable]]` | `None` |

```python
IHSidebar(root, items=[("Ventas", show_sales), ("Stock", show_stock)])
```

### `IHMenuItem`

Item canvas para navegacion.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `text` | `str` | `""` |
| `icon` | image | `None` |
| `active` | `bool` | `False` |
| `command` | callable | `None` |
| `width` | `int` | `158` |

Metodos:

- `set_active(active)`
- `invoke()`

### `IHDrawerMenu`

Panel lateral flotante con apertura animada.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str | None` | `None` |
| `side` | `str` | `"right"` |
| `width` | `int` | `300` |
| `animation_step` | `int` | `24` |
| `animation_delay` | `int` | `10` |

Metodos:

- `open()`
- `close()`
- `toggle()`
- `add_item(text, command=None, icon=None, active=False)`
- `add_widget(widget, **pack_options)`
- `clear()`
- `create_toggle_button(master=None, text="Menu", **kwargs)`

```python
drawer = IHDrawerMenu(root, title="Herramientas")
drawer.add_item("Cambios", command=show_changes)
drawer.create_toggle_button(root, text="Menu").pack()
```

### `IHTopbar`

Barra superior.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str` | `""` |
| `on_toggle_theme` | callable | `None` |

### `IHBreadcrumb`

Trail simple de ubicacion.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `items` | iterable | `()` |
| `separator` | `str` | `"/"` |

## Data

### `IHTable`

Tabla basada en `Treeview`.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `columns` | iterable | `()` |
| `rows` | `list[tuple] | None` | `None` |

Metodos:

- `load(rows)`

### `IHFilterBar`

Barra con input de busqueda y botones.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `on_search` | callable | `None` |
| `on_refresh` | callable | `None` |

### `IHPagination`

Control basico de paginacion.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `page` | `int` | `1` |
| `total_pages` | `int` | `1` |
| `on_prev` | callable | `None` |
| `on_next` | callable | `None` |

### `IHEmptyState`

Estado vacio.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str` | `"Sin datos"` |
| `message` | `str` | `"No hay registros para mostrar."` |

## Feedback

### `IHAlert`

Mensaje inline.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str` | `""` |
| `message` | `str` | `""` |
| `variant` | `str` | `"info"` |

### `IHLoading`

Indicador indeterminado.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `text` | `str` | `"Cargando..."` |

Metodos:

- `start(interval=10)`
- `stop()`

### `IHToast`

Notificacion temporal.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `message` | `str` | `""` |
| `duration` | `int` | `3000` |

### `IHProgress`

Barra de progreso determinada.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `label` | `str | None` | `None` |
| `value` | `int` | `0` |
| `maximum` | `int` | `100` |

Metodos:

- `set(value)`

## Display

### `IHBadge`

Etiqueta compacta de estado.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `text` | `str` | `""` |
| `variant` | `str` | `"success"` |

### `IHSectionHeader`

Titulo de seccion.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `title` | `str` | `""` |
| `subtitle` | `str | None` | `None` |

### `IHDivider`

Separador.

Parametro:

- `orient="horizontal"`

### `IHLogo`

Logo o marca textual.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `text` | `str` | `"Inforhard"` |
| `image_path` | `str | Path | None` | `None` |

## Layout

### `IHPage`

Pagina base con padding estandar.

Parametro:

- `padding=24`

### `IHContainer`

Contenedor generico.

Parametro:

- `padding=16`

### `IHStack`

Stack vertical.

Metodo:

- `add(child, fill="x", pady=6)`

### `IHScrollFrame`

Frame scrollable.

Uso:

```python
scroll = IHScrollFrame(root)
scroll.pack(fill="both", expand=True)
child = IHCard(scroll.content)
```

### `IHGrid`

Grid helper.

Parametros:

| Parametro | Tipo | Default |
| --- | --- | --- |
| `columns` | `int` | `3` |
| `gap` | `int` | `12` |

Metodo:

- `add(child, index)`

### `screen_bucket(width)`

Devuelve:

- `"compact"`
- `"medium"`
- `"wide"`

## Convenciones

- Preferir imports desde `TkInforHard.widgets` y `TkInforHard.layout`.
- No usar colores hardcodeados en pantallas consumidoras.
- Para nuevos componentes, actualizar esta referencia, el changelog y la demo.
