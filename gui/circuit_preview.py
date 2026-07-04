import tkinter as tk
from tkinter import ttk

from gui.circuit_factory import CircuitFactory


class CircuitPreviewPanel(ttk.LabelFrame):
    WIRE = "#111827"
    RESISTOR = "#dc2626"
    CAPACITOR = "#2563eb"
    INDUCTOR = "#16a34a"
    SOURCE = "#f97316"
    SWITCH = "#6b7280"
    TEXT = "#111827"
    LABEL_BG = "#ffffff"

    def __init__(self, master):
        super().__init__(master, text="Vista del circuito", padding=8)
        self._preview_data = {}
        self._canvas = tk.Canvas(
            self,
            background="#f8fafc",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
        )
        self._canvas.pack(fill="both", expand=True)
        self._canvas.bind("<Configure>", lambda _event: self._redraw())

    def show_preview(self, preview_data: dict):
        self._preview_data = preview_data
        self._redraw()

    def clear(self):
        self._preview_data = {}
        self._redraw()

    def _redraw(self):
        self._canvas.delete("all")
        width = max(self._canvas.winfo_width(), 360)
        height = max(self._canvas.winfo_height(), 260)

        margin = max(24, min(width, height) * 0.08)
        x0, y0 = margin, margin
        x1, y1 = width - margin, height - margin
        self._draw_background(width, height, margin)

        circuit_type = self._preview_data.get("circuit_type", CircuitFactory.RC_SERIES)
        draw_methods = {
            CircuitFactory.RC_SERIES: self._draw_rc_series,
            CircuitFactory.RC_PARALLEL: self._draw_rc_parallel,
            CircuitFactory.RL_SERIES: self._draw_rl_series,
            CircuitFactory.RL_PARALLEL: self._draw_rl_parallel,
            CircuitFactory.RLC_SERIES: self._draw_rlc_series,
            CircuitFactory.RLC_PARALLEL: self._draw_rlc_parallel,
            CircuitFactory.CUSTOM: self._draw_custom,
        }
        draw_methods.get(circuit_type, self._draw_unknown)(x0, y0, x1, y1)

    def _draw_background(self, width: float, height: float, margin: float):
        self._rounded_rect(margin * 0.35, margin * 0.35, width - margin * 0.35, height - margin * 0.35, 12, "#ffffff")

    def _draw_rc_series(self, x0: float, y0: float, x1: float, y1: float):
        self._draw_series(x0, y0, x1, y1, ("R", "C"))

    def _draw_rl_series(self, x0: float, y0: float, x1: float, y1: float):
        self._draw_series(x0, y0, x1, y1, ("R", "L"))

    def _draw_rlc_series(self, x0: float, y0: float, x1: float, y1: float):
        self._draw_series(x0, y0, x1, y1, ("R", "L", "C"))

    def _draw_rc_parallel(self, x0: float, y0: float, x1: float, y1: float):
        self._draw_parallel(x0, y0, x1, y1, ("R", "C"))

    def _draw_rl_parallel(self, x0: float, y0: float, x1: float, y1: float):
        self._draw_parallel(x0, y0, x1, y1, ("R", "L"))

    def _draw_rlc_parallel(self, x0: float, y0: float, x1: float, y1: float):
        self._draw_parallel(x0, y0, x1, y1, ("R", "L", "C"))

    def _draw_series(self, x0: float, y0: float, x1: float, y1: float, components: tuple[str, ...]):
        width = x1 - x0
        height = y1 - y0
        top = y0 + height * 0.30
        bottom = y0 + height * 0.76
        left = x0 + width * 0.12
        right = x1 - width * 0.08
        source_radius = min(width, height) * 0.075

        self._wire(left, top, left, bottom)
        self._source(left, (top + bottom) / 2, source_radius)
        self._wire(left, top, x0 + width * 0.25, top)

        path_start = x0 + width * 0.25
        path_end = right
        pitch = (path_end - path_start) / len(components)
        symbol_width = min(pitch * 0.46, width * 0.16)

        for index, component in enumerate(components):
            cx = path_start + pitch * (index + 0.5)
            self._wire(path_start + pitch * index, top, cx - symbol_width * 0.62, top)
            self._component(component, cx, top, symbol_width, height * 0.14, "above")
            self._wire(cx + symbol_width * 0.62, top, path_start + pitch * (index + 1), top)

        self._wire(right, top, right, bottom)
        self._wire(right, bottom, left + width * 0.35, bottom)
        self._switch(left + width * 0.25, bottom, width * 0.17)
        self._wire(left + width * 0.165, bottom, left, bottom)
        self._arrow(left + width * 0.47, bottom, left + width * 0.34, bottom)

    def _draw_parallel(self, x0: float, y0: float, x1: float, y1: float, components: tuple[str, ...]):
        width = x1 - x0
        height = y1 - y0
        top = y0 + height * 0.18
        bottom = y0 + height * 0.84
        left = x0 + width * 0.12
        bus_left = x0 + width * 0.34
        bus_right = x1 - width * 0.12
        source_radius = min(width, height) * 0.075

        self._wire(left, top, left, bottom)
        self._source(left, (top + bottom) / 2, source_radius)
        self._wire(left, top, bus_right, top)
        self._wire(bus_right, top, bus_right, bottom)
        self._wire(bus_right, bottom, left + width * 0.28, bottom)
        self._switch(left + width * 0.18, bottom, width * 0.15)
        self._wire(left + width * 0.105, bottom, left, bottom)

        branch_gap = (bottom - top) / (len(components) + 1)
        symbol_width = min(width * 0.22, (bus_right - bus_left) * 0.44)
        for index, component in enumerate(components, start=1):
            y = top + branch_gap * index
            self._junction(bus_left, y)
            self._junction(bus_right, y)
            self._wire(bus_left, y, (bus_left + bus_right) / 2 - symbol_width * 0.62, y)
            self._component(component, (bus_left + bus_right) / 2, y, symbol_width, height * 0.12, "inline")
            self._wire((bus_left + bus_right) / 2 + symbol_width * 0.62, y, bus_right, y)
            self._arrow(bus_left + width * 0.05, y, bus_left + width * 0.12, y)

        self._wire(bus_left, top, bus_left, bottom)
        self._wire(left, top, bus_left, top)
        self._wire(left, bottom, bus_left, bottom)

    def _draw_custom(self, x0: float, y0: float, x1: float, y1: float):
        width = x1 - x0
        height = y1 - y0
        top = y0 + height * 0.20
        bottom = y0 + height * 0.82
        left = x0 + width * 0.12
        node_x = x0 + width * 0.58
        right = x1 - width * 0.12
        source_radius = min(width, height) * 0.075

        self._wire(left, top, left, bottom)
        self._source(left, (top + bottom) / 2, source_radius)
        self._wire(left, top, x0 + width * 0.27, top)
        self._component("R", x0 + width * 0.42, top, width * 0.20, height * 0.13, "above")
        self._wire(x0 + width * 0.54, top, node_x, top)
        self._wire(node_x, top, node_x, bottom)
        self._wire(right, top, right, bottom)
        self._wire(right, bottom, left + width * 0.30, bottom)
        self._switch(left + width * 0.19, bottom, width * 0.15)
        self._wire(left + width * 0.115, bottom, left, bottom)
        self._junction(node_x, top)

        for component, y in (("C", y0 + height * 0.45), ("L", y0 + height * 0.65)):
            self._junction(node_x, y)
            self._junction(right, y)
            self._wire(node_x, y, x0 + width * 0.67, y)
            self._component(component, x0 + width * 0.75, y, width * 0.16, height * 0.11, "inline")
            self._wire(x0 + width * 0.84, y, right, y)
            self._arrow(node_x + width * 0.04, y, node_x + width * 0.11, y)

    def _draw_unknown(self, x0: float, y0: float, x1: float, y1: float):
        self._label((x0 + x1) / 2, (y0 + y1) / 2, "Vista no disponible", self.TEXT)

    def _component(self, component: str, x: float, y: float, width: float, height: float, label_position: str):
        if component == "R":
            self._resistor(x, y, width, height)
            text = f"R1  R = {self._value('resistance')} ohm"
            color = self.RESISTOR
        elif component == "C":
            self._capacitor(x, y, width, height)
            text = f"C1  C = {self._value('capacitance')} F"
            color = self.CAPACITOR
        elif component == "L":
            self._inductor(x, y, width, height)
            text = f"L1  L = {self._value('inductance')} H"
            color = self.INDUCTOR
        else:
            return

        label_y = y - height * 0.82 if label_position == "above" else y - height * 0.58
        self._label(x, label_y, text, color)

    def _resistor(self, x: float, y: float, width: float, height: float):
        lead = width * 0.12
        body = width - lead * 2
        step = body / 8
        amp = max(7, height * 0.22)
        start = x - width / 2 + lead
        points = [(start, y)]
        for index in range(1, 8):
            points.append((start + step * index, y - amp if index % 2 else y + amp))
        points.append((x + width / 2 - lead, y))
        self._wire(x - width / 2, y, start, y, color=self.RESISTOR)
        self._canvas.create_line(points, fill=self.RESISTOR, width=2.6, joinstyle="round", capstyle="round")
        self._wire(x + width / 2 - lead, y, x + width / 2, y, color=self.RESISTOR)

    def _capacitor(self, x: float, y: float, width: float, height: float):
        plate_gap = width * 0.10
        plate_height = max(28, height * 0.70)
        self._wire(x - width / 2, y, x - plate_gap, y, color=self.CAPACITOR)
        self._wire(x + plate_gap, y, x + width / 2, y, color=self.CAPACITOR)
        self._wire(x - plate_gap, y - plate_height / 2, x - plate_gap, y + plate_height / 2, 3, self.CAPACITOR)
        self._wire(x + plate_gap, y - plate_height / 2, x + plate_gap, y + plate_height / 2, 3, self.CAPACITOR)

    def _inductor(self, x: float, y: float, width: float, height: float):
        loops = 4
        radius = width / (loops * 2.5)
        start = x - width / 2 + radius * 0.4
        self._wire(x - width / 2, y, start, y, color=self.INDUCTOR)
        for index in range(loops):
            left = start + radius * 2 * index
            self._canvas.create_arc(
                left,
                y - radius,
                left + radius * 2,
                y + radius,
                start=0,
                extent=180,
                style=tk.ARC,
                outline=self.INDUCTOR,
                width=2.6,
            )
        end = start + radius * 2 * loops
        self._wire(end, y, x + width / 2, y, color=self.INDUCTOR)

    def _source(self, x: float, y: float, radius: float):
        radius = max(20, radius)
        self._canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            outline=self.SOURCE,
            width=2.6,
            fill="#fff7ed",
        )
        self._canvas.create_line(x, y - radius * 0.62, x, y - radius * 0.20, fill=self.SOURCE, width=2)
        self._canvas.create_line(x - radius * 0.20, y - radius * 0.41, x + radius * 0.20, y - radius * 0.41, fill=self.SOURCE, width=2)
        self._canvas.create_line(x - radius * 0.20, y + radius * 0.36, x + radius * 0.20, y + radius * 0.36, fill=self.SOURCE, width=2)
        self._label(x, y - radius - 20, f"Vs  {self._value('source_voltage')} V", self.SOURCE)

    def _switch(self, x: float, y: float, width: float):
        width = max(48, width)
        left = x - width / 2
        right = x + width / 2
        blade_end_x = right - width * 0.10
        blade_end_y = y - width * 0.30
        self._wire(left - width * 0.20, y, left, y)
        self._wire(right, y, right + width * 0.20, y)
        self._node(left, y, self.SWITCH)
        self._node(right, y, self.SWITCH)
        self._canvas.create_line(left, y, blade_end_x, blade_end_y, fill=self.SWITCH, width=2.6, capstyle="round")
        self._canvas.create_line(blade_end_x, blade_end_y, right - width * 0.08, blade_end_y, fill=self.SWITCH, width=2)
        self._label(x, y + 22, "SW1", self.SWITCH)

    def _wire(self, x1: float, y1: float, x2: float, y2: float, line_width: float = 2.2, color: str | None = None):
        self._canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill=color or self.WIRE,
            width=line_width,
            capstyle="round",
            joinstyle="round",
        )

    def _arrow(self, x1: float, y1: float, x2: float, y2: float):
        self._canvas.create_line(
            x1,
            y1,
            x2,
            y2,
            fill="#475569",
            width=1.8,
            arrow=tk.LAST,
            arrowshape=(9, 11, 4),
        )
        self._canvas.create_text((x1 + x2) / 2, y1 - 10, text="i", fill="#475569", font=("Segoe UI", 8, "italic"))

    def _junction(self, x: float, y: float):
        self._node(x, y, self.WIRE)

    def _node(self, x: float, y: float, color: str):
        self._canvas.create_oval(x - 3.2, y - 3.2, x + 3.2, y + 3.2, fill=color, outline=color)

    def _label(self, x: float, y: float, text: str, color: str):
        label = self._canvas.create_text(x, y, text=text, fill=color, font=("Segoe UI", 8, "bold"))
        bbox = self._canvas.bbox(label)
        if bbox is None:
            return
        pad_x = 6
        pad_y = 3
        label_background = self._rounded_rect(
            bbox[0] - pad_x,
            bbox[1] - pad_y,
            bbox[2] + pad_x,
            bbox[3] + pad_y,
            6,
            self.LABEL_BG,
            "#e2e8f0",
        )
        for item in label_background:
            self._canvas.tag_lower(item, label)

    def _rounded_rect(
        self,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        radius: float,
        fill: str,
        outline: str = "#e2e8f0",
    ):
        radius = min(radius, abs(x1 - x0) / 2, abs(y1 - y0) / 2)
        items = [
            self._canvas.create_rectangle(x0 + radius, y0, x1 - radius, y1, fill=fill, outline=fill),
            self._canvas.create_rectangle(x0, y0 + radius, x1, y1 - radius, fill=fill, outline=fill),
            self._canvas.create_arc(x0, y0, x0 + radius * 2, y0 + radius * 2, start=90, extent=90, fill=fill, outline=fill),
            self._canvas.create_arc(x1 - radius * 2, y0, x1, y0 + radius * 2, start=0, extent=90, fill=fill, outline=fill),
            self._canvas.create_arc(x1 - radius * 2, y1 - radius * 2, x1, y1, start=270, extent=90, fill=fill, outline=fill),
            self._canvas.create_arc(x0, y1 - radius * 2, x0 + radius * 2, y1, start=180, extent=90, fill=fill, outline=fill),
        ]
        if outline:
            items.extend(
                [
                    self._canvas.create_line(x0 + radius, y0, x1 - radius, y0, fill=outline),
                    self._canvas.create_line(x1, y0 + radius, x1, y1 - radius, fill=outline),
                    self._canvas.create_line(x0 + radius, y1, x1 - radius, y1, fill=outline),
                    self._canvas.create_line(x0, y0 + radius, x0, y1 - radius, fill=outline),
                ]
            )
        return tuple(items)

    def _value(self, key: str) -> str:
        value = self._preview_data.get(key, "")
        return value if str(value).strip() else "?"
