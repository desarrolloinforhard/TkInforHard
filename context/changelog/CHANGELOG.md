# Changelog

Formato basado en versionado semantico.

## [Unreleased]

### Changed

- Sin cambios pendientes.

## [1.1.0] - 2026-05-26

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
- Se agrega demo `Iconos` para explorar providers `mat`, `gmi` y `fa` de `ttkbootstrap-icons`.
- Se agrega `IHImageGridTable` para grillas paginadas de imagenes/iconos con renderer canvas, cache y celdas reutilizables.
- Se agrega `IHRenderHost` para renderizar pantallas detras de un loader antes de hacer swap visual.
- Se documentan patrones de rendering para evitar que Tkinter muestre frames parcialmente construidos.
- Se amplian las cards con seleccion, variantes semanticas, metric cards enriquecidas e `IHCardGrid`.
- Se agrega `IHAnimator` y transiciones suaves en `IHCard` para hover/pressed tipo CSS.
- `IHRenderHost` incorpora duracion minima de loader, delay de render y cache de vistas para transiciones de modulo mas suaves.
- Se agrega `IHLoader`, loader corporativo circular Canvas con iniciales IH, y demo standalone `demo/demo_ih_loader.py`.
- `IHLoader` vuelve a Canvas puro, asegura letras IH visibles con `tag_raise`, mayor tamano en `IHRenderHost` y fondo unificado.
- `IHLoader` agrega render suavizado en memoria con Pillow cuando esta disponible, sin GIF ni archivos externos, para mejorar definicion en Windows.
- `IHRenderHost` agrega `min_loader_cycles`, `settle_delay` y coordinacion con `IHLoader.revolution_ms()` para completar al menos una vuelta antes de construir/swapear modulos pesados.
- `IHRenderHost` soporta preparacion asincronica con `prepare_for_render(on_done, on_error)`, callback `prepare`, `on_error`, timeout y token interno para ignorar resultados de navegaciones viejas.
- Se agrega `IHBusyOverlay` para procesos largos dentro de una pantalla, con `IHLoader`, thread daemon, callbacks en hilo UI, minimo visible y bloqueo visual opcional.

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

