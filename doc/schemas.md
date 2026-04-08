# Mengapa Butuh Schemas?

## 1. Validasi

Sebelum data dikirim (dari user atau ke user), data dicek apakah tipenya sudah benar.

## 2. Serialisasi

Sama seperti bahasa pemrograman yang memiliki syntax tersendiri, atau gambar yang memiliki berbagai format (JPG, PNG, IMG, IMEG, dll), data juga memiliki bentuknya masing-masing. Oleh karena itu, dibutuhkan serialisasi yang mengubah bentuk suatu data menjadi bentuk lain agar bisa dimengerti oleh bahasa pemrograman. 
Berikut perbedaan nyata bentuknya

### Format Database (SQL)

Database seperti PostgreSQL atau MySQL menyimpan data dalam blok-blok besar. Di dalam blok itu, data disusun berurutan. Di dalam tabel mentah database, tulisannya akan terlihat seperti baris panjang berisi:
- Header baris: Informasi tersembunyi (metadata) kapan data dibuat/urutan ke berapa dan apakah data sudah dihapus.
- Isi data: Nilai aslinya
- Padding: Ruang kosong untuk memastikan data berikutnya dimulai dari titik yang tepat.

Fun Fact: Seperti penjelasan di atas, di banyak database modern, saat perintah `DELETE` dijalankan, data tidak langsung hilang. Database hanya memberikan tanda (sering disebut Delete Bit atau Xmax) yang menyatakan *Baris ini sudah tidak berlaku lagi*, dan data ini menjadi data sampah/dead tuples.
Menghapus data dari tengah-tengah file itu sangat berat secara proses (seperti menghapus satu kata di tengah buku setebal 1000 halaman dan menggeser semua huruf sisanya). Jauh lebih cepat bagi database untuk cuma memberi coretan "Sudah Dihapus" di atasnya.

Dalam wujud biner, setiap karakter ditulis sebagai bit (hanya 0 dan 1). Jika tipenya `Integer`, di memori akan terlihat dalam sistem 8-bit sederhana. Jika `String`, maka komputer menggunakan standar seperti UTF-8

Contoh, jika kita memasukan data angka "1", maka bentuknya seperti ini:
| Tampilan (Manusia) | Tabel Mentah (Struktur DB) | Biner (Memori/Disk)|
| :---: | :---: | :---: |
| 1 (Angka) | [Header][Value: 1][Offset] | 00000001 |
| A (Teks) | [Header][Length: 1][Value: 65] | 01000001 |

Untuk melihatnya agar berbentuk tabel, dibutuhkan bahasa SQL.

### Format Objek Python (SQLAlchemy)

Setelah menarik data dari database dengan SQLAlchemy, Python membungkusnya menjadi Instance/Object. Misal:
- `produk = db.query(Product).first()`: Mengubah tabel mentah menjadi object python bernama `produk`.
- `print(produk)`: Menampilkan object python. Tapi hasilnya bukan teks, tapi identitas objek `produk` di RAM, yaitu `<app.models.Product object at 0x7f8...>`.
- `print(produk.name)`: Mengakses isi salah satu yang ada di dalam objek `produk` dengan titik (.), sehingga hasilnya berupa string.

Masalahnya, tidak mungkin mengirim objek python ini langsung ke HP user(Android/iOS). Mereka tidak mengerti objek python.

### Format JSON (JavaScript Object Notation)

Inilah bahasa universal internet. Semua perangkat (Mobile, PC, Smart TV, dll) mengerti JSON. Bentuknya adalah teks/string tang terstruktur:
```
{
  "id": 1,
  "name": "Laptop",
  "price": 5000.0
}
```

Secara visual, JSON mirip dengan Python Dictionary. Keduanya menggunakan kurung kurawal `{}`, memiliki key (kunci) dan value (nilai). Namun, ada perbedaan mendasar dalam status mereka di program:
- Dictionary: Struktur data internal Python yang hidup di RAM saat program berjalan. Bisa langsung menambah data, menghapus, atau diterapkan fungsi.
- JSON: Teks string biasa yang mengikuti aturan penulisan tertentu. Karena bentuknya teks biasa, JSON bisa dibaca oleh bahasa pemrograman apa pun.

Selain itu, ada beberapa aturan penulisan yang berbeda:
| Fitur | Python Dictionary | JSON (Teks) |
| :---: | :---: | :---: |
| Tanda Kutip | Boleh tunggal (`'`) atau ganda (`"`) | Wajib tanda kutip ganda (`"`) |
| Nilain Boolean | Ditulis `True` atau `False` (Huruf besar) | Ditulis `true` atau `false` (Huruf kecil) |
| Nilai Kosong | Ditulis `None` | Ditulis `null` |
| Trailing Comma | Boleh ada koma di item terakhir | Tidak boleh ada koma di item terakhir |

### Kenapa Ini Penting?

Di backend e-commerce, prosesnya akan seperti inii:
1. Database: Menyimpan data (Format Tabel).
2. SQLAlchemy: Begitu menjalankan `db.query()`, SQLAlchemy menarik data ke Python (Format Object).
3. Pydantic: FastAPI menggunakan Schema (Pydantic) untuk membedah objek tersebut. Pydantic mengambil atribut-atributnya dan mengubahnya menjadi Python Dictionary.
4. FastAPI (JSON String): Mengambil dictionary tersebut dan melakukan JSON Encoding (mengubah `{}` menjadi teks `"{"..."}"`) untuk dikirim melalui internet.
4. Aplikasi Mobile/PC: Menerima string JSON, lalu mengubahnya kembali menjadi objek di bahasa mereka masing-masing (misal menjadi Map di Flutter atau Object di JavaScript).

# Format Penulisan

### `BaseModel`

Dalam Pydantic, kita menggunakan class yang mewarisi (turunan) dari `BaseModel`. Ini adalah syarat mutlak agar class yang dibuat bisa melakukan validasi otomatis dan mengubahnya menjadi dictionary.
Untuk menggunakannya, perlu menginstall library Pydantic dengan:
```
pip install pydantic
```
Selanjutnya, di dalam file `schemas.py`, panggil dengan perintah:
```
from pydantic import BaseModel
```

## Simbol

### 1. Titik Dua (`:`) - Type Hinting

Digunakan untuk menentukan Tipe Data. Ini memberi tahu Python dan Pydantic *"Variabel ini harus berupa tipe ini"*. Contoh:
- `id: int`: Artinya `id` harus berupa angka bulat.
- `name: str`: Artinya `name` harus berupa teks.

### 2. Sama Dengan (`=`) - Default Value

Digunakan untuk memberikan Nilai Awal (Default). Jika user tidak mengirimkan data, maka nilai inilah yang akan digunakan. Contoh:
- `is_active: bool = True`: Jika tidak diisi, otomatis dianggap True.
- `price: float = 0.0`: Jika tidak diisi, otomatis dianggap 0.0.

### 3. Kurung Siku (`[]`) - Generic Types

Memberikan detail tambahan pada sebuah tipe data. Contoh:
- `full_name: Optional[str]`: Artinya `full_name` berupa sting. Tapi, kalau user mengirim `null` atau `None`, itu boleh-boleh saja. Tanpa `Optional`, jika kamu hanya menulis `full_name: str = None`, beberapa alat pengecek kode (linter) mungkin akan protes: 
*"Lho, katanya tipe datanya string (`str`), kok kamu kasih nilai default `None`? `None` kan bukan string!"*
- `tags: list[str]`: Artinya field `tags` berisi kumpulan teks (contoh: `["elektornik", "laptop"]`.

# Parameter

- `Field(..., ...)`: Titik tiga (Ellipsis) berarti wajib diisi. Bisa ditambah argumen `default=...`.
- `min_length=3`/`max_length=255`: Minimal memiliki 3 karakter, maksimal 255 karakter.
- `Decimal`: 
- `gt=0`: Singkatan dari Greater Than. Harga wajib di atas 0. Tidak boleh gratis atau minus.
- `ge=0`: Singkatan dari Greater or Equal. Stok boleh 0, tapi tidak boleh -1.

# Akhir

```
class Config:
    from_attributes = True
```

Baris itulah yang memberikan instruksi kepada Pydantic:
*"Ambil Object dari SQLAlchemy, lalu preteli isinya menjadi Dictionary supaya bisa kita jadikan JSON."*