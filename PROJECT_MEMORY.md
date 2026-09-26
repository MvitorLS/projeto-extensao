# PROJECT_MEMORY — projeto-extensao

- Bracelete ESP32 p/ baixa visão (Práticas de Extensão III/V, IFPR Pinhais). Autores: Matheus Schionato + Vairtles Liel; orientador Alvaro Cantieri.
- `Pratica 3/`: proposta LaTeX abnTeX2 (`proposta_main.tex`), compila com `compilar_linux.sh`. `Pratica 5/` ainda é cópia da estrutura.
- Comunicação **ESP32 -> celular apenas**, via BLE notify (ESP32 = GATT server/periférico). Característica só READ|NOTIFY, sem WRITE: celular não comanda o bracelete.
  - Service `309229c8-9c1c-477a-a03f-3384523c5ebc`, char `09104702-68f7-4e84-b2d0-de4fe213ea52`, payload texto `"<cm>,<nivel>"` (nível 0 livre .. 3 muito perto; cm=-1 sem leitura).
  - Notifica a cada 500 ms ou na troca de nível.
  - Firmware: `Pratica 3/firmware/bracelete_ble/` (core esp32 3.x: `ledcAttach`/`ledcWrite(pin,...)`, sem `ledcSetup`). Compilado OK com esp32 3.3.11 (84% flash).
  - Receptor: `Pratica 3/app-web/index.html` (Web Bluetooth: Chrome Android, exige HTTPS/localhost → GitHub Pages; fala via speechSynthesis + vibra). iOS não suporta (usar app Bluefy).
- Sensor ainda indefinido: esquema técnico sem ultrassom, mas firmware/anexos usam HC-SR04 (GPIO5 trig, 18 echo, 19 motor). Trocar só `readDistanceCm()`.
