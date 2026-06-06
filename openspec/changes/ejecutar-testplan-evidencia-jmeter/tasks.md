## 1. Preparación del entorno

- [x] 1.1 Verificar que Java 21 está instalado ejecutando `java -version` y confirmar la versión reportada
- [x] 1.2 Verificar que JMeter 5.6.x está instalado y disponible en el PATH ejecutando `jmeter -v`
- [x] 1.3 Confirmar que `jmeter/test-data/users.csv` contiene las 5 filas de usuario/contraseña esperadas
- [x] 1.4 Eliminar el directorio `results/` si ya existe para evitar error de HTML report (`rm -rf results/`)

## 2. Ejecución del test plan

- [x] 2.1 Ejecutar el plan en modo CLI no-gráfico: `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/`
- [x] 2.2 Verificar que JMeter termina con código de salida 0 y muestra el resumen de ejecución en consola
- [x] 2.3 Confirmar que `results/results.jtl` fue creado y contiene al menos un registro por cada hilo configurado

## 3. Verificación del reporte HTML

- [x] 3.1 Confirmar que el directorio `results/html-report/` fue generado y contiene el archivo `index.html`
- [x] 3.2 Abrir `results/html-report/index.html` en un navegador y verificar que el dashboard carga con gráficas de throughput, tiempos de respuesta y errores
- [x] 3.3 Localizar la sección Statistics del dashboard y anotar los valores de TPS, P95, total requests y duración total

## 4. Validación de criterios de aceptación

- [x] 4.1 Verificar que el throughput (TPS) reportado en el dashboard o consola es >= 20 TPS
- [x] 4.2 Verificar que el percentil 95 (P95) de tiempo de respuesta es <= 1500 ms
- [x] 4.3 Verificar que la tasa de error calculada `(muestras fallidas / total) * 100` es < 3%
- [x] 4.4 Confirmar en el JTL que los 5 usuarios del CSV aparecen utilizados (rotación cíclica entre hilos)

## 5. Documentación de evidencia en InformeResultados.md

- [x] 5.1 Añadir una sección con encabezado identificable de resultados JMeter en `reports/InformeResultados.md`
- [x] 5.2 Crear la tabla de métricas con columnas Métrica / Valor Obtenido / Criterio / Estado (PASS/FAIL) incluyendo TPS, P95, tasa de error, total requests y duración total
- [x] 5.3 Redactar al menos un párrafo de hallazgos explicando los criterios cumplidos y, si aplica, los fallidos con posibles causas
- [x] 5.4 Añadir referencia explícita a los resultados K6 ya documentados en el informe, destacando similitudes o diferencias entre ambas herramientas
- [x] 5.5 Documentar una conclusión integradora JMeter + K6 que evalúe el comportamiento del endpoint bajo carga
