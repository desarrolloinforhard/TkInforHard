# Changelog

Formato basado en versionado semantico.

## [Unreleased]

### Changed

- Se actualiza `context/` para documentar `IHStatusCard`, `RoundedTableview`, modo declarativo de `IHFilterBar`, tags de `IHTable`, modo indeterminado de `IHProgress` y la demo de reportes.
- La demo principal reemplaza la sidebar fija por `IHDrawerMenu` como navegacion real y corrige el cierre del drawer al cancelar animaciones previas.
- La vista `Navigation` demuestra el `IHDrawerMenu` como menu lateral izquierdo con control de mostrar/ocultar.
- La demo incorpora una vista `Navigation` y se formaliza la regla de showcase obligatorio para cada componente nuevo.
- Se agrega `widget_reference.md` como referencia unificada de API, parametros y ejemplos de todos los widgets publicos.
- Se agrega `IHDrawerMenu`, un panel lateral animado con API para items y widgets internos.
- Las cards pasan a superficies canvas redondeadas con variantes `default`, `outlined`, `elevated` e interaccion opcional.
- La familia de inputs pasa a superficies canvas redondeadas con estados visuales centralizados, placeholders y tokens light/dark propios.
- `IHButton` adopta una ergonomia compacta inspirada en el sistema de referencia: `Segoe UI 10 bold`, alturas reducidas y canvas suavizado con `splinesteps=24`.
- `IHMenuItem` pasa a ser un componente canvas propio para navegacion lateral, con dimensiones `158x46`, radio `14`, hover y estado activo.
- Se agregan tokens de navegacion centralizados para sidebar light/dark.
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
