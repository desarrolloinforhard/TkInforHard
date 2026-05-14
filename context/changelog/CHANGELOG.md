# Changelog

Formato basado en versionado semantico.

## [Unreleased]

### Changed

- Paleta base redefinida con verde Inforhard `#008A46`, variantes para hover y tokens especificos para modo claro/oscuro.
- `IHButton` ahora usa Canvas internamente para garantizar bordes redondeados reales y estados visuales consistentes.
- `IHIconButton` e `IHToggleButton` heredan el nuevo comportamiento canvas de `IHButton`.
- `ThemeManager` tolera fallos internos de reconstruccion de themes de `ttkbootstrap` y mantiene tokens/estilos propios activos.

## [1.0.0]

### Added

- Estructura inicial de TkInforHard.
- Theme engine con `inforhard_dark` e `inforhard_light`.
- Design tokens de color, spacing, tipografia y radius.
- Componentes base: buttons, cards, inputs, feedback, navigation, data y display.
- Layout primitives: page, container, stack, scrollframe y grid.
- Demo showcase.
- Carpeta `context/` como memoria tecnica permanente.

### Changed

- No aplica en la version inicial.

### Fixed

- No aplica en la version inicial.

### Removed

- No aplica en la version inicial.
