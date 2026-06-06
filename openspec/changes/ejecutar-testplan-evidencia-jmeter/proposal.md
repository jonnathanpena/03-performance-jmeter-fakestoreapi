## Why

El plan de prueba JMeter (`test-plan.jmx`) está configurado y parametrizado, pero no existe evidencia de su ejecución real: no hay archivo `.jtl` de resultados ni reporte HTML generado. Sin ejecutar el plan y capturar métricas concretas no es posible validar que los criterios de aceptación (≥ 20 TPS, P95 ≤ 1 500 ms, error rate < 3 %) se cumplen en la herramienta definida para el ejercicio (JMeter).

## What Changes

- Ejecutar `jmeter/test-plan.jmx` en modo CLI no-gráfico y producir `results/results.jtl` + `results/html-report/`.
- Validar contra las aserciones embebidas (HTTP 200, token en body, duración ≤ 1 500 ms).
- Capturar y documentar métricas clave de la ejecución (throughput, P95, error rate) como evidencia del ejercicio.
- Complementar `reports/InformeResultados.md` con una sección de resultados JMeter que contraste con el análisis K6 ya existente.

## Capabilities

### New Capabilities

- `ejecucion-carga-jmeter`: Ejecución CLI del plan de prueba JMeter, parámetros de arranque, generación de artefactos de resultados (JTL + HTML dashboard) y criterios de éxito medibles.
- `evidencia-resultados-jmeter`: Captura estructurada de la evidencia de ejecución: tabla de métricas (TPS, P95, error rate, pass/fail por criterio) y actualización del informe con hallazgos JMeter.

### Modified Capabilities

## Impact

- `jmeter/test-plan.jmx` — lectura/ejecución; no se modifica el archivo.
- `results/` — directorio generado en ejecución (excluido de git); se crean `results.jtl` y `results/html-report/`.
- `reports/InformeResultados.md` — se añade sección de resultados JMeter.
- Dependencia externa: `fakestoreapi.com` debe estar disponible al momento de la ejecución.
