# Icons

La demo incluye un `Icon Browser` para explorar providers instalados de `ttkbootstrap-icons`.

Providers iniciales:

- `ttkbootstrap-icons-mat`: Material Design Icons.
- `ttkbootstrap-icons-gmi`: Google Material Icons.
- `ttkbootstrap-icons-fa`: Font Awesome 6 Free.

La vista usa `IHImageGridTable` para listar iconos visualmente en una grilla paginada. Permite cambiar provider, estilo, tamano y color, buscar por nombre, previsualizar el icono seleccionado y copiar el nombre para usarlo en codigo.

`IHImageGridTable` queda disponible como componente reusable para futuras tablas visuales con imagenes. Acepta datos, un `image_factory`, callbacks de seleccion y argumentos de filas/columnas con limite configurable de hasta 10x10.

La implementacion actual usa `renderer="canvas"` y cache de imagenes para evitar que el usuario vea la construccion progresiva de cada icono. La grilla prioriza legibilidad: color estable por tema para los iconos de la grilla y color preset aplicado al preview seleccionado.

Uso en el demo:

- Sidebar: `Iconos`.
- Provider/style/size/color arriba.
- Busqueda por nombre.
- Grilla visual paginada con `IHImageGridTable`.
- Panel derecho con preview, nombre, provider, unicode y `Copy Name`.

Uso base:

```python
from ttkbootstrap_icons_mat import MatIcon
from ttkbootstrap_icons_gmi import GMatIcon
from ttkbootstrap_icons_fa import FAIcon

mat = MatIcon("home", size=24, color="#009845", style="fill")
gmi = GMatIcon("home", size=24, color="#009845", style="outlined")
fa = FAIcon("house", size=24, color="#009845", style="solid")
```
