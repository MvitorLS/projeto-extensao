#!/usr/bin/env bash
# Compila, grava no ESP32 e abre o monitor serial. Uso: ./gravar.sh [porta]
# Placa padrão ESP32-C3; para ESP32 clássico: FQBN=esp32:esp32:esp32 ./gravar.sh
set -euo pipefail
cd "$(dirname "$0")"
PORTA="${1:-$(ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | head -n1 || true)}"
[ -z "$PORTA" ] && { echo "ESP32 não encontrado. Conecte o cabo USB (de dados, não só carga)."; exit 1; }
FQBN="${FQBN:-esp32:esp32:esp32c3:CDCOnBoot=cdc}"
echo "Usando porta $PORTA ($FQBN)"
arduino-cli compile --fqbn "$FQBN" bracelete_ble
arduino-cli upload --fqbn "$FQBN" -p "$PORTA" bracelete_ble
arduino-cli monitor -p "$PORTA" -c baudrate=115200
