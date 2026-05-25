# 🚗 Sistema Completo de Controle de Acesso Veicular com LPR/ANPR

## 📋 Visão Geral

Sistema inteligente e modular para identificação automática de placas de veículos (LPR/ANPR) em tempo real, integrado com banco de dados, gerenciamento web e controle de hardware (Arduino/ESP32) para abertura automática de portões.

### ✨ Características Principais

- ✅ Captura de vídeo em tempo real (câmera IP, USB, webcam)
- ✅ Detecção automática de veículos com YOLO
- ✅ Reconhecimento de placas com OCR (EasyOCR + Tesseract)
- ✅ Validação em banco de dados em tempo real
- ✅ Abertura automática de portão (relé + Arduino/ESP32)
- ✅ Registro completo de acessos (histórico)
- ✅ Painel administrativo web responsivo
- ✅ API REST documentada
- ✅ Sistema de autenticação com JWT
- ✅ Suporte a múltiplas câmeras
- ✅ Modo noturno com infravermelhos
- ✅ Geração de relatórios (PDF/Excel)
- ✅ Backup automático de dados

---

## 📁 Estrutura do Projeto

```
lpr-anpr-vehicle-access-control/
├── backend/                          # Backend Python (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # Aplicação principal
│   │   ├── config.py                 # Configurações
│   │   ├── database.py               # Configuração do BD
│   │   ├── security.py               # Autenticação/JWT
│   │   ├── logging_config.py         # Logging
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # Endpoints de autenticação
│   │   │   ├── vehicles.py           # CRUD de veículos
│   │   │   ├── owners.py             # CRUD de proprietários
│   │   │   ├── access_logs.py        # Histórico de acessos
│   │   │   ├── camera.py             # Gerenciamento de câmeras
│   │   │   ├── dashboard.py          # Endpoints de dashboard
│   │   │   ├── reports.py            # Geração de relatórios
│   │   │   └── hardware.py           # Controle de hardware
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # Model de usuário
│   │   │   ├── vehicle.py            # Model de veículo
│   │   │   ├── owner.py              # Model de proprietário
│   │   │   ├── access_log.py         # Model de log de acesso
│   │   │   └── camera_config.py      # Model de configuração de câmera
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── lpr_service.py        # Serviço de LPR/ANPR
│   │   │   ├── vehicle_service.py    # Validação de veículos
│   │   │   ├── camera_service.py     # Gerenciamento de câmeras
│   │   │   ├── hardware_service.py   # Controle de hardware
│   │   │   ├── report_service.py     # Geração de relatórios
│   │   │   └── notification_service.py # Notificações
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── ocr_processor.py      # OCR com Tesseract/EasyOCR
│   │   │   ├── image_processor.py    # Processamento de imagens
│   │   │   ├── video_processor.py    # Processamento de vídeo
│   │   │   ├── validators.py         # Validadores
│   │   │   ├── constants.py          # Constantes do sistema
│   │   │   └── helpers.py            # Funções auxiliares
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── vehicle_schema.py
│   │       ├── owner_schema.py
│   │       ├── access_log_schema.py
│   │       └── user_schema.py
│   ├── migrations/                   # Migrações do banco
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   ├── test_lpr.py
│   │   ├── test_database.py
│   │   └── test_hardware.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
│
├── frontend/                         # Frontend React
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   ├── VehicleManagement/
│   │   │   ├── OwnerManagement/
│   │   │   ├── AccessLogs/
│   │   │   ├── CameraManager/
│   │   │   ├── Reports/
│   │   │   ├── Login/
│   │   │   ├── Navbar/
│   │   │   └── Sidebar/
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── context/
│   │   │   └── AuthContext.js
│   │   ├── styles/
│   │   ├── utils/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
│
├── microcontroller/                  # Código Arduino/ESP32
│   ├── esp32_gate_controller/
│   │   ├── esp32_gate_controller.ino
│   │   └── config.h
│   ├── arduino_relay_control/
│   │   └── arduino_relay_control.ino
│   └── README.md
│
├── database/
│   ├── schema.sql                    # Schema do banco de dados
│   ├── seed.sql                      # Dados iniciais
│   └── procedures.sql                # Stored procedures
│
├── docs/
│   ├── ARQUITECTURA.md               # Arquitetura do sistema
│   ├── INSTALACAO.md                 # Manual de instalação
│   ├── USUARIO.md                    # Manual do usuário
│   ├── API.md                        # Documentação da API
│   ├── CONFIGURACAO.md               # Guia de configuração
│   ├── SEGURANCA.md                  # Boas práticas de segurança
│   ├── TROUBLESHOOTING.md            # Resolução de problemas
│   └── INTEGRACAO_HARDWARE.md        # Integração com hardware
│
├── docker-compose.yml
├── .env.example
└── .gitignore
```

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.9+
- Node.js 16+
- MySQL/PostgreSQL
- Docker & Docker Compose (opcional)
- Arduino IDE (para ESP32/Arduino)

### Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/EderaldoRatz/lpr-anpr-vehicle-access-control.git
cd lpr-anpr-vehicle-access-control

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Configure o arquivo .env com suas credenciais

# Banco de dados
mysql -u root -p < ../database/schema.sql

# Executar servidor
uvicorn app.main:app --reload

# Frontend (novo terminal)
cd frontend
npm install
npm start
```

### Com Docker

```bash
docker-compose up -d
```

---

## 📊 Funcionalidades

### Painel Administrativo
- Dashboard em tempo real com estatísticas
- Gerenciamento de veículos autorizados
- Gerenciamento de proprietários/motoristas
- Histórico completo de acessos
- Filtros avançados (data, placa, usuário)
- Geração de relatórios (PDF/Excel)
- Gerenciamento de câmeras
- Controle de múltiplas câmeras

### Sistema de LPR/ANPR
- Detecção de veículos em tempo real
- Reconhecimento automático de placas
- Validação contra banco de dados
- Captura de imagens de evidência
- Modo noturno com IR
- Precisão > 95%

### Integração de Hardware
- Acionamento de relé (abertura de portão)
- Sensores de presença
- Cancela automática
- Comunicação serial e MQTT
- ESP32 + Arduino

---

## 🔐 Segurança

- ✅ Autenticação JWT
- ✅ Hash de senhas (bcrypt)
- ✅ Rate limiting
- ✅ CORS configurado
- ✅ Validação de entrada
- ✅ Proteção contra SQL injection
- ✅ Logs de auditoria
- ✅ Encriptação de dados sensíveis

---

## 🔧 Tecnologias

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- OpenCV
- YOLOv5
- EasyOCR/Tesseract
- PySerial
- JWT

### Frontend
- React
- Axios
- React Router
- Material-UI
- Chart.js

### Banco de Dados
- MySQL/PostgreSQL

### IoT/Hardware
- Arduino IDE
- MQTT
- Serial

---

## 📚 Documentação

Consulte os arquivos em `/docs/` para documentação completa.

---

**Desenvolvido com ❤️ por EderaldoRatz**
