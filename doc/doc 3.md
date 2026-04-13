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

## Day 7 - Penerapan

### 