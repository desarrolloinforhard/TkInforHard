"""Provider-agnostic chat conversation component."""

from __future__ import annotations

import tkinter as tk
from typing import Callable

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore

from TkInforHard.layout import IHScrollFrame
from TkInforHard.widgets.buttons import IHButton
from TkInforHard.widgets.data._collection_helpers import current_tokens, format_datetime, metadata_text
from TkInforHard.widgets.data.empty_state import IHEmptyState
from TkInforHard.widgets.display.badge import IHBadge


class IHChatConversation(ttk.Frame):
    """Reusable conversation UI with generic messages and callbacks."""

    def __init__(
        self,
        master=None,
        messages: list[dict] | None = None,
        on_send_message: Callable[[str], None] | None = None,
        on_attachment_click: Callable[[dict], None] | None = None,
        on_message_action: Callable[[dict, str], None] | None = None,
        **kwargs,
    ):
        super().__init__(master, style="IH.Surface.TFrame", **kwargs)
        self.messages: list[dict] = []
        self.on_send_message = on_send_message
        self.on_attachment_click = on_attachment_click
        self.on_message_action = on_message_action

        self._scroll = IHScrollFrame(self)
        self._scroll.pack(fill="both", expand=True)
        self._composer = ttk.Frame(self, style="IH.Surface.TFrame", padding=(0, 10, 0, 0))
        self._composer.pack(fill="x")
        self._text_var = ttk.StringVar()
        self.entry = ttk.Entry(self._composer, textvariable=self._text_var, style="IH.TEntry")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _event: self._send())
        IHButton(self._composer, text="Enviar", variant="success", command=self._send).pack(side="left", padx=(8, 0))

        if messages is None:
            self._show_empty()
        else:
            self.load(messages)

    def load(self, messages: list[dict]) -> None:
        """Replace all messages."""

        self.messages = messages or []
        self._clear_messages()
        if not self.messages:
            self._show_empty()
            return
        for message in self.messages:
            self._render_message(message)
        self._scroll_to_end()

    def add_message(self, message: dict) -> None:
        """Append one message to the conversation."""

        if not self.messages:
            self._clear_messages()
        self.messages.append(message)
        self._render_message(message)
        self._scroll_to_end()

    def _send(self) -> None:
        text = self._text_var.get().strip()
        if not text:
            return
        self._text_var.set("")
        if self.on_send_message is not None:
            self.on_send_message(text)

    def _clear_messages(self) -> None:
        for child in self._scroll.content.winfo_children():
            child.destroy()

    def _show_empty(self) -> None:
        self._clear_messages()
        IHEmptyState(
            self._scroll.content,
            title="Sin mensajes",
            message="No hay mensajes para mostrar.",
        ).pack(fill="x")

    def _render_message(self, message: dict) -> None:
        tokens = current_tokens()
        color = tokens["color"]
        outgoing = message.get("direction") == "outgoing"

        row = ttk.Frame(self._scroll.content, style="IH.Surface.TFrame")
        row.pack(fill="x", pady=(0, 8))
        bubble = ttk.Frame(row, style="IH.Card.TFrame", padding=(10, 8))
        bubble.pack(side="right" if outgoing else "left", fill="x", padx=(80, 0) if outgoing else (0, 80))

        accent = tk.Canvas(bubble, width=4, height=52, highlightthickness=0, bg=color["surface"])
        accent.pack(side="left", fill="y", padx=(0, 8))
        accent_color = color["primary"] if outgoing else color["border"]
        accent.create_rectangle(0, 0, 4, 999, fill=accent_color, outline=accent_color)

        content = ttk.Frame(bubble, style="IH.Card.TFrame")
        content.pack(side="left", fill="both", expand=True)
        header = ttk.Frame(content, style="IH.Card.TFrame")
        header.pack(fill="x")
        ttk.Label(header, text=str(message.get("author", "")), style="IH.CardTitle.TLabel").pack(side="left")
        when = format_datetime(message.get("datetime"))
        if when:
            ttk.Label(header, text=when, style="IH.CardMuted.TLabel").pack(side="right", padx=(10, 0))

        text = message.get("text")
        if text:
            ttk.Label(content, text=str(text), style="IH.Surface.TLabel", wraplength=520).pack(anchor="w", pady=(6, 0))

        attachments = message.get("attachments") or []
        if attachments:
            attachments_frame = ttk.Frame(content, style="IH.Card.TFrame")
            attachments_frame.pack(fill="x", pady=(8, 0))
            for attachment in attachments:
                label = str(attachment.get("name", attachment.get("title", "Adjunto")))
                button = IHButton(
                    attachments_frame,
                    text=label,
                    variant="secondary",
                    outline=True,
                    command=lambda value=attachment: self._attachment_click(value),
                )
                button.pack(side="left", padx=(0, 6), pady=(0, 4))

        footer = ttk.Frame(content, style="IH.Card.TFrame")
        footer.pack(fill="x", pady=(8, 0))
        IHBadge(footer, text=str(message.get("status", "sent")), variant=self._status_variant(str(message.get("status", "sent")))).pack(side="left")
        if self.on_message_action is not None:
            IHButton(footer, text="Accion", variant="secondary", outline=True, command=lambda m=message: self.on_message_action(m, "action")).pack(side="right")

        meta = metadata_text(message.get("metadata"))
        if meta:
            ttk.Label(content, text=meta, style="IH.CardMuted.TLabel", wraplength=520).pack(anchor="w", pady=(6, 0))

    def _attachment_click(self, attachment: dict) -> None:
        if self.on_attachment_click is not None:
            self.on_attachment_click(attachment)

    def _status_variant(self, status: str) -> str:
        normalized = status.lower()
        if normalized == "read":
            return "success"
        if normalized == "delivered":
            return "info"
        if normalized == "failed":
            return "danger"
        return "secondary"

    def _scroll_to_end(self) -> None:
        self.update_idletasks()
        self._scroll.canvas.yview_moveto(1.0)
