# Colors

La paleta se define en `TkInforHard/theme/palette.py`.

Colores base:

- Verde corporativo light: `PRIMARY = "#008A46"`.
- Verde hover light: `PRIMARY_HOVER = "#00A653"`.
- Verde UI suave: `PRIMARY_SOFT = "#33B56F"`.
- Verde corporativo dark: `DARK_PRIMARY = "#00A653"`.
- Verde hover dark: `DARK_PRIMARY_HOVER = "#20C76F"`.
- Fondo light: `LIGHT_BACKGROUND = "#F5F7F6"`.
- Cards light: `LIGHT_SURFACE = "#FFFFFF"`.
- Bordes light: `LIGHT_BORDER = "#D9E2DD"`.
- Texto light: `LIGHT_TEXT = "#1F2A24"`.
- Texto secundario light: `LIGHT_MUTED = "#5B6B63"`.
- Fondo dark: `DARK_BACKGROUND = "#0E1512"`.
- Fondo secundario dark: `DARK_SURFACE_ALT = "#151F1A"`.
- Cards dark: `DARK_SURFACE = "#1C2721"`.
- Bordes dark: `DARK_BORDER = "#2E4037"`.
- Texto dark: `DARK_TEXT = "#E8F1EC"`.
- Texto secundario dark: `DARK_MUTED = "#AAB8B0"`.
- Semanticos: `SUCCESS`, `INFO`, `WARNING`, `DANGER`.

Regla: no hardcodear colores dentro de widgets. Toda decision visual debe salir de tokens, estilos o theme manager.

## Modo Claro

| Uso | Hex |
| --- | --- |
| Primario | `#008A46` |
| Hover primario | `#00A653` |
| Verde suave | `#33B56F` |
| Fondo principal | `#F5F7F6` |
| Fondo cards | `#FFFFFF` |
| Bordes | `#D9E2DD` |
| Texto principal | `#1F2A24` |
| Texto secundario | `#5B6B63` |
| Exito | `#22C55E` |
| Advertencia | `#F59E0B` |
| Error | `#EF4444` |

## Modo Oscuro

| Uso | Hex |
| --- | --- |
| Primario | `#00A653` |
| Hover primario | `#20C76F` |
| Fondo principal | `#0E1512` |
| Fondo secundario | `#151F1A` |
| Cards | `#1C2721` |
| Bordes | `#2E4037` |
| Texto principal | `#E8F1EC` |
| Texto secundario | `#AAB8B0` |
| Exito | `#22C55E` |
| Advertencia | `#FBBF24` |
| Error | `#F87171` |
