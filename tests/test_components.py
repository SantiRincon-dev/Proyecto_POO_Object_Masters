# tests/test_components.py
import pytest
import numpy as np
from components import Resistor, Capacitor, Inductor, Switch


class TestResistor:
    def test_instanciacion_correcta(self):
        r = Resistor(resistance=1000, label="R1")
        assert r.resistance == 1000
        assert r.label == "R1"
        assert r.node_pos == 0
        assert r.node_neg == 0

    def test_conductancia(self):
        r = Resistor(resistance=1000)
        assert r.conductance == pytest.approx(0.001)

    def test_resistencia_negativa_lanza_error(self):
        with pytest.raises(ValueError):
            Resistor(resistance=-100)

    def test_resistencia_cero_lanza_error(self):
        with pytest.raises(ValueError):
            Resistor(resistance=0)

    def test_stamp_nodo_tierra(self):
        """Resistor entre nodo 1 y tierra — solo estampa G[0][0]"""
        r = Resistor(resistance=1000)
        r.node_pos = 1
        r.node_neg = 0
        G = np.zeros((2, 2))
        b = np.zeros(2)
        node_map = {1: 0, 0: None}
        r.stamp(G, b, node_map)
        assert G[0][0] == pytest.approx(0.001)

    def test_stamp_dos_nodos(self):
        """Resistor entre nodo 1 y nodo 2"""
        r = Resistor(resistance=1000)
        r.node_pos = 1
        r.node_neg = 2
        G = np.zeros((3, 3))
        b = np.zeros(3)
        node_map = {1: 0, 2: 1, 0: None}
        r.stamp(G, b, node_map)
        assert G[0][0] == pytest.approx(0.001)
        assert G[1][1] == pytest.approx(0.001)
        assert G[0][1] == pytest.approx(-0.001)
        assert G[1][0] == pytest.approx(-0.001)

    def test_get_voltage(self):
        r = Resistor(resistance=1000)
        r.node_pos = 1
        r.node_neg = 0
        node_map = {1: 0, 0: None}
        x = np.array([5.0, -0.005])
        assert r.get_voltage(x, node_map) == pytest.approx(5.0)

    def test_get_current(self):
        r = Resistor(resistance=1000)
        r.node_pos = 1
        r.node_neg = 0
        node_map = {1: 0, 0: None}
        x = np.array([5.0, -0.005])
        assert r.get_current(x, node_map) == pytest.approx(0.005)


class TestCapacitor:
    def test_instanciacion_correcta(self):
        c = Capacitor(capacitance=1e-6, initial_voltage=2.0, label="C1")
        assert c.capacitance == 1e-6
        assert c.initial_voltage == 2.0
        assert c.V_prev == 2.0

    def test_capacitancia_negativa_lanza_error(self):
        with pytest.raises(ValueError):
            Capacitor(capacitance=-1e-6)

    def test_reset(self):
        c = Capacitor(capacitance=1e-6, initial_voltage=3.0)
        c.V_prev = 5.0
        c.reset()
        assert c.V_prev == 3.0

    def test_stamp_agrega_geq(self):
        c = Capacitor(capacitance=1e-6)
        c.node_pos = 1
        c.node_neg = 0
        G = np.zeros((2, 2))
        b = np.zeros(2)
        node_map = {1: 0, 0: None}
        dt = 1e-6
        c.stamp(G, b, node_map, dt=dt)
        geq = 1e-6 / 1e-6  # C/dt = 1.0
        assert G[0][0] == pytest.approx(geq)

    def test_stamp_sin_dt_lanza_error(self):
        c = Capacitor(capacitance=1e-6)
        c.node_pos = 1
        c.node_neg = 0
        G = np.zeros((2, 2))
        b = np.zeros(2)
        node_map = {1: 0, 0: None}
        with pytest.raises(ValueError):
            c.stamp(G, b, node_map)

    def test_update_state(self):
        c = Capacitor(capacitance=1e-6)
        c.node_pos = 1
        c.node_neg = 0
        node_map = {1: 0, 0: None}
        x = np.array([3.0, -3e-6])
        c.update_state(x, node_map)
        assert c.V_prev == pytest.approx(3.0)


class TestInductor:
    def test_instanciacion_correcta(self):
        l = Inductor(inductance=0.01, initial_current=1.0, label="L1")
        assert l.inductance == 0.01
        assert l.initial_current == 1.0
        assert l.I_prev == 1.0

    def test_inductancia_negativa_lanza_error(self):
        with pytest.raises(ValueError):
            Inductor(inductance=-0.01)

    def test_reset(self):
        l = Inductor(inductance=0.01, initial_current=2.0)
        l.I_prev = 5.0
        l.reset()
        assert l.I_prev == 2.0

    def test_stamp_sin_current_var_idx_lanza_error(self):
        l = Inductor(inductance=0.01)
        l.node_pos = 1
        l.node_neg = 0
        G = np.zeros((3, 3))
        b = np.zeros(3)
        node_map = {1: 0, 0: None}
        with pytest.raises(RuntimeError):
            l.stamp(G, b, node_map, dt=1e-6)

    def test_get_current_con_idx(self):
        l = Inductor(inductance=0.01)
        l.node_pos = 1
        l.node_neg = 0
        l.current_var_idx = 1
        node_map = {1: 0, 0: None}
        x = np.array([5.0, 0.025])
        assert l.get_current(x, node_map) == pytest.approx(0.025)


class TestSwitch:
    def test_abierto_antes_de_t_close(self):
        sw = Switch(t_close=0.001)
        assert sw.is_closed(0.0) == False
        assert sw.is_closed(0.0009) == False

    def test_cerrado_en_t_close(self):
        sw = Switch(t_close=0.001)
        assert sw.is_closed(0.001) == True
        assert sw.is_closed(0.002) == True

    def test_reset(self):
        sw = Switch(t_close=0.001)
        sw.is_closed(0.002)
        sw.reset()
        assert sw.closed == False

    def test_stamp_abierto_no_modifica_G(self):
        sw = Switch(t_close=0.001)
        G = np.zeros((2, 2))
        b = np.zeros(2)
        node_map = {1: 0, 0: None}
        sw.node_pos = 1
        sw.node_neg = 0
        sw.stamp(G, b, node_map, t=0.0)
        assert np.all(G == 0)

    def test_t_close_negativo_lanza_error(self):
        with pytest.raises(ValueError):
            Switch(t_close=-1.0)
