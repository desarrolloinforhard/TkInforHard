"""Minimal examples for IHTimeline, IHKanbanBoard and IHChatConversation."""

from __future__ import annotations

from datetime import datetime

from TkInforHard import IHApplication, IHChatConversation, IHConfig, IHKanbanBoard, IHTimeline
from TkInforHard.layout import IHGrid, IHPage


class CollectionsExample(IHPage):
    """Small smoke view for collection-style widgets."""

    def __init__(self, master=None):
        super().__init__(master)
        grid = IHGrid(self, columns=3)
        grid.pack(fill="both", expand=True)

        timeline = IHTimeline(grid)
        timeline.load(
            [
                {
                    "title": "Creado",
                    "description": "Evento generico inicial.",
                    "datetime": datetime(2026, 6, 2, 9, 0),
                    "actor": "Sistema",
                    "variant": "success",
                    "metadata": {"modulo": "demo"},
                },
                {
                    "title": "Actualizado",
                    "description": "Otro evento reutilizable.",
                    "datetime": datetime(2026, 6, 2, 10, 30),
                    "actor": "Usuario",
                    "variant": "info",
                },
            ]
        )
        grid.add(timeline, 0)

        board = IHKanbanBoard(
            grid,
            columns=[
                {"title": "Pendiente", "status": "pending"},
                {"title": "En proceso", "status": "in_progress"},
                {"title": "Finalizado", "status": "done"},
            ],
        )
        board.load(
            [
                {
                    "title": "Entidad movible",
                    "subtitle": "Sin dominio especifico",
                    "status": "pending",
                    "priority": "media",
                    "metadata": {"owner": "demo"},
                }
            ]
        )
        grid.add(board, 1)

        chat = IHChatConversation(grid)
        chat.load(
            [
                {
                    "author": "Cliente",
                    "text": "Mensaje entrante.",
                    "datetime": datetime(2026, 6, 2, 11, 0),
                    "direction": "incoming",
                    "status": "delivered",
                },
                {
                    "author": "Operador",
                    "text": "Respuesta saliente con adjunto.",
                    "datetime": datetime(2026, 6, 2, 11, 2),
                    "direction": "outgoing",
                    "status": "sent",
                    "attachments": [{"name": "documento.pdf", "type": "document"}],
                },
            ]
        )
        grid.add(chat, 2)


if __name__ == "__main__":
    app = IHApplication(IHConfig(title="TkInforHard Collections Example"))
    CollectionsExample(app).pack(fill="both", expand=True)
    app.mainloop()
