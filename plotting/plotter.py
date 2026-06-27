# plotting/plotter.py
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from simulation.sim_result import SimResult


class Plotter:
    """
    Genera gráficas de voltaje y corriente a partir de un SimResult.

    Parámetros:
        result : SimResult — resultados de la simulación
        style  : str       — estilo de matplotlib (default: 'seaborn-v0_8')
    """

    STYLES = ["seaborn-v0_8", "ggplot", "bmh", "classic"]

    def __init__(self, result: SimResult, style: str = "seaborn-v0_8"):
        if not isinstance(result, SimResult):
            raise TypeError(f"result debe ser un SimResult, se recibió: {type(result)}")
        if style not in self.STYLES:
            raise ValueError(f"Estilo no válido. Opciones: {self.STYLES}")

        self._result = result
        self._style = style
        plt.style.use(style)

    # ── Propiedades ──────────────────────────────────────────────

    @property
    def result(self) -> SimResult:
        return self._result

    @property
    def style(self) -> str:
        return self._style

    # ── Métodos privados ──────────────────────────────────────────

    def _format_time_axis(self, ax: plt.Axes) -> None:
        """
        Formatea el eje de tiempo con las unidades más legibles
        dependiendo del rango de la simulación.
        """
        t_end = self._result.t_end

        if t_end < 1e-3:
            scale, unit = 1e6, "μs"
        elif t_end < 1:
            scale, unit = 1e3, "ms"
        else:
            scale, unit = 1, "s"

        ticks = ax.get_xticks()
        ax.set_xticklabels([f"{t * scale:.1f}" for t in ticks])
        ax.set_xlabel(f"Tiempo [{unit}]")

    def _get_labels_without_switch(self) -> list:
        """Retorna todas las etiquetas — el switch ya no viene en los resultados."""
        return self._result.labels

    # ── Métodos públicos ──────────────────────────────────────────

    def plot_voltage(self, show: bool = True) -> plt.Figure:
        """
        Grafica el voltaje en función del tiempo para cada elemento.

        Parámetros:
            show : bool — si True muestra la figura inmediatamente

        Retorna:
            matplotlib.figure.Figure
        """
        labels = self._get_labels_without_switch()
        fig, ax = plt.subplots(figsize=(10, 5))

        for label in labels:
            ax.plot(
                self._result.time,
                self._result.get_voltage(label),
                label=label,
                linewidth=2,
            )

        ax.set_ylabel("Voltaje [V]")
        ax.set_title("Voltaje vs Tiempo")
        ax.legend()
        ax.grid(True)
        self._format_time_axis(ax)
        fig.tight_layout()

        if show:
            plt.show()

        return fig

    def plot_current(self, show: bool = True) -> plt.Figure:
        """
        Grafica la corriente en función del tiempo para cada elemento.

        Parámetros:
            show : bool — si True muestra la figura inmediatamente

        Retorna:
            matplotlib.figure.Figure
        """
        labels = self._get_labels_without_switch()
        fig, ax = plt.subplots(figsize=(10, 5))

        for label in labels:
            ax.plot(
                self._result.time,
                self._result.get_current(label),
                label=label,
                linewidth=2,
            )

        ax.set_ylabel("Corriente [A]")
        ax.set_title("Corriente vs Tiempo")
        ax.legend()
        ax.grid(True)
        self._format_time_axis(ax)
        fig.tight_layout()

        if show:
            plt.show()

        return fig

    def plot_all(self, show: bool = True) -> plt.Figure:
        """
        Grafica voltaje y corriente de cada elemento en subplots
        individuales organizados en una grilla.

        Cada elemento ocupa una fila con dos columnas:
        voltaje a la izquierda, corriente a la derecha.

        Parámetros:
            show : bool — si True muestra la figura inmediatamente

        Retorna:
            matplotlib.figure.Figure
        """
        labels = self._get_labels_without_switch()
        n = len(labels)

        fig = plt.figure(figsize=(14, 4 * n))
        gs = gridspec.GridSpec(n, 2, figure=fig)

        for row, label in enumerate(labels):
            ax_v = fig.add_subplot(gs[row, 0])
            ax_i = fig.add_subplot(gs[row, 1])

            ax_v.plot(
                self._result.time,
                self._result.get_voltage(label),
                color="steelblue",
                linewidth=2,
            )
            ax_v.set_ylabel("Voltaje [V]")
            ax_v.set_title(f"{label} — Voltaje")
            ax_v.grid(True)
            self._format_time_axis(ax_v)

            ax_i.plot(
                self._result.time,
                self._result.get_current(label),
                color="coral",
                linewidth=2,
            )
            ax_i.set_ylabel("Corriente [A]")
            ax_i.set_title(f"{label} — Corriente")
            ax_i.grid(True)
            self._format_time_axis(ax_i)

        fig.suptitle("Resultados de simulación", fontsize=14, y=1.01)
        fig.tight_layout()

        if show:
            plt.show()

        return fig

    def plot_power(self, show: bool = True) -> plt.Figure:
        """
        Grafica la potencia instantánea P = V * I
        en función del tiempo para cada elemento.

        Parámetros:
            show : bool — si True muestra la figura inmediatamente

        Retorna:
            matplotlib.figure.Figure
        """
        labels = self._get_labels_without_switch()
        fig, ax = plt.subplots(figsize=(10, 5))

        for label in labels:
            ax.plot(
                self._result.time,
                self._result.get_power(label),
                label=label,
                linewidth=2,
            )

        ax.set_ylabel("Potencia [W]")
        ax.set_title("Potencia vs Tiempo")
        ax.legend()
        ax.grid(True)
        self._format_time_axis(ax)
        fig.tight_layout()

        if show:
            plt.show()

        return fig

    def save(self, path: str, dpi: int = 150) -> None:
        """
        Guarda la gráfica completa (plot_all) en un archivo.

        Parámetros:
            path : str — ruta del archivo (ej: 'resultados/rc_serie.png')
            dpi  : int — resolución de la imagen
        """
        fig = self.plot_all(show=False)
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)
        print(f"Gráfica guardada en: {path}")

    # ── Representación ────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"Plotter [estilo={self._style}, elementos={self._result.labels}]"
