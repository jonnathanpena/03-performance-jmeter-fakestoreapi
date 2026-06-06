## Context

`reports/InformeResultados.md` contiene el análisis completo de los resultados de rendimiento (K6/JMeter) para FakeStoreAPI, pero solo existe como archivo Markdown. Los flujos de entrega corporativos y los stakeholders del reto Sofka esperan documentación en `.docx`, formato ampliamente soportado sin dependencias de herramientas de renderizado. La fuente de datos `textSummary.txt` (salida K6) tampoco estaba versionada, lo que rompe la trazabilidad.

El cambio es local al directorio `reports/` y no toca el plan de prueba JMeter ni el contenido del informe.

## Goals / Non-Goals

**Goals:**
- Generar `reports/InformeResultados.docx` a partir de `reports/InformeResultados.md` de forma reproducible.
- Proveer un script de conversión (`reports/convert_to_docx.sh`) ejecutable en cualquier entorno con pandoc instalado.
- Versionar `reports/textSummary.txt` para trazabilidad completa de los datos fuente.

**Non-Goals:**
- Modificar el contenido o estructura de `reports/InformeResultados.md`.
- Establecer un pipeline CI/CD automatizado para la conversión.
- Dar soporte a otros formatos de salida (PDF, HTML, etc.).
- Instalar o gestionar dependencias del sistema (pandoc).

## Decisions

### D1 — Usar pandoc como conversor Markdown → DOCX

**Decisión:** pandoc CLI.

**Rationale:** pandoc es el estándar de facto para conversión de documentos técnicos. Soporta Markdown extendido (tablas, bloques de código, énfasis) que aparece en `InformeResultados.md`, produce `.docx` con fidelidad estructural y es fácilmente integrable en scripts de shell. No requiere runtime adicional (Python, Java, Node).

**Alternativas descartadas:**
- `python-docx` con parser Markdown manual → mayor complejidad de implementación, riesgo de pérdida de formato.
- LibreOffice `--headless --convert-to docx` → convierte desde ODT/HTML, no desde Markdown nativo; introduces una conversión intermedia con pérdida de fidelidad.
- Extensión VS Code / pandoc GUI → no reproducible en entornos headless.

### D2 — Script Bash (`convert_to_docx.sh`) como punto de entrada

**Decisión:** script shell minimalista que envuelve el comando pandoc.

**Rationale:** un script en `reports/` auto-documentado centraliza el comando exacto, permite añadir opciones de referencia de estilo en el futuro (`--reference-doc`) y evita que el usuario tenga que recordar flags de pandoc. Bash es suficiente dado que el entorno objetivo es macOS/Linux.

**Alternativas descartadas:**
- Makefile → overhead de configuración para un único objetivo.
- Script Python → innecesario para un wrapper de CLI.

### D3 — Versionar `textSummary.txt` directamente en `reports/`

**Decisión:** commit del archivo tal cual como fuente de datos.

**Rationale:** el informe hace referencia explícita a métricas de ese archivo; versionarlo en el mismo directorio que el informe garantiza que cualquier revisión futura del `.docx` pueda verificarse contra los datos originales sin acceso a un entorno de ejecución K6.

## Risks / Trade-offs

- **pandoc no instalado en el entorno** → el script falla con error claro. Mitigación: el README debe documentar `brew install pandoc` (macOS) como prerequisito; el script puede verificar la presencia del binario e imprimir instrucciones si falta.
- **Fidelidad de formato** → pandoc respeta tablas GFM y bloques de código, pero estilos visuales (fuentes, colores) usarán el estilo DOCX por defecto. Mitigación: aceptable para entrega técnica; se puede añadir `--reference-doc` en el futuro si se requiere identidad corporativa.
- **Artefacto binario `.docx` en git** → los archivos `.docx` son binarios y no se visualizan en diffs. Mitigación: el `.md` fuente permanece como fuente de verdad; el `.docx` es artefacto de salida. Se puede añadir al `.gitignore` si el equipo prefiere no versionar binarios, regenerándolo bajo demanda con el script.

## Migration Plan

1. Verificar que pandoc está instalado: `pandoc --version`.
2. Crear `reports/convert_to_docx.sh` con el comando de conversión.
3. Ejecutar el script: `bash reports/convert_to_docx.sh`.
4. Verificar que `reports/InformeResultados.docx` fue generado y abre correctamente.
5. Hacer commit de `textSummary.txt`, `convert_to_docx.sh` e `InformeResultados.docx`.

**Rollback:** sin impacto — el `.md` original no se modifica. Si el `.docx` no es satisfactorio, se puede eliminar y regenerar ajustando opciones del script.

## Open Questions

- ¿Se debe añadir `InformeResultados.docx` al `.gitignore` y tratarlo como artefacto no versionado, o versionarlo para entrega inmediata? (Por defecto: versionado para facilitar la entrega del reto.)
- ¿Se requiere un estilo corporativo Sofka (`--reference-doc sofka-style.docx`)? Si es así, se necesita un archivo de referencia que no está disponible actualmente.
