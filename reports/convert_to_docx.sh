#!/usr/bin/env bash
set -euo pipefail

if ! command -v pandoc &> /dev/null; then
  echo "Error: pandoc no está instalado."
  echo "Instálalo con: brew install pandoc  (macOS)"
  echo "               sudo apt-get install pandoc  (Debian/Ubuntu)"
  exit 1
fi

pandoc -f markdown -t docx -o reports/InformeResultados.docx reports/InformeResultados.md

echo "Conversión completada: reports/InformeResultados.docx"
