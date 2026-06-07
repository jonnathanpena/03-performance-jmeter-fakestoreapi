## ADDED Requirements

### Requirement: Parseo del archivo results.jtl en formato CSV
El script `scripts/validate_thresholds.py` SHALL leer y parsear el archivo `results/results.jtl` generado por JMeter como un CSV estándar usando la librería estándar de Python (`csv` + `statistics`), sin dependencias externas adicionales.

#### Scenario: Parseo exitoso del jtl con datos válidos
- **WHEN** el script recibe la ruta a un `results.jtl` con al menos una fila de datos válida
- **THEN** el script carga todas las filas y extrae las columnas `elapsed`, `success` y `timeStamp` sin error

#### Scenario: Archivo jtl inexistente provoca salida con error
- **WHEN** el script recibe una ruta a un archivo `results.jtl` que no existe
- **THEN** el script termina con código de salida `1` e imprime un mensaje de error indicando que el archivo no fue encontrado

#### Scenario: Archivo jtl vacío o sin filas de datos provoca salida con error
- **WHEN** el script parsea un `results.jtl` que contiene únicamente la cabecera CSV sin filas de datos
- **THEN** el script termina con código de salida `1` e imprime un mensaje indicando que no hay datos para validar

---

### Requirement: Validación de throughput mínimo de 20 TPS
El script SHALL calcular el throughput total de la prueba como `número_total_de_requests / duración_total_en_segundos` y SHALL fallar si el resultado es menor a 20 transacciones por segundo.

#### Scenario: Throughput igual o mayor a 20 TPS pasa la validación
- **WHEN** el total de requests dividido por la duración total en segundos es mayor o igual a 20.0
- **THEN** el script no reporta fallo por throughput y continúa con las siguientes validaciones

#### Scenario: Throughput menor a 20 TPS falla la validación
- **WHEN** el total de requests dividido por la duración total en segundos es menor a 20.0
- **THEN** el script imprime el throughput calculado junto al umbral requerido y acumula el fallo para reportarlo al final

---

### Requirement: Validación del percentil P95 de tiempo de respuesta ≤ 1500 ms
El script SHALL calcular el percentil 95 de los tiempos de respuesta (`elapsed`) de todas las requests y SHALL fallar si el valor supera 1500 milisegundos.

#### Scenario: P95 igual o menor a 1500 ms pasa la validación
- **WHEN** el percentil 95 calculado sobre todos los valores de `elapsed` es menor o igual a 1500
- **THEN** el script no reporta fallo por P95 y continúa con las siguientes validaciones

#### Scenario: P95 mayor a 1500 ms falla la validación
- **WHEN** el percentil 95 calculado sobre todos los valores de `elapsed` es mayor a 1500
- **THEN** el script imprime el valor de P95 calculado junto al umbral requerido y acumula el fallo para reportarlo al final

---

### Requirement: Validación de tasa de error menor al 3%
El script SHALL calcular la tasa de error como `(requests_fallidas / total_requests) * 100` donde una request fallida es aquella cuya columna `success` es `false`, y SHALL fallar si la tasa de error es mayor o igual al 3%.

#### Scenario: Error rate menor a 3% pasa la validación
- **WHEN** el porcentaje de requests con `success=false` sobre el total es menor a 3.0
- **THEN** el script no reporta fallo por error rate y continúa con las siguientes validaciones

#### Scenario: Error rate igual o mayor a 3% falla la validación
- **WHEN** el porcentaje de requests con `success=false` sobre el total es mayor o igual a 3.0
- **THEN** el script imprime el error rate calculado junto al umbral requerido y acumula el fallo para reportarlo al final

---

### Requirement: Reporte consolidado y código de salida según resultado de validaciones
El script SHALL imprimir un resumen de las tres métricas validadas (throughput, P95, error rate) con sus valores calculados y umbrales, y SHALL terminar con código de salida `1` si al menos una validación falló, o `0` si todas las validaciones pasaron.

#### Scenario: Todas las validaciones pasan, script termina con código 0
- **WHEN** throughput ≥ 20 TPS, P95 ≤ 1500 ms y error rate < 3% simultáneamente
- **THEN** el script imprime un resumen con los tres valores aprobados y termina con código de salida `0`

#### Scenario: Al menos una validación falla, script termina con código 1
- **WHEN** cualquiera de los tres umbrales (throughput, P95, error rate) no es satisfecho
- **THEN** el script imprime el resumen indicando cuáles métricas fallaron y cuáles pasaron, y termina con código de salida `1`, lo que provoca que el step de GitHub Actions marque el pipeline como fallido
