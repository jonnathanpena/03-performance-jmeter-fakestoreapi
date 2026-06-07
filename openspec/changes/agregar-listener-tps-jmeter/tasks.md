## 1. Inspección del JMX actual

- [x] 1.1 Abrir `jmeter/test-plan.jmx` e identificar la línea donde cierra el bloque del `Summary Report` existente (`<hashTree/>` correspondiente al `ResultCollector` con `guiclass="SummaryReport"`)
- [x] 1.2 Verificar que el `Summary Report` está al nivel del Test Plan (fuera del `<hashTree>` del Thread Group)
- [x] 1.3 Confirmar que no existe aún ningún `ResultCollector` con `guiclass="StatVisualizer"` en el JMX

## 2. Inserción del listener Aggregate Report

- [x] 2.1 Insertar inmediatamente después del `<hashTree/>` que cierra el `Summary Report` el bloque `<ResultCollector guiclass="StatVisualizer" ...>` con `testname="Aggregate Report"` y `filename="results/tps-report.jtl"`
- [x] 2.2 Agregar el `<hashTree/>` de cierre vacío correspondiente al nuevo `ResultCollector`
- [x] 2.3 Verificar que el XML resultante está bien formado (sin etiquetas descuadradas)

## 3. Verificación estructural del JMX

- [x] 3.1 Inspeccionar el JMX editado y confirmar que el atributo `filename` del nuevo `ResultCollector` apunta a `results/tps-report.jtl`
- [x] 3.2 Confirmar que todos los elementos preexistentes (Thread Group, CSV Data Set Config, HTTP Request, Response Assertion, Duration Assertion, ConstantThroughputTimer, Summary Report) mantienen su configuración original sin alteraciones
- [ ] 3.3 Abrir el JMX modificado en JMeter GUI y verificar que el `Aggregate Report` aparece en el árbol del Test Plan al mismo nivel que el `Summary Report`

## 4. Verificación funcional en CLI

- [x] 4.1 Crear el directorio `results/` si no existe antes de ejecutar
- [x] 4.2 Ejecutar `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/` y confirmar que la ejecución finaliza sin errores de clase faltante relacionados con el listener
- [x] 4.3 Confirmar que el archivo `results/tps-report.jtl` se genera con registros de throughput tras la ejecución CLI
