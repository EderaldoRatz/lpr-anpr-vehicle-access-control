# Arquitetura do Sistema - LPR/ANPR Vehicle Access Control

## 📐 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                   │
│  ┌──────────────────┐              ┌──────────────────┐   │
│  │  React Frontend  │              │   Swagger Docs   │   │
│  │   (Web UI)       │              │   (API Docs)     │   │
│  └────────┬─────────┘              └────────┬─────────┘   │
│           │                                 │              │
└───────────┼─────────────────────────────────┼──────────────┘
            │ HTTP/HTTPS                      │
            │                                 │
┌───────────┼─────────────────────────────────┼──────────────┐
│           │    CAMADA DE SERVIÇOS (API)    │              │
│  ┌────────▼──────────────────────────────────▼─────┐      │
│  │          FastAPI Server (Python)               │      │
│  │  ┌────────────────────────────────────────────┐ │      │
│  │  │  Endpoints REST                            │ │      │
│  │  │  - /api/auth       (Autenticação)          │ │      │
│  │  │  - /api/vehicles   (Veículos)              │ │      │
│  │  │  - /api/owners     (Proprietários)         │ │      │
│  │  │  - /api/access-logs (Histórico)            │ │      │
│  │  │  - /api/cameras    (Câmeras)               │ │      │
│  │  │  - /api/hardware   (Controle)              │ │      │
│  │  │  - /api/reports    (Relatórios)            │ │      │
│  │  └────────────────────────────────────────────┘ │      │
│  └────────────────────────────────────────────────┘       │
│           │                    │                           │
│  ┌────────▼────────┐   ┌───────▼────────┐                │
│  │ LPR Service     │   │  Other Services │               │
│  │ - YOLO Detect   │   │  - Vehicle SVC  │               │
│  │ - OCR Process   │   │  - Hardware SVC │               │
│  │ - Plate Match   │   │  - Report SVC   │               │
│  └────────┬────────┘   └────────┬────────┘                │
│           │                    │                           │
└───────────┼────────────────────┼──────────────────────────┘
            │ OpenCV/Torch       │ Serial/MQTT
            │                    │
┌───────────┼────────────────────┼──────────────────────────┐
│    CAMADA DE INTEGRAÇÃO        │                          │
│  ┌────────▼────────┐   ┌───────▼────────┐               │
│  │  Câmera         │   │  Hardware      │               │
│  │  - IP/USB       │   │  - Serial Port │               │
│  │  - Vídeo Stream │   │  - MQTT        │               │
│  │  - Frame Grab   │   │  - Relay       │               │
│  └────────┬────────┘   └────────┬────────┘               │
│           │                    │                           │
└───────────┼────────────────────┼──────────────────────────┘
            │                    │
┌───────────▼────────────────────▼──────────────────────────┐
│            CAMADA DE DADOS (DATABASE)                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  MySQL / PostgreSQL                               │  │
│  │  ┌──────────────────────────────────────────────┐ │  │
│  │  │ Tables:                                      │ │  │
│  │  │ - users          (Usuários)                  │ │  │
│  │  │ - vehicles       (Veículos)                  │ │  │
│  │  │ - owners         (Proprietários)             │ │  │
│  │  │ - access_logs    (Histórico)                 │ │  │
│  │  │ - camera_configs (Configurações câmera)     │ │  │
│  │  └──────────────────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Redis Cache (Opcional)                           │  │
│  │  - Session tokens                                 │  │
│  │  - Plate recognition cache                        │  │
│  │  - Rate limiting                                  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │  File Storage                                      │  │
│  │  - Captured images                                │  │
│  │  - Evidence photos                                │  │
│  │  - Reports                                        │  │
│  │  - Backups                                        │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

```

## 🔄 Fluxo de Processamento LPR/ANPR

```
1. Captura de Vídeo
   ↓
2. Detecção de Veículo (YOLO)
   ↓
3. Extração de Placa
   ↓
4. Pré-processamento de Imagem
   ↓
5. OCR (EasyOCR/Tesseract)
   ↓
6. Normalização de Placa
   ↓
7. Consulta Banco de Dados
   ↓
8. Decisão de Autorização
   ├─ SIM → 9a. Abrir Portão
   │       → 9b. Registrar Entrada
   │       → 9c. Salvar Imagem
   │
   └─ NÃO → 10a. Manter Fechado
            → 10b. Registrar Negativa
            → 10c. Alertar Admin
```

## 📦 Estrutura de Arquivos

```
lpr-anpr-vehicle-access-control/
│
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # Aplicação principal
│   │   ├── config.py                 # Configurações
│   │   ├── database.py               # Session BD
│   │   ├── security.py               # JWT & Autenticação
│   │   ├── logging_config.py         # Logging
│   │   │
│   │   ├── api/                      # Endpoints REST
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # Autenticação
│   │   │   ├── vehicles.py           # Veículos
│   │   │   ├── owners.py             # Proprietários
│   │   │   ├── access_logs.py        # Logs de Acesso
│   │   │   ├── camera.py             # Câmeras
│   │   │   ├── dashboard.py          # Dashboard
│   │   │   ├── reports.py            # Relatórios
│   │   │   └── hardware.py           # Hardware
│   │   │
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User model
│   │   │   ├── vehicle.py            # Vehicle model
│   │   │   ├── owner.py              # Owner model
│   │   │   ├── access_log.py         # AccessLog model
│   │   │   └── camera_config.py      # CameraConfig model
│   │   │
│   │   ├── services/                 # Business Logic
│   │   │   ├── __init__.py
│   │   │   ├── lpr_service.py        # LPR/ANPR Core
│   │   │   ├── vehicle_service.py    # Vehicle CRUD
│   │   │   ├── camera_service.py     # Camera Management
│   │   │   ├── hardware_service.py   # Hardware Control
│   │   │   ├── report_service.py     # Reports
│   │   │   └── notification_service.py # Notifications
│   │   │
│   │   ├── utils/                    # Utilities
│   │   │   ├── __init__.py
│   │   │   ├── ocr_processor.py      # OCR wrapper
│   │   │   ├── image_processor.py    # Image utils
│   │   │   ├── video_processor.py    # Video capture
│   │   │   ├── validators.py         # Validators
│   │   │   ├── constants.py          # Constants
│   │   │   └── helpers.py            # Helpers
│   │   │
│   │   └── schemas/                  # Pydantic Schemas
│   │       ├── __init__.py
│   │       └── *.py                  # Schema files
│   │
│   ├── migrations/                   # Alembic migrations
│   ├── tests/                        # Test suite
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
│
├── frontend/                         # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/               # React Components
│   │   │   ├── Dashboard/
│   │   │   ├── VehicleManagement/
│   │   │   ├── AccessLogs/
│   │   │   ├── Login/
│   │   │   ├── Navbar/
│   │   │   └── Sidebar/
│   │   ├── pages/                    # Page components
│   │   ├── services/                 # API client
│   │   ├── context/                  # React Context
│   │   ├── styles/                   # CSS/SASS
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
│
├── microcontroller/                  # Arduino/ESP32
│   ├── esp32_gate_controller/
│   │   ├── esp32_gate_controller.ino # Main code
│   │   └── config.h                  # Configuration
│   ├── arduino_relay_control/
│   │   └── arduino_relay_control.ino
│   └── README.md
│
├── database/                         # SQL Scripts
│   ├── schema.sql                    # Database structure
│   ├── seed.sql                      # Initial data
│   └── procedures.sql                # Stored procedures
│
├── docs/                             # Documentation
│   ├── ARQUITECTURA.md               # This file
│   ├── INSTALACAO.md
│   ├── API.md
│   ├── CONFIGURACAO.md
│   ├── USUARIO.md
│   ├── SEGURANCA.md
│   ├── TROUBLESHOOTING.md
│   └── INTEGRACAO_HARDWARE.md
│
├── docker-compose.yml                # Docker compose
├── .env.example                      # Environment template
├── .gitignore
└── README.md                         # Main README
```

## 🔐 Camadas de Segurança

```
1. Autenticação (JWT Tokens)
   ↓
2. Autorização (Role-based access)
   ↓
3. Validação de Entrada (Pydantic)
   ↓
4. Proteção contra SQL Injection (SQLAlchemy ORM)
   ↓
5. Hash de Senhas (Bcrypt)
   ↓
6. CORS Configuration
   ↓
7. Rate Limiting
   ↓
8. Auditoria (Access Logs)
```

## 📊 Modelos de Dados

### User
```
id: UUID
username: VARCHAR(50) UNIQUE
email: VARCHAR(120) UNIQUE
password_hash: VARCHAR(255)
role: ENUM(admin, operator, viewer)
is_active: BOOLEAN
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

### Vehicle
```
id: UUID
plate: VARCHAR(20) UNIQUE
plate_normalized: VARCHAR(20) UNIQUE
owner_id: FK(Owner)
model: VARCHAR(100)
color: VARCHAR(50)
brand: VARCHAR(100)
is_authorized: BOOLEAN
created_at: TIMESTAMP
updated_at: TIMESTAMP
```

### AccessLog
```
id: UUID
plate: VARCHAR(20)
plate_normalized: VARCHAR(20)
vehicle_id: FK(Vehicle)
access_type: ENUM(entry, exit)
is_authorized: BOOLEAN
confidence: VARCHAR(10)
image_path: VARCHAR(255)
timestamp: DATETIME
gate_opened: BOOLEAN
created_at: TIMESTAMP
```

## 🚀 Performance

### Otimizações Implementadas

1. **Cache**
   - Redis para tokens e placas frequentes
   - TTL de 5 minutos

2. **Índices de Banco de Dados**
   - plate_normalized (busca rápida)
   - timestamp (logs)
   - is_authorized (filtros)

3. **Processamento de Imagem**
   - Resize antes de YOLO
   - Grayscale para OCR
   - Cache de modelos

4. **Rate Limiting**
   - 100 requisições/minuto por IP
   - Proteção contra DDoS

## 🔌 Integrações

### Câmeras
- IP (RTSP)
- USB (OpenCV)
- Webcam

### OCR
- EasyOCR (Python)
- Tesseract (Fallback)

### Hardware
- Serial (Arduino/ESP32)
- MQTT (Broker)
- HTTP REST

### Notificações
- Email (SMTP)
- WhatsApp (Twilio)

## 📈 Escalabilidade

```
1-10 vehicles:     Single server (4GB RAM)
10-100 vehicles:   Separate DB server
100+ vehicles:     Load balancer + multiple API instances
```

---

Para implementação detalhada, consulte os arquivos específicos em `/docs/`.
