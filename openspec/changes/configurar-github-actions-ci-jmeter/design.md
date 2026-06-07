## Context

Las pruebas de performance con JMeter se ejecutan únicamente de forma manual en entornos locales. No existe ningún mecanismo automatizado que valide los criterios de aceptación (≥ 20 TPS, P95 ≤ 1 500 ms, error rate < 3 %) en cada cambio al repositorio. Esto deja una brecha: un cambio puede romper silenciosamente los umbrales sin que el equipo lo detecte hasta la siguiente ejecución manual.

El cambio introduce un pipeline de CI con GitHub Actions que instala las dependencias (Java 21 + JMeter 5.6.3), ejecuta el plan JMeter en modo CLI, valida los umbrales sobre el `.jtl` generado y publica reportes como artefactos descargables.

**Stakeholders**: equipo QA / reto Sofka.

## Goals / Non-Goals

**Goals:**
- Ejecutar automáticamente el plan JMeter (`jmeter/test-plan.jmx`) en cada push/PR a `main` sin intervención manual.
- Instalar Java 21 y Apache JMeter 5.6.3 de forma reproducible en el runner de GitHub Actions.
- Publicar `results.jtl` y el reporte HTML como artefactos descargables del pipeline.
- Fallar el pipeline si throughput < 20 TPS, P95 > 1 500 ms o error rate ≥ 3 %.
- Mantener el plan de prueba `jmeter/test-plan.jmx` y `users.csv` sin cambios.

**Non-Goals:**
- Soporte a otros proveedores de CI (Jenkins, CircleCI, GitLab CI).
- Ejecución distribuida / clúster JMeter.
- Notificaciones externas (Slack, email) por fallo de pipeline.
- Almacenamiento histórico de resultados entre ejecuciones (tendencias).

## Decisions

### 1. GitHub Actions como plataforma de CI

**Decisión**: usar GitHub Actions (runner `ubuntu-latest`).

**Rationale**: el repositorio ya está en GitHub; no requiere infraestructura adicional. El runner gratuito `ubuntu-latest` soporta Java y permite descargar binarios externos.

**Alternativas descartadas**:
- Jenkins / self-hosted: requiere servidor dedicado, fuera de alcance para un reto académico.
- GitHub Actions con runner self-hosted: añade complejidad sin beneficio para este contexto.

---

### 2. Instalación de JMeter vía descarga directa (no Docker)

**Decisión**: descargar el tarball de JMeter 5.6.3 desde los mirrors de Apache en el step del workflow.

**Rationale**: la imagen Docker oficial de JMeter tiene mantenimiento irregular; usar el binario oficial garantiza versión exacta (`5.6.3`) y reproducibilidad. La descarga añade ~30 s al pipeline pero evita dependencia de imágenes de terceros.

**Alternativas descartadas**:
- `justb4/jmeter` Docker image: mantenimiento irregular, versiones desfasadas.
- Acción de marketplace para JMeter: ninguna tiene soporte activo para 5.6.x con garantías.

---

### 3. Script Python para validación de umbrales

**Decisión**: implementar `scripts/validate_thresholds.py` que parsea el `.jtl` (CSV) y aplica los tres umbrales; sale con código 1 si alguno falla.

**Rationale**: el `.jtl` de JMeter es un CSV estándar; Python (`csv` + `statistics`) lo parsea sin dependencias externas adicionales en el runner `ubuntu-latest` (Python 3 preinstalado). Un script Python es más legible y testeable que bash puro para lógica con percentiles.

**Alternativas descartadas**:
- Bash + `awk`: cálculo de percentiles en awk es verboso y propenso a errores de precisión.
- Plugin JMeter de umbrales (e.g. `jmeter-plugins`): requiere instalación extra de plugins y no integra bien con salida de código de error para CI.

---

### 4. Estructura de steps del workflow

**Decisión**: el workflow tendrá los siguientes steps en orden:
1. `actions/checkout@v4`
2. `actions/setup-java@v4` (temurin, Java 21)
3. Descarga y extracción de JMeter 5.6.3
4. Ejecución CLI de JMeter (`jmeter -n -t ... -l results/results.jtl -e -o results/html-report/`)
5. Validación de umbrales con `python3 scripts/validate_thresholds.py`
6. `actions/upload-artifact@v4` para `results/results.jtl`
7. `actions/upload-artifact@v4` para `results/html-report/`

**Rationale**: publicar artefactos incluso si el step de validación falla (`if: always()`) para permitir diagnóstico post-fallo.

---

### 5. Trigger del workflow

**Decisión**: `on: push` y `pull_request` limitados a la rama `main`.

**Rationale**: cubre los dos eventos de integración principales sin ejecutar en cada rama de feature. Suficiente para el alcance del reto.

## Risks / Trade-offs

- **Disponibilidad del mirror de Apache** → el tarball de JMeter se descarga de `https://archive.apache.org/dist/`; si el mirror falla, el pipeline falla. Mitigación: usar `archive.apache.org` (siempre disponible para versiones históricas) en lugar de mirrors CDN.

- **Tiempo de ejecución del plan JMeter en CI** → el plan configura 20 hilos con rampa; una ejecución completa tarda ~3-5 min en local. En el runner `ubuntu-latest` puede ser ligeramente más lento. Mitigación: aceptable para el alcance del reto; si se requiere agilidad, se puede reducir la duración de la prueba en CI vía parámetro JMeter property.

- **FakeStoreAPI como dependencia externa** → el endpoint `POST /auth/login` es un servicio público de terceros; una caída o throttling externo puede fallar el pipeline por razones ajenas al código. Mitigación: documentar la dependencia; no se mockea el servicio dado el objetivo del ejercicio (prueba real de carga).

- **Percentil P95 calculado sobre muestra pequeña** → con 20 hilos y duración corta, la muestra puede ser < 100 requests, haciendo el P95 estadísticamente ruidoso. Mitigación: el umbral de 1 500 ms tiene margen suficiente; se documenta la limitación en el README.
