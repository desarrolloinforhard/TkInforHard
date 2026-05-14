# Folder Structure

La estructura fija del framework separa responsabilidades:

- `core/`: aplicacion, config, constantes y enums.
- `theme/`: design tokens, themes y estilos.
- `widgets/`: componentes visuales.
- `layout/`: primitives de composicion.
- `utils/`: helpers no visuales.
- `assets/`: logo, iconos y fuentes.
- `demo/`: showcase app.
- `context/`: memoria tecnica permanente.

No mezclar widgets de demo dentro de `demo/`; la demo debe consumir solo componentes de la libreria.

