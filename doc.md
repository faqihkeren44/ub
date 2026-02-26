# Day 1 - Setup Project

## 1. Buat Folder Project

```
mkdir UB
cd UB
```

## 2. Buat Virtual Environment

```
python -m venv venv
.\venv\Scripts\activate
```

## 3. Install Dependency Dasar

```
pip install fastapi uvicorn
```

## 4. Buat Struktur Folder Awal

```
UB/
│
├── app/
│   ├── main.py
│
├── requirements.txt
└── venv/
```

## 5. Buat Server Pertama

Buka app/main.py, lalu isi:
```
from fastapi import FastAPI

app = FastAPI ()

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

## 6. Jalankan Server

Dari root project:
`uvicorn app.main:app --reload`

Kalau sukses akan muncul:
`Uvicorn running on http://127.0.0.1:8000`

## 7. Test endpoint

Buka browser, lalu masukan:
`http://127.0.0.1:8000`

Harus muncul JSON:
`{"status": "ok}"

## 8. Cek Auto Docs
Buka `http://127.0.0.1:8000/docs`
