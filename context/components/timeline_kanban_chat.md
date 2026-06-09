# Timeline, Kanban and Chat

Componentes:

- `IHTimeline`
- `IHKanbanBoard`
- `IHChatConversation`

Estos widgets viven en `TkInforHard.widgets.data` porque representan colecciones visuales reutilizables. No contienen logica de negocio de Inforhard Desk ni acoples a tickets, WhatsApp, Meta, Evolution API o proveedores especificos.

## IHTimeline

Muestra eventos ordenados cronologicamente por el campo `datetime`.

```python
from TkInforHard.widgets import IHTimeline

timeline = IHTimeline(parent)
timeline.pack(fill="both", expand=True)
timeline.load([
    {
        "title": "Evento creado",
        "description": "Se registro un evento generico.",
        "datetime": "2026-06-02T10:30:00",
        "actor": "Sistema",
        "variant": "info",
        "metadata": {"origen": "demo"},
    }
])
```

Tambien soporta `set_loading(True)` y estado vacio automatico.

## IHKanbanBoard

Muestra entidades agrupadas por estado en columnas configurables. El cambio de estado se emite por callback desde un selector liviano por card.

```python
from TkInforHard.widgets import IHKanbanBoard

board = IHKanbanBoard(
    parent,
    columns=[
        {"title": "Pendiente", "status": "pending"},
        {"title": "En proceso", "status": "in_progress"},
        {"title": "Finalizado", "status": "done"},
    ],
    on_card_click=lambda card: print(card),
    on_status_change=lambda card, status: print(card, status),
)
board.pack(fill="both", expand=True)
board.load([
    {
        "title": "Entidad reutilizable",
        "subtitle": "Puede representar cualquier dominio",
        "status": "pending",
        "priority": "media",
        "metadata": {"tipo": "generico"},
    }
])
```

Drag and drop queda como mejora futura para no agregar complejidad ni fragilidad innecesaria sobre Tkinter.

## IHChatConversation

Renderiza conversaciones genericas con mensajes entrantes y salientes, adjuntos y callbacks.

```python
from TkInforHard.widgets import IHChatConversation

chat = IHChatConversation(
    parent,
    on_send_message=lambda text: print(text),
    on_attachment_click=lambda attachment: print(attachment),
    on_message_action=lambda message, action: print(message, action),
)
chat.pack(fill="both", expand=True)
chat.load([
    {
        "author": "Operador",
        "text": "Mensaje saliente generico.",
        "datetime": "2026-06-02T11:00:00",
        "direction": "outgoing",
        "status": "sent",
        "attachments": [{"name": "archivo.pdf", "type": "document"}],
    }
])
```
