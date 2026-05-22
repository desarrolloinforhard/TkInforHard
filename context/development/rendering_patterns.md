# Rendering Patterns

## IHRenderHost

`IHRenderHost` es el contenedor recomendado para navegar entre pantallas pesadas.

Patron:

1. Mostrar un loader inmediatamente.
2. Construir el nuevo frame mientras el loader esta visible.
3. Hacer swap cuando el frame ya esta listo.
4. Destruir el frame anterior despues del render nuevo.

Esto evita que el usuario vea como se construyen widgets, grillas o previews de a partes.

Uso:

```python
host = IHRenderHost(parent, loading_text="Cargando modulo...")
host.show(lambda master: MyView(master))
```

En controllers:

```python
view_class = self.views[view_name]
self.content.show(view_class, on_ready=self._set_current)
```

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
