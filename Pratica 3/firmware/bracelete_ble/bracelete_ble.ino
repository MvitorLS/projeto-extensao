// Bracelete Inteligente ESP32 - Prática de Extensão III (IFPR Pinhais)
// Matheus Schionato e Vairtles Liel
//
// Sem sensor de distância: o bracelete escuta balizas BLE (aparelhos cujo nome
// começa com "BALIZA-", ex.: "BALIZA-Escada") presas em pontos de interesse,
// estima a distância pela intensidade do sinal (RSSI), vibra e ENVIA a baliza
// mais próxima ao celular via BLE (notify). Fluxo unidirecional ESP32 -> celular:
// a característica não aceita escrita, então o celular não comanda o bracelete.
//
// Placa: ESP32-C3 (padrão) ou ESP32 Dev Module | Core: esp32 by Espressif 3.x

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEScan.h>
#include <BLE2902.h>

// No ESP32-C3 os GPIO 18/19 são o USB nativo e 2/8/9 são de boot
#if CONFIG_IDF_TARGET_ESP32C3
#define MOTOR_PIN 5
#define BOOT_PIN 9
#else
#define MOTOR_PIN 19
#define BOOT_PIN 0
#endif

#define DEVICE_NAME "Bracelete-ESP32"
#define SERVICE_UUID "309229c8-9c1c-477a-a03f-3384523c5ebc"
#define DIST_CHAR_UUID "09104702-68f7-4e84-b2d0-de4fe213ea52"
#define BEACON_PREFIX "BALIZA-"

const int PWM_FREQ = 5000;
const int PWM_RES = 8;
const unsigned long NOTIFY_MS = 500;
const unsigned long BEACON_TIMEOUT_MS = 3000;

// Modelo log-distância: RSSI medido a 1 m e expoente do ambiente (2 = aberto,
// 3 = interno com obstáculos). Calibrar com a baliza real a 1 m.
const float RSSI_1M = -59.0;
const float PATH_LOSS_N = 2.5;
const float RSSI_ALPHA = 0.3;  // suavização da média móvel exponencial

struct Beacon {
  char name[16];
  float rssi;
  unsigned long lastSeen;
};

const int MAX_BEACONS = 8;
Beacon beacons[MAX_BEACONS];
portMUX_TYPE beaconsMux = portMUX_INITIALIZER_UNLOCKED;

// Modo demonstração: simula a "BALIZA-Escada" indo e voltando (6 m -> 0,3 m).
// Liga/desliga apertando o botão BOOT com a placa rodando.
volatile bool demoMode = false;
volatile unsigned long lastPress = 0;

BLECharacteristic *distChar;
bool connected = false;
String lastKey = "";
unsigned long lastNotify = 0;

class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *) override { connected = true; }
  void onDisconnect(BLEServer *) override {
    connected = false;
    BLEDevice::startAdvertising();
  }
};

class ScanCallbacks : public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice dev) override {
    if (!dev.haveName()) return;
    String full = dev.getName();
    if (!full.startsWith(BEACON_PREFIX)) return;
    String name = full.substring(strlen(BEACON_PREFIX));
    int rssi = dev.getRSSI();
    unsigned long now = millis();

    portENTER_CRITICAL(&beaconsMux);
    int slot = -1, oldest = 0;
    for (int i = 0; i < MAX_BEACONS; i++) {
      if (beacons[i].lastSeen && name.equals(beacons[i].name)) { slot = i; break; }
      if (beacons[i].lastSeen < beacons[oldest].lastSeen) oldest = i;
    }
    if (slot < 0) {
      slot = oldest;
      strlcpy(beacons[slot].name, name.c_str(), sizeof(beacons[slot].name));
      beacons[slot].rssi = rssi;
    } else {
      beacons[slot].rssi += RSSI_ALPHA * (rssi - beacons[slot].rssi);
    }
    beacons[slot].lastSeen = now;
    portEXIT_CRITICAL(&beaconsMux);
  }
};

// Interrupção: o loop fica bloqueado em delay e perderia toques rápidos
void IRAM_ATTR onBootPress() {
  unsigned long now = millis();
  if (now - lastPress > 300) {
    demoMode = !demoMode;
    lastPress = now;
  }
}

int rssiToCm(float rssi) {
  return 100 * pow(10, (RSSI_1M - rssi) / (10 * PATH_LOSS_N));
}

// Baliza visível mais próxima; false se nenhuma foi vista nos últimos segundos
bool nearestBeacon(String &name, int &cm) {
  if (demoMode) {
    const unsigned long PERIOD = 16000;
    long t = millis() % PERIOD;
    name = "Escada";
    cm = 30 + labs(t - (long)PERIOD / 2) * 570 / (PERIOD / 2);
    return true;
  }
  unsigned long now = millis();
  int best = -1;
  char bestName[16];
  float bestRssi = 0;
  portENTER_CRITICAL(&beaconsMux);
  for (int i = 0; i < MAX_BEACONS; i++) {
    if (!beacons[i].lastSeen || now - beacons[i].lastSeen > BEACON_TIMEOUT_MS) continue;
    if (best < 0 || beacons[i].rssi > beacons[best].rssi) best = i;
  }
  if (best >= 0) {
    strlcpy(bestName, beacons[best].name, sizeof(bestName));
    bestRssi = beacons[best].rssi;
  }
  portEXIT_CRITICAL(&beaconsMux);
  if (best < 0) return false;
  name = bestName;
  cm = rssiToCm(bestRssi);
  return true;
}

// 3 = até 1 m, 2 = até 2 m, 1 = até 4 m, 0 = longe
int levelFor(int cm) {
  if (cm <= 0) return 0;
  if (cm <= 100) return 3;
  if (cm <= 200) return 2;
  if (cm <= 400) return 1;
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
  distChar->setValue(",-1,0,0");
  service->start();

  BLEAdvertising *adv = BLEDevice::getAdvertising();
  adv->addServiceUUID(SERVICE_UUID);
  adv->setScanResponse(true);
  BLEDevice::startAdvertising();

  // Varredura contínua com janela de 50% para sobrar rádio à conexão do celular
  BLEScan *scan = BLEDevice::getScan();
  scan->setAdvertisedDeviceCallbacks(new ScanCallbacks(), true);
  scan->setActiveScan(true);
  scan->setInterval(160);
  scan->setWindow(80);
  scan->start(0, nullptr, false);
}

void setup() {
  Serial.begin(115200);
  pinMode(BOOT_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BOOT_PIN), onBootPress, FALLING);
  ledcAttach(MOTOR_PIN, PWM_FREQ, PWM_RES);
  setupBle();
  Serial.println("Bracelete pronto, anunciando via BLE como " DEVICE_NAME);
}

void loop() {
  String name = "";
  int cm = -1;
  bool found = nearestBeacon(name, cm);
  int level = found ? levelFor(cm) : 0;
  ledcWrite(MOTOR_PIN, DUTY[level]);

  // Envia a cada NOTIFY_MS ou imediatamente quando baliza/nível mudam
  String key = name + level;
  unsigned long now = millis();
  if (connected && (key != lastKey || now - lastNotify >= NOTIFY_MS)) {
    String payload = name + "," + String(cm) + "," + String(level) + "," + String(demoMode);
    distChar->setValue(payload.c_str());
    distChar->notify();
    lastNotify = now;
    lastKey = key;
  }

  if (found) Serial.printf("baliza=%s dist~%d cm nivel=%d%s\n", name.c_str(), cm, level, demoMode ? " [demo]" : "");
  else Serial.println("nenhuma baliza");
  delay(200);
}
