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
│       ├── auth.py           # Endpoint terkait Autentikasi
│       └── products.py       # Endpoint terkait Produk
├── alembic/                  # Folder migrasi database
│   ├── versions/             # File histori perubahan tabel
│   ├── env.py                # Konfigurasi penghubung Alembic & App
│   └── script.py.mako        # Template migrasi
├── .env                      # File rahasia (Password & URL DB)
├── alembic.ini               # Konfigurasi utama Alembic
└── requirements.txt          # Daftar library yang diinstal
```

## 2. Function `get_db()`

Seperti yang sudah diketahui, fungsi ini merupakan penjaga yang membuka dan menutup kembali pintu ke database. Karena semua endpoint sudah dipisah (tidak dijadikan satu di file `main.py`), dan kebanyakan dari endpoint membutuhkan akses ke database. Untuk menyingkat kode, pindahkan fungsi `get_db()` ke dalam file `database.py`:

```
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Dalam pemanggilannya nanti, ada dua cara:
1. Import langsung fungsi. Ini cara yang paling sering dipakai karena kodenya jadi lebih pendek saat digunakan.
```
from ..database import get_db
@router.post("/login")
def login(db: Session = Depends(get_db)):
    ...
```
2. Import modul database. Cara ini bagus jika ingin menghindari nama fungsi (misal ada fungsi `get_db` lain dari library yang berbeda.
```
from .. import database
@router.post("/login")
def login(db: Session = Depends(database.get_db)):
    ...
```

## 3. `app/routers/products.py`

Pindahkan logika terkait produk dari `main.py` ke sini. Sebagai pengganti `@app`, gunakan `.APIRouter`(`@router`). Jangan lupa juga ganti `get_db` menjadi `database.get_db`:
```
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

@router.get("/", response_model=list[schemas.ProductOut])
def get_products(db: Session = Depends(database.get_db)):
    products = db.query(models.Product).all()
    return products

@router.post("/", response_model=schemas.ProductOut)
def input_product(product_data:schemas.ProductCreate, db: Session = Depends(database.get_db)):
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

## 4. `app/routers/users.py`

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
@router.post("/register", response_model=schemas.UserOut)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    ...
```

## 5. `app/routers/auth.py`

Fungsi utama file ini sebagai pusat kendali sistem autentikasi dan otorisasi. Saat ini, akan dibahas untuk sistem loginnya terlebih dahulu.

### `APIRouter`

Pertama, kita definisikan dulu `router` agar bisa jadi pintu masuk ke lorong-lorong kuhusus dari `main.py`. 
Untuk `tags` diisi `[Authentication]` agar semua endpoint yang ada di bawah ini dikelompokan dalam satu judul. 
Karena `prefix` bersifat opsional, bisa diabaikan (tidak ditambah), sehingga nanti alamatnya langsung `/login`. Atau ditambah, nanti alamatnyna jadi `/auth/login`.
```
router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)
```

### Pendefinisian awal

- `@router.post("/login")`: Pertama, beri tahu fungsi di bawah ini adalah sebagai endpoint 
- `response: Response`: Parameter ini memberikan akses ke objek respons yang akan dikirim balik ke browser. Nantinya, ini berguna jika kita ingin menyelipkan Cookie.
- `OAuth2PasswordRequestForm`: Alat dari FastAPI untuk menangkap data dari form login. Secara otomatis, ia mencari input bernama username dan password.
- `Depends()`: FastAPI akan otomatis mengisi variabel user_data ini dengan data yang dikirim user dari form.
- `db: Session = Depends(database.get_db)`: Meminjam koneksi ke database. 

### Pencarian Data

- `user = db.query(models.User)...`: Di sinilah pencarian dimulai *"Tolong cari di tabel User (`models.User`)"*.
- `.filter(models.User.email == user_data.username)`: Ini adalah kriteria pencariannya. *"Apakah ada email di database yang sama dengan yang diketik user?"*. Ingat, `OAuth2PasswordRequestForm` selalu menyimpan data email/username di atribut `.username`.
- `.first()`: Ambil hasil pertama yang ditemukan. Jika tidak ada yang cocok, variabel `user` akan berisi `None`.

### Response

Ada perubahan di akhir kode tentang nilai yang dikembalikan oleh `return`. Berikut yang ditambahkan:
- `RedirectResponse(url="/me", ...)`: Ini memberitahu browser *"Setelah urusan di sini selesai, segera pergi ke halaman `/me`"*.
- `status_code=status.HTTP_303_SEE_OTHER`: Cara standar untuk mengatakan bahwa setelah `POST` (login), browser harus melakukan `GET` ke alamat baru.
- `response.set_cookie(...)`: Server menitipkan token ke dalam penyimpanan aman milik browser (Cookie). Berbeda dengan sebelumnya yang hanya teks mentah dalam dict dan disimpan di `localStorage`.
- `key="access_token`: Label atau nama laci penyimpanan di browser. Nanti, saat user pindah ke halaman `/me`, FastAPI akan mencari Cookie dengan nama `"access_token"`.
- `value=f"Bearer {token}"`: Di dunia web, tidak cukup membawa tokennya, tapi juga harus punya tipe. `Bearer` artinya siapapun yang membawa (bearing) token ini, dia berhak masuk.
- `httponly=True`: Fitur keamanan agar kode JvaScript jahat tidak bisa mencuri token. Hanya browser yang bisa memegangnya.
- `max_age=1800`: Hancur otomatis setelah 1800 detik (30 menit). Atau bisa menggunakan perkalian (`max_age = 60 * 30`). Atau menggunakan `timedelta` juga bisa.
- `samesite="lax"`: Menjaga agar cookie tidak dikirim sembarangan saat user klik link dari situs luar.

## 6. Hubungan Antar File

Sekarang, hapus kode itu dari `main.py`, ganti dengan memanggil router yang dibuat:
```
from .routers import products, users, auth

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Selamat datang di API UB!"}
```

### Bedah kode

- `from .router import products`: Import departemen atau rute nya.
- `app.include_router(products.router)`: Agar FastAPI tau rute-rute di file `products.py`.

## 7. File `app/routers/members.py`

File ini spesifik membahas data user, mulai dari profil, tabungan, bagi hasil, dsb. Jadi, buat file baru bernama `members.py` di folder `/routers/`.
Isinya yang pertama yaitu endpoint `/me` yang ada dalam `app/main.py`:
```
router = APIRouter(
    prefix="/dashboard",
    tags=["Member Area"]
)

@router.get("/me")
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
Karena sekarang token ada di Cookies, perlu ada penyesuaian dalam decode nya:

### Mengambil `access_token`

Masih ingat `request: Request`? Di FastAPI, `Request` adalah objek raksasa yang berisi semua informasi tentang kunjungan user. Mulai dari alamat IP, jenis browser, hingga Cookie yang dibawa. Saat ada `def get(request: Request)`, menyuruh FastAPI *"Tolong ambilkan semua data dari koneksi ini dan masukan ke variabel `request`"*.
Ada dua cara untuk mengambil Cookie dari objek `Request`:

1. Lewat parameter Cookie:
    `def get_me(access_token: str = Cookie(None)):`
2. Kadang butuh `request` untuk hal lain (seperti merender template Jinja2). Bisa mengambil cookie langsung dari dalamnya:
    ```
    def get_me(request: Request):
    token = request.cookies.get("access_token")
    ```

Tambahan untuk pengecekan, bisa tambahkan `print(f"Token yang diterima: {access_token}")`. Ini hanya debugging bahwa token benar-benar diterima.

### Membuka Token

Ingat saat login, token disimpan dengan format `Bearer {token}`. Dalam cookie, teksnya terlihat seperti `Bearer ...`. Pertama, potong teksnya menjadi dua bagian berdasarkan spasi menggunakan `.split(" ")`. Hasilnya, akan ada index `[0]` yang berisi kata `"Bearer"`, dan index [1] yang berisi token JWT.

Token JWT tidak bisa langsung dibaca begitu saja, karena menggunakan kunci (`SECRET_KEY`). Proses membongkarnya itu menggunakan `jwt.decode`. 

Ganti `raise HTTPException` dengan `return RedirectResponse(url="/login")`. Artinya, jika `access_token` belum ada, akan ditendang kembali ke halaman `/login`.

### Cara mendapatkan `"sub"`

Sebelumnya, untuk mendapatkan `"sub"` atau `id` dalam `payload`, menggunakan kode `payload["sub"]`. Namun, ada kekurangan jika ditulis seperti itu. Jika karena suatu alasan (misalnya token rusak) kunci `"sub"` tidak ditemukan di dalam `payload`, Python akan langsung Error dan memunculkan `KeyError`. Aplikasi bisa langsung crash di baris tersebut jika tidak dibungkus `try-except`.

Ganti menjadi `payload.get("sub")`. Haslinya, jika kunci `"sub"` tidak ada, Python tidak akan marah. Dia hanya akan memberikan nilai `None`. Setelahnya, bisa melakukan pengecekan yang lebih sopan, misalnya `if not user_id: return RedirectResponse(url="/login")`

### Kode Akhir

```
def login_user(response: Response, user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_data.username).first()
    
    if user is None:
        raise HTTPException(status_code=401, detail="Email atau password salah")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    exp = datetime.utcnow() + timedelta(minutes=30)
    payload = {"sub": str(user.id), "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    response = RedirectResponse(url="/me", status_code=status.HTTP_303_SEE_OTHER)

    response.set_cookie(
        key="access_token", 
        value=f"Bearer {token}", 
        httponly=True,
        max_age=1800,
        samesite="lax" 
    )

    return response
```