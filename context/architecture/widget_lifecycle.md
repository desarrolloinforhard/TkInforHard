# Widget Lifecycle

El ciclo de vida recomendado para un widget es:

1. Recibir parametros semanticos.
2. Resolver estilos desde tokens o estilos `IH.*`.
3. Construir subwidgets internos.
4. Exponer metodos publicos pequenos (`get`, `set`, `load`, `start`, `stop`).
5. Mantener estado interno controlado por variables Tk cuando corresponda.

Los widgets compuestos deben separar la API publica de la composicion visual interna.

