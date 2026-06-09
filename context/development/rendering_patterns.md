# Rendering Patterns

## IHRenderHost

`IHRenderHost` es el contenedor recomendado para navegar entre pantallas pesadas.

Patron:

1. Mostrar un loader inmediatamente.
2. Dejar que el loader pinte y complete al menos una vuelta si la transicion lo necesita.
3. Construir el nuevo frame mientras el loader esta visible.
4. Montar el frame nuevo detras del loader.
5. Esperar un `settle_delay` corto para que Tkinter pinte el frame completo.
6. Hacer swap visual cuando el frame ya esta listo.
7. Ocultar el loader y retirar/destruir el frame anterior segun cache.

Esto evita que el usuario vea como se construyen widgets, grillas o previews de a partes.

Reglas de UX:

- El loader debe tener una duracion minima visible, incluso si el modulo ya esta cacheado.
- Usar `render_delay` para permitir que el loader pinte y empiece a animar antes de construir una vista pesada.
- Usar `min_loader_ms` para evitar cambios demasiado rapidos o bruscos.
- Usar `min_loader_cycles=1` cuando se quiera que el loader complete al menos una vuelta antes de construir/cambiar el modulo.
- Usar `settle_delay` para dar tiempo a que Tkinter pinte la vista oculta antes del swap visual.
- Usar `cache_key` para reutilizar vistas ya construidas y preservar estado.
- Usar `IHLoader` como loader corporativo dentro del host.
- Para demo o modulos pesados, usar como base `render_delay=140`, `min_loader_ms=1300`, `min_loader_cycles=1`, `settle_delay=120`, `cache_views=True`.
- El fondo del overlay debe salir de `theme_manager.tokens()["color"]["background"]`, no del color nativo de ttkbootstrap, para evitar un gris distinto al verde corporativo.
- Si la vista tiene `prepare_for_render(on_done, on_error)`, `IHRenderHost` debe esperar `on_done` antes del swap.
- `prepare_for_render` debe iniciar trabajo pesado en background y volver al hilo UI con `after(0)`.
- `on_error` debe mostrar estado de error o delegar en callback, sin romper la app.
- Si el usuario cambia de modulo antes de terminar, el token interno debe ignorar el resultado viejo.

Uso:

```python
host = IHRenderHost(
    parent,
    loading_text="Cargando modulo...",
    render_delay=140,
    min_loader_ms=1300,
    min_loader_cycles=1,
    settle_delay=120,
    cache_views=True,
)
host.show(lambda master: MyView(master), cache_key="my-view")
```

Preparacion asincronica:

```python
class ReportesView(ttk.Frame):
    def prepare_for_render(self, on_done, on_error=None):
        def worker():
            try:
                data = service.consultar()
                self.after(0, lambda: self._aplicar_data(data, on_done))
            except Exception as exc:
                self.after(0, lambda: on_error(exc) if on_error else None)

        threading.Thread(target=worker, daemon=True).start()

    def _aplicar_data(self, data, on_done):
        self.tabla.load(data)
        on_done()
```

Tambien se puede pasar una preparacion externa:

```python
host.show(
    factory,
    cache_key="reportes",
    prepare=lambda view, done, fail: view.cargar_datos_async(done, fail),
)
```

En controllers:

```python
view_class = self.views[view_name]
self.content.show(view_class, on_ready=self._set_current, cache_key=view_name)
```

Notas:

- Una vuelta del `IHLoader` actual tarda aproximadamente `1260ms` con `speed=28`.
- Si la construccion de una vista pesada congela la UI durante milisegundos, conviene retrasar esa construccion hasta despues de la primera vuelta del loader. El usuario percibe una transicion intencional en vez de un salto.
- `IHRenderHost` no vuelve asincronico el trabajo pesado de Tkinter; ordena el render para que el tiron no coincida con el arranque visual del loader y para que el swap ocurra cuando la vista ya esta montada.
- SQL, APIs, reportes y lectura pesada no deben correr en el hilo principal. Tkinter solo debe usarse para UI.

## Procesos Largos Dentro De Una Pantalla

Para acciones largas que no cambian de modulo, usar `IHBusyOverlay`.

```python
overlay = IHBusyOverlay(parent, text="Generando reporte...", block_input=True)
overlay.run(
    task=lambda: service.generar_reporte(),
    on_success=lambda result: self.mostrar_resultado(result),
    on_error=lambda exc: messagebox.showerror("Error", str(exc)),
)
```

Reglas de thread:

- El `task` no debe tocar widgets Tkinter.
- `on_success` y `on_error` corren en hilo UI.
- Para cancelacion, no matar threads a la fuerza; usar flags/tokens e ignorar resultados tardios.

## Grillas Visuales Pesadas

Para grillas de iconos o imagenes, evitar crear/destruir muchos widgets por pagina. Tkinter muestra el armado progresivo y la experiencia se siente cortada.

Patron recomendado:

1. Usar `IHImageGridTable(renderer="canvas")`.
2. Reutilizar celdas fijas en `Canvas`.
3. Actualizar con `itemconfig` y coordenadas, no recrear widgets.
4. Cachear `PhotoImage` con `image_key_getter`.
5. Mantener una pagina acotada, idealmente 8x10 o hasta 10x10.
6. Usar `IHRenderHost` para cambios de modulo completos.

Clave de cache recomendada:

```python
def image_key(item):
    return "|".join([
        item["provider"],
        item["style"],
        item["name"],
        str(size),
        color,
    ])
```

Cuando renderizar con Canvas:

- Icon browsers.
- Product pickers con imagen.
- Galerias de miniaturas.
- Selectores visuales.

Cuando seguir con widgets:

- Pocos items.
- Controles complejos por celda.
- Cada celda necesita inputs reales, menus o interacciones nativas.

## Microinteracciones

Para imitar efectos CSS en Tkinter, usar `IHAnimator`.

Patron:

```python
animator = IHAnimator(widget, duration=140, easing="ease_out")
animator.animate_to(1.0, lambda value: redraw(value))
```

Usar para:

- Hover suave.
- Pressed state.
- Cambios de inset, sombra, color o borde.
- Drawers y menus animados.

Evitar animaciones largas. En desktop interno se recomiendan duraciones de 90 a 180 ms.
