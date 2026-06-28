# tests/test_circuits.py
import pytest
from components import Resistor, Capacitor, Inductor, Switch
from sources import DCVoltageSource
from circuits import (
    RCSeries,
    RCParallel,
    RLSeries,
    RLParallel,
    RLCSeries,
    RLCParallel,
)


def make_components():
    """Fixture auxiliar — crea componentes base para los tests."""
    r = Resistor(resistance=1000, label="R1")
    c = Capacitor(capacitance=1e-6, label="C1")
    l = Inductor(inductance=0.01, label="L1")
    src = DCVoltageSource(voltage=5.0, label="Vs")
    sw = Switch(t_close=0.0, label="SW1")
    return r, c, l, src, sw


class TestRCSeries:
    def test_instanciacion(self):
        r, c, l, src, sw = make_components()
        circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
        assert circuit is not None

    def test_node_count(self):
        r, c, l, src, sw = make_components()
        circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
        assert circuit.node_count == 3

    def test_nodos_asignados_correctamente(self):
        r, c, l, src, sw = make_components()
        circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
        assert circuit.source.node_pos == 1
        assert circuit.source.node_neg == 0
        assert circuit.switch.node_pos == 2
        assert circuit.switch.node_neg == 1
        assert r.node_pos == 3
        assert r.node_neg == 2
        assert c.node_pos == 3
        assert c.node_neg == 0

    def test_get_elements_no_incluye_switch(self):
        r, c, l, src, sw = make_components()
        circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
        elements = circuit.get_elements()
        assert sw not in elements

    def test_get_all_no_incluye_switch(self):
        r, c, l, src, sw = make_components()
        circuit = RCSeries(resistor=r, capacitor=c, source=src, switch=sw)
        all_e = circuit.get_all()
        assert sw not in all_e
        assert src in all_e

    def test_tipo_incorrecto_lanza_error(self):
        r, c, l, src, sw = make_components()
        with pytest.raises(TypeError):
            RCSeries(resistor=c, capacitor=c, source=src, switch=sw)


class TestRCParallel:
    def test_node_count(self):
        r, c, l, src, sw = make_components()
        circuit = RCParallel(resistor=r, capacitor=c, source=src, switch=sw)
        assert circuit.node_count == 2

    def test_nodos_r_y_c_iguales(self):
        r, c, l, src, sw = make_components()
        circuit = RCParallel(resistor=r, capacitor=c, source=src, switch=sw)
        assert r.node_pos == c.node_pos
        assert r.node_neg == c.node_neg


class TestRLSeries:
    def test_node_count(self):
        r, c, l, src, sw = make_components()
        circuit = RLSeries(resistor=r, inductor=l, source=src, switch=sw)
        assert circuit.node_count == 3

    def test_nodos_asignados(self):
        r, c, l, src, sw = make_components()
        circuit = RLSeries(resistor=r, inductor=l, source=src, switch=sw)
        assert r.node_pos == 3
        assert r.node_neg == 2
        assert l.node_pos == 3
        assert l.node_neg == 0

    def test_tipo_incorrecto_lanza_error(self):
        r, c, l, src, sw = make_components()
        with pytest.raises(TypeError):
            RLSeries(resistor=l, inductor=l, source=src, switch=sw)


class TestRLParallel:
    def test_node_count(self):
        r, c, l, src, sw = make_components()
        circuit = RLParallel(resistor=r, inductor=l, source=src, switch=sw)
        assert circuit.node_count == 2

    def test_nodos_r_y_l_iguales(self):
        r, c, l, src, sw = make_components()
        circuit = RLParallel(resistor=r, inductor=l, source=src, switch=sw)
        assert r.node_pos == l.node_pos
        assert r.node_neg == l.node_neg


class TestRLCSeries:
    def test_node_count(self):
        r, c, l, src, sw = make_components()
        circuit = RLCSeries(resistor=r, inductor=l, capacitor=c, source=src, switch=sw)
        assert circuit.node_count == 4

    def test_nodos_asignados(self):
        r, c, l, src, sw = make_components()
        circuit = RLCSeries(resistor=r, inductor=l, capacitor=c, source=src, switch=sw)
        assert r.node_pos == 3
        assert r.node_neg == 2
        assert l.node_pos == 4
        assert l.node_neg == 3
        assert c.node_pos == 4
        assert c.node_neg == 0

    def test_get_elements_contiene_r_l_c(self):
        r, c, l, src, sw = make_components()
        circuit = RLCSeries(resistor=r, inductor=l, capacitor=c, source=src, switch=sw)
        elements = circuit.get_elements()
        assert r in elements
        assert l in elements
        assert c in elements


class TestRLCParallel:
    def test_node_count(self):
        r, c, l, src, sw = make_components()
        circuit = RLCParallel(
            resistor=r, inductor=l, capacitor=c, source=src, switch=sw
        )
        assert circuit.node_count == 2

    def test_nodos_r_l_c_iguales(self):
        r, c, l, src, sw = make_components()
        circuit = RLCParallel(
            resistor=r, inductor=l, capacitor=c, source=src, switch=sw
        )
        assert r.node_pos == l.node_pos == c.node_pos
        assert r.node_neg == l.node_neg == c.node_neg

    def test_tipo_incorrecto_lanza_error(self):
        r, c, l, src, sw = make_components()
        with pytest.raises(TypeError):
            RLCParallel(resistor=r, inductor=r, capacitor=c, source=src, switch=sw)
