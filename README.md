# Proyecto simulador de circuitos

## Circuit simulator

## Introducción:

Este proyecto consiste en el desarrollo de una aplicación en Python llamada circuit simulator para simular circuitos eléctricos que contienen resistencias, capacitores e inductores en cualquier configuración, utilizando los conceptos de Programación Orientada a Objetos. El sistema representa componentes ideales como resistencias, capacitores, inductores, interruptores y fuentes de voltaje DC mediante clases, permitiendo organizar el programa de manera modular y reutilizable.

La simulación se basa en las leyes de Kirchhoff y en la resolución numérica de ecuaciones diferenciales para analizar cómo cambian los voltajes y corrientes a lo largo del tiempo. Además, el programa permite el estudio del comportamiento transitorio de distintos circuitos eléctricos.

## Objetivos:

### *Objetivo general:*

Desarrollar una aplicación en Python usando los conceptos de Programación Orientada a Objetos, que permitan simular y analizar el comportamiento transitorio de circuitos eléctricos RC, RL y RLC.

### *Objetivos específicos:*

- Diseñar una arquitectura orientada a objetos para representar componentes eléctricos y topologías de circuitos.
- Aplicar las leyes de Kirchhoff para obtener las ecuaciones diferenciales asociadas a cada circuito.
- Aplicar principios de Programación Orientada a Objetos como herencia, encapsulamiento, abstracción y polimorfismo en el desarrollo del sistema.

## Lógica del programa:

El simulador está estructurado en cinco módulos principales: componentes, fuentes, circuitos, simulación y visualización. Cada módulo agrupa las clases responsables de una etapa específica del proceso, desde la definición del circuito hasta la generación de gráficas.

El usuario comienza instanciando los componentes pasivos que conforman el circuito: resistencias, capacitores e inductores, junto con al menos una fuente de tensión DC y un switch. Cada componente se crea con sus parámetros físicos (resistencia en ohms, capacitancia en faradios, etc.) y el switch define el instante en que el circuito se activa. 

Con estos objetos, el usuario es libre de instanciar cualquier topología. Además, se crearon unas clases que permiten instanciar ciertas topologías predefinida, por ejemplo: RCSeries o RLCParallel, que internamente asigna los nodos a cada componente de forma automática, sin que el usuario tenga que numerarlos manualmente.

Una vez definido el circuito, se crea un Solver al que se le pasa la topología junto con los parámetros de simulación: tiempo de inicio, tiempo final e intervalo de tiempo. El solver construye internamente la matriz del sistema usando el método de Análisis Nodal Modificado (MNA), donde cada componente contribuye a la matriz según su naturaleza eléctrica a través del método stamp(). Para circuitos con capacitores o inductores, el sistema de ecuaciones se convierte en una ecuación diferencial ordinaria que el solver resuelve numéricamente paso a paso en el tiempo usando scipy. El resultado de la simulación se almacena en unas listas SimResult, que contiene los vectores de tiempo, voltaje y corriente para cada componente del circuito.

Finalmente, el Plotter recibe el SimResult y genera las gráficas de voltaje y corriente en función del tiempo para cada elemento, permitiendo visualizar el comportamiento transitorio del circuito.

## Interfaz Gráfica (GUI)

Además de la interfaz por consola, el proyecto cuenta con una interfaz gráfica desarrollada con Tkinter. La GUI no reemplaza la lógica original del simulador: funciona como una capa de presentación adicional que utiliza las mismas clases de circuitos, componentes, fuentes y motor de simulación.

La aplicación gráfica se puede ejecutar de cualquiera de estas dos formas:

```bash
python -m gui.app
```

o también:

```bash
python run_gui.py
```

Desde la interfaz gráfica el usuario puede:

- Seleccionar el tipo de circuito a simular: RC, RL, RLC en serie o paralelo, y circuito personalizado.
- Modificar los parámetros de simulación, como resistencia, capacitancia, inductancia, voltaje de la fuente, tiempo inicial, tiempo final y paso de simulación.
- Ver una vista previa del circuito seleccionado, dibujada en un panel Tkinter Canvas con símbolos eléctricos y valores actualizados.
- Ejecutar la simulación usando el motor numérico existente.
- Visualizar gráficas de voltaje y corriente generadas con matplotlib dentro de la ventana.
- Consultar un panel con el resumen de resultados de la simulación.

La interfaz por consola sigue existiendo y continúa funcionando. La GUI es únicamente una forma adicional de interactuar con el simulador.

## Diagrama UML:

``` mermaid

classDiagram
    direction TB

    class CircuitElement {
        <<abstract>>
        -int node_pos
        -int node_neg
        -str label
        +stamp(G, b, nodes) void
        +get_voltage(x, node_map) float
        +get_current(x, node_map) float
    }

    class Resistor {
        -float resistance
        +stamp(G, b, nodes) void
        +get_current(x, node_map) float
        +get_voltage(x, node_map) float
    }

    class Capacitor {
        -float capacitance
        -float initial_voltage
        +stamp(G, b, nodes, dt, Vp) void
        +get_current(x, node_map) float
        +get_voltage(x, node_map) float
    }

    class Inductor {
        -float inductance
        -float initial_current
        -int current_var_idx
        +stamp(G, b, nodes, dt, Ip) void
        +get_current(x, node_map) float
        +get_voltage(x, node_map) float
    }

    class Switch {
        -float t_close
        -bool _closed
        +is_closed(t) bool
        +stamp(G, b, nodes, t) void
        +get_current(x, node_map) float
        +get_voltage(x, node_map) float
    }

    class Source {
        <<abstract>>
        -int node_pos
        -int node_neg
        -str label
        -int current_var_idx
        +stamp(G, b, nodes) void
        +get_current(x) float
        +get_voltage(x) float
    }

    class DCVoltageSource {
        -float voltage
        +stamp(G, b, nodes) void
        +get_current(x) float
        +get_voltage(x) float
    }

    class ACVoltageSource {
        -float amplitude
        -float frequency
        -float phase
        +stamp(G, b, nodes, t) void
        +get_current(x) float
        +get_voltage(t) float
    }

    class BaseCircuit {
        <<abstract>>
        -Source source
        -Switch switch
        -list~CircuitElement~ elements
        -int node_count
        -int ground_node
        +_assign_nodes() void
        +get_elements() list
        +get_sources() list
    }

    class RCSeries {
        +_assign_nodes() void
    }

    class RCParallel {
        +_assign_nodes() void
    }

    class RLSeries {
        +_assign_nodes() void
    }

    class RLParallel {
        +_assign_nodes() void
    }

    class RLCSeries {
        +_assign_nodes() void
    }

    class RLCParallel {
        +_assign_nodes() void
    }

    class CustomCircuit {
        +resistor Resistor
        +capacitor Capacitor
        +inductor Inductor
        +_assign_nodes() void
    }

    class Solver {
        -BaseCircuit circuit
        -float t_start
        -float t_end
        -float dt
        +build_mna_matrix() tuple
        +solve() SimResult
        +solve_dc() SimResult
        +solve_transient() SimResult
        +solve_ac() SimResult
    }

    class SimResult {
        -ndarray time
        -dict voltages
        -dict currents
        +to_dataframe() DataFrame
        +summary() str
    }

    class Plotter {
        -SimResult result
        -str style
        +plot_voltage() Figure
        +plot_current() Figure
        +plot_all() Figure
        +plot_bode() Figure
        +save(path) void
    }

    namespace gui {
        class app {
            <<module>>
            +main() void
        }

        class main_window {
            <<module>>
            +create_main_window(root) MainWindow
        }

        class MainWindow {
            -SimulationRunner _simulation_runner
            -ParameterPanel _parameters
            -PlotPanel _plot_panel
            -ResultsPanel _results
            -CircuitPreviewPanel _circuit_preview
            +_simulate() void
            +_clear() void
        }

        class parameter_panel {
            <<module>>
        }

        class ParameterPanel {
            -dict _entries
            -StringVar _circuit_type
            +get_config() SimulationConfig
            +get_preview_data() dict
            +reset() void
        }

        class plot_panel {
            <<module>>
        }

        class PlotPanel {
            +show_result(result) void
            +clear() void
        }

        class results_panel {
            <<module>>
        }

        class ResultsPanel {
            +show_summary(summary) void
            +show_error(message) void
            +clear() void
        }

        class circuit_preview {
            <<module>>
        }

        class CircuitPreviewPanel {
            +show_preview(preview_data) void
            +clear() void
        }

        class simulation_runner {
            <<module>>
        }

        class SimulationRunner {
            -CircuitFactory _circuit_factory
            +run(config) SimResult
        }

        class circuit_factory {
            <<module>>
        }

        class CircuitFactory {
            +create(config) BaseCircuit
        }

        class config {
            <<module>>
        }

        class SimulationConfig {
            <<dataclass>>
            +str circuit_type
            +float resistance
            +float capacitance
            +float inductance
            +float source_voltage
            +float t_start
            +float t_end
            +float dt
        }
    }

    CircuitElement <|-- Resistor
    CircuitElement <|-- Capacitor
    CircuitElement <|-- Inductor
    CircuitElement <|-- Switch

    Source <|-- DCVoltageSource
    Source <|-- ACVoltageSource

    BaseCircuit <|-- RCSeries
    BaseCircuit <|-- RCParallel
    BaseCircuit <|-- RLSeries
    BaseCircuit <|-- RLParallel
    BaseCircuit <|-- RLCSeries
    BaseCircuit <|-- RLCParallel
    BaseCircuit <|-- CustomCircuit

    BaseCircuit *-- CircuitElement
    BaseCircuit *-- Source
    BaseCircuit *-- Switch

    app ..> main_window
    main_window ..> MainWindow
    MainWindow *-- ParameterPanel
    MainWindow *-- PlotPanel
    MainWindow *-- ResultsPanel
    MainWindow *-- CircuitPreviewPanel
    MainWindow *-- SimulationRunner
    parameter_panel ..> ParameterPanel
    plot_panel ..> PlotPanel
    results_panel ..> ResultsPanel
    circuit_preview ..> CircuitPreviewPanel
    simulation_runner ..> SimulationRunner
    circuit_factory ..> CircuitFactory
    config ..> SimulationConfig

    ParameterPanel ..> SimulationConfig
    ParameterPanel ..> CircuitFactory
    CircuitPreviewPanel ..> CircuitFactory
    SimulationRunner *-- CircuitFactory
    SimulationRunner ..> Solver
    CircuitFactory ..> SimulationConfig
    CircuitFactory ..> BaseCircuit
    CircuitFactory ..> Resistor
    CircuitFactory ..> Capacitor
    CircuitFactory ..> Inductor
    CircuitFactory ..> Switch
    CircuitFactory ..> DCVoltageSource
    PlotPanel ..> SimResult
    ResultsPanel ..> SimResult
    BaseCircuit ..> Solver
    Solver ..> SimResult
    Solver ..> BaseCircuit
    Plotter <.. SimResult

``` 

## Interfaz gráfica:

### Tkinter
Ventajas:

 - Hay mucha documentación y ejemplos.
 - Es la más simple.

Desventajas:

 - Incrustar gráficas de matplotlib dentro de la ventana requiere código adicional.
 - Visualmente es anticuada.

### PyQt6
Ventajas:

 - Interfaz visual moderna.
 - Integración nativa con matplotlib.

Desventajas:

 - Es la más compleja de aprender.

### Streamlit
Ventajas:

 - Rápida de implementar.
 - Las gráficas de matplotlib y plotly se integran de forma nativa.

Desventajas:

 - Corre en el navegador como una app web.
 - Re-ejecuta todo el script en cada interacción




# Autores:
- [Brayan Santiago Rincón Rodríguez](https://github.com/santiagorinconrodriguez)
- [Nicolás Garzón Peña ](https://github.com/yoyomasterNGP)
- [Diego Alejandro Henao Lara ](https://github.com/AlejoHenao8)
