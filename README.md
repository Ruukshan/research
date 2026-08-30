# Smart Career Pathway Recommendation System for Sri Lankan GCE A/L Students

A machine learning-driven educational decision-support and career pathway recommendation system tailored for Sri Lankan students transitioning from GCE Ordinary Level (O/L, Grade 11) to GCE Advanced Level (A/L, Grade 12–13).

---

## 🔬 Core Research Pipeline

```
Student Profile Intake 
       ↓
Data Preprocessing & Validation
       ↓
Multi-Class ML Stream Prediction (RF / XGBoost / DNN)
       ↓
Hybrid Recommendation Engine (ML Score + Content Similarity + Collaborative Filtering)
       ↓
Ranked Top-5 Career Pathways
       ↓
Explainable AI (SHAP Feature Attribution)
       ↓
Interactive Decision-Support Web Application
```

---

## 🏛️ Supported A/L Streams

1. **Physical Science** (Combined Mathematics, Physics, Chemistry / ICT)
2. **Biological Science** (Biology, Chemistry, Physics / Agriculture)
3. **Commerce** (Accounting, Business Studies, Economics / ICT)
4. **Arts** (Languages, Social Sciences, Law, Fine Arts)
5. **Technology** (Engineering Technology, Biosystems Technology, Science for Technology, BICT)

---

## 📁 Repository Structure

```
research_2/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application entrypoint & OpenAPI docs
│   │   ├── config.py                   # Pydantic settings & DATA_MODE configuration
│   │   ├── database.py                 # SQLAlchemy database session & engine
│   │   ├── api/
│   │   │   └── endpoints/              # REST routes: health, assessment, prediction, pathways, evaluation
│   │   ├── schemas/                    # Pydantic input/output schemas
│   │   ├── models/                     # SQLAlchemy ORM models
│   │   ├── services/                   # Assessment & recommendation domain logic
│   │   └── ml/                         # ML & Data Pipeline Subsystem
│   │       ├── config/                 # ML constants, seeds, class weights
│   │       ├── schema/                 # Sri Lankan survey schema & grade mappings
│   │       ├── data/
│   │       │   ├── synthetic/          # Generated synthetic development records
│   │       │   ├── real/               # Future real Google Forms survey CSVs
│   │       │   ├── processed/          # Preprocessed train/test datasets
│   │       │   └── knowledge_base/     # Verified Sri Lankan degree & career pathways JSON
│   │       ├── generator/              # Domain-modeled synthetic dataset generator
│   │       ├── validation/             # Schema & data integrity validation suite
│   │       ├── preprocessing/          # Feature transformers & scalers (Phase 2/3)
│   │       ├── training/               # Model trainers (Phase 3)
│   │       ├── prediction/             # Probability inference
│   │       ├── recommendation/         # Hybrid recommendation engine
│   │       ├── explainability/         # SHAP explanation module
│   │       └── evaluation/             # Metrics & experiment tracking
│   ├── tests/                          # Pytest suite
│   ├── requirements.txt
│   └── .env.example
├── frontend/                           # Vue 3 + TypeScript + Vite Web Application
│   ├── src/
│   │   ├── views/                      # Home, Assessment (6-step), Results, Dashboard
│   │   ├── components/                 # Navbar, Footer, UI Cards
│   │   ├── stores/                     # Pinia assessment store
│   │   └── style.css                   # Custom Academic CSS theme
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## ⚙️ Setup & Execution Guide

### 1. Backend Environment Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Running Synthetic Dataset Generator & Validation

Generate 1,200 statistically plausible synthetic student records:
```bash
cd backend
python -m app.ml.generator.synthetic_generator --count 1200 --seed 42
```

Validate dataset integrity:
```bash
python -m app.ml.validation.data_validator --file app/ml/data/synthetic/synthetic_students.csv
```

### 3. Running Backend Unit Tests

```bash
cd backend
pytest tests/ -v
```

### 4. Running the Backend API Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```
- Interactive API Docs (Swagger): `http://127.0.0.1:8000/docs`
- Alternative API Docs (Redoc): `http://127.0.0.1:8000/redoc`

### 5. Running the Frontend Development Server

```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## ⚖️ Academic & Ethical Disclaimer

> **Important Notice**: This software provides AI-assisted career pathway recommendations for **educational decision support**. It is intended to assist students, parents, and teachers during the GCE O/L to A/L transition. Recommendations do **not** replace advice from qualified guidance counsellors or official Sri Lankan University Grants Commission (UGC) admission policies.
