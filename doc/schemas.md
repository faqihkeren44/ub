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