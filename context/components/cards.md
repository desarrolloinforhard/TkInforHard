# Cards

Componentes:

- `IHCard`
- `IHCardGrid`
- `IHMetricCard`
- `IHInfoCard`
- `IHStatusCard`

Las cards agrupan informacion de dashboards, formularios y pantallas ERP.

Ejemplo:

```python
IHMetricCard(title="Ventas", value="$ 1.240.000", delta="+12%")
```

## Sistema visual

Las cards usan una superficie canvas con radio `12` y cuerpo interno componible.

Variantes:

- `default`: superficie base con borde suave.
- `outlined`: semantica de borde visible.
- `elevated`: sombra simulada para mayor jerarquia.
- `primary`, `success`, `info`, `warning`, `danger`: acento semantico lateral para estados.
- `interactive=True`: hover suave y callback opcional.
- `selected=True`: borde/acento activo para opciones seleccionables.
- El hover en cards interactivas debe sentirse como acercamiento: se reduce el inset interno de dibujo para que la superficie parezca crecer dentro de su celda.
- El hover y pressed usan `IHAnimator` para transiciones suaves tipo CSS. Evitar cambios bruscos de estado en cards interactivas.
- El contenido creado por la card debe compartir el mismo fondo que la superficie canvas. Evitar `ttk.Label` internos con fondo `IH.Surface.TFrame` porque generan rectangulos cuadrados sobre bordes redondeados.

Ejemplos:

```python
IHCard(title="Resumen", variant="outlined")
IHCard(title="Local", interactive=True, command=seleccionar, selected=True)
IHMetricCard(title="Ventas", value="$ 1.240.000", variant="elevated")
IHInfoCard(title="Operacion", body="Resumen breve", interactive=True)
```

Metodos de `IHCard`:

- `set_selected(selected=True)`: cambia el estado seleccionado.
- `set_variant(variant)`: cambia la variante visual.

## IHCardGrid

`IHCardGrid` organiza cards en columnas con spacing consistente.

Uso:

```python
grid = IHCardGrid(parent, columns=3)
grid.add(IHMetricCard(grid, title="Ventas", value="$ 1.240.000"))
```

Se recomienda usarlo en dashboards, selectores visuales y grupos de cards.

## Metric Cards

`IHMetricCard` soporta datos de dashboard enriquecidos:

- `delta`
- `delta_variant`
- `badge`
- `helper`
- `icon`

Ejemplo:

```python
IHMetricCard(
    title="Ventas",
    value="$ 1.240.000",
    delta="12%",
    delta_variant="success",
    badge="Hoy",
    icon="$",
)
```

## Status Cards

`IHStatusCard` es una card orientada a reportes y semaforos operativos.

Uso:

```python
IHStatusCard(
    title="Aprobados con monto coincidente",
    count="80",
    detail="transacciones - $240,983.26",
    bg="#0D3320",
    fg="#22C55E",
    muted="#FFFFFF",
)
```

Metodos:

- `update(count, detail)`: actualiza el valor y detalle.
- `set_colors(bg, fg, muted)`: cambia colores y redibuja.

Se recomienda usarla para dashboards, reportes y estados agregados.
