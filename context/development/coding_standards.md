# Coding Standards

Reglas:

- Python 3.12+.
- Desarrollo siempre dentro de `.venv`.
- Docstrings en clases publicas.
- APIs semanticas.
- Componentes pequenos y componibles.
- Sin colores hardcodeados en widgets.
- Imports publicos desde `TkInforHard.widgets`.
- Todo componente, variante o estado visual nuevo debe agregarse tambien a la demo en la misma fase.

Verificacion obligatoria por fase:

```powershell
.\.venv\Scripts\python.exe -m py_compile <archivos creados>
.\.venv\Scripts\python.exe -c "from TkInforHard import *"
```

Si se agregan dependencias, actualizar `requirements.txt` e instalarlas con:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
