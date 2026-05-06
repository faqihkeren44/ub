# Table Of Contents

- [Review](#review)
- [Day 9 - Update Database](#day-9---update-database)
- [Day 10 - Update Register Form](#day-10---update-register-form)

# Review

Pembuatan MVP register dan login sudah selesai. Namun, ada tambahan dan perubahan yang diajukan, berikut detail penjelasannya:

## 1. Form Pendaftaran

Database setiap anggota dan formulir registrasi setiap anggota disesuaikan dalam google form berikut:
```
https://docs.google.com/forms/d/e/1FAIpQLSfV4WeC5GikSRXo_mHeOnEAv7HywzYvwMhYHQelfFwygdTW_Q/viewform
```

Berikut isinya:
- Nomor Anggota
- Nama Lengkap
- Tempat Tanggal Lahir
- Jenis Kelamin
- Alamat Rumah
- No Kartu Keluarga
- No KTP
- No HP/Telp
- Nama Istri/Suami
- Kelompok/DKM:
    - DKM DARUSSALAM - Gunung Gede
    - DKM AL BAROKAH - Pondok Rumput
    - DKM DARUL HIKMAH - Green Arofah
    - DKM AR-RAUDHOH - Pakuan
    - DKM BAITUL IZZA - Tajur
    - DKM AN-NASHR - Cikaret
    - DKM AR-ROHMAN - Ciapus
- Jumlah Setoran Simpanan Wajib
    - Rp. 25000
    - Rp. 50000
    - Rp. 100000
    - Rp. 250000
    - Rp. 500000

## 2. Alur Pendaftaran Anggota

- Setelah anggota mengisi formulir, data formulir terkirim ke pengurus.
- Data diverifikasi oleh pengurus.
- Jika pengurus sudah menyetujui, baru data disimpan ke database dengan otomatis mendapat Id Anggota dan Password

## 3. Profile Website

Pada halaman home website, ada bagian profile yang perlu ada tambahan dan disesuaikan dengan file "Profile Koperasi UB Mandiri Sejahtera"

# Day 9 - Update Database

## 1. Melihat Tabel `users`

Sebelum mangubah tabel `users`, bisa dicek terlebih dahulu seperti apa tabel yang sudah pernah dibuat sebelumnya. Caranya, masuk ke Command Prompt, lalu masukan perintah:
- `psql -U postgres`: Masuk ke PostgreSQL dengan user bernama `postgres`.
- `\l`: Melihat daftar database yang sudah dibuat.
- `\c ub_db`: Masuk ke database `ub_db`.
- `\dt`: Cek tabel yang sudah dibuat.
- `\d users;`: Melihat informasi terkait tabel `users`.
- `SELECT * FROM users;`: Melihat isi semua yang tercatat di dalam tabel `users`.
- `\q`: Keluar dari database PostgreSQL

Karena perubahannya sangat besar, dan isi dari tabel juga bukanlah data yang penting, tabel `users` ini bisa dihapus dengan perintah `DROP TABLE users;` di PostgreSQL. Selanjutnya, sesuaikan model di Python (`models.py`), dan jalankan ulang skip `Base.metadata.create_all(bind=engine)`

### Tabel `alembic_version`

Sebelumnya tidak pernah buat tabel `alembic_version`, tapi kok tiba-tiba ada di database? Ini adalah tabel khusus yang digunakan Alembic sebagai alat migrasi database untuk SQLAlchemy. Fungsinya sebagai versi kontrol untuk struktur database.

Di dalamnya hanya terdapat satu kolom dan satu baris yang berisi kode unik (hash). Kode ini menunjukan revisi terakhir yang telah diterapkan ke database. Tabel ini memastikan tidak menjalankan migrasi yang sama dua kali, yang bisa menyebabkan error pada database.

## 2. Mendifinisikan Pilihan Terbatas

Setelah mengapus/drop tabel `users` dengan perintah `DROP TABLE users;` di PostgreSQL, selanjutnya ubah model `User` dalam `models.py`:
```
import enum
from sqlalchemy import Column, Integer, String, Enum
from database import Base

class KelompokDKM(enum.Enum):
    DARUSSALAM = "DKM DARUSSALAM - Gunung Gede"
    AL_BAROKAH = "DKM AL BAROKAH - Pondok Rumput"
    DARUL_HIKMAH = "DKM DARUL HIKMAH - Green Arofah"
    AR_RAUDHOH = "DKM AR-RAUDHOH - Pakuan"
    BAITUL_IZZA = "DKM BAITUL IZZA - Tajur"
    AN_NASHR = "DKM AN-NASHR - Cikaret"
    AR_ROHMAN = "DKM AR-ROHMAN - Ciapus"

class SetoranWajib(enum.IntEnum):
    LEVEL_25K = 25000
    LEVEL_50K = 50000
    LEVEL_100K = 100000
    LEVEL_250K = 250000
    LEVEL_500K = 500000

class GenderType(enum.Enum):
    MALE = "Pria"
    FEMALE = "Wanita"

class UserStatus(IntFlag):
    PENDING = 1
    APPROVED = 2
    REJECTED = 4
```

### Enum

Enum adalah singkatan dari Enumeration, yang secara harfiah berarti penyebutan satu per satu. Dalam pemrograman, Enum digunakan untuk membuat sekumpulan konstanta (nilai yang tetap dan tidak berubah) yang memiliki nama yang jelas. Dengan menggunakan Enum, pilihan yang tersedia akan dibatasi. Jika pilihannya hanya A, B, atau C, user tidak bisa memasukkan Z.

Dalam Python, tanda kurung menunujukan Inheritance (Pewarisan). Jadi, untuk menggunakan enum, bisa dituliskan dengan memanggil modul `enum` dulu, baru mengambil kelas `Enum` di dalamnya. Atau langsung `Enum`, jika sebelumnya sudah melakukan `from enum Import Enum`.

Adapun `IntEnum` adalah variasi khusus dari `Enum` yang memastikan nilainya diperlakukan sebagai angka. Selain `IntEnum`, ada juga `IntFlag` yang cocok untuk logika Bit-wise.

## 3. Model Utama `users`

Bentuk baru model atau table `users` adalah seperti ini:
```
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # Data Identitas
    full_name = Column(String, nullable=False)
    birth_info = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    family_card_number = Column(String, nullable=False) # No KK
    identity_number = Column(String, unique=True, nullable=False) # No KTP
    phone_number = Column(String, nullable=False)
    spouse_name = Column(String, nullable=True)
    
    # Pilihan Terbatas
    dkm_group = Column(Enum(KelompokDKM), nullable=False)
    mandatory_savings = Column(Enum(SetoranWajib), nullable=False)

    # Akun Anggota
    member_id = Column(String, unique=True, nullable=True) 
    hashed_password = Column(String, nullable=True)
```

## 4. Status

Untuk memberitahu anggota bagaimana status registrasi sedang berlangsung, dibuat `status_flags`. Ketika suda di-approve oleh pengurus, nama pengurus tersebut akan disimpan dalam kolom `approved_by`:
```
class User(Base):
    __tablename__ = "users"
    ...
    # Menggunakan Integer untuk menyimpan bitwise
    status_flags = Column(Integer, default=UserStatus.PENDING.value)
    approved_by = Column(String, nullable=True)
```

### Bedah Kode

Cara memasukan nilai default pada kolom bit-wise bukan dengan `default=Enum(UserStatus)`, melainkan memasukan langsung nilai dari Enum tersebut:
- `UserStatus`: Memanggil class `UserStatus`
- `.PENDING`: Memilih status `PENDING`
- `.value`: Mengambil nilai yang ada dalam `UserStatus.PENDING` (`1`)

### Kenapa 3 angka?

Dalam sistem bit-wise yang umum digunakan di industri (seperti status e-commerce tadi) itu menggunakan angka pangkat dua (1, 2, 4, 8, 16, ...) karena setiap angka tersebut menguasai satu posisi bit yang unik.

Kalau menggunakan angka 3 (11), komputer akan bingung. Secara logika matematika biner, angka 3 adalah hasil dari 1 + 2. Artinya, sistem bisa menganggap User tersebut berstatus Pending (1) SEKALIGUS Approved (2). Dengan menggunakan 1, 2, 4, tidak ada kombinasi angka lain yang bisa menghasilkan angka 4 selain angka 4 itu sendiri.

## 5. Versi Alembic

Jalankan `main.py`. Dengan kode `Base.metadata.create_all(bind=engine)` yang ada di dalamnya, otomatis Python membuat tabel `users` yang belum ada di database.

Jika memperbarui manual di PostgreSQL, perubahan ini tidak akan otomatis tersimpan di Alembic. Sama seperti GitHub, perbedaan struktur tabel di database dengan yang disimpan di Alembic ini bisa menyebabkan konflik di masa depan.

Setelah Menghapus tabel `users` dan update `models.py`, ada dua cara untuk mereset sinkronisasi:
1. Menghapus folder `versions` dan tabel `alembic_version`, lalu melakukan `alembic revision --autogenerate` seolah-olah ini adalah database baru.
2. Menggunakan perintah `alembic stamp head` untuk memberi tahu database bahwa struktur yang sekarang sudah merupakan versi terbaru, tanpa menjalankan skrip migrasi.

Jika berhasil, akan muncul:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

# Day 10 - Update Register Form

## 1. Penyesuaian `schemas.py`

Karena kode akan panjang di `users.py`, tambahkan metode pembantu agar skema `UserCreate` bisa membaca data dari form. Berikut kode nya:
```
class UserCreate(BaseModel):
    full_name: str
    birth_info: str
    gender: str
    address: str
    family_card_number: str
    identity_number: str
    phone_number: str
    spouse_name: Optional[str] = None
    dkm_group: str
    mandatory_savings: int
    password: str

    @classmethod
    def as_form(
        cls,
        full_name: str = Form(...),
        birth_info: str = Form(...),
        gender: str = Form(...),
        address: str = Form(...),
        family_card_number: str = Form(...),
        identity_number: str = Form(...),
        phone_number: str = Form(...),
        spouse_name: Optional[str] = Form(None),
        dkm_group: str = Form(...),
        mandatory_savings: int = Form(...),
        password: str = Form(...)
    ):
        return cls(
            full_name=full_name,
            birth_info=birth_info,
            gender=gender,
            address=address,
            family_card_number=family_card_number,
            identity_number=identity_number,
            phone_number=phone_number,
            spouse_name=spouse_name,
            dkm_group=dkm_group,
            mandatory_savings=mandatory_savings,
            password=password
        )
```

### Bedah Kode

- Bagian pertama mendefinisikan skema Pydantic, yang memastikan bahwa setiap data yang masuk memiliki tipe yang benar. Field yang wajib diisi seperti `full_name`,`identity_number`, dll. Atau field opsional seperti `spouse_name`.
- `as_form`: Secara bawaan, FastAPI tidak bisa langsung membaca model Pydantic dari input form HTML biasa (`application/x-www-form-urlencoded`). Metode `@classmethod def as_form(...)` berfungsi sebagai pembantu untuk mengumpulkan data dari setiap kolom input di file `register.html`, dan membungkus semua data itu ke dalam objek `UserCreate`.
- `@classmethod`: Fungsi itu milik kelas itu sendiri, bukan milik objek (instance) tertentu.
- `cls`: Parameter yang merujuk pada kelas `UserCreate` itu sendiri.
- `as_form`: Nama fungsi buatan (bisa diganti). Fungsinya sebagai jembatan dengan FastAPI. Dengan mendaftarkan semua parameter (`full_name: str = Form(..)`), sama saja memberitahu FastAPI *"Tolong ambil data dari input HTML yang bernama `full_name`"*
- `return cls`: Setelah semua data terkumpul, Pydantic mengecek tipe datanya. Jika ada yang salah, Pydantic langsung memberikan error sebelum data diproses.

## 2. Penyesuaian `users.py`

Parameter `user_data` diambil dari `schemas.UserCreate.as_form` menggunakan `Depends`:
```
@router.post("/register")
def register_user(
    confirm_password: str = Form(...),
    user_data: schemas.UserCreate = Depends(schemas.UserCreate.as_form),
    db: Session = Depends(database.get_db)
):
```

Pertama, cek apakah password dan confirmation_password sama:
```
if user_data.password != confirm_password:
        return RedirectResponse(url="/users/register?msg=password_mismatch", status_code=303)
```

Kode pengecekan data yang seperti berikut sudah tidak dibutuhkan, dihapus saja:
```
    try:
        user_data = schemas.UserCreate(
            ...
        )
    except ValueError as e: return RedirectResponse(...)
```

Yang kedua, pengecekan dengan no KTP. Apakah KTP yang didaftarkan sudah ada dalam database? Jika sudah ada, kirim pesan `already_exist`:
```
    if db.query(models.User).filter(models.User.identity_number == user_data.identity_number).first():
        return RedirectResponse(url="/users/register?msg=already_exists", status_code=303)
```

Setelah semua pengecekan, buka `user_data` (kecuali nilai `password`) dengan `.model_dump(exclude={'password'})`. Simpan nilai ini dalam variabel `data`:
```
    data = user_data.model_dump(exclude={'password'})

    data['dkm_group'] = models.KelompokDKM(data['dkm_group'])
    data['mandatory_savings'] = models.SetoranWajib(data['mandatory_savings'])
```

Selanjutnya, simpan password yang dimasukan kedalam database dengan si enkripsi terlebih dahulu. Sekaligus membuat `member_id` secara otomatis:
- `f"UB-"`: Ini adalah awalan (prefix) tetap yang menandakan identitas "Unit Bisnis" agar ID terlihat formal.
- `user_data.identity_number[-4:]`: Bagian ini mengambil 4 digit terakhir dari Nomor KTP (NIK) yang diinput oleh pengguna.
- `random.randint(10, 99)`: Ini menambahkan bumbu acak berupa angka antara 10 sampai 99. Hal ini berguna untuk memperkecil kemungkinan adanya dua orang yang memiliki 4 digit NIK terakhir yang sama mendapatkan ID yang persis serupa.
```
    hashed_pw = utils.hash_password(user_data.password)
    gen_id = f"UB-{user_data.identity_number[-4:]}{random.randint(10, 99)}"
```

Terakhir, masukan ke dalam variabel `new_user`, lalu disimpan dalam database untuk meminta persetujuan pengurus:
```
    new_user = models.User(
        **data,
        member_id=gen_id,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    teks_sambutan = f"Selamat, {new_user.full_name} sudah berhasil mendaftar!"
    pesan_sukses = quote(teks_sambutan)

    return RedirectResponse(
        url=f"/auth/login?msg={pesan_sukses}&status=sukses", 
        status_code=303
    )
```

## 3. Pembaruan `register.html`

Tambahkan semua input (field) yang diwajibkan oleh database. Sesuaikan persis opsi `select` dengan nilai `Enum` yang ada di `models.py`:
```
{% if pesan %}  
    <div class="alert {% if status == 'sukses' %}alert-success{% else %}alert-danger{% endif %}">
        {{ pesan }}
    </div>
{% endif %}

<form action="/users/register" method="post">
    <div class="form-group">
        <label for="full_name">Nama Lengkap (Sesuai KTP)</label>
        <input type="text" id="full_name" name="full_name" required>
    </div>

    <div class="form-group">
        <label for="identity_number">Nomor KTP (NIK)</label>
        <input type="text" id="identity_number" name="identity_number" required placeholder="16 digit angka">
    </div>

    <div class="form-group">
        <label for="family_card_number">Nomor Kartu Keluarga (KK)</label>
        <input type="text" id="family_card_number" name="family_card_number" required>
    </div>

    <div class="form-group">
        <label for="birth_info">Tempat, Tanggal Lahir</label>
        <input type="text" id="birth_info" name="birth_info" required placeholder="Contoh: Bogor, 17 Agustus 1990">
    </div>

    <div class="form-group">
        <label for="gender">Jenis Kelamin</label>
        <select id="gender" name="gender" required>
            <option value="Pria">Pria</option>
            <option value="Wanita">Wanita</option>
        </select>
    </div>

    <div class="form-group">
        <label for="address">Alamat Domisili Lengkap</label>
        <textarea id="address" name="address" rows="3" required></textarea>
    </div>

    <div class="form-group">
        <label for="phone_number">Nomor Telepon / WhatsApp</label>
        <input type="text" id="phone_number" name="phone_number" required>
    </div>

    <div class="form-group">
        <label for="spouse_name">Nama Suami/Istri (Kosongkan jika belum menikah)</label>
        <input type="text" id="spouse_name" name="spouse_name">
    </div>

    <div class="form-group">
        <label for="dkm_group">Kelompok DKM</label>
        <select id="dkm_group" name="dkm_group" required>
            <option value="DKM DARUSSALAM - Gunung Gede">DKM DARUSSALAM - Gunung Gede</option>
            <option value="DKM AL BAROKAH - Pondok Rumput">DKM AL BAROKAH - Pondok Rumput</option>
            <option value="DKM DARUL HIKMAH - Green Arofah">DKM DARUL HIKMAH - Green Arofah</option>
            <option value="DKM AR-RAUDHOH - Pakuan">DKM AR-RAUDHOH - Pakuan</option>
            <option value="DKM BAITUL IZZA - Tajur">DKM BAITUL IZZA - Tajur</option>
            <option value="DKM AN-NASHR - Cikaret">DKM AN-NASHR - Cikaret</option>
            <option value="DKM AR-ROHMAN - Ciapus">DKM AR-ROHMAN - Ciapus</option>
        </select>
    </div>

    <div class="form-group">
        <label for="mandatory_savings">Pilihan Setoran Wajib / Bulan</label>
        <select id="mandatory_savings" name="mandatory_savings" required>
            <option value="25000">Rp 25.000</option>
            <option value="50000">Rp 50.000</option>
            <option value="100000">Rp 100.000</option>
            <option value="250000">Rp 250.000</option>
            <option value="500000">Rp 500.000</option>
        </select>
    </div>

    <div class="form-group">
        <label for="password">Kata Sandi</label>
        <input type="password" id="password" name="password" required placeholder="Minimal 8 karakter">
    </div>

    <div class="form-group">
        <label for="confirm_password">Konfirmasi Kata Sandi</label>
        <input type="password" id="confirm_password" name="confirm_password" required placeholder="Ulangi kata sandi">
    </div>

    <button type="submit" class="btn-login">Kirim Pendaftaran</button>
</form>
```

## 4. Perbarui `auth.py`

Karena sekarang tidak menggunakan `email, tapi bisa menggunakan `identity_number` atau `member_id`, perlu ada penyesuaian:
```
from sqlalchemy import or_

login_user(response: Response, user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        or_(
            models.User.identity_number == user_data.username,
            models.User.member_id == user_data.username
        )
    ).first()
```

# Day 11 - Akun Pengurus

## 1. Pembuatan Tabel `admins`

Tambahkan tabel `Admin` di file `models.py`:
```
class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="superadmin")
```

## 2. Logic Login

Agar ketika yang dimasukan `admin_id` dilempar ke dashboard amin, tambahkan di file `auth.py`:
```
def login_user(response: Response, user_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == user_data.username).first()
    
    if admin:
        if utils.verify_password(user_data.password, admin.hashed_password):
            token = create_access_token(data={"sub": str(admin.id), "role": "admin"})
            response = RedirectResponse(url="/admin/dashboard", status_code=303)
            response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
            return response
```

Jika bukan admin, maka dilempar ke dashboard anggota:
```
user = db.query(models.User).filter(
        or_(models.User.identity_number == user_data.username, models.User.member_id == user_data.username)
    ).first()

    if user and utils.verify_password(user_data.password, user.hashed_password):
        token = create_access_token(data={"sub": str(user.id), "role": "user"})
        response = RedirectResponse(url="/dashboard/me", status_code=303)
        response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
        return response

    return RedirectResponse(url="/auth/login?msg=invalid", status_code=303)
```

## 3. Buat Admin Pertama

Untuk alasan keamanan, tidak ada form pembuatan akun. Semua akun admin yang ingin didaftarkan harus dilakukan oleh pemegang database langsung. Untuk mempermudah, simpan skrip dengan nama `create_admin.py`. Ketika mau bikin akun admin tinggal jalankan skrip nya:
```
# Jalankan ini di terminal: python create_admin.py
from app.database import SessionLocal
from app import models, utils

def create_initial_admin():
    db = SessionLocal()
    hashed_pw = utils.hash_password("admin123") # Ganti password ini!
    admin = models.Admin(
        username="admin_ub",
        full_name="Administrator Utama",
        hashed_password=hashed_pw
    )
    db.add(admin)
    db.commit()
    print("Admin berhasil dibuat! Username: admin_ub, Pass: admin123")

if __name__ == "__main__":
    create_initial_admin()
```