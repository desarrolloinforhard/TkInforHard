# Cards

Componentes:

- `IHCard`
- `IHMetricCard`
- `IHInfoCard`

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
