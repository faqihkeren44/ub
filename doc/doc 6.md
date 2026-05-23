# Table 0f Contents

- [Review](#review)
- [Day 12 - Format Baru](#day-12---format-baru)
- [Day 13 - Edit Profil](#day-13---edit-profil)
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

# Day 13 - Edit Profil

Alur password yang akan digunakan yaitu:
- Calon anggota mengisi formulir pendaftaran tanpa memasukan password.
- Data disimpan di tabel `registrations`.
- Admin menekan tombol "Terima"
- Sistem membuat `member_id` dan password sementara (`temporary_password`) sekaligus `hashed_password` ke tabel `users`.
- Password asli (`temporary_password`) ditampilkan ke admin.
- Saat login, anggota diminta mengganti password.
- Setelah anggota mengganti password, password yang asli tidak ditampilkan di dashboard admin, melainkan diganti dengan tulisan *Password sudah diganti oleh anggota*.

## 1. Verifikasi Token User

Buat fungsi di `/routers/auth` yang mengecek apakah user sudah login, dan apakah memang dia user yang berhak:
```
def verify_user(
        request: Request,
        db: Session = Depends(database.get_db)
):
    ...
```

Di dalam fungsi `verify_user`, berikut langkah yang dilakukan:
1. Mengambil token JWT yang ada di cookie `token_cookie = request.cookies.get("access_token")`.
2. Kalau tidak ada, kembalikan `return RedirectResponse(url="/auth/login?msg=not_login", status_code=303)`
3. Bongkar token dan ambil `user_id`:
```
try:
    token = token_cookie.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("sub")
```
4. Jika tidak ada `user_id` (`None`), kembalikan `return RedirectResponse(url="/auth/login?msg=not_login", status_code=303)`.
5. Jika dalam mencoba (`try`) bongkar token ada error:
```
    except ExpiredSignatureError:
        response = RedirectResponse(url="/auth/login?msg=expired", status_code=303)
        response.delete_cookie("access_token")
        return response
    except Exception as e:
        print(f"LOG ERROR: {e}")
        return RedirectResponse(url="/auth/login?msg=error", status_code=303)
```
6. Mencari di database, apakah nilai `user_id` dalam token memang benar-benar terdaftar dalam database:
```
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        print(f"LOG: Admin dengan ID {user_id} tidak ada di database!")
        response = RedirectResponse(url="/auth/login?msg=admin_not_found", status_code=303)
        response.delete_cookie("access_token")
        return response
```
7. Mengembalikan nilai: `return user`

## 2. Kolom Baru

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

## 3. Tambah Schema

Schema untuk mengubah password:
```
from pydantic import BaseModel, field_validator, model_validator

class PasswordChange(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password minimal 8 karakter")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Harus mengandung huruf besar")

        if not re.search(r"[a-z]", value):
            raise ValueError("Harus mengandung huruf kecil")

        if not re.search(r"\d", value):
            raise ValueError("Harus mengandung angka")

        return value
```

### Bedah Kode

- `import field_validator, model_validator`: Keduanya akan digunakan dalam validasi Pydantic ini. Agar validasi bisa berjalan, keduanya harus di-import dulu.
- `class PasswordChange`: Nama Schema yang akan digunakan untuk menerima data dari user ketika mengganti password. Misalnya user mengisi form `<input name="new_password">`
- `BaseModel`: Mewarisi class `BaseModel` dari Pydantic agar Python tahu bahwa `PasswordChange` merupakan Pydantic, sehingga bisa menjalankan tugasnya untuk memvalidasi input.
- `current_password: str`: Field bernama `current_password` harus berupa string.
- `@field_validator`: Ini disebut decorator, yaitu instruksi tambahan untuk fungsi di bawahnya. Artinya, jalankan fungsi `validate_password()` untuk `new_password`.
- `@classmethod`: Menandakan fungsi ini milik class, bukan untuk objek tertentu. Validator Pydantic memang harus menggunakan format seperti ini.
- `cls`: Berisi class `PasswordChange`.
- `value`: Nilai field yang sedang divalidasi. Jika user mengirim `"new_password": "123"`, maka `value = "123"`.
- `len()`: Menghitung jumlah karakter `value`.
- `re.search`: Mencari pola dalam teks. Kalau dalam `value` tidak ada huruf besar (`[A-Z]`), maka tampil `ValueError`.

## 4. Validator Password

Di dalam schema `PasswordChange`, tambahkan validasi antar data yang dimasukan:
```
    @model_validator(mode="after")
    def verify_password_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("Konfirmasi password baru tidak cocok")
        if self.current_password == self.new_password:
            raise ValueError("Password baru tidak boleh sama dengan password lama")
        return self
```

### Bedah Kode

- `model_validator`: Jika `@field_validator` hanya memeriksa satu data spesifik (seperti apakah `new_password` mengandung huruf besar`), maka @model_validator memeriksa hubungan atau kombinasi antar field. Validator ini memilki akses ke seluruh data yang diinput melalui objek `self`.
- `mode="after": Fungsi ini beru akan dijalankan setelah Pydantic selesai memastikan bahwa semua data yang dikirim lolos validasi tipe data awal dan lolos validator field.
- `def validator_password_match(self)`: Fungsi untuk memeriksa logika dalam pengubahan password. Di dalam fungsi ini memanfaatkan `self` untuk mengambil nilai yang sudah divalidasi untuk lalu dibandingkan.
- `return self`: Jika tidak ada kesalahan (`ValueError`), fungsi mengembalikan objek data yang utuh dan bersih kepada FastAPI/Router.

## 5. Cara Pydantic Membaca Form HTML

Jangan lupa bahwa Pydantic tidak bisa membaca Form HTML secara murni. Secara bawaan (native), FastAPI dirancang untuk menerima data JSON. Sedangkan Form HTML pada umumnya mengirim data dengan format FORM Data (`application/x-www-form-urlencoded`). Solusinya, buat fungsi helper:
```
def get_password_form(
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
) -> PasswordChange:
    return PasswordChange(
        current_password=current_password,
        new_password=new_password,
        confirm_password=confirm_password
    )
```

### Bedah Kode

- `current_password: str = Form(..)`: Menangkap data Form HTML.
- `-> PasswordChange:`: Type hinting bahwa fungsi `get_password_form` ini akan mengeluarkan sebuah objek yang memiliki format sesuai dengan cetakan `PasswordChange`.
- `return PasswordChange(...)`: Setelah ketiga data tersebut ditangkap dari form, data dimasukkan ke dalam `PasswordChange(...)`. Proses validasi otomatis terjadi di dalamnya. Jika lolos pemeriksaan `PasswordChange`, data dibungkus menjadi objek dan dikirim (return) ke router.

## 6. Router Ganti Password

Untuk menjalankan penggantian password, berikut routernya:
```
@router.post("/change-password")
def change_password(
    request: Request,
    form_data: PasswordChange = Depends(get_password_form),
    db: Session = Depends(get_db),
    user : models.User = Depends(verify_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Password lama salah")

    user.hashed_password = hash_password(new_password)

    db.commit()
    return RedirectResponse("/profile?password_changed=1", status_code=303)
```

### Bedah Kode

- `Depends(get_password_form)`: `Depends` adalah singkatan dari Dependencies (Ketergantungan). Ketika user menekan submit saat ubah password, FastAPI melihat ada `Depends(...)`. FastAPI langsung paham *Oh, sebelum menjalankan isi fungsi sendiri, harus menjalankan fungsi `get_password_form` terlebih dahulu.
- `form_data: PasswordChage`: Type hinting bahwa variabel `form_data` adalah sebuah objek yang sesuai skema PasswordChange.
- `Depends(verify_user)`: Menjalankan fungsi `verify_user` sebelum menjalankan kode.
- `current_user = request.state.user`: 

## 4. Tampilan Edit

```
<h2>Ganti Password</h2>

<form
    method="post"
    action="/profile/change-password"
>

    <label>Password Lama</label>
    <input
        type="password"
        name="current_password"
        required
    >

    <label>Password Baru</label>
    <input
        type="password"
        name="new_password"
        required
    >

    <label>Konfirmasi Password Baru</label>
    <input
        type="password"
        name="confirm_password"
        required
    >

    <button type="submit">
        Ganti Password
    </button>

</form>
```

## 5. Edit Profil

### Schema

```
class UserUpdate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Nomor telepon hanya boleh angka")
        return value
```

### Router

```
# routers/profile.py

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/update")
def update_profile(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    current_user = request.state.user

    user = db.query(User).filter(
        User.id == current_user.id
    ).first()

    user.full_name = full_name
    user.email = email
    user.phone = phone

    db.commit()

    return RedirectResponse(
        "/profile?success=1",
        status_code=303
    )
```

### HTML

```
<h2>Edit Profil</h2>

<form method="post" action="/profile/update">

    <label>Nama Lengkap</label>
    <input
        type="text"
        name="full_name"
        value="{{ user.full_name }}"
        required
    >

    <label>Email</label>
    <input
        type="email"
        name="email"
        value="{{ user.email }}"
        required
    >

    <label>Nomor Telepon</label>
    <input
        type="text"
        name="phone"
        value="{{ user.phone }}"
        required
    >

    <button type="submit">
        Simpan Perubahan
    </button>

</form>
```


# Result