## 1. Prerequisitos

- [x] 1.1 Verificar que pandoc está instalado ejecutando `pandoc --version`
- [x] 1.2 Instalar pandoc si no está disponible: `brew install pandoc` (macOS)

## 2. Crear el script de conversión

- [x] 2.1 Crear `reports/convert_to_docx.sh` con verificación del binario pandoc e instrucciones de instalación si falta
- [x] 2.2 Incluir en el script el comando exacto: `pandoc -f markdown -t docx -o reports/InformeResultados.docx reports/InformeResultados.md`
- [x] 2.3 Dar permisos de ejecución al script: `chmod +x reports/convert_to_docx.sh`

## 3. Ejecutar y verificar la conversión

- [x] 3.1 Ejecutar `bash reports/convert_to_docx.sh` desde la raíz del repositorio
- [x] 3.2 Verificar que `reports/InformeResultados.docx` fue generado
- [x] 3.3 Abrir el `.docx` y confirmar que tablas, encabezados, bloques de código y énfasis están presentes
- [x] 3.4 Confirmar que `reports/InformeResultados.md` no fue modificado (contenido ni metadatos)

## 4. Trazabilidad de datos fuente

- [x] 4.1 Confirmar que `reports/textSummary.txt` existe en el repositorio
- [x] 4.2 Verificar que los valores numéricos en `reports/textSummary.txt` corresponden con las métricas referenciadas en `reports/InformeResultados.md`

## 5. Commit de artefactos

- [x] 5.1 Decidir si `reports/InformeResultados.docx` se versiona o se añade a `.gitignore`
- [x] 5.2 Hacer commit de `reports/convert_to_docx.sh` y `reports/textSummary.txt`
- [x] 5.3 Incluir en el commit `reports/InformeResultados.docx` si se decidió versionarlo
