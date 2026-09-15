// ==============================================================================
// PROJETO: Bracelete Inteligente ESP32 - Prática de Extensão III
// AUTORES: Matheus Schionato e Vairtles Liel
// DESCRIÇÃO: Código do protótipo para leitura do sensor HC-SR04 e 
//            acionamento de motor de vibração (feedback háptico) via PWM.
// ==============================================================================

#define TRIG_PIN 5
#define ECHO_PIN 18
#define MOTOR_PIN 19

// Configurações do PWM (ESP32)
const int freq = 5000;
const int motorChannel = 0;
const int resolution = 8; // Variação de 0 a 255

void setup() {
  // Inicializa comunicação serial para debug
  Serial.begin(115200);
  
  // Configura pinos do sensor ultrassônico
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  // Configura o canal PWM para o motor de vibração (feedback tátil)
  ledcSetup(motorChannel, freq, resolution);
  ledcAttachPin(MOTOR_PIN, motorChannel);
  
  Serial.println("Iniciando Sistema do Bracelete Inteligente...");
}

void loop() {
  // 1. Dispara o pulso ultrassônico
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  // 2. Calcula o tempo de retorno do eco
  long duration = pulseIn(ECHO_PIN, HIGH);
  
  // 3. Converte tempo para centímetros (velocidade do som = 343 m/s)
  float distance = (duration * 0.0343) / 2;
  
  Serial.print("Distância do obstáculo aéreo: ");
  Serial.print(distance);
  Serial.println(" cm");
  
  // 4. Lógica de Feedback Háptico (Vibração Proporcional)
  if (distance > 0 && distance <= 50) {
    // Muito perto (0 a 50cm): Vibração Máxima
    ledcWrite(motorChannel, 255);
  } 
  else if (distance > 50 && distance <= 100) {
    // Média distância (50 a 100cm): Vibração Média
    ledcWrite(motorChannel, 150);
  }
  else if (distance > 100 && distance <= 150) {
    // Alerta leve (100 a 150cm): Vibração Fraca
    ledcWrite(motorChannel, 80);
  } 
  else {
    // Caminho livre (Acima de 1.5 metros): Sem vibração
    ledcWrite(motorChannel, 0);
  }
  
  // Pausa antes da próxima varredura (10 leituras por segundo)
  delay(100); 
}
