## ADDED Requirements

### Requirement: Ejecución CLI no-gráfica del test plan JMeter
El sistema SHALL soportar la ejecución del plan de prueba `jmeter/test-plan.jmx` en modo no-gráfico mediante el comando:
`jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/`

#### Scenario: Inicio exitoso del plan en modo CLI
- **WHEN** se ejecuta el comando JMeter CLI con los parámetros `-n -t -l -e -o`
- **THEN** JMeter inicia la ejecución sin errores de configuración y registra el progreso en consola

#### Scenario: Finalización limpia de la ejecución
- **WHEN** todos los hilos del test plan completan sus iteraciones
- **THEN** JMeter termina con código de salida 0 y muestra un resumen en consola

### Requirement: Generación del archivo JTL de resultados
El sistema SHALL crear el archivo `results/results.jtl` con los registros de todas las transacciones ejecutadas durante el test.

#### Scenario: Archivo JTL creado al finalizar la ejecución
- **WHEN** la ejecución del plan de prueba concluye
- **THEN** existe el archivo `results/results.jtl` con al menos un registro por hilo configurado

#### Scenario: Contenido mínimo del JTL
- **WHEN** se abre el archivo `results/results.jtl`
- **THEN** contiene campos: timeStamp, elapsed, label, responseCode, success, threadName, bytes

### Requirement: Generación del reporte HTML dashboard
El sistema SHALL generar el directorio `results/html-report/` con el dashboard HTML completo navegable al usar los flags `-e -o`.

#### Scenario: Directorio del reporte creado
- **WHEN** la ejecución finaliza con los flags `-e -o results/html-report/`
- **THEN** existe el directorio `results/html-report/` con el archivo `index.html` y los recursos necesarios

#### Scenario: Dashboard accesible en navegador
- **WHEN** se abre `results/html-report/index.html` en un navegador
- **THEN** se visualiza el dashboard de JMeter con gráficas de throughput, tiempos de respuesta y errores

### Requirement: Parametrización con datos CSV
El plan de prueba SHALL utilizar los 5 usuarios definidos en `jmeter/test-data/users.csv` para parametrizar las solicitudes de login.

#### Scenario: Todos los usuarios del CSV son utilizados
- **WHEN** el test plan ejecuta los hilos de carga
- **THEN** cada uno de los 5 pares usuario/contraseña del CSV es utilizado al menos una vez durante la ejecución

#### Scenario: Rotación de usuarios entre hilos
- **WHEN** el número de hilos supera el número de filas del CSV
- **THEN** los usuarios se reutilizan de forma cíclica entre los hilos adicionales

### Requirement: Cumplimiento del criterio de throughput mínimo
El plan de prueba SHALL ejecutarse con al menos 20 hilos activos y el throughput medido SHALL ser >= 20 TPS.

#### Scenario: Throughput alcanza el mínimo requerido
- **WHEN** finaliza la ejecución con la configuración de carga definida
- **THEN** el throughput (requests/segundo) reportado en el JTL es >= 20 TPS

### Requirement: Cumplimiento del criterio de tiempo de respuesta P95
El sistema SHALL verificar que el percentil 95 del tiempo de respuesta es <= 1 500 ms.

#### Scenario: P95 dentro del límite
- **WHEN** se analiza el percentil 95 de `elapsed` en el archivo JTL
- **THEN** el valor P95 es <= 1 500 ms

#### Scenario: Duration Assertion activa en el plan
- **WHEN** una transacción supera 1 500 ms de duración
- **THEN** la Duration Assertion del test plan marca esa muestra como fallida en el JTL

### Requirement: Cumplimiento del criterio de tasa de error
El sistema SHALL mantener una tasa de error < 3 % durante la ejecución del test.

#### Scenario: Tasa de error dentro del límite
- **WHEN** se calcula `(muestras fallidas / total de muestras) * 100` sobre el JTL
- **THEN** el resultado es < 3 %

#### Scenario: Response Assertion activa en el plan
- **WHEN** una solicitud retorna un código HTTP distinto de 200
- **THEN** la Response Assertion del test plan marca esa muestra como fallida en el JTL
