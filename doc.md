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

**Apa Itu Endpoint?**

Endpoint adalah alamat di server yang bisa diakses lewat URL untuk melakukan sesuatu. Contoh kalau buka `http://127.0.0.1:8000/health` Bagian `/health` itu adalah endpoint.<br>
Berbeda dengan function biasa yang tidak bisa diakses lewat internet, endpoint bisa diakses lewat browser, postman, atau frontend.

**Kenapa Namanya `/health/

Karena itu adalah Health Check Endpoint, artinya endpoint untuk mengecek apakah server sedang sehat atau tidak.

**Bedah Kode**

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