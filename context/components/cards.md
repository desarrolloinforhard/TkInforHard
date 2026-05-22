# Cards

Componentes:

- `IHCard`
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
- `interactive=True`: hover suave y callback opcional.

Ejemplos:

```python
IHCard(title="Resumen", variant="outlined")
IHMetricCard(title="Ventas", value="$ 1.240.000", variant="elevated")
IHInfoCard(title="Operacion", body="Resumen breve", interactive=True)
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
