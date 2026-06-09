# Feedback

Componentes:

- `IHAlert`
- `IHBusyOverlay`
- `IHLoader`
- `IHLoading`
- `IHToast`
- `IHProgress`

Feedback debe ser claro, no invasivo y consistente con los variants semanticos.

## IHLoader

`IHLoader` es el loader corporativo recomendado para estados de carga visibles.

Caracteristicas:

- Canvas puro, sin GIF ni imagen externa. Si Pillow esta disponible, el aro se renderiza internamente en memoria a mayor escala para mejorar definicion.
- Las letras se dibujan despues del aro y el arco, y se elevan con `canvas.tag_raise(text_id)`.
- Iniciales `IH` fijas dentro de un circulo.
- Aro circular con arco verde animado, evitando `create_arc` para reducir el dentado visual en Windows.
- Color principal: `#008A46`.
- Gris apagado por tema: `#D1D5DB` en light mode y `#374151` en dark mode.
- Liviano: usa `after()` y no bloquea la interfaz.
- Funciona bien en `32`, `48`, `64` y `96`.
- En transiciones de modulo, `IHRenderHost` usa 96px para mayor presencia visual.
- Tamano de fuente recomendado: `font_size=max(14, int(size * 0.28))`.
- `revolution_ms()` expone el tiempo aproximado de una vuelta completa para coordinar transiciones.
- En dark mode corporativo, el fondo recomendado del loader es el token `color.background` (`#0E1512`) para que no aparezcan bloques grises.

API:

```python
loader = IHLoader(parent, size=48, mode="dark")
loader.start()
loader.stop()
loader.set_size(64)
loader.set_theme("light")
loader.revolution_ms()
```

Parametros principales:

- `size`
- `primary_color`
- `background`
- `speed`
- `ring_width`
- `font_family`
- `mode`
- `high_quality`
- `text`
- `text_position`
- `show_percent`
- `progress_text`

Notas de implementacion:

- No usar `font=("Arial", 10)`; vuelve ilegibles las iniciales.
- Las letras `IH` deben ser siempre el ultimo item visual o elevarse con `canvas.tag_raise(text_id)`.
- En Windows, `create_arc` se ve dentado. El componente evita ese camino y usa render suavizado cuando Pillow esta disponible.
- El render con Pillow es interno y en memoria: no genera archivos, no usa GIF y no agrega assets externos.

Uso:

```python
from TkInforHard.components import IHLoader

loader = IHLoader(frame, size=64, primary_color="#008A46")
loader.pack()
loader.start()
```

Demo standalone:

```powershell
python demo/demo_ih_loader.py
python demo/demo_ih_busy_overlay.py
```

`IHRenderHost` usa `IHLoader` internamente para transiciones entre modulos.

## IHBusyOverlay

`IHBusyOverlay` es el overlay visual recomendado para procesos largos dentro de una pantalla ya abierta.

Usar para:

- Generar reportes.
- Exportar PDF.
- Sincronizar datos.
- Consultas SQL/API disparadas por un boton.
- Procesos que no implican cambiar de modulo.

Regla:

- `IHRenderHost` se usa para cambiar pantallas.
- `IHBusyOverlay` se usa para acciones largas dentro de la pantalla actual.

API:

```python
overlay = IHBusyOverlay(
    parent,
    text="Procesando...",
    subtext="Esto puede tardar unos segundos",
    block_input=True,
    min_visible_ms=700,
    cancellable=False,
)

overlay.run(
    task=lambda: service.generar_reporte(),
    on_success=lambda result: vista.mostrar_resultado(result),
    on_error=lambda exc: messagebox.showerror("Error", str(exc)),
)
```

Comportamiento:

- Usa `IHLoader` internamente.
- Ejecuta `task` en un thread daemon.
- Mantiene visible el overlay al menos `min_visible_ms` para evitar parpadeos.
- Devuelve `on_success` y `on_error` al hilo principal con `after(0)`.
- Si se cancela visualmente, ignora resultados tardios mediante token interno.

## IHProgress

`IHProgress` soporta dos modos:

- `determinate`: barra con valor numerico.
- `indeterminate`: animacion continua para cargas.

Ejemplos:

```python
IHProgress(label="Carga", value=64)

loader = IHProgress(mode="indeterminate")
loader.start()
loader.stop()
```

Parametros:

- `label`
- `value`
- `maximum`
- `mode`
