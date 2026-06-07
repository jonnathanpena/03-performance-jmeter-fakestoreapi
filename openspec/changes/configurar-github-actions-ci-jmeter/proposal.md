## Why

El proyecto carece de integración continua: las pruebas de performance con JMeter solo se ejecutan manualmente en local, lo que impide detectar regresiones de forma automática y garantizar que los criterios de aceptación (≥ 20 TPS, P95 ≤ 1 500 ms, error rate < 3 %) se cumplan en cada cambio al repositorio.

## What Changes

- Agregar un workflow de GitHub Actions (`.github/workflows/performance.yml`) que ejecute el plan JMeter en modo CLI en cada push/PR a `main`.
- Publicar el reporte HTML de JMeter como artefacto descargable del pipeline.
- Publicar el archivo `results.jtl` como artefacto para trazabilidad.
- Configurar un step de validación que lea el `results.jtl` y falle el pipeline si throughput < 20 TPS, P95 > 1 500 ms, o error rate ≥ 3 %.
- Agregar instalación automática de Java 21 y Apache JMeter 5.6.3 en el runner de GitHub Actions.

## Capabilities

### New Capabilities

- `ci-pipeline`: Definición del workflow de GitHub Actions para ejecución automatizada de pruebas JMeter, instalación de dependencias, generación de reportes y publicación de artefactos.
- `threshold-validation`: Lógica de validación de umbrales de performance (TPS, P95, error rate) que lee el `.jtl` y falla el pipeline si no se cumplen los criterios de aceptación.

### Modified Capabilities

## Impact

- **Nuevo archivo**: `.github/workflows/performance.yml`
- **Nuevo script**: `scripts/validate_thresholds.py` (o bash) para parsear el `.jtl` y aplicar umbrales
- **`.gitignore`**: verificar que `results/` siga ignorado pero los artefactos del CI se publiquen vía Actions
- **Dependencias externas**: runner `ubuntu-latest`, `actions/setup-java@v4`, descarga directa de JMeter 5.6.3 desde Apache mirrors
- **Sin cambios** al plan de prueba `jmeter/test-plan.jmx` ni a `jmeter/test-data/users.csv`
