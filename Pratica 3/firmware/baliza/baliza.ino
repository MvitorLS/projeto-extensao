// Baliza BLE para o Bracelete Inteligente ESP32
// Grave em um ESP32 extra e fixe-o no ponto de interesse (porta, escada...).
// Ela só anuncia o próprio nome; o bracelete mede a distância pelo sinal.
//
// Placa: ESP32-C3 (padrão) ou ESP32 Dev Module | Core: esp32 by Espressif 3.x

#include <BLEDevice.h>

// Nome falado pelo celular. Máx. 15 caracteres, sem vírgula.
#define NOME_BALIZA "Escada"

void setup() {
  Serial.begin(115200);
  BLEDevice::init("BALIZA-" NOME_BALIZA);
  BLEDevice::setPower(ESP_PWR_LVL_N0);  // potência fixa para a estimativa de distância ser estável
  BLEAdvertising *adv = BLEDevice::getAdvertising();
  adv->setScanResponse(true);
  adv->setMinInterval(160);  // 100 ms
  adv->setMaxInterval(160);
  BLEDevice::startAdvertising();
  Serial.println("Baliza anunciando como BALIZA-" NOME_BALIZA);
}

void loop() {
  delay(1000);
}
