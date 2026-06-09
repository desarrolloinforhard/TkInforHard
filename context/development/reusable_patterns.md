# Reusable Patterns

Patrones aprobados:

- Composite Widget Pattern para inputs, cards y feedback.
- Controller separado para demo y navegacion.
- `ThemeManager` como punto unico de theme.
- `load(rows)` para componentes de datos.
- `get/set` para componentes de entrada.
- `IHRenderHost` para navegar entre pantallas pesadas mostrando `IHLoader`, esperando una vuelta minima si hace falta, montando el frame detras del loader y haciendo swap cuando el frame esta listo.
- `IHLoader` como loader corporativo reutilizable: iniciales IH fijas, aro circular animado, fondo adaptable al frame padre y render suavizado en memoria cuando Pillow esta disponible.
- `IHBusyOverlay` para procesos largos dentro de una pantalla, usando thread daemon, callbacks en hilo UI y bloqueo visual opcional.
- `IHImageGridTable(renderer="canvas")` para grillas visuales de imagenes/iconos con cache y celdas reutilizables.
- `IHAnimator` para microinteracciones tipo CSS transition usando `after()`, easing y callbacks por frame.
