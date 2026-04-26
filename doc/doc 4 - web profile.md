# Day 8 - Persiapan

## 1. Pengaturan Folder

Karena FastAPI pada dasarnya adalah framework untuk Backend (API), dia tidak punya folder otomatis untuk file HTML seperti framework PHP atau server Apache. Dalam standar FastAPI/Python, biasanya menggunakan folder:
- `templates/`: Untuk file HTML
- `static/`: Untuk file pendukung seperti gambar, CSS, dan JavaScript.

Struktur folder menjadi seperti ini:
```
UB\
├── app/
│   ├── main.py
│   ├── routers/
│   └── ...
├── static/
│   ├── css/
│   ├── img/
│   └── js/
├── templates/
│   └── index.html
└── ...
```

## 2. Cara FastAPI Membaca

Sebelumnya, perlu menginstal satu library tambahan:
```
pip install jinja2
```

Lalu, di `app/main.py`, perlu memberitahu FastAPI cara menyajikan file HTML tersebut dengan kode:
```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .routers import products, users, auth, members

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.included_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(members.router)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

Hasilnya, pada saat membuka `/`, FastAPI akan memberikan file `index.html`.

## 3. Ngrok

### 1. Install Ngrok

1. Download Ngrok di ngrok.com
2. Ekstrak file zip. Simpan file `ngrok.exe` di folder project.
3. Kembali ke browser, login ke dahshboard Ngrok. Di sidebar, pilih `Your Authtoken` lalu salin `authtoken`-nya.
4. Di terminal laptop, ketik `ngrok config add-authtoken <token-yang-disalin`.
5. Jalankan uvicorn `uvicorn app.main:app --port 8000`.
6. Di terminal lain, ketik `ngrok http 8000`.
7. Selesai. Link `http://https://...ngrok-free.app` yang didapat bisa diakses di device lain.