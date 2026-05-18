# TkInforHard

TkInforHard es una libreria profesional de componentes UI para Python desktop basada en `tkinter`, `ttk` y `ttkbootstrap`.

El objetivo no es crear un sistema final, sino un mini framework frontend desktop reutilizable para ERP, POS, verificadores de precios, totens publicitarios, configuradores y herramientas tecnicas internas.

## Instalacion

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Requiere Python 3.12+.

## Filosofia

Los proyectos consumidores no deben usar widgets base directamente para construir pantallas finales:

```python
from TkInforHard.widgets import IHButton

IHButton(text="Guardar", variant="success", outline=False, rounded=True)
```

La libreria encapsula `ttkbootstrap` y centraliza decisiones visuales en `TkInforHard/theme/`.

## Estructura

```text
TkInforHard/
  core/       app, config, constantes y enums
  theme/      tokens, paleta, tipografia, spacing, radius, themes y manager
  widgets/    componentes reutilizables por dominio
  layout/     page, containers, scrollframe, grid y responsive
  utils/      helpers transversales
  assets/     logo, iconos y fuentes
demo/         showcase app que consume solo TkInforHard
context/      memoria tecnica permanente del framework
```

## Themes

Incluye dos themes semanticos:

- `inforhard_dark`
- `inforhard_light`

Uso:

```python
from TkInforHard.core import IHApplication, IHConfig

app = IHApplication(IHConfig(theme="inforhard_dark"))
app.toggle_theme()
app.mainloop()
```

## Demo

```powershell
.\.venv\Scripts\Activate.ps1
python demo/main.py
```

La demo muestra botones, cards, inputs, tablas, navegacion y feedback usando componentes `IH*`.

## Referencia de Widgets

La guia completa de API, parametros y ejemplos de uso vive en:

- `context/components/widget_reference.md`

## Screenshots

Los screenshots se agregaran en futuras iteraciones:

- `docs/screenshots/showcase-dark.png`
- `docs/screenshots/showcase-light.png`

## Crear nuevos widgets

1. Crear el componente dentro de la categoria correspondiente en `TkInforHard/widgets/`.
2. Usar tokens y estilos centralizados; no hardcodear colores en la API del widget.
3. Exportar el componente en el `__init__.py` de su categoria y en `TkInforHard/widgets/__init__.py`.
4. Agregar ejemplo en la demo.
5. Documentar en `context/components/`.
6. Registrar el cambio en `context/changelog/CHANGELOG.md`.
7. Ejecutar:

```bash
.\.venv\Scripts\python.exe -m py_compile <archivos creados>
.\.venv\Scripts\python.exe -c "from TkInforHard import *"
```

No se avanza de fase si hay errores.
