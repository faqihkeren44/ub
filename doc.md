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

### Apa Itu Endpoint?

Endpoint adalah alamat di server yang bisa diakses lewat URL untuk melakukan sesuatu. Contoh kalau buka `http://127.0.0.1:8000/health` Bagian `/health` itu adalah endpoint.<br>
Berbeda dengan function biasa yang tidak bisa diakses lewat internet, endpoint bisa diakses lewat browser, postman, atau frontend.

### Kenapa Namanya `/health/`

Karena itu adalah Health Check Endpoint, artinya endpoint untuk mengecek apakah server sedang sehat atau tidak.

### Bedah Kode

- `@app.get("/health")`: Kalau ada request GET ke `/health`, jalankan fungsi di bawah
- `return {"status": "ok"}`: Balas dengan menampilkan JSON {"status": "ok}

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

## 9. Connect Github

Berikut langkahnya:
```
git init
git remote add origin https://github.com/faqihkeren44/ub.git
git add .
git commit -m "Day 1"
git branch -M main
git push -u origin main
```

# Day 2

## 1. Hubungkan github

Sebelum memulai bekerja, ambil semua yang ada di github ke lokal dengan
```
git pull origin main
```
Setelah selesai baru lakukan push
```
git add .
git commit -m "update"
git push
```

## 2. Install PostgreSQL

Berikut langkah-langkah cara install PostgreSQL:
1. Masuk ke [website resmi postgreSQL](https://www.postgresql.org/)
2. Pilih download
3. Download sesuai OS
4. Install postgreSQL
5. Masukan, ingat, dan catat password user postgres
6. Default port: `5432`

## 3. Buat Database Baru

Masuk ke PostgreSQL, lalu buat database:
```
CREATE DATABASE ub;
```

## 4. Install Dependency Tambahan

Aktifkan venv lalu install
```
pip install sqlalchemy psycopg2-binary python-dotenv
```

## 5. Struktur Folder Baru

```
app/
│
├── main.py
├── database.py
├── models.py
└── config.py
```

Bisa gunakan `type nul > nama_file.txt` atau `notepad nama_file.txt`.

## 6. File `.env` di root project
```
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/ub
```
Ganti `PASSWORD` dengan password kamu

Jangan commit file ini, makanya kita masukan `.env` kedalam `.gitignore`

## 7. File `config.py`
```
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

## 8. Setup Database Connection

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

## 9. Model Pertama (Test Table)

```
from sqlalchemy import Column, Integer, String
from app.database import Base

class TestTable(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
```

## 10. Buat Table Saat Startup

Edit `main.py`:
```
from fastapi import FastAPI
from app.database import engine, Base
from app import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}
```