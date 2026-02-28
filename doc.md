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
7. Pilih `PostgreSQL 16 (x64) on port 5432`
8. Saat ada pilihan "Select applications you would link to install", pilih `Database Server`, dan ceklis `PostgreSQL (64 bit) v 16.12-1`

## 3. Buat Database Baru

Masuk ke PostgreSQL dengan `psql -U postgres`:
- `psql`: Perintah untuk masuk ke PostgreSQL
- `-U postgres`: Login sebagai user bernama `postgres`, yaitu superuser default yang dibuat saat install

### Perintah Dasar SQL

- Buat database: `CREATE DATABASE ub_db;`. Kalau sukses akan muncul `CREATE DATABASE`.
- Lihat daftar database: `\l`
- Masuk ke database: `\c ub_db`
- Buat table sederhana:
```
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(225) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Cek table: `\dt`


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

Ini bisa disebut connection string, yaitu alamat untuk backend agar bisa terhubung ke database
```
DATABASE_URL=postgresql://postgres:PASSWORD@localhost:5432/ub
```
Ganti `PASSWORD` dengan password kamu

Jangan commit file ini, makanya kita masukan `.env` kedalam `.gitignore`

### Bedah Kode

- Format umum: `postgresql://USERNAME:PASSWORD@HOST:PORT/DATABASE_NAME`
- `postgresql://`: Menentukan jenis database. Kalau MySQL biasanya diawali `mysql://`
- `postgres`: Nama default user saat install PostgreSQL
- `PASSWORD`: Password untuk user tersebut
- `@HOST`: Server tempat database berjalan. Isi `localhost` jika berjalan di lokal komputer, atau kalau di server lain `192.168.1.10`, `d.myserver.com`.
- `PORT`: Secara default postgreSQL selalu berjalan di `5432`, kecuali mau diubah.
- `DATABASE_NAME`: Nama database.

## 7. File `config.py`

Buka `app/config.py`, lalu masukan kode berikut:
```
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

### Kenapa Harus Gini?

Untuk menyimpan sebuah variabel, bisa saja dibuat seperti ini:
```
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/ub_db"
```
Tapi itu tidak aman, dan tidak bisa dipakai saat produksi nanti. Selain itu, password nya bisa ke-commit ke GitHub, dan akhirnya tersebar.

### Bedah kode:
- `import os`: Module bawaan Python. Di sini untuk mengakses environment variable (variabel rahasia yang disimpan di sistem). Contohnya password database, API key payment, secret JWT.
- `from dotenv import load_dotenv`: Membaca file `.env`, lalu memasukan isinya ke environment variable. Karena secara default Python tiak bisa otomatis membaca file `.env`.
- `load_dotenv()`: Membaca file `.env` di folder. Setelah ini dijalankan, Python bisa mengakses nilai yang ada di dalam file `.env` itu.
- `DATABASE_URL = os.getenv("DATABASE_URL")`: 

## 8. Setup Database Connection

Buka `app/database.py`, lalu masukan:
```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### Apa Itu SQLAlchemy?

SQLAlchemy adalah library Python untuk berinteraksi dengan database menggunakan Python tanpa harus menulis SQL mentah terus menerus.

### Bedah Kode

- `engine = create_engine(DATABASE_URL)`: Membuat mesin koneksi ke database berdasarkan alamat di `DATABASE_URL`.
- `SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)`: Jembatan antara kode Python dengan database
- `autocommit=False`: Database tidak otomatis menyimpan perubahan. Harus ada perintah `db.commit()` agar data benar-benar tersimpan.
- `autoflush=False`: SQLAlchemy tidak otomatis kirim perubahan ke database sebelum waktunya. 
- `flush` mengirim SQL ke database, sedangkan `commit` yang mempermanenkan SQL itu.
- `bind=engine`: Session ini menggunakan `engine` tadi untuk koneksi.
- `Base = declarative_base()`: Parent class untuk semua table di database.

### Kenapa Harus Ada Base?

Karena SQLAlchemy perlu tahu class mana yang table, nama table nya apa, kolomnya apa saka, primary key nya yang mana, dsb. Semua itu didaftakan ke `Base`. 
Contoh, misalkan membuat sebuah model:
```
class User(Base):
    __table__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
```
Maka, class `User` yang dibuat mewarisi `Base`, dan otomatis SQLAlchemy mendaftarkan `users` ke metadata

Kurang lebih flow nya akan seperti ini:
```
Base
 ├── User
 ├── Product
 ├── Order
 └── Cart
```
Semua model terdaftar di satu root, yaitu `Base`.

### Apa Itu Metadata

Metadata itu kayak blueprint semua table. Di dalamnya ada daftar table, nama kolom, tipe data, dll.  Sehingga kita bisa membuat semua table yang terdaftar di Base.

### Database VS Table VS Model

1. **Database**: Wadah besar untuk menyimpan data. Seperti sebuah gedung perpustakaan yang menyimpan banyak buku dalam rak buku.
2. **Table**: Bagian dari database. Di dalam table ini disimpan berbagai jenis data. Bentuknya sama seperti spreadsheet/excel (Ada kolom dan baris).
Kalau database itu perpustakannya, table itu rak buku nya.
3. **Model**: Representasi table dalam bentuk kode Python. Table yang seharusnya berbentuk kotak-kotak menjadi beberapa baris kode.
```
Model User  →  Table users
Model Product → Table products
Model Order → Table orders
```

## 9. Model Pertama (Test Table)

Untuk tes, buka `app/models.py`, lalu buat sebuah model:
```
from sqlalchemy import Column, Integer, String
from app.database import Base

class TestTable(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
```

### Bedah Kode

- `class TetsTable(Base):`: Buat model bernama TestTable yang mewarisi Base. Sehingga model ini akan masuk ke `Base.metadata`.
- `__tablename__ = "test_table"`: Nama table di database adalah `test_table`.
- `id = Column(Integer, primary_key=True, index=True)`: Nama kolom `id`, tipe data integer, `primary_key=True` ini kunci utama, `index=True` membuat index.
- `name = Column(String, index=True)`: Nama kolomnya `name`, tipe data String (VARCHAR).
- Ketika menjalankan `Base.metadata.create_all(bind=engine), maka akan membuat table di PostgreSQL seperti berikut:
```
CREATE TABLE test_table (
    id INTEGER PRIMARY KEY,
    name VARCHAR
    # Plus tambahan index
);
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
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except:
        return {"status": "error", "database": "diconnected"}
```

### Cara Kerja `create_all()`

Ketika `Base.metadata.create_all(bind=engine)` dieksekusi, maka SQLAlchemy akan:
1. Cek semua model turunan `Base` (class/model dibuat menggunakan `Base`)
2. Lihat __tablename__
3. Lihat kolom-kolomnya
4. Cek apakah table sudah ada di database
5. Jika belum ada maka dibuat, jika sudah ada tidak akan dibuat ulang.
Karena ini diletakkan di global scope, maka akan berjalan ketika aplikasi dimulai (Saat menjalankan `uvicorn main:app --reload`

### Bedah Kode

- `from app import models`: Karena `models.py` di-import, berarti semua class model akan dijalankan dan terdaftar ke `Base.metadata`. Kalau tidak import `models.py`, `Base` tidak tahu ada model aja saja dan `create_all()` tidak bikin apa-apa.
- `app = FastAPI()`: Membuat instance aplikasi (Server API kamu)
- `Base.metadata.create_all(bind=engine)`: Buat semua table yang terdaftar di `Base.metadata` ke database.

### Cek TestTable Lewat Terminal

Untuk memastikan kode berjalan, dan TestTable sudah dibuat, cek table nya lewat psql (terminal). :
1. Masuk ke PostgreSQL `psql -U postgres`
2. Masuk ke database `\c ub_db`
3. Lihat daftar table `dt`
4. Lihat struktur table `\d test_table`

### Session VS Engine

Dalam SQLAlchemy, ada 2 jalur dalam memberikan perintah
1. **Jalur ORM (Session)**: Mengikuti aturan session yang dibuat. Kalau `autocommit=False`, maka harus `db.commit()`. Contoh yang harus menggunakan `commit` yaitu `INSERT`, `UPDATE`, `DELETE`.
2. **Jalur Core/Engine (DDL)**: Langkung kirim SQL ke dtaabase lewat engine, tidak pakai session atau commit manual. Bisa dilihat dari code perintahnya `Base.metadata.create_all(bind=engine)`. Yang termasuk transaksi sendiri (implicit commit) yaitu `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`.