# Day 8 - Persiapan

## 

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
├── templates/
│   └── index.html
├── templates/
└── ...
```

## Cara FastAPI Membaca

Sebelumnya, perlu menginstal satu library tambahan:
```
pip install jinja2
```

Lalu, di `app/main.py`, perlu memberitahu FastAPI cara menyajikan file HTML tersebut dengan kode:
```
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .routers import products, users, auth

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.included_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}
```

Hasilnya, pada saat membuka `/`, FastAPI akan memberikan file `index.html`.