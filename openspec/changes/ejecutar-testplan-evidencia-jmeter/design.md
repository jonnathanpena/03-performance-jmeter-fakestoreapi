## Context

El proyecto ya cuenta con un `test-plan.jmx` funcional y parametrizado con `users.csv` (5 usuarios), pero no existe evidencia de una ejecución real: no hay `.jtl` ni reporte HTML. El `InformeResultados.md` actual documenta análisis basado en resultados de k6, no de JMeter. Este diseño cubre cómo ejecutar el plan, capturar artefactos y documentar los resultados de forma reproducible.

**Estado actual:**
- `jmeter/test-plan.jmx` — configurado con 20 hilos, ramp-up, CSV Data Set Config, Response/Duration Assertions.
- `reports/InformeResultados.md` — análisis existente basado en k6 (`textSummary.txt`).
- `results/` — no existe; se genera en ejecución y está en `.gitignore`.

**Restricciones:**
- JMeter 5.6.x + Java 21 (no se requieren plugins adicionales).
- La API `fakestoreapi.com` debe estar disponible en el momento de la ejecución.
- El `.jtl` y el HTML dashboard **no se versionan** (excluidos por `.gitignore`).

## Goals / Non-Goals

**Goals:**
- Ejecutar `jmeter/test-plan.jmx` en modo CLI no-gráfico y producir `results/results.jtl` + `results/html-report/`.
- Validar que las aserciones embebidas (HTTP 200, token en body, duración ≤ 1 500 ms) funcionen correctamente.
- Documentar las métricas clave (throughput, P95, error rate) como evidencia del ejercicio en `reports/InformeResultados.md`.

**Non-Goals:**
- Modificar la lógica del `test-plan.jmx`.
- Crear infraestructura de CI/CD para ejecuciones automáticas.
- Comparar resultados entre múltiples corridas o hacer análisis de tendencia.

## Decisions

### 1. Ejecución en modo CLI no-gráfico con reporte HTML integrado

**Decisión:** Usar el comando único:
```
jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/
```

**Rationale:** El flag `-e -o` genera el HTML dashboard en la misma ejecución sin pasos extra. Es la forma oficial recomendada por Apache JMeter para ejecuciones de CI/carga. No requiere plugins adicionales.

**Alternativa descartada:** Generar el reporte en un paso separado con `jmeter -g results/results.jtl -o results/html-report/` — añade un paso sin ventaja cuando el `.jtl` se genera desde cero.

---

### 2. Directorio `results/` efímero, no versionado

**Decisión:** Los artefactos de resultados (`.jtl` + HTML report) se excluyen de git. Solo se versiona la evidencia estructurada en `InformeResultados.md`.

**Rationale:** El `.jtl` puede superar varios MB y su contenido varía entre ejecuciones (timestamps, IPs). Versionar artefactos binarios/voluminosos en git degrada la experiencia del repositorio. La evidencia relevante se extrae manualmente y se documenta en Markdown.

**Alternativa descartada:** Versionar capturas del HTML report como imágenes — overhead alto, difícil de diff.

---

### 3. Captura de métricas a partir del HTML report y/o salida de consola

**Decisión:** Las métricas clave (throughput en TPS, P95, error rate %) se extraen de la sección *Statistics* del HTML dashboard o de la salida de consola de JMeter al final de la ejecución.

**Rationale:** JMeter imprime un resumen agregado al terminar la ejecución en modo `-n`. El HTML dashboard ofrece valores de percentil configurables. Ambas fuentes son inmediatas, sin necesidad de herramientas adicionales de análisis.

---

### 4. Documentación de evidencia en `InformeResultados.md`

**Decisión:** Se añade una sección dedicada a JMeter en el informe existente, con tabla de métricas y análisis de pass/fail por criterio de aceptación.

**Rationale:** El informe ya tiene el análisis de k6; añadir JMeter como sección paralela permite comparar herramientas y consolida toda la evidencia del ejercicio en un solo documento.

## Risks / Trade-offs

- **Disponibilidad de `fakestoreapi.com`** → La API pública puede tener downtime o rate-limiting. Mitigación: ejecutar en horario de baja carga; si falla, documentar el error y reintentar.
- **Resultados variables por red** → Las métricas (P95, throughput) dependen de la latencia de red del host de ejecución. Mitigación: documentar el entorno (red, hardware) junto a las métricas.
- **`results/` no vacío antes de ejecutar** → Si el directorio ya existe con datos anteriores, JMeter fallará al generar el HTML report. Mitigación: eliminar o renombrar `results/` antes de cada ejecución (`rm -rf results/`).
- **Java 21 requerido** → Versiones anteriores de Java pueden causar errores de compatibilidad con JMeter 5.6.x. Mitigación: verificar con `java -version` antes de ejecutar.
