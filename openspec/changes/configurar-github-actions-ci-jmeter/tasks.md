## 1. Preparación del repositorio

- [x] 1.1 Crear el directorio `.github/workflows/` en la raíz del repositorio
- [x] 1.2 Crear el directorio `scripts/` en la raíz del repositorio
- [x] 1.3 Verificar que `results/` está listado en `.gitignore` para evitar subir `.jtl` y `html-report/` al repositorio

## 2. Workflow de GitHub Actions

- [x] 2.1 Crear `.github/workflows/performance.yml` con trigger `on: push` y `pull_request` limitado a la rama `main`
- [x] 2.2 Agregar step `actions/checkout@v4` como primer step del job
- [x] 2.3 Agregar step `actions/setup-java@v4` con distribución Temurin y Java 21
- [x] 2.4 Agregar step de descarga del tarball `apache-jmeter-5.6.3.tgz` desde `https://archive.apache.org/dist/jmeter/binaries/` y extracción en el runner
- [x] 2.5 Agregar step de ejecución CLI: `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/` con el binario JMeter en PATH
- [x] 2.6 Agregar step de validación de umbrales: `python3 scripts/validate_thresholds.py results/results.jtl`
- [x] 2.7 Agregar step `actions/upload-artifact@v4` para `results/results.jtl` con nombre `jmeter-jtl` y condición `if: always()`
- [x] 2.8 Agregar step `actions/upload-artifact@v4` para `results/html-report/` con nombre `jmeter-html-report` y condición `if: always()`

## 3. Script de validación de umbrales

- [x] 3.1 Crear `scripts/validate_thresholds.py` con lectura y parseo del `.jtl` usando `csv` de la librería estándar de Python; extraer columnas `elapsed`, `success` y `timeStamp`; fallar con código 1 si el archivo no existe o no tiene filas de datos
- [x] 3.2 Implementar validación de throughput: calcular `total_requests / duración_total_segundos` y acumular fallo si el resultado es menor a 20 TPS
- [x] 3.3 Implementar validación de P95: calcular el percentil 95 sobre la lista de valores `elapsed` usando `statistics.quantiles` y acumular fallo si supera 1500 ms
- [x] 3.4 Implementar validación de error rate: calcular `(requests con success=false / total_requests) * 100` y acumular fallo si es mayor o igual a 3%
- [x] 3.5 Implementar reporte consolidado que imprima los tres valores calculados con sus umbrales y termine con código de salida `0` si todas las validaciones pasan o `1` si al menos una falla

## 4. Verificación del pipeline

- [x] 4.1 Ejecutar `python3 scripts/validate_thresholds.py` localmente con un `.jtl` de prueba para confirmar parseo correcto y comportamiento del código de salida
- [ ] 4.2 Hacer push a `main` (o abrir un PR hacia `main`) y confirmar en la pestaña Actions de GitHub que el workflow `performance.yml` se dispara automáticamente
- [ ] 4.3 Verificar que los artefactos `jmeter-jtl` y `jmeter-html-report` quedan disponibles para descarga en la UI de GitHub Actions, incluso si el step de validación falla
- [ ] 4.4 Confirmar que un pipeline con umbrales incumplidos reporta el step de validación como fallido y el run queda marcado como rojo en GitHub Actions
