## ADDED Requirements

### Requirement: Trigger automático en push y pull_request a main
El workflow de GitHub Actions SHALL ejecutarse automáticamente ante eventos `push` y `pull_request` dirigidos a la rama `main`. No SHALL ejecutarse en otras ramas.

#### Scenario: Push a main dispara el workflow
- **WHEN** se realiza un `git push` a la rama `main`
- **THEN** el workflow `performance.yml` es disparado automáticamente por GitHub Actions

#### Scenario: Pull request hacia main dispara el workflow
- **WHEN** se abre o actualiza un pull request con `main` como rama destino
- **THEN** el workflow `performance.yml` es disparado automáticamente por GitHub Actions

#### Scenario: Push a rama que no es main no dispara el workflow
- **WHEN** se realiza un `git push` a cualquier rama diferente de `main`
- **THEN** el workflow `performance.yml` NO es disparado

---

### Requirement: Instalación reproducible de Java 21 y Apache JMeter 5.6.3
El runner `ubuntu-latest` SHALL instalar Java 21 (distribución Temurin) mediante `actions/setup-java@v4` y SHALL descargar y extraer el binario oficial de Apache JMeter 5.6.3 desde `https://archive.apache.org/dist/` antes de ejecutar el plan de prueba.

#### Scenario: Java 21 disponible en el runner antes de ejecutar JMeter
- **WHEN** el step de instalación de Java se completa
- **THEN** el comando `java -version` en el runner retorna una versión 21.x compatible con JMeter 5.6.3

#### Scenario: JMeter 5.6.3 descargado y disponible en PATH
- **WHEN** el step de descarga y extracción del tarball de JMeter 5.6.3 se completa
- **THEN** el binario `jmeter` está accesible en el PATH del runner y ejecuta sin error con la flag `-version`

#### Scenario: Fallo de descarga del tarball detiene el pipeline
- **WHEN** el mirror `archive.apache.org` no responde o retorna un error HTTP durante la descarga del tarball
- **THEN** el step de instalación de JMeter falla y el workflow reporta error en ese step específico

---

### Requirement: Ejecución CLI del plan JMeter en modo no-GUI
El workflow SHALL ejecutar el plan de prueba `jmeter/test-plan.jmx` en modo CLI (`-n`) generando el archivo de resultados `results/results.jtl` y el reporte HTML en `results/html-report/`.

#### Scenario: JMeter ejecuta el plan completo sin error de configuración
- **WHEN** el step de ejecución CLI invoca `jmeter -n -t jmeter/test-plan.jmx -l results/results.jtl -e -o results/html-report/`
- **THEN** el proceso termina con código de salida 0 y genera `results/results.jtl` con al menos una fila de datos

#### Scenario: El archivo results.jtl es generado tras la ejecución
- **WHEN** la ejecución CLI de JMeter concluye
- **THEN** el archivo `results/results.jtl` existe en el workspace del runner con formato CSV válido

#### Scenario: El reporte HTML es generado tras la ejecución
- **WHEN** la ejecución CLI de JMeter concluye con flag `-e -o results/html-report/`
- **THEN** el directorio `results/html-report/` existe y contiene al menos el archivo `index.html`

---

### Requirement: Publicación de artefactos del pipeline siempre que la ejecución ocurra
El workflow SHALL publicar `results/results.jtl` y el directorio `results/html-report/` como artefactos descargables del pipeline usando `actions/upload-artifact@v4`, incluso si el step de validación de umbrales falla.

#### Scenario: Artefacto results.jtl publicado al terminar el pipeline
- **WHEN** el step de upload de `results.jtl` se ejecuta (con condición `if: always()`)
- **THEN** el artefacto `jmeter-jtl` queda disponible para descarga en la interfaz de GitHub Actions del run correspondiente

#### Scenario: Artefacto HTML report publicado al terminar el pipeline
- **WHEN** el step de upload del directorio `results/html-report/` se ejecuta (con condición `if: always()`)
- **THEN** el artefacto `jmeter-html-report` queda disponible para descarga en la interfaz de GitHub Actions del run correspondiente

#### Scenario: Artefactos publicados aunque la validación de umbrales falle
- **WHEN** el step `validate_thresholds.py` termina con código de salida distinto de 0
- **THEN** los steps de upload de artefactos se ejecutan igualmente y los artefactos quedan disponibles para diagnóstico
