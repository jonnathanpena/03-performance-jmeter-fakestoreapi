## Why

El plan de prueba JMeter valida el criterio de >= 20 TPS mediante un `ConstantThroughputTimer`, pero carece de un listener que muestre el throughput real en tiempo de ejecución. Sin este listener, no existe evidencia visual del TPS alcanzado durante la sesión GUI ni en los reportes generados.

## What Changes

- Agregar un listener de tipo **Transactions per Second** al archivo `jmeter/test-plan.jmx`.
- Configurar el listener para registrar resultados en un archivo de salida dentro de `results/`, alineado con la salida del `Summary Report` ya existente.
- Habilitar el listener tanto para ejecución GUI (visualización en tiempo real) como CLI (escritura a archivo `.jtl`).

## Capabilities

### New Capabilities

- `tps-listener`: Listener JMeter que captura y muestra el throughput real (TPS) durante la ejecución de la prueba de carga, permitiendo verificar el criterio de >= 20 TPS con evidencia visual y en archivo.

### Modified Capabilities

## Impact

- `jmeter/test-plan.jmx` — se agrega un nuevo elemento `ResultCollector` con `guiclass` de reporte de throughput dentro del bloque de listeners del plan de prueba.
- Sin impacto en assertions, thread group ni parametrización CSV existente.
- Sin dependencias nuevas de plugins si se usa el `Aggregate Report` nativo; se requiere JMeter Plugins Manager si se opta por `jp@gc - Transactions per Second`.
