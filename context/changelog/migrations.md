# Migrations

## 1.1.0

Release compatible. No requiere migracion obligatoria para proyectos que ya usan `1.0.0`.

Para adoptar las nuevas APIs:

- Usar `IHRenderHost.show(..., on_error=...)` para errores de render/preparacion.
- Implementar `prepare_for_render(on_done, on_error)` en vistas que cargan SQL, APIs o reportes antes de mostrarse.
- Usar `IHBusyOverlay.run(...)` para procesos largos dentro de una pantalla ya abierta.
- Mantener widgets Tkinter en el hilo principal y volver desde threads con `after(0)`.
- Actualizar dependencias consumidoras a `TkInforHard>=1.1.0`.

## 1.0.0

Version inicial. No hay migraciones previas.

Futuras migraciones deben documentar:

- Cambio.
- Motivo.
- Codigo antes/despues.
- Impacto en proyectos consumidores.
