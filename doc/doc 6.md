# Table 0f Contents

- [Review](#review)
- [Day 12 - Format Baru](#day-12---format-baru)
- [Day 13 - Pengaturan Password](#day-13---pengaturan-password)
- [Result](#result)

# Review

Sampai saat ini, hampir semua hal yang berkaitan dengan pendaftaran dan database user sudah selesai. Berikut yang sudah ada:
- Halaman pendaftaran anggota sesuai permintaan.
- Data pendaftaran yang diisi anggota dikirim dan disimpan ke dalam `registrations` untuk selanjutnya mendapat persetujuan dari pengurus koperasi.
- Tabel admin dibuat terpisah, dengan data pribadi lebih sedikit. Poin utama dalam tabel `admins` adalah kolom `role` yang berisi `admin`.
- Untuk kebutuhan pengujian, dibuat akun admin dengan `id = admin_ub_001`, dan `password = admin123`.
- Di halaman awal dashboard admin terdapat dua buah tabel. Yang satu berisi daftar anggota yang mengajukan pendaftaran, yang lain adalah tabel user yang sudah menjadi anggota.
- Tombol `detail` paling kanan setiap baris digunakan untuk melihat detail dari user/anggota tersebut.
- Di halaman detail, admin bisa memutuskan untuk menerima user tersebut sebagai anggota adau ditolak.
- Jika admin menyetujui, secara otomatis dibuat `member_id` dan `password` yang akan digunakan user/anggota untuk login ke dashboard masing-masing.
- Semua endpoint/halaman sudah dibuat tampilan html dan css-nya, dan bersifat responsible.

Selanjutnya, berikut yang perlu ditambah dan diperbaiki:
- Reset password oleh admin/pengurus
- Pop-up setelah berhasil daftar *Terima kasih sudah mendaftar menjadi calon anggota Koperasi UB Mandiri Sejahtera. Data akan diperiksa dan divalidasi oleh pengurus/admin. Mohon tunggu konfirmasi selanjutnya dari pengurus Koperasi*.
- Format `member_id` anggota diubah menjadi `UB[tahun]-[no urut anggota]`. Contohnya `UB2026-354`.
- Aturan password minimal 8 karakter, dengan kombinasi huruf besar dan kecil, serta angka.
- Saat password dibuat atau direset oleh admin, admin bisa melihat passwordnya. Saat sudah diganti oleh anggota, admin tidak bisa melihat passwordnya.
- Setelah data disetujui, otomatis terbuat file `.pdf` yang bisa dicetak untuk keperluan pendaftaran fisik. Templatenya seperti `Data Anggota Koperasi.pdf`.
- Syarat-syarat menjadi anggota Koperasi yang ada di `Data Anggota Koperasi.pdf`

# Day 12 - Format Baru

## 1. Pengaturan Folder

Karena sistem yang semakin besar, perlu ada penyesuaian lagi dalam struktur file.

### `/core`

`/core` adalah tempat untuk kode-kode inti (core utilities) yang digunakan di banyak bagian aplikasi. Folder ini berisi konfigurasi global/menyeluruh dan pengaturan dasar yang mengontrol jalannya aplikasi yang sifatnya jarang berubah. File yang akan dipindahkan kedalam sini yaitu `config.py`, `.database.py`

### `/models` dan `/schemas`

Seperti bisa dilihat, model dan schema yang dibuat sudah sangat banyak. Ini akan membingungkan jika terus bertambah. Maka dari itu, model dan schema akan dipecah sesuai kegunaannya, dan disimpan dalam folder:
```
app/
├── models/
│   ├── user.py
│   ├── admin.py
│   └── product.py
├── schemas/
│   ├── user.py
│   └── token.py
├── ...
```

### `/routers`

Folder ini bertanggung jawab mengatur endpoints/URL. Router ini sebaiknya tidak berisis logika bisnis yang rumit. Tugasnya hanya menerima data lalu mengembalikan respon. Untuk logika bisnis seperti CRUD, sebaiknya disimpan dalam folder `/services`. Tapi karena belum dibutuhkan, folder `/services` ini belum dibuat.

### `__init__.py`

Karena models dan schemas dipecah menjadi banyak bagian file `.py`, cara import nya pasti berbeda. Tidak cukup `from app import models`. Ini akan menghasilkan error. Sebenarnya banyak cara untuk import, seperti
- import setiap `class` yang akan digunakan, misal `from app.models.user import Registration, User`.
- `from app.schemas import user as schema` lalu dipanggil, misal `response_model=schema.Registration`.
- Yang akan dipakai yaitu menginisiasikan `__init__.py` di setiap folder. Di router, cukup `from app import models, schemas`. Panggil dengan `models.Users`.

Di dalam `models`, isi `__init__.py` dengan:
```
from .admin import Admin
from .product import Product
from .user import Registration, User
```

Isi `schemas/__init.py`:
```
from .user import *
from .product import *
```

## 2. Format`member_id`

Dalam endpoint `/registrations/{user_is}/approve` di file `/routers/admin.py`, ganti kode generate `member_id`-nya menjadi:
```
year = datetime.now().year
gen_id = f"UB{year}-{models.Registration.id:03d}"
```

### Bedah Kode
- `datetime.now().year`: Mengambil tanggal saat anggota disetujui (Hanya mengambil tahunnya saja).
- `models.Registration.id`: Mengambil `id` anggota dalam database.
- `:03d`: Mengubah format `id` menjadi format tiga digit.

## 3. Password Otomatis

Dalam `app/core/`, buat file baru bernama `password.py` yang akan memuat kode untuk generate password otomatis:
```
import secrets
import string
import random

def generate_password(length: int = 8) -> str:
    if length < 8:
        raise ValueError("Panjang password minimal 8 karakter")

    lowercase = secrets.choice(string.ascii_lowercase)
    uppercase = secrets.choice(string.ascii_uppercase)
    digit = secrets.choice(string.digits)

    all_chars = string.ascii_letters + string.digits
    remaining = [
        secrets.choice(all_chars)
        for _ in range(length - 3)
    ]

    password_chars = [lowercase, uppercase, digit] + remaining

    random.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)
```

### Bedah Kode

- `length: int = 8`: Fungsi `generate_password` menerima parameter `length` yang berupa integer/bilangan bulat. Jika tidak diisi, akan diisi otomatis (default) dengan nilai `8`.
- `-> str`: Hasil fungsi harus dikembalikan dalam bentuk string.
- `raise`: Menghentikan program dan memunculkan error.
- `string.ascii_lower`: Berisi kumpulan karakter yang sudah disediakan oleh python berupa alfabet kecil.
- `secrets.choice(...)`: Memilih salah satu karakter di dalam kurung `(...)` secara acak. Dengan 
- `all_chars = ...`: Memuat semua karakter dalam `string.ascii_letters` ditambah `string.digits`.
- `remaining = [...]`: Mengisi kekurangan jumlah karakter yang dibutuhkan.
- `random.SystemRandom().shuffle(...)`: Mengacak posisi karakter. Kalau tidak, huruf kecil, besar, dan angka selalu muncul di awal. Itu akan membuat pola mudah ditebak.
- `"".join(password_chars)`: Mengubah list menjadi string.

### Mengapa Menggunakan List?

Alasan utamanya yaitu karena fungsi `shuffle()` hanya bisa mengacak list. Karena string bersifat immutable (tidak bisa diubah isi atau urutannya secara langsung), python akan memberikan error seperti:
```
TypeError: 'str' object does not support item assignment
```
Karena itu prosesnya biasanya membuat list karakter, acak list, baru gabungkan lagi menjadi string.

### Underscroe (`_`) dalam `for`

Pengulangan `for` merupakan dasar yang harus dikuasai oleh setiap developer. Biasanya seperti 
```
for i in range(3):
    print("Halo")
```
Hasilnya, `Halo` dicetak sebanyak 3 kali. Namun, coba perhatikan lagi. Variabel `i` di sini sebenarnya tidak dipakai. Tidak ada perintah `print(i)` atau `i + 1`. Nah, untuk memberi tahu *Saya hanya butuh pengulangannya, nilai variabelnya tidak dipakai*, digunakanlah underscore(`_`):
```
for _ in range(3):
    print("Halo")
```
Haslinya tetap sama. Jadi, underscore adalah konvensi Python untuk variabel yang sengaja diabaikan.

## 4. Jalankan `generate_password`

Saatnya menerapkan fungsi `generate_password` saat admin menyetujui anggota tersebut. Di endpoint `/registartions/{user_id}/approve` dalam `admin.py`, ubah `hashed_pw` menjadi:
```
from app.core.password import generate_password

...
hashed_pw = security.hash_password(generate_password(8))
...
```

# Day 13 - Pengaturan Password

Alur password yang akan digunakan yaitu:
- Calon anggota mengisi formulir pendaftaran tanpa memasukan password.
- Data disimpan di tabel `registrations`.
- Admin menekan tombol "Terima"
- Sistem membuat `member_id` dan password sementara (`temporary_password`) sekaligus `hashed_password` ke tabel `users`.
- Password asli (`temporary_password`) ditampilkan ke admin.
- Saat login, anggota diminta mengganti password.
- Setelah anggota mengganti password, password yang asli tidak ditampilkan di dashboard admin, melainkan diganti dengan tulisan *Password sudah diganti oleh anggota*.

## 1. Kolom Baru

Di `app/models/user.py`, buat kolom baru:
```
temporary_password = Column(String, nullable=True)
must_change_password = Column(Boolean, default=True)
```

Jangan lupa sesuaikan format input `new_user` di `app/routers/admin.py` agar tidak terjadi error:
```
member_id=gen_id,
temporary_password=temporary_password,
must_change_password=True,
hashed_password=hashed_pw,
...
```

Agar `temporary_password` bisa terlihat di dashboard admin, sesuaikan juga template `admin_user_detail.html`:
```
Password: {{ user.temporary_password or 'Password sudah diganti oleh anggota' }}
```

Karena tadi sudah merubah isi models, perlu perbarui tabel di SQLAlchemy dengan alembic:
```
alembic revision --autogenerate
alembic stamp head
```

# Result