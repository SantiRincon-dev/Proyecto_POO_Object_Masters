import tkinter as tk
from tkinter import ttk


class ResultsPanel(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Resultados", padding=8)
        self._text = tk.Text(self, height=12, wrap="none")
        y_scroll = ttk.Scrollbar(self, orient="vertical", command=self._text.yview)
        x_scroll = ttk.Scrollbar(self, orient="horizontal", command=self._text.xview)
        self._text.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self._text.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def show_summary(self, summary: str):
        self._replace_text(summary)

    def show_error(self, message: str):
        self._replace_text(f"Error:\n{message}")

    def clear(self):
        self._replace_text("")

    def _replace_text(self, value: str):
        self._text.configure(state="normal")
        self._text.delete("1.0", tk.END)
        self._text.insert(tk.END, value)
        self._text.configure(state="disabled")

