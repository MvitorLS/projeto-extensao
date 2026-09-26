# PROJECT_MEMORY — projeto-extensao

- Bracelete ESP32 p/ baixa visão (Práticas de Extensão III/V, IFPR Pinhais). Autores: Matheus Schionato + Vairtles Liel; orientador Alvaro Cantieri.
- `Pratica 3/`: proposta LaTeX abnTeX2 (`proposta_main.tex`), compila com `compilar_linux.sh`. `Pratica 5/` ainda é cópia da estrutura.
- Comunicação **ESP32 -> celular apenas**, via BLE notify (ESP32 = GATT server/periférico). Característica só READ|NOTIFY, sem WRITE: celular não comanda o bracelete.
  - Service `309229c8-9c1c-477a-a03f-3384523c5ebc`, char `09104702-68f7-4e84-b2d0-de4fe213ea52`, payload texto `"<cm>,<nivel>,<demo>"` (nível 0 livre .. 3 muito perto; cm=-1 sem leitura).
  - Notifica a cada 500 ms ou na troca de nível.
  - Firmware: `Pratica 3/firmware/bracelete_ble/`, gravar com `firmware/gravar.sh` (arduino-cli em ~/.local/bin). Placa real = **ESP32-C3** (USB nativo /dev/ttyACM0, 4MB, MAC 70:af:09:01:5c:3c), FQBN `esp32:esp32:esp32c3:CDCOnBoot=cdc` (sem CDCOnBoot o Serial não sai pela USB). Pinos C3: TRIG 3, ECHO 4, MOTOR 5 (18/19 = USB; 2/8/9 = strapping). Gravado e rodando em 2026-09-26.
  - Receptor: `Pratica 3/app-web/index.html` (Web Bluetooth: Chrome Android, publicado em https://mvitorls.github.io/projeto-extensao/Pratica%203/app-web/ (Pages da main, raiz; `.nojekyll` obrigatório — Jekyll quebra com os .md do repo); fala via speechSynthesis + vibra). iOS não suporta (usar app Bluefy).
- Sensor ainda indefinido: esquema técnico sem ultrassom, mas firmware/anexos usam HC-SR04 (pinos do ESP32 clássico nos anexos: 5/18/19 — desatualizados para o C3). Trocar só `readDistanceCm()`.
- Modo demonstração: botão BOOT (GPIO9 no C3, GPIO0 no clássico) liga/desliga em tempo de execução; simula obstáculo 200->20->200 cm em 16 s. Payload ganha 3º campo `demo` (0/1): `"<cm>,<nivel>,<demo>"`; página mostra "MODO DEMONSTRAÇÃO". Sempre inicia desligado.
- Página: cm<=0 é anunciado como "Sensor sem leitura", nunca "Caminho livre" (segurança).
