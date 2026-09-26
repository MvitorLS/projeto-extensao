// Bracelete Inteligente ESP32 - Prática de Extensão III (IFPR Pinhais)
// Matheus Schionato e Vairtles Liel
//
// Lê a distância do obstáculo, aciona o motor de vibração e ENVIA a leitura
// ao celular via BLE (notify). Fluxo unidirecional ESP32 -> celular: a
// característica não aceita escrita, então o celular não comanda o bracelete.
//
// Placa: ESP32-C3 (padrão) ou ESP32 Dev Module | Core: esp32 by Espressif 3.x

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>

// No ESP32-C3 os GPIO 18/19 são o USB nativo e 2/8/9 são de boot
#if CONFIG_IDF_TARGET_ESP32C3
#define TRIG_PIN 3
#define ECHO_PIN 4
#define MOTOR_PIN 5
#define BOOT_PIN 9
#else
#define TRIG_PIN 5
#define ECHO_PIN 18
#define MOTOR_PIN 19
#define BOOT_PIN 0
#endif

// Modo demonstração: simula um obstáculo indo e voltando (200 -> 20 cm).
// Liga/desliga apertando o botão BOOT com a placa rodando.
bool demoMode = false;

#define DEVICE_NAME "Bracelete-ESP32"
#define SERVICE_UUID "309229c8-9c1c-477a-a03f-3384523c5ebc"
#define DIST_CHAR_UUID "09104702-68f7-4e84-b2d0-de4fe213ea52"

const int PWM_FREQ = 5000;
const int PWM_RES = 8;
const unsigned long NOTIFY_MS = 500;

BLECharacteristic *distChar;
bool connected = false;
bool lastBoot = HIGH;
int lastLevel = -1;
unsigned long lastNotify = 0;

class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *) override { connected = true; }
  void onDisconnect(BLEServer *) override {
    connected = false;
    BLEDevice::startAdvertising();
  }
};

// Troque esta função se o sensor mudar (ex.: VL53L0X); o resto não muda.
int demoDistanceCm() {
  const unsigned long PERIOD = 16000;
  long t = millis() % PERIOD;
  return 20 + labs(t - (long)PERIOD / 2) * 180 / (PERIOD / 2);
}

void checkBootButton() {
  bool now = digitalRead(BOOT_PIN);
  if (lastBoot == HIGH && now == LOW) {
    demoMode = !demoMode;
    Serial.printf("Modo demonstracao: %s\n", demoMode ? "LIGADO" : "DESLIGADO");
  }
  lastBoot = now;
}

int readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) return -1;
  return duration * 0.0343 / 2;
}

// 3 = muito perto, 2 = médio, 1 = alerta leve, 0 = livre
int levelFor(int cm) {
  if (cm <= 0) return 0;
  if (cm <= 50) return 3;
  if (cm <= 100) return 2;
  if (cm <= 150) return 1;
  return 0;
}

const int DUTY[] = {0, 80, 150, 255};

void setupBle() {
  BLEDevice::init(DEVICE_NAME);
  BLEServer *server = BLEDevice::createServer();
  server->setCallbacks(new ServerCallbacks());

  BLEService *service = server->createService(SERVICE_UUID);
  distChar = service->createCharacteristic(
      DIST_CHAR_UUID,
      BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);
  distChar->addDescriptor(new BLE2902());
  distChar->setValue("-1,0");
  service->start();

  BLEAdvertising *adv = BLEDevice::getAdvertising();
  adv->addServiceUUID(SERVICE_UUID);
  adv->setScanResponse(true);
  BLEDevice::startAdvertising();
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BOOT_PIN, INPUT_PULLUP);
  ledcAttach(MOTOR_PIN, PWM_FREQ, PWM_RES);
  setupBle();
  Serial.println("Bracelete pronto, anunciando via BLE como " DEVICE_NAME);
}

void loop() {
  checkBootButton();
  int cm = demoMode ? demoDistanceCm() : readDistanceCm();
  int level = levelFor(cm);
  ledcWrite(MOTOR_PIN, DUTY[level]);

  // Envia a cada NOTIFY_MS ou imediatamente quando o nível de alerta muda
  unsigned long now = millis();
  if (connected && (level != lastLevel || now - lastNotify >= NOTIFY_MS)) {
    String payload = String(cm) + "," + String(level) + "," + String(demoMode);
    distChar->setValue(payload.c_str());
    distChar->notify();
    lastNotify = now;
    lastLevel = level;
  }

  Serial.printf("dist=%d cm nivel=%d%s\n", cm, level, demoMode ? " [demo]" : "");
  delay(100);
}
