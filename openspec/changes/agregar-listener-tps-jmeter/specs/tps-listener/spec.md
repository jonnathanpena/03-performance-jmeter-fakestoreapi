## ADDED Requirements

### Requirement: Listener TPS presente en el plan de prueba
El archivo `jmeter/test-plan.jmx` SHALL contener un elemento `ResultCollector` configurado como listener de throughput (TPS), ubicado dentro del bloque de listeners del Thread Group o del Test Plan.

#### Scenario: Listener declarado en el JMX
- **WHEN** se abre el archivo `jmeter/test-plan.jmx` en un editor de texto o en JMeter GUI
- **THEN** existe al menos un elemento `<ResultCollector>` con atributo `guiclass` correspondiente a un reporte de throughput (ej. `SummaryReport` nativo o `TransactionsPerSecondGui` del plugin jp@gc)

### Requirement: Escritura de resultados TPS a archivo en CLI
El listener SHALL estar configurado para escribir sus resultados en un archivo `.jtl` dentro de la carpeta `results/`, de modo que la ejecución en modo CLI (`jmeter -n`) genere dicha salida sin intervención manual.

#### Scenario: Archivo de resultados generado tras ejecución CLI
- **WHEN** se ejecuta `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/`
- **THEN** el directorio `results/` contiene un archivo `.jtl` con registros de throughput producidos por el listener

#### Scenario: Ruta de salida definida en el elemento ResultCollector
- **WHEN** se inspecciona el atributo `filename` del `<ResultCollector>` de throughput dentro del JMX
- **THEN** el valor apunta a un path dentro de `results/` (ej. `results/tps.jtl`)

### Requirement: Compatibilidad con ejecución GUI
El listener SHALL mostrarse en tiempo real durante la ejecución desde JMeter GUI, sin requerir configuración adicional por parte del usuario.

#### Scenario: Visualización en tiempo real en GUI
- **WHEN** se abre `jmeter/test-plan.jmx` en JMeter GUI y se ejecuta la prueba
- **THEN** el listener aparece en el árbol de elementos y actualiza su gráfica o tabla de TPS en tiempo real mientras corren los hilos

### Requirement: Sin impacto en elementos existentes del plan
La adición del listener SHALL no modificar ni eliminar ningún elemento preexistente del plan de prueba (Thread Group, CSV Data Set Config, HTTP Request, Response Assertion, Duration Assertion, ConstantThroughputTimer, Summary Report).

#### Scenario: Elementos previos intactos tras el cambio
- **WHEN** se compara el JMX antes y después de agregar el listener
- **THEN** todos los elementos existentes mantienen su configuración original sin alteraciones

### Requirement: No requerir plugins adicionales (opción nativa)
Si se utiliza el `Aggregate Report` nativo de JMeter como listener de throughput, el plan SHALL ejecutarse sin necesidad de instalar el JMeter Plugins Manager ni ningún plugin externo.

#### Scenario: Ejecución sin plugins externos con listener nativo
- **WHEN** se ejecuta el plan en un entorno JMeter 5.6.x limpio (sin plugins adicionales) usando el listener nativo
- **THEN** el plan inicia y completa la ejecución sin errores relacionados con clases faltantes del listener
