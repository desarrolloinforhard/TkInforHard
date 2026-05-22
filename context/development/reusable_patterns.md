# Reusable Patterns

Patrones aprobados:

- Composite Widget Pattern para inputs, cards y feedback.
- Controller separado para demo y navegacion.
- `ThemeManager` como punto unico de theme.
- `load(rows)` para componentes de datos.
- `get/set` para componentes de entrada.
- `IHRenderHost` para navegar entre pantallas pesadas mostrando loader y haciendo swap cuando el frame esta listo.
- `IHImageGridTable(renderer="canvas")` para grillas visuales de imagenes/iconos con cache y celdas reutilizables.
