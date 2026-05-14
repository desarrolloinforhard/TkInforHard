"""Toast component."""

try:
    import ttkbootstrap as ttk
except Exception:  # pragma: no cover
    from tkinter import ttk  # type: ignore


class IHToast(ttk.Toplevel):
    """Small transient notification window."""

    def __init__(self, master=None, message: str = "", duration: int = 3000, **kwargs):
        super().__init__(master, **kwargs)
        self.overrideredirect(True)
        self.configure(padx=14, pady=10)
        ttk.Label(self, text=message, style="IH.Surface.TLabel").pack()
        self.after(duration, self.destroy)

