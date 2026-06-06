## ADDED Requirements

### Requirement: Conversión de InformeResultados.md a DOCX
El sistema SHALL proporcionar un mecanismo reproducible para convertir `reports/InformeResultados.md` a `reports/InformeResultados.docx` mediante pandoc CLI, preservando tablas GFM, bloques de código y énfasis presentes en el archivo fuente.

#### Scenario: Conversión exitosa con pandoc disponible
- **WHEN** el usuario ejecuta `bash reports/convert_to_docx.sh` en un entorno donde pandoc está instalado
- **THEN** el sistema genera `reports/InformeResultados.docx` con estructura y contenido equivalente al Markdown fuente

#### Scenario: Fidelidad estructural del documento generado
- **WHEN** se genera `reports/InformeResultados.docx`
- **THEN** el archivo `.docx` SHALL contener todas las tablas, encabezados, bloques de código y énfasis presentes en `reports/InformeResultados.md`

### Requirement: Script de conversión ejecutable
El sistema SHALL incluir `reports/convert_to_docx.sh`, un script de shell que encapsula el comando pandoc exacto para la conversión, permitiendo reproducción sin necesidad de recordar flags individuales.

#### Scenario: Ejecución del script genera el DOCX
- **WHEN** el usuario ejecuta `bash reports/convert_to_docx.sh` desde la raíz del repositorio
- **THEN** el script invoca pandoc con los parámetros correctos (`-f markdown -t docx -o reports/InformeResultados.docx reports/InformeResultados.md`) y produce el archivo de salida

#### Scenario: El script no modifica el archivo fuente
- **WHEN** el usuario ejecuta `bash reports/convert_to_docx.sh`
- **THEN** `reports/InformeResultados.md` SHALL permanecer sin cambios en contenido ni metadatos

### Requirement: Verificación de dependencia pandoc
El script `convert_to_docx.sh` SHALL verificar la presencia del binario pandoc antes de ejecutar la conversión e imprimir instrucciones de instalación si no está disponible.

#### Scenario: pandoc no está instalado
- **WHEN** el usuario ejecuta `bash reports/convert_to_docx.sh` y pandoc no está en el PATH
- **THEN** el script SHALL terminar con código de salida distinto de cero e imprimir un mensaje indicando cómo instalar pandoc (ej. `brew install pandoc` para macOS)

#### Scenario: pandoc está instalado
- **WHEN** el usuario ejecuta `bash reports/convert_to_docx.sh` y pandoc está disponible en el PATH
- **THEN** el script SHALL proceder con la conversión sin emitir advertencias sobre la dependencia

### Requirement: Versionado de textSummary.txt como fuente de datos
El sistema SHALL incluir `reports/textSummary.txt` (salida original de K6) como artefacto versionado en el repositorio, garantizando trazabilidad completa entre los datos fuente y el contenido del informe.

#### Scenario: Archivo textSummary.txt disponible en el repositorio
- **WHEN** un revisor clona o navega el repositorio
- **THEN** `reports/textSummary.txt` SHALL estar presente y contener las métricas de ejecución K6 que sustentan los hallazgos de `reports/InformeResultados.md`

#### Scenario: Coherencia entre textSummary.txt e InformeResultados.md
- **WHEN** se comparan las métricas referenciadas en `reports/InformeResultados.md`
- **THEN** los valores numéricos SHALL corresponder con los registros presentes en `reports/textSummary.txt`
