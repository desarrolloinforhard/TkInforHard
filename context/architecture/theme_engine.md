# Theme Engine

`ThemeManager` es el punto central para aplicar themes.

Responsabilidades:

- Traducir `inforhard_dark` e `inforhard_light` a themes base de `ttkbootstrap`.
- Registrar estilos `IH.*`.
- Exponer tokens activos.
- Alternar theme con `toggle_theme()`.

Los widgets consumen estilos registrados por `TkInforHard/theme/styles.py`.

