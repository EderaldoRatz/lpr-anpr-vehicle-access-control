// ESP32 License Plate Recognition Gate Controller
// Controla abertura de portão com sensor de presença e feedback serial

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ============ CONFIGURAÇÕES ============
#define RELAY_PIN 5           // Pino do relé (portão)
#define SENSOR_PIN 34         // Pino do sensor analógico
#define LED_STATUS 2          // LED indicador
#define BUZZER_PIN 4          // Buzzer

// WiFi
const char* SSID = "seu_wifi";
const char* PASSWORD = "sua_senha_wifi";
const char* API_URL = "http://192.168.1.100:8000/api";

// Variáveis de controle
bool gateOpen = false;
unsigned long gateOpenTime = 0;
const unsigned long GATE_DURATION = 5000;     // 5 segundos
const int SENSOR_THRESHOLD = 2000;             // Limite do sensor

// ============ SETUP ============
void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(SENSOR_PIN, INPUT);
  
  // Estado inicial
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(LED_STATUS, LOW);
  
  delay(1000);
  Serial.println("\n\n=== ESP32 Gate Controller ===");
  Serial.println("Iniciando sistema...");
  
  connectToWiFi();
  
  Serial.println("✅ Sistema pronto!");
  beep(1);
}

// ============ LOOP PRINCIPAL ============
void loop() {
  // Verificar sensor de presença
  int sensorValue = analogRead(SENSOR_PIN);
  
  // Se detecta veículo e portão fechado
  if (sensorValue > SENSOR_THRESHOLD && !gateOpen) {
    Serial.println("\n🚗 Veículo detectado!");
    beep(2);
    openGate();
  }
  
  // Fechar portão após duration
  if (gateOpen && (millis() - gateOpenTime > GATE_DURATION)) {
    closeGate();
  }
  
  // Status LED
  digitalWrite(LED_STATUS, gateOpen ? HIGH : LOW);
  
  delay(100);
}

// ============ CONECTAR WiFi ============
void connectToWiFi() {
  Serial.print("\nConectando ao WiFi: ");
  Serial.println(SSID);
  
  WiFi.begin(SSID, PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ Falha ao conectar WiFi");
  }
}

// ============ ABRIR PORTÃO ============
void openGate() {
  digitalWrite(RELAY_PIN, HIGH);
  gateOpen = true;
  gateOpenTime = millis();
  
  Serial.println("🟢 PORTÃO ABERTO");
  beep(1);
  
  // Enviar para API
  sendStatusToAPI("open");
}

// ============ FECHAR PORTÃO ============
void closeGate() {
  digitalWrite(RELAY_PIN, LOW);
  gateOpen = false;
  
  Serial.println("🔴 PORTÃO FECHADO");
  beep(3);
  
  // Enviar para API
  sendStatusToAPI("closed");
}

// ============ BUZZER ============
void beep(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);
  }
}

// ============ ENVIAR STATUS PARA API ============
void sendStatusToAPI(String status) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ WiFi não conectado");
    return;
  }
  
  HTTPClient http;
  String url = String(API_URL) + "/hardware/status";
  
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  // Criar JSON
  StaticJsonDocument<200> doc;
  doc["gate"] = status;
  doc["sensor"] = analogRead(SENSOR_PIN);
  doc["timestamp"] = millis();
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpCode = http.POST(jsonString);
  
  if (httpCode > 0) {
    Serial.print("📤 API Response: ");
    Serial.println(httpCode);
  } else {
    Serial.println("❌ Erro ao conectar API");
  }
  
  http.end();
}

// ============ EVENT SERIAL ============
void serialEvent() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    Serial.print("📨 Comando: ");
    Serial.println(command);
    
    if (command == "OPEN") {
      openGate();
    } 
    else if (command == "CLOSE") {
      closeGate();
    } 
    else if (command == "STATUS") {
      printStatus();
    }
    else if (command == "PING") {
      Serial.println("PONG");
    }
  }
}

// ============ IMPRIMIR STATUS ============
void printStatus() {
  Serial.println("\n=== STATUS DO SISTEMA ===");
  Serial.print("Portão: ");
  Serial.println(gateOpen ? "ABERTO" : "FECHADO");
  
  Serial.print("Sensor: ");
  Serial.println(analogRead(SENSOR_PIN));
  
  Serial.print("WiFi: ");
  Serial.println(WiFi.status() == WL_CONNECTED ? "Conectado" : "Desconectado");
  
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  
  Serial.print("Uptime: ");
  Serial.print(millis() / 1000);
  Serial.println(" segundos");
}
