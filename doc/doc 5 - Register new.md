# Table Of Contents

- [Review](#review)
- [Day 9 - Update Database](#day-9---update-database)

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
    PENDING = 1    # 001
    APPROVED = 2   # 010
    REJECTED = 4   # 100
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