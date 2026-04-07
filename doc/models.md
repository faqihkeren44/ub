## Apa itu SQLAlchemy model?

SQLAlchemy bertindak sebagai ORM (Object-Relational Mapper), yang artinya berinteraksi dengan database (SQL) menggunakan sintaks Python (Objek) tanpa perlu menulis query SQL mentah secara manual.

Hal pertama yang harus ditulis adalah `class Product(Base)`

# Mendefinisikan Nama Tabel

Sebelum masuk ke kolom, perlu memberitahu dulu nama tabelnya, dengan kode:
```
__tablename__ = "products"
```

Dalam Python, penggunaan garis di awal dan di akhir nama variabel (seperti __tablename__) sering disebut sebagai Dunder (singkatan dari double underscore). Ini memberi tahu Python bahwa variabel ini memiliki peran khusus yang sudah ditentukan oleh sistem atau library (dalam hal ini SQLAlchemy).

Seperti yang kita bahas sebelumnya, karena `Product` adalah turunan dari `Base`, SQLAlchemy akan memindai isi class tersebut. Saat sistem melihat `__tablename__`, ia akan berhenti dan berkata:

*"Oke, saya tidak akan menjadikan ini sebagai kolom di database. Saya akan menggunakan nilai string di dalamnya sebagai nama tabel fisik di SQL nanti."*

Contoh perbandingan:
```
class Product(Base):
    # Ini KONFIGURASI (karena pakai __)
    __tablename__ = "tb_produk_toko" 

    # Ini KOLOM DATABASE (karena tidak pakai __)
    name = Column(String) 
    price = Column(Integer)
```

# Mendefinisikan Kolom

Format umumnya adalah:
```
nama_kolom = Column(TipeData, argumen_tambahan)
```

## Tipe Data

### 1. Tipe Data Teks

- `String(length)`: Teks pendek dengan batasan jumlah karakter (`length`).
- `Text`: Teks yang sangat panjang tanpa batasan jumlah karakter yang kaku, seperti deskripsi.

### 2. Tipe Data Angka

- `Integer`: Angka bulat tanpa desimal.
- `Float`: Angka desimal (misal 4.5).
- `Numeric`/`Decimal`: Angka desimal dengan presisi tetap seperti apa yang ditulis (tidak ada pembulatan otomatis). Misalkan harga 15000.00.

### 3. Tipe Data Logika dan Waktu

- `Boolean`: Hanya berisi `True` dan `False`.
- `DateTime`: Menyimpan tanggal dan waktu sekaligus.
- `Date`: Hanya menyimpan tanggal (tanpa ada waktu).

## Argumen Tambahan

### 1. `primary_key=True`

Fungsinya sebagai identitas unik setiap baris. Karena database butuh cara untuk membedakan setiap produk, meskipun namanya sama. Biasanya digunakan pada kolom `id`.

### 2. `index=True`

Membuat index di database untuk kolom tersebut. Seperti katalog buku di perpustakaan. Tanpa katalog/indeks, petugas harus mengecek buku satu per satu dari rak pertama sampai rak terakhir. Proses ini tentu akan memakan waktu sangat lama. Di dalam database, `index=True` berfungsi membuat katalog itu.

Secara teknis, ketika menandai sebuah kolom dengan `index=True`, database membuat struktur data tambahan (biasa disebut B-Tree) yang menyimpan nilai kolom tersebut beserta lokasinya di tabel utama.

Memang dengan penggunaan `index=True` akan membuat kecepatan membaca (`SELECT`), karena pencarian dilakukan dengan metode belah dua atau pencarian cepat lainnya. 

Akan tetapi, karena harus membuat struktur data, maka membuthukan ruang penyimpanan tambahan. Oleh karena itu, gunakan hanya pada kolom yang:
- Sering muncul di bagian `WHERE` dalam query (misal, mencari user berdasarkan `username`).
- Digunakan untuk mengurutkan data
- Digunakan untuk menghubungkan dua tabel (foreign key)

### 3. `nullable=False`

Menentukan apakah kolom ini boleh dikosongkan (`NULL`) atau tidak. Karena secara default, kolom boleh dikosongkan (`nullable=True`). Namun, beberapa kasus seperti di e-commerce tidak boleh mengosongkan nama dan harga produk agar tidak terjadi error.

### 4. `unique=True`

Memastikan tidak ada dua baris yang memiliki nilai yang sama di kolom tersebut. Ini sangat penting untuk `email` agar tidak ada duplikasi yang membingungkan sistem. Jika ada user yang mencoba mendaftar dengan `email` yang sudah ada, maka:
- Database menolak perintah `INSERT` karena melanggar aturan (Unique Constraint Violation).
- SQLAlchemy akan menangkap penolakan tersebut, lalu melempar sebuah exception (biasanya `IntegrityError`).
- Jika tidak ada kode yang menangani error ini, aplikasi bisa mengalami crash atau menampilkan halaman "Internal Server Error" (500) kepada user.

### 5. `default=...`

Untuk memberikan nilai otomatis jika tidak diisi. Contoh, `stock = Column(Integer, default=0)`. Jika menambah produk baru tanpa mengisi berapa stoknya, otomatis database mengisinya dengan angka 0.

### 6. `server_default=...`

Mirip dengan `default`, nilai diatur langsung oleh sisi database (bukan oleh kode Python). Sering digunakan untuk timestamp seperti `create_at`.
