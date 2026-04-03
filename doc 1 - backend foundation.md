# Table 0f Contents

- [Day 1 - Setup Project](#day-1---setup-project)
- [Day 2 - Setup Database](#day-2---setup-database)
- [Day 3 - Register User](#day-3---register-user)
- [Day 4 - JWT Login](#day-4---jwt-login)

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

# Day 2 - Setup Database

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
- `from dotenv import load_dotenv`: Membaca file `.env`, lalu memasukan isinya ke environment variable. Karena secara default Python tidak bisa otomatis membaca file `.env`.
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
from sqlalchemy import text
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
        return {"status": "error", "database": "disconnected"}
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

# Day 3 - Register User

![register-user-workflow](register-user-workflow.jpg)

## 1. Membuat Schemas

Schema berfungsi sebagai cetakan data yang memastikan input dari user sudah benar. Misalnya email tidak pakai simbol @, password kosong, maka FastAPI otomatis menolaknya.
Berikut kode yang dimasukan ke dalam file `schemas.py`:
```
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        from_attributes = True
```

`EmailStr` butuh package tambahan bernama `email-validator`, yang tidak ikut ter-install saat install biasa. Jika tidak di-install terlebih dahulu, akan muncul error:
`ImportError: email-validator is not installed`.
Oleh karena itu, install dependency yang kurang : `pip install "pydantic[email]"`

### Perbedaan `UserCreate` Dengan `UserOut`

- `UserCreate`: Menerima input data dari user, lalu disimpan ke server.
- `UserOut`: Respon yang diberikan server ke aplikasi user itu sendiri agar tahu bahwa pendaftaran berhasil.
*"Akun dengan ID ..., email ..., dan namamu ... sudah terdaftar!"*
- **Mengapa dipisah?**: Jika data yang masuk dan data yang dikeluarkan untuk memberitahu user tidak dibedakan, secara tidak sengaja server bisa saja mengirimkan kembali `password`. Meskipun sudah di-hash, tapi ini kurang aman.
- `class Config: from_attributes = True`: Saat mengambil data dari database menggunakan `db.query`, hasilnya berupa objek Python, seperti `user.full_name`. Sedangkan Pydantic bekerja dengan data Dictionary yang diakses dengan kurung siku `user["full_name"]`. `from_attributes = True` adalah penerjemahnya.

## 2. Kelola Koneksi `SessionLocal`

Bayangkan database adalah gedung kantor. Setiap kali ada orang yang ingin daftar (requset), sebuah pintu terbuka. Jika lupa menutup pintu setelah daftar selesai, pintu ini akan terus terbuka. Akhirnya, gedung jadi penuh sesak, dan orang baru tidak bisa masuk lagi.

Oleh karena itu, sekarang buat fungsi kecil bernama `get_db` yang bertugas untuk membuka dan menutup pintu setelah selesai:
```
...
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Bedah Kode

- `db = SessionLocal`: Di dalam `database.py`, sudah dibuat `SessionLocal = sessionmaker(...)`. Ini pembuatan session. Setiap kali ini dipanggil, maka akan membuat koneksi baru (session) ke database.
- `yield db`: Endpoint pakai db.

### Generator Function `yield`

Seperti `return`, `yield` juga mengembalikan nilai dari sebuah fungsi. Perbedaannya yaitu:

**`return`**: Fungsi selesai, langung keluar, baris setelahnya tidak dijalankan. Contoh:
```
def contoh():
    return 5
   print("Halo")
```
Maka, `"Halo"` tidak akan tercetak

**`yield`**: Fungsi tidak selesai, tapi berhenti sementara. Ketika dipanggil kembali, baru lanjut. Contoh:
```
def contoh()
    print("A")
    yield 5
    print("B")
```
Maka, fungsi `contoh()` dijalankan sampai bertemu `yield`, lalu mengirim nilai 5. Fungsi berhenti sementara. Ketika dipanggil lagi, baru `"B"` jalan.

### Visualisasi Tanpa API

Perhatikan contoh di bawah, dan tebak urutan yang akan muncul
```
def contoh()
    print("A")
    yield "DATA"
    print("B")

gen = contoh()

print("Step 1")
value = next(gen)
print("Step 2:", value)
next(gen)
```

Berikut urutan yang akan berjalan:
1. `gen = contoh()`: Inilah perbedaan generator function `yield` dengan fungsi biasa. Di sini, fungsi `contoh()` tidak akan dijalankan sampai ada perintah `next`.
2. `print("Step 1")`: Menampilkan string `"Step 1"`
3. `value = next(gen)`: Artinya jalankan fungsi. Maka `print("A")` dijalankan, ketika bertemu `yield "DATA"`, berhenti (pause), lalu return sementara nilai `"DATA"`.
4. `print("Step 2:", value)`: Sesuai kode sebelumnya, nilai variabel `value` adalah `"DATA"`. Maka, akan menampilkan `"Step 2: DATA"`.
5. `next(gen)`: Fungsi berlanjut, baru `print("B")` dijalankan

## 3. Membuat Endpoint `/register`

Tambahkan endpoint baru di `app/main.py`. Tempatkan setelah koneksi `SessionLocal`:
```
@app.post("/register", response_model=schemas.UserOut):
```

## 4. Membuat Fungsi Register

Tambahkan dalam endpoint `/register` yang sudah dibuat:
```
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
```

### Bedah Kode

- `user_data: schemas.UserCreate`: FastAPI tau ini Pydantic model, berarti ambil data dari request body. Jadi, saat client kirim request:
    ```
    {
        "email":"a@mail.com",
        "password": "123",
        "full_name": "Alif"
    }
    ```
FastAPI akan:
    1. Ambil JSON
    2. Validasi menggunakan `schemas.UserCreate`
    3. Buat objek `UserCreate`
    4. Masukkan ke parameter `user_data`
- `db: Session`: `db` adalah parameter fungsi `register_user` yang berisi objek session (parameter yang di-inject oleh FastAPI). Adapun `: Session`, itu adalah hint tipe data. Sama seperti `x: int = 5`.
- `Dependes(get_db)`: Membuat session.

### Kenapa Import `sqlalchemy.orm import Session`

Memang seandainya tidak menambahkan `: Session`, kode tetap akan jalan. Namun, ini alasan kenapa tetap pakai:
- Untuk editor/autocomplete seperti VSCode/PyCharm, bisa kasih suggestion seperti `.query()`, `.add()`, `.commit()` karena editor tau `db` itu apa.
- Tools seperti mypy/pyright akan memakai type hint untuk cek error sebelum runtime
- Dokumentasi dan clean code agar orang lain yang baca langsung tau *"Oh, ini SQLAlchemy Session"*.

### Dependency Injection

Kenapa tidak ada `next(gen)`? Karena kita menyuruh FastAPI untuk membuatnya (dependency injection).
Ketika kita memasukan `db: Session = Depends(get_db)` ke dalam parameter fungsi `register_user`, sama saja kita menyuruh FastAPI untuk menyiapkan `db` dari `get_db` terlebih dahulu. Makanya, sebelum masuk baris pertama, di dalam FastAPI membuat kode:
```
gen = get_db()
db = next(gen)
```
Akhirnya, parameter fungsi menjadi lengkap (`register_user(user_data, db)`. Setelah selesai, otomatis FastAPI menjalankan:
```
next(gen)
```

## 5. Buat Model user

Di `app/models.py` tambahkan:
```
class User(Base):
    __table__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable(True)
```

### Bedah Kode

- `unique=True`: Email tidak boleh sama
- `index=True`: Buat index
- `nullable=False`: Tidak boleh kosong

Jika sebelumnya sudah pernah membuat table dengan nama `users` tapi struktur kolomnya beda, hapus table itu dengan `DROP TABLE users;`, agar tidak menimbulkan bentrok ketika insert/select.

## 6. Buat Helper Hashing Password

Di folder `app`, buat file baru bernama `utils.py`:
```
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_password.verify(plain_password, hashed_password)
```

Agar program di atas dapat dijalankan, maka perlu install package `pip install passlib[bcrypt]`

## 7. Test Register

1. Jalankan FastAPI: `uvicorn app.main:app --reload`
2. Buka browser ke Swagger UI: `http://127.0.0.1:8000/docs`
3. Temukan `/register` endpoint, pilih, lalu klik "try it out"
4. Masukan email, password, full_name, lalu execute
5. Cek di PostgreSQL: `SELECT * FROM users;`

# Day 4 - JWT Login

## 1. Apa itu JWT

JWT adalah singkatan jadi JSON Web Token. Sederhananya, JWT itu kartu identitas /ID card digital yang dikasih ke user setelah login. Sama seperti masuk ke gedung, kalau kita punya IDc card, setiap mau masuk ruangan tinggal tunjukin ID cardnya (Gak perlu login ulang).

Di dalam JWT, cuman ada string panjang, yang dibagi menjadi 3 bagian:
```
header.payload.signature
```

### Payload

Isinya:
```
{
    "sub": user.id,
    "exp": exp
}
```
- sub = siapa usernya
- exp = kapan token kadaluarsa

`user.id` cukup untuk JWT, tidak perlu email dan password. Karena:
- `id` itu unik, dan bisa dipakai untuk query ke database.
- JWT bisa di-decode. Jadi, jangan sampai menyimpan data sensitif.
- Kalau email berubah, JWT lama jadi ngaco.
- Single source of truth: Semua data tetap di database. JWT hanya menjadi identitas, bukan sumber data.
Jadi, ketika ada yang nanya ke JWT "Ini siapa?" dijawab dengan `user.id`, bukan memberitahu semua data user.

### Signature

JWT tidak hanya payload, tapi juga harus di-encode (ditandatangai) menggunakan secret key dan algorithm (biasanya `HS256`). Oleh karena itu, kita perlu fungsi untuk mengubahnya menjadi JWT string. Biasanya di library JWT manapun, polanya selalu `encode(payload, secret_key, algorithm=...)`.

Maka, tambahkan:
```
from jose import jwt

token = jwt.encode(payload, SECRET_KEY, algorith="HS256")
```

### Expired

User sudah memilki password, kenapa harus menggunakan JWT? Inilah perbedaan antara JWT dengan password biasa. Selain agar tidak harus mengisi password berkali kali ketika ganti halaman, JWT memiliki batas waktu penggunaan. Ketika masa berlaku itu sudah selesai (expired), maka JWT yang diberikan tidak bisa digunakan kembali.

Oleh karena itu, perlu ditambahkan:
```
from datetime import datetime, timedelta

now = datetime.utcnow() # Mengambil waktu saat ini
exp = now + timedelta(minutes=30) # Waktu expired JWT 30 menit
```

### Alur sebenarnya

1. Ketika user selesai login dan berhasil, server (`POST /login`) return token:
```
{
    "access_token": "...",
    "token_type": "bearer"
}
```
2. Frontend menyimpan token itu. Biasanya di localStorage, memory, atau cookie.
3. Saat user klik sesuatu (Misalkan klik profile), frontend request `GET /me`, dan frontend otomatis menambahkan header menjadi `Authorization: Bearer <token>` (Ini bukan otomatis dari HTTP, tapi otomatis dari kode frontend).

Contohnya, kalau pakai JavaScript:
```
fetch("/me", {
  headers: {
    Authorization: `Bearer ${token}`
  }
})
```

## 2. Membuat schema baru

Untuk login, kita harus mengambil data dari database untuk mencocokan input login dengan yang ada di database. Maka, kita butuh schema baru di `schemas.py`:
```
class UserLogin(BaseModel):
    email: EmailStr,
    password: str
```

## 3. Membuat endpoint `/login`

Sekarang kita buat endpoint untuk login:
```
@app.post("/login")
def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(models.User.email == user_data.email).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Email atau password salah")
    
    plain_password = user_data.password
    hashed_password = user.password

    if not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    exp = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": str(user.id), "exp": exp}

    token = jwt.encode(payload, SECRET_KEY, algorithm=HS256)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
```

### Bedah Kode

- `@app.post("/login")`: Login berarti user memasukan data. Karenanya, menggunakan metode post.
- `user_data: schemas.UserLogin`: Mengambil data dari request body menggunakan format `schemas.UserLogin`.
- `db: Session = Depends(get_db)`: Membuka pintu agar user bisa mengakses database  untuk login, dan otomatis menutupnya kembali ketika sudah selesai.
- `user == ...`: Untuk memfilter email yang dimasukan user ada di database atau tidak
- `if user is None:`: `None` itu singleton (objek unik di Python). Untuk membandingkannya bisa menggunakan `is`, sehingga tidak hanya sekedar cek value, tapi juga identity check. Maka, jika `user` tidak ada di database, jalankan kode di bawahnya.
- `raise HTTPException(...)`: Menampilkan pesan error dengan status kode 401 (Permintaan gagal karena kredensial autentikasi tidak valid), dan pesan detail.
- `plain_password`: Diambil dari password yang diisi oleh user (Dari `user_data).
- `hashed_password`: Diambil dari password yang sudah di hash di database.
- `if not pwd_context.verify(...)`: Verifikasi apakah `plain_password` yang dimasukan sama dengan `hashed_password`. Jika tidak, jalankan kode di bawahnya.

## 4. Endpoint khusus untuk melihat profil sendiri

Bayangkan di sebuah area gym, kamu sudah datang ke resepsionis, menyerahkan KTP dan memvalidasi dengan password. Resepsionis juga sudah membenarkan, bahwa kamu member gym bernama Fulan. Sebagai ganti KTP, resepsionis memberikan kartu member gym yang bisa dipakai untuk akses masuk ke kamar gym. Kartu member gym itulah yang sudah dibuat barusan (Token JWT/ access token).

Agar kartu member/Token JWT/access token yang di dapat dari resepsionis bisa dikenali, kita perlu membuat alat (endpoint) yang bisa membacanya. Sehingga ketika di depan ruang gym, tidak perlu menyebutkan *"Nama saya Fulan, dengan ID 5"*. Cukup berikan kartu member/access token itu. Endpoint ini biasa dinamakan `/me`, karena singkat, jelas, dan ini nama standar industri di hampir semua API besar.

```
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = payload["sub"]

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return {
        "id": user.id,
        "email": user.email
    }
```

### Bedah Kode
- `token: str`: Penanda bahwa isi dari variabel token adalah str.
- `Depends(oauth2_scheme)`: Ambil header `Authorization`, ambil bagian `<token>`nya, simpan ke variabel `token`. Jika user tidak mengimkan header, otomatis FastAPI (`OAuth2PasswordBearer`) langsung kirim `{"detail": "Not authenticated"}`, status `401 Unauthorized`.
- `db = Depends(get_db)`: Karena nanti akan mengambil data yang ada di database, maka otomatis harus membuka pintu akses ke databasenya.
- `try:... except:...`: Melakukan pengujian membongkar isi token. Jika invalid, maka akan menampilkan bagian `except` (error).
- `jwt.decode(...)`: Decode token yang didapat. Maka, isi yang didapat adalah dictionary payload `{"sub": str(user.id), "exp": exp}`. Lalu kita simpan ke dalam variabel `payload`.
- `payload["sub"]`: Dari dict `payload`, ambil isi dengan kata kunci `"sub"`.
- `db.query(models.User)`: Memberitahu SQLAlchemy untuk mencari di `models.User`.
- `.filter(models.User.id == user_id)`: Pilih dengan nomor id yang sama dengan `user_id` (seperti `WHERE` di bahasa SQL).
- `.first`: Mengambil data pertama yang didapat.
- `if user in None`: Kalau `user` tidak ada di database, maka jalankan kode di bawahnya (menampilkan pesan error).

### Fungsi `try-except`

Fungsi `jwt.decode` didesain untuk meledak (menampilkan error) ketika tokennya salah. Bayangkan 2 skenario saat seseorang masuk dengan token palsu:
1. Tanpa `try-except`: Server akan mengirimkan pesan error asli
`AttributeError: 'NoneType' object has no attribute 'get' in jwt_decoder.py line 45`.
Akibatnya, hacker jadi tahu *Oh, ini pakai library JWT versi ini, dan kodenya pecah di bagian ini*
2. Pakai `try-except`: Server mengirim `{"detail": "Invalid credentials"}`. Hacker  cuma bisa gigit jari, gak tahu kenapa kodenya gagal.

Dalam membongkar brangkas (decode token JWT), ada banyak hal yang bisa terjadi:
- Brangkasnya palsu (Invalid token)
- Kuncinya salah (Wrong secret key)
- Isi brangkasnya kadaluarsa (Expired token)
Jika ditulis `except Exception:`, maka artinya sama saja bilang ke Python
*Apapun masalahnya (Entah kuncinya salah atau palus), kalau ada error di bagian `try`, langsung jalankan `raise HTTPException`.*

### Status 401

Dalam standar industri, status kode 401 dapat digunakan untuk memberitahu bahwa authentication gagal:
- User tidak dapat ditemukan di database saat login
- Password salah
- Token invalid
- Token benar, tapi user di database sudah dihapus

## 5. Cek Hasil

### Manual menggunakan Swagger FastAPI

1. Buka `http://127.0.0.1:8000/docs`.
2. Test `/register` dengan memasukan email dan password.
3. Pastikan sudah masuk di database.
4. Test `/login` dengan memasukan email dan password yang tadi dibuat.
5. Cek output, lalu copy:
```
{
    "access_token": "...",
    "token_type": "bearer"
}
```
6. Test `/me`. Di Swagger, klik Authorize, lalu isi `Bearer <token>`. Jalankan `/me`. Maka harus keluar:
```
{
    "id": 1,
    "email": ...
}
```

# Result

## Fase 1: Register (Pembuatan akun)

1. User kirim email dan password
2. Server hash password, lalu simpan di database, dan kasih respon *"Akun berhasil dibuat*

## Fase 2: Login

1. User kirim email dan password
2. Server cek ke database, kalau benar membuat JWT

## Fase 3: Akses data

1. User kirim `Authorization: Bearer <token>`
2. Server decode JWT, ambil `user_id`, terus dicari di database. Kalau ketemu kasih data ke user.