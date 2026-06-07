## Context

El plan de prueba `jmeter/test-plan.jmx` ya cuenta con un `ConstantThroughputTimer` configurado a 1200 req/min (20 TPS objetivo) y un listener `Summary Report` que escribe resultados agregados en `results/results.jtl`. Sin embargo, el `Summary Report` solo expone el throughput como un valor escalar acumulado, sin representación temporal. Esto impide verificar visualmente si se alcanzó el umbral de 20 TPS durante la ejecución.

La necesidad es agregar un listener que capture el TPS de forma continua (serie de tiempo) y genere evidencia verificable, tanto en sesión GUI como en ejecución CLI.

## Goals / Non-Goals

**Goals:**
- Agregar un listener de TPS al archivo `jmeter/test-plan.jmx` al mismo nivel que el `Summary Report` existente.
- Proveer evidencia del throughput real alcanzado durante la prueba de carga.
- Mantener compatibilidad con ejecución CLI (`jmeter -n -t ...`) sin romper el flujo existente.

**Non-Goals:**
- Modificar Thread Group, assertions, CSV DataSet o el `ConstantThroughputTimer`.
- Reemplazar el `Summary Report` existente.
- Introducir cambios en el proceso de análisis de resultados (Ejercicio 2).

## Decisions

### Decisión 1: Tipo de listener — Plugin `jp@gc - Transactions per Second` vs. `Aggregate Report` nativo

**Elección: `Aggregate Report` nativo (`StatVisualizer`)**

Razones:
- El stack del proyecto no declara el JMeter Plugins Manager como dependencia. Instalar el plugin `jp@gc - Transactions per Second` requeriría añadir una dependencia externa, pasos de instalación adicionales y condicionaría la ejecución en entornos CI que no tengan el plugin disponible.
- El `Aggregate Report` es parte del JMeter base (5.6.x) y no requiere configuración adicional.
- El criterio de aceptación pide evidencia del TPS alcanzado, no necesariamente una gráfica de serie de tiempo. El `Aggregate Report` expone la columna **Throughput (req/s)** suficiente para verificar el umbral de 20 TPS.

Alternativa descartada: `jp@gc - Transactions per Second` ofrece una gráfica de TPS en tiempo real más expresiva, pero introduce una dependencia de plugin (JMeter Plugins Manager + `jmeter-plugins-graphs-basic`) que no está en el stack actual.

### Decisión 2: Archivo de salida — separado vs. compartido con `results.jtl`

**Elección: Archivo separado `results/tps-report.jtl`**

Razones:
- Mantener la separación de concerns: `results.jtl` ya es consumido por el HTML report (`-e -o results/html-report/`). Agregar un segundo listener apuntando al mismo archivo puede generar conflictos de escritura concurrente.
- Un archivo separado permite distinguir claramente la fuente de datos del `Aggregate Report` nuevo.
- En ejecución CLI, si no se desea escribir el segundo archivo, basta con dejar el `filename` vacío o comentarlo; la convención ya establecida en el proyecto es tener el campo presente pero configurable.

Alternativa descartada: Reusar `results/results.jtl` evitaría un segundo archivo, pero introduce riesgo de corrupción cuando ambos listeners escriben al mismo path en paralelo.

### Decisión 3: Ubicación en el JMX — nivel Test Plan vs. dentro del Thread Group

**Elección: Nivel Test Plan (mismo nivel que `Summary Report` existente)**

Razones:
- El `Summary Report` ya está al nivel del Test Plan (fuera del `<hashTree>` del Thread Group). Colocar el nuevo listener al mismo nivel mantiene consistencia estructural.
- Los listeners al nivel del Test Plan reciben eventos de todos los Thread Groups, lo que es el comportamiento esperado.

## Risks / Trade-offs

- **Doble escritura a disco** → Dos `ResultCollector` activos incrementan ligeramente el I/O durante la prueba. Mitigación: los archivos `.jtl` son texto plano secuencial; el impacto es despreciable para 40 hilos.
- **`results/tps-report.jtl` no existe al inicio de la prueba** → JMeter crea el archivo automáticamente si el directorio `results/` existe. Si `results/` no existe, la ejecución lanza un error silencioso. Mitigación: documentar en README que se debe crear `results/` antes de la ejecución CLI (ya mencionado en `readme.txt`).
- **`Aggregate Report` no muestra serie de tiempo** → El throughput es un valor agregado, no una curva temporal. Mitigación: el HTML report generado con `-e -o results/html-report/` incluye la gráfica de Throughput over Time a partir de `results.jtl`, cubriendo la necesidad visual.

## Migration Plan

1. Editar `jmeter/test-plan.jmx`: insertar un elemento `ResultCollector` con `guiclass="StatVisualizer"` y `filename=results/tps-report.jtl` inmediatamente después del `<hashTree/>` que cierra el `Summary Report` existente (línea 226).
2. Verificar que el directorio `results/` esté en `.gitignore` (ya lo está) para no versionar archivos de salida.
3. Validar abriendo el JMX en la GUI de JMeter: el listener `Aggregate Report` debe aparecer en el árbol del Test Plan.
4. Ejecutar con CLI y confirmar que `results/tps-report.jtl` se genera correctamente.

**Rollback:** Eliminar el bloque `<ResultCollector guiclass="StatVisualizer" ...>` y su `<hashTree/>` correspondiente del JMX. No hay cambios en base de datos ni estado externo.

## Open Questions

- *(Resuelto)* Plugin vs. nativo → se optó por nativo `StatVisualizer`.
- *(Resuelto)* Archivo compartido vs. separado → se optó por `results/tps-report.jtl` separado.
