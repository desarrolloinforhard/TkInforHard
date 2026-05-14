"""Feedback showcase view."""

from TkInforHard.layout import IHPage, IHStack
from TkInforHard.widgets import IHAlert, IHLoading, IHProgress, IHSectionHeader


class FeedbackView(IHPage):
    """Shows feedback components."""

    def __init__(self, master=None):
        super().__init__(master)
        IHSectionHeader(self, title="Feedback", subtitle="Mensajes, progreso y estados de carga.").pack(fill="x")
        stack = IHStack(self)
        stack.pack(fill="x", pady=16)
        stack.add(IHAlert(stack, title="Operacion exitosa", message="Los datos fueron sincronizados.", variant="success"))
        stack.add(IHAlert(stack, title="Atencion", message="Revisar la conexion antes de continuar.", variant="warning"))
        progress = IHProgress(stack, label="Carga de precios", value=64)
        stack.add(progress)
        loading = IHLoading(stack, text="Procesando informacion...")
        stack.add(loading)

