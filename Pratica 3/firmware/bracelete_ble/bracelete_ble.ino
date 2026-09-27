// Bracelete Inteligente ESP32 - Prática de Extensão III (IFPR Pinhais)
// Matheus Schionato e Vairtles Liel
//
// Sem sensor de distância: o bracelete escuta balizas BLE (aparelhos cujo nome
// começa com "BALIZA-", ex.: "BALIZA-Porta") espalhadas pela sala, estima a
// distância de cada uma pela intensidade do sinal (RSSI), vibra conforme a mais
// próxima e ENVIA todas ao celular via BLE (notify) para orientação.
// Fluxo unidirecional ESP32 -> celular: a característica não aceita escrita.
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
// Anúncios se perdem enquanto o rádio atende o celular: tolera alguns segundos
const unsigned long BEACON_TIMEOUT_MS = 6000;

// Modelo log-distância: RSSI medido a 1 m e expoente do ambiente (2 = aberto,
// 3 = interno com obstáculos). Calibrar com a baliza real a 1 m.
const float RSSI_1M = -59.0;
const float PATH_LOSS_N = 2.5;
const float RSSI_ALPHA = 0.15;  // suavização da média móvel exponencial

struct Beacon {
  char name[16];
  float rssi;
  unsigned long lastSeen;
};

struct Point {
  char name[16];
  int cm;
  int rssi;
};

const int MAX_BEACONS = 8;
Beacon beacons[MAX_BEACONS];
portMUX_TYPE beaconsMux = portMUX_INITIALIZER_UNLOCKED;

// Modo demonstração: simula três balizas se movendo pela sala.
// Liga/desliga apertando o botão BOOT com a placa rodando.
volatile bool demoMode = false;
volatile unsigned long lastPress = 0;

BLEServer *server;
BLECharacteristic *distChar;
bool connected = false;
unsigned long lastNotify = 0;
int motorLevel = 0;

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
    name.replace(",", " ");
    name.replace(";", " ");
    name.replace(":", " ");
    name.replace("|", " ");
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

int demoCm(unsigned long period, int minCm, int maxCm, unsigned long offset) {
  long t = (millis() + offset) % period;
  return minCm + labs(t - (long)period / 2) * (maxCm - minCm) / (period / 2);
}

// Balizas vistas nos últimos segundos, da mais próxima para a mais distante
int visiblePoints(Point *out) {
  int n = 0;
  if (demoMode) {
    const char *names[] = {"Porta", "Mesa", "Janela"};
    int cms[] = {demoCm(20000, 50, 600, 0), demoCm(14000, 80, 400, 5000), demoCm(26000, 150, 700, 9000)};
    for (int i = 0; i < 3; i++) {
      strlcpy(out[n].name, names[i], sizeof(out[n].name));
      out[n].rssi = 0;
      out[n++].cm = cms[i];
    }
  } else {
    unsigned long now = millis();
    float rssi[MAX_BEACONS];
    portENTER_CRITICAL(&beaconsMux);
    for (int i = 0; i < MAX_BEACONS; i++) {
      if (!beacons[i].lastSeen || now - beacons[i].lastSeen > BEACON_TIMEOUT_MS) continue;
      strlcpy(out[n].name, beacons[i].name, sizeof(out[n].name));
      rssi[n++] = beacons[i].rssi;
    }
    portEXIT_CRITICAL(&beaconsMux);
    for (int i = 0; i < n; i++) {
      out[i].rssi = rssi[i];
      out[i].cm = rssiToCm(rssi[i]);
    }
  }
  for (int i = 1; i < n; i++)
    for (int j = i; j > 0 && out[j].cm < out[j - 1].cm; j--) {
      Point tmp = out[j]; out[j] = out[j - 1]; out[j - 1] = tmp;
    }
  return n;
}

// 3 = até 1 m, 2 = até 2 m, 1 = até 4 m, 0 = longe.
// Histerese: para afastar de nível precisa passar 25% do limite, senão o
// ruído do RSSI faz a vibração ficar alternando na fronteira.
const int LIMITS[] = {400, 200, 100};

int levelWithHysteresis(int cm, int current) {
  int level = 0;
  for (int i = 0; i < 3; i++) if (cm <= LIMITS[i]) level = i + 1;
  if (level < current && cm <= LIMITS[current - 1] * 1.25) return current;
  return level;
}

const int DUTY[] = {0, 80, 150, 255};

void setupBle() {
  BLEDevice::init(DEVICE_NAME);
  BLEDevice::setMTU(247);  // cabe a lista de balizas numa notificação
  server = BLEDevice::createServer();
  server->setCallbacks(new ServerCallbacks());

  BLEService *service = server->createService(SERVICE_UUID);
  distChar = service->createCharacteristic(
      DIST_CHAR_UUID,
      BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);
  distChar->addDescriptor(new BLE2902());
  distChar->setValue("0|");
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
  Point points[MAX_BEACONS];
  int n = visiblePoints(points);
  motorLevel = n ? levelWithHysteresis(points[0].cm, motorLevel) : 0;
  ledcWrite(MOTOR_PIN, DUTY[motorLevel]);

  // Payload: "<demo>|Nome:cm;Nome:cm;..." (mais próxima primeiro), limitado ao MTU
  String payload = String(demoMode ? 1 : 0) + "|";
  unsigned long now = millis();
  if (connected && now - lastNotify >= NOTIFY_MS) {
    size_t maxLen = server->getPeerMTU(server->getConnId()) - 3;
    for (int i = 0; i < n; i++) {
      String item = String(i ? ";" : "") + points[i].name + ":" + points[i].cm;
      if (payload.length() + item.length() > maxLen) break;
      payload += item;
    }
    distChar->setValue(payload.c_str());
    distChar->notify();
    lastNotify = now;
  }

  if (n == 0) Serial.println("nenhuma baliza");
  else {
    // RSSI bruto (média) para calibrar RSSI_1M: coloque a baliza a 1 m e copie o valor
    for (int i = 0; i < n; i++) Serial.printf("%s~%dcm(%ddBm) ", points[i].name, points[i].cm, points[i].rssi);
    Serial.printf("| motor=%d%s\n", motorLevel, demoMode ? " [demo]" : "");
  }
  delay(200);
}
