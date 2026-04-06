# Table of Contents

- [Review](#review)

# Review

Sebelum lanjut ke tahap berikutnya, ada baiknya membaca ulang secara garis besar apa yang sudah dibuat sebelumnya, dan bagaimana gambaran besarnya.

## 1. Struktur Folder

- `config.py`: Tempat penyimpanan semua pengaturan yang bersifat rahasia.
- `database.py`: Jembatan yang menghubungkan kode Python ke Database (PostgreSQL).
- `models.py`: Blueprint tabel database (misal, tabel `users` harus punya kolom email, dan password).
- `schemas.py`: Satpam yang memastikan data yang masuk dari user formatnya benar (misal, email harus ada @ nya).
- `utils.py`: Alat untuk mengacak (hash) password agar aman.
- `main.py`: Resepsionis atau kepala utama, dimana semua file dikumpulkan untuk melayani user.

## 2. Register Flow

Ketika user menekan tombol daftar, berikut hal yang terjadi di balik layar:
1. User mengirim nama, email, dan password ke endpoint `/register`.
2. Di dalam file `schemas.py`, pydantic mengecek inputan user, *Apakah passwordnya string?*, *Apakah format emailnya valid?*.
3. Cek duplikasi data yang dikirim user dengan yang ada di database *Email ini sudah ada belum?*. Jika ada, kirim pesan error.
4. Mengubah password asli menjadi kode acak di file `utils.py`. Mengembalikan nilainya ke dalam file `main.py`, lalu disimpan dalam variabel `hashed_password`.
5. Membuat objek baru untuk disimpan di dalam database dengan nama `new_user`.
6. Menyimpan objek `new_user` ke dalam database

Atau seperi inilah jika dianalogikan:<br>
- Ketika ada user yang datang ingin mendaftar (masuk endpoint `/register`), terjadilah prosedur `register_user`.
- Saat itu juga datanglah `schemas` membawa selembar formulir pendaftaran (`UserCreate`) untuk diisi oleh user. Di dalam lembaran itu sudah ada ketentuan apa saja yang harus diisi, yaitu `email`, `password`, dan `full_name`. Dalam pengisian form tersebut, ada aturan yang wajib dipenuhi user agar formulir nya tidak ditolak.
- Jika user selesai mengisi form, `schemas` otomatis mengecek form tersebut menggunakan `pydantic`. Kalau formulir sesuai aturan, pintu `Session` terbuka, lalu menyerahkan lembaran formulir itu ke manajer (`main`). Tapi, kalau isi formulir itu ada yang tidak sesuai aturan tadi, otomatis lembaran form itu langsung ditolak di tempat.
- `main` menyuruh divisi `models` untuk melihat excel `database`, dan mengecek apakah `email` di form tadi ada yang sama dengan yang di database atau nggak. Kalau ada, kasih pesan error. Kalo nggak, divisi `utils` ngubah `password` jadi sandi baru yang gak gampang dimengerti biar lebih aman.
- Balik lagi ke divisi `models`. Setelah dapet password baru dari `utils`, `models` bikin baris baru di excel `database`, terus ngetik ulang form ke database (dibuat `new_user`).
- Kalau mau, di sini bisa dilakukan pengecekan lagi sebelum disimpan di `database`. Kalau yakin, baru manajer memerintahkan `add`, `commit` untuk menyimpan di `database`. 
- Kalo nanti `schemas` minta jawaban form tadi, bagian `models` bisa ngasih sesuai yang diminta `schemas` (misal minta gak pake `password`). `schemas` bisa datang lagi ke user buat ngasih tau kalo pendaftarannya udah selesai, dan dapet nomor id sekian.