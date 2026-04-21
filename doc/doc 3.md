# Role Management

# Day 6 - Memperbarui Database

## 1. Urgensi

Kenapa perlu memperbaruib database? Karena kita sudah membuat tabel `users` dengan kolom yang sudah ditentukan. Saat menjalankan `Base.metadata.create_all(bind=engine)`, SQL Alchemy hanya membuat tabel jika tabel itu belum ada. SQLAlchemy tidak akan mengecek apakah ada pembaruan dalam kolomnya. Untuk itu, kita perlu memperbarui tabel `users` kita. Ada dua cara yang bisa kita gunakan:
1. Cara cepat: Menghapus file database `ub`, dengan resiko semua data akan hilang.
2. Cara professional: Menggunakan alat bernama Alembic.

Sebagai seorang professional, kita akan menggunakan cara dua.

### Apa itu Alembic?

Cara kerja Alembic sama seperti Git. Ia mencatat perubahan, tapi di skema database. Tanpa Alembic, untuk mengubah model (seperti menambah kolom `is_admin`) harus menghapus database dan membuatnya dari awal. Alembic memungkinkan mengubah struktur database tanpa kehilangan data yang sudah ada.

Selayaknya Git yang terkenal dengan version control, Alembic juga mempunyai konsep version control yang berjalan di database. Setiap kali mengubah skema model, Alembic membuat satu versi (seperti commit). Ketika terjadi kesalahan, bisa membatalkan perubahan.

Alembic bekerja dengan membandingkan model python (`models.py`) dengan struktur tabel di database (`users` atau `products`). Ketika menjalankan perintah migrasi, Alembic membuat sebuah file *Migration Scripts*, yang berisi instruksi SQL untuk mengubah database agar sesuai dengan model terbaru. Dalam keseharian, alur kerjanya biasanya seperti ini:
1. Tambah atau ubah kolom di `models.py`
2. Membuat file migrasi otomatis (Alembic melihat perbedaan).
3. Menjalankan migrasi tersebut agar database benar-benar berubah.

## 2. Perbarui `app.models.py`

Role model admin akan ditentukan dengan nilai `Boolean` (`True` jika dai admin, `False` jika bukan admin). Tambahkan di `class User`:
```
is_admin = Column(Boolean, default=False, nullable=False)
```

## 3. Persiapan dan Konfigurasi

Langkah pertama adalah menyiapkan lingkungan Alembic di dalam folder. Jalankan perintah ini di root folder proyek dalam terminal:
```
pip install alembic
alembic init alembic
```
Ini akan membuat folder baru bernama `alembic/` dan file konfigurasi `alembic.ini`.

Agar Alembic bisa melihat model yang sudah dibuat, edit file `alembic/env.py` dan tambahkan:
```
from app.config import DATABASE_URL
from app.database import Base
from app import models

config = context.config

config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata
```

### Bedah Kode

- `import DATABASE_URL`: Mengambil alamat database yang disimpan di `.env`. Agar Alembic tau ke mana ketika harus pergi ke database.
- `import Base`: Wadah tempat semua tabel yang dibuat
- `import models`: Agar semua model terlihat oleh Alembic.
- `context.config`: Membawa sebuah objek konfigurasi (yang awalnya berisi data dari `alembic.ini`).
- `config.set_main_option("sqlalchemy", DATABASE_URL)`: Menimpa (overwrite) pengaturan yang ada di file `alembic.ini`. Alembic yanng tadinya membaca `driver://user:pass...` di file `.ini`, sekarang dipaksa menggunakan `DATABASE_URL`.
- `target_metadata`: *Tabel apa saja yang harus saya awasi?*
- `Base.metadata`: *Awasi semua model yang terhubung ke `Base`*.

## 4. Autogenerate

Karena ini pertama kalinya menggunakan Alembic, akan ada proses Autogenerate. Alembic akan membandingkan kode di `models.py` (yang sudah ada is_admin) dengan tabel di database (yang belum ada is_admin). Ia akan otomatis menuliskan kode Python untuk menambah kolom tersebut.

Jalankan perintah berikut di terminal:
```
alembic revision --autogenerate -m "add is_admin to user table"
```
Setelah itu, periksa folder `alembic/versions/`. Di dalamnya akan ada file `.py` dengan nama unik (`script.py.mako`), itulah Migration Script. Ada dua fungsi utama:
1. Fungsi `upgrade()`: 
2. Fungsi `downgrade()` 

## 5. Error

Bayangkan punya buku absen (tabel `users`) yang sudah berisi 10 nama. Tiba-tiba ada kolom baru dan kolom ini Wajib Diisi (`NOT NULL`). Postgres bingung: *"Oke, saya tambah kolomnya, tapi 10 orang yang sudah ada di buku ini statusnya apa? Saya tidak boleh mengosongkannya (`null`)"*. Itulah jenapa muncul error
`psycopg2.errors.NotNullViolation: column "is_admin" of relation "users" contains null values`

Oleh karena itu, tambahkan nilai default di bagian `upgrade` menjadi:
```
def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='true'))
```

## 5. Eksekusi

Jalankan di terminal:
```
alembic upgrade head
```
- `upgrade`: Menjalankan `upgrade()` di file script.
- `head`: Memberitahu Alembic untuk maju ke versi yang paling baru (paling atas).

Cek di database apakah sudah menambah kolom baru:
- Masuk dengan `psql -U postgres`.
- `\l` untuk melihat daftar database, dan `\c nama_database` untuk masuk.
- `\dt` untuk melihat semua tabel.
- `\d nama_tabel` untuk melihat detail tabel (termasuk kolom).
- `SELECT * FROM nama_tabel;` untuk melihat isi tabel.
- `\q` untuk keluar.

Jika ingin mengubah nilai `is_admin` pada data user yang sudah dimasukan, gunakan perintah:
```
UPDATE users SET is_admin = false WHERE email = user@example.com;
```

# Day 7 - Penerapan

## 1. Struktur Folder Proyek

```
├── app/                      # Folder utama aplikasi (Python Package)
│   ├── __init__.py           # Menandakan folder ini adalah package
│   ├── config.py             # Pengaturan environment (.env)
│   ├── database.py           # Pengaturan koneksi database
│   ├── main.py               # Titik masuk utama (Entry point) API
│   ├── models.py             # Definisi tabel database (SQLAlchemy)
│   ├── schemas.py            # Definisi validasi data (Pydantic)
│   ├── oauth2.py             # Logika keamanan & JWT Token
│   ├── dependencies.py       # Fungsi role checker
│   ├── utils/                # Fungsi untuk enkripsi password
│   └── routers/              # Folder khusus rute/endpoint
│       ├── __init__.py
│       ├── users.py          # Endpoint terkait User (Register, Login)
│       └── products.py       # Endpoint terkait Produk
├── alembic/                  # Folder migrasi database
│   ├── versions/             # File histori perubahan tabel
│   ├── env.py                # Konfigurasi penghubung Alembic & App
│   └── script.py.mako        # Template migrasi
├── .env                      # File rahasia (Password & URL DB)
├── alembic.ini               # Konfigurasi utama Alembic
└── requirements.txt          # Daftar library yang diinstal
```

## 2. `app/routers/products.py`

Pindahkan logika terkait produk dari `main.py` ke sini. Sebagai pengganti `@app`, gunakan `.APIRouter`:
```
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.post("/", response_model=schemas.ProductOut)
def input_product(product_data:schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
```

### Bedah Kode
- `prefix="/products"`: Artinya, semua fungsi di dalam file ini secara otomatis akan dimulai dengan `/products`. 
Jika membuat `@router.get("/")`, alamat aslinya jadi `/products/`.
Jika membuat `@router.get("/{id}")`, alamat aslinya jadi `/products/{id}`.
- `tags=['Products']`: Ini untuk estetika dan organisasi di Dokumentasi Swagger (`/docs`). Semua rute di file ini akan dikelompokkan dalam folder `Products`.

### API Router

Dalam sebuah proyek kecil, biasanya semua rute/endpoint (`/login`, `/register`, `/products`) ditulis menumpuk dalam satu file `main.py`. Masalahnya, kalau aplikasi terus berkembang menjadi puluhan atau ratusan rute, tentu akan pusing mencarinya.

Sekarang bayangkan mall besar seperti Granda Indonesia atau Pakuwon Mall. Dalam operasionalnya, dibagi menjadi beberapa departemen atau sayap (wing).
- Sayap A: Khusus Fashion.
- Sayap B: Khusung Food Court.
- Sayap C: Khusus ELektronik.
`APIRouter` adalah gambaran dari departemen atau sayap tersebut. Mereka mengatur urusan masing-masing tanpa mengganggu sayap lain. `main.py` bertugas sebagai Lobi Utama yang menghubungkan semua sayap tersebut agar pengunjung bisa masuk ke mana saja.

Ketika terjadi kesalahan di bagian Produk, tidak perlu menyentuh kode User. Cukup pergi ke sayap produk (`app/routers/products.py`) dan memperbaikinya di sana.

Dalam kerja sama tim, satu orang bisa fokus di `products.py`, orang lain di `users.py`, tanpa harus rebutan mengedit file `main.py` yang sama.

### Router, Route, Endpoint

1. Router (`router = APIRouter(...))`: Objek untuk mengelompokan tugas.
2. Endpoint (`POST /products/`): Gabungan lengkap dari Route (`/products/`) dan HTTP Method (`POST`). Inilah titik akhir di mana data data `product` diterima dan diproses oleh fungsi (misal oleh `create_product`).
3. Route / Rute (`/products/`) : Jalur atau alamat URL yang dituju. Karena di router `prefix="/products"` dan menggunakan `"/"` di dekorator fungsi, maka route-nya atau alamat yang diketik user di browser adalah gabungan keduanya (`/products/`). 

## 3. `app/routers/user.py`

Seperti sebelumnya, pertama definisikan dulu `APIRouter`:
```
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)
```

Selanjutnya tinggal copy endpoint `/register` dari file `main.py` ke `routers/users.py`.
```
@router.post("/", response_model=schemas.UserOut)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    ...
```

## 4. Hubungan Antar File

Sekarang, hapus kode itu dari `main.py`, ganti dengan memanggil router yang dibuat:
```
from .routers import products

app = FastAPI()

app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Selamat datang di API UB!"}
```

### Bedah kode

- `from .router import products`: Import departemen atau rute nya.
- `app.include_router(products.router)`: Agar FastAPI tau rute-rute di file `products.py`.