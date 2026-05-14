# Architecture Overview

TkInforHard sigue una arquitectura de componentes. Cada pantalla futura debe componerse con widgets `IH*`, layout primitives y servicios de theme centralizados.

Principios:

- Component-Based UI Architecture.
- Design Token System.
- Composite Widget Pattern.
- Separacion visual/logica.
- Reutilizacion total de componentes.
- Dark mode y light mode.
- Theme Engine centralizado.

Restriccion de calidad por fase:

```powershell
.\.venv\Scripts\python.exe -m py_compile <archivos creados>
.\.venv\Scripts\python.exe -c "from TkInforHard import *"
```

Si una fase falla, no se avanza hasta corregirla.

Todo desarrollo local debe ejecutarse dentro del entorno virtual `.venv` del proyecto.
