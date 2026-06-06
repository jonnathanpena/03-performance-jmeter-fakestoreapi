## Why

El informe `reports/InformeResultados.md` está completo en contenido técnico pero existe únicamente en formato Markdown. Para entrega formal a stakeholders, clientes o integración en repositorios de documentación corporativa se requiere formato `.docx`, ya que Markdown no es universalmente legible en flujos de trabajo empresariales sin herramientas de conversión instaladas.

Adicionalmente, el archivo fuente `textSummary.txt` (salida de K6) no estaba versionado en el repositorio, lo que impedía trazabilidad completa de los datos que sustentan el informe.

## What Changes

- Generación de `reports/InformeResultados.docx` a partir de `reports/InformeResultados.md` usando pandoc.
- Adición de `reports/textSummary.txt` al repositorio como fuente de datos k6 versionada.
- Script de conversión (`reports/convert_to_docx.sh`) para reproducibilidad del proceso.

## Capabilities

### New Capabilities

- `docx-report-generation`: Pipeline de conversión automatizada de `InformeResultados.md` a `InformeResultados.docx` mediante pandoc CLI, con script reproducible y artefacto `.docx` versionado.

### Modified Capabilities

(ninguna)

## Impact

- **Archivos nuevos:** `reports/InformeResultados.docx`, `reports/textSummary.txt`, `reports/convert_to_docx.sh`
- **Dependencia externa:** pandoc (CLI) — debe estar instalado en el entorno de ejecución.
- **Sin cambios** al contenido de `reports/InformeResultados.md` ni al plan de prueba JMeter.
