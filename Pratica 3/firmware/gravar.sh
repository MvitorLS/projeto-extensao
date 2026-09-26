#!/usr/bin/env bash
# Compila, grava no ESP32 e abre o monitor serial. Uso: ./gravar.sh [porta]
set -euo pipefail
cd "$(dirname "$0")"
PORTA="${1:-$(ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | head -n1 || true)}"
[ -z "$PORTA" ] && { echo "ESP32 não encontrado. Conecte o cabo USB (de dados, não só carga)."; exit 1; }
echo "Usando porta $PORTA"
arduino-cli compile --fqbn esp32:esp32:esp32 bracelete_ble
arduino-cli upload --fqbn esp32:esp32:esp32 -p "$PORTA" bracelete_ble
arduino-cli monitor -p "$PORTA" -c baudrate=115200
