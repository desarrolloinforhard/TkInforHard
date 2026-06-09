# Versions

TkInforHard usa versionado semantico:

- MAJOR: cambios incompatibles.
- MINOR: componentes o features compatibles.
- PATCH: fixes internos compatibles.

Version actual: `1.1.0`.

## 1.1.0

Minor release compatible.

Incluye:

- `IHLoader` mejorado.
- `IHRenderHost` con preparacion asincronica.
- `IHBusyOverlay`.
- Mejoras de rendering, transiciones y contexto.

Los proyectos consumidores deben requerir `TkInforHard>=1.1.0` para usar `IHBusyOverlay` o `prepare_for_render`.
