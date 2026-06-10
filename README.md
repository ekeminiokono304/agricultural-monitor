=======
# agricultural-monitor
=======
# 🌿 AgriVision Crop Monitoring Production API

Production-grade crop disease detection and agricultural advisory engine powered by an **EfficientNetB0 CNN** classification layer and a multi-tool **Google ADK Agent (Gemini 2.0 Flash)**.

---

## 🏗️ System Architecture
Farmer uploads image
│
▼
FastAPI Gateway Engine (POST /predict/disease)
│
▼
EfficientNetB0 CNN Pipeline ──► Disease Label + Confidence Score
│
▼
Google ADK Agent Framework (Gemini 2.0 Flash Runtime)
├── get_disease_info()
├── get_treatment_advice()
└── estimate_yield_impact()
│
▼
Structured Response Serialized via Pydantic Schema Contracts


---

## 🧭 API Endpoints Catalog

| Method | Route | Description | Request Payload |
| :--- | :--- | :--- | :--- |
| **GET** | `/health` | Core system vitality status check | None |
| **GET** | `/model/info` | Telemetry details describing the CNN layer | None |
| **GET** | `/diseases` | Full catalog listing all supported disease labels | None |
| **POST** | `/predict/disease` | Evaluates a single crop image and generates AI advice | `file` (binary), `field_id` (form) |
| **POST** | `/predict/batch` | Evaluates an array of crop files concurrently | `files` (multi), `field_id` (form) |
| **POST** | `/feedback` | Registers calibration feedback logs for tracking drift | `FeedbackRequest` (JSON) |

---

## 🚀 Quickstart Guide

### 1. Initialize Local Environments
```bash
# Clone and enter the project directory
git clone [https://github.com/your-username/agrivision-api.git](https://github.com/your-username/agrivision-api.git)
cd agrivision-api

# Create your runtime environment configuration file
cp .env.example .env
