## ADDED Requirements

### Requirement: Tabla de métricas de ejecución JMeter
La evidencia SHALL incluir una tabla estructurada con las métricas clave de la ejecución, el criterio de aceptación y el estado PASS/FAIL de cada uno.

#### Scenario: Tabla de métricas presente en la evidencia
- **WHEN** se documenta la evidencia de ejecución JMeter
- **THEN** existe una tabla con las columnas: Métrica, Valor Obtenido, Criterio, Estado

#### Scenario: Estado PASS cuando el criterio se cumple
- **WHEN** el valor obtenido de una métrica satisface su criterio de aceptación
- **THEN** la columna Estado de esa fila muestra PASS

#### Scenario: Estado FAIL cuando el criterio no se cumple
- **WHEN** el valor obtenido de una métrica no satisface su criterio de aceptación
- **THEN** la columna Estado de esa fila muestra FAIL

### Requirement: Cobertura de métricas clave en la tabla
La tabla de métricas SHALL incluir, como mínimo, las siguientes métricas: TPS (throughput), P95 (tiempo de respuesta percentil 95), tasa de error, total de requests y duración total de la ejecución.

#### Scenario: Métricas obligatorias presentes
- **WHEN** se verifica la tabla de métricas de la evidencia
- **THEN** existen filas individuales para TPS, P95, tasa de error, total de requests y duración total

### Requirement: Sección de resultados JMeter en InformeResultados.md
El archivo `reports/InformeResultados.md` SHALL contener una sección dedicada a los resultados de la ejecución JMeter con la tabla de métricas y un análisis de hallazgos.

#### Scenario: Sección JMeter añadida al informe
- **WHEN** se abre `reports/InformeResultados.md`
- **THEN** existe una sección con encabezado identificable como resultados JMeter que incluye la tabla de métricas y al menos un párrafo de hallazgos

#### Scenario: Hallazgos documentados en la sección JMeter
- **WHEN** se lee la sección de resultados JMeter del informe
- **THEN** el análisis de hallazgos menciona los criterios que se cumplieron, los que fallaron (si aplica) y posibles causas o conclusiones observadas

### Requirement: Contraste con análisis K6 en el informe
La sección JMeter en `reports/InformeResultados.md` SHALL incluir una comparación o complemento con los hallazgos del análisis K6 ya documentado en el informe.

#### Scenario: Referencia cruzada con K6 presente
- **WHEN** se lee la sección de resultados JMeter
- **THEN** el contenido hace referencia explícita a los resultados K6 previos, destacando similitudes, diferencias o conclusiones complementarias entre ambas herramientas

#### Scenario: Conclusión comparativa documentada
- **WHEN** se revisa el informe completo
- **THEN** existe al menos una conclusión que integra los datos de JMeter y K6 para evaluar el comportamiento del endpoint bajo carga
