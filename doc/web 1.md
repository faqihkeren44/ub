## 1. Mempersiapkan Fondasi (HTML)

Setiap file HTML membutuhkan elemen dasar agar browser tahu bahwa ini adalah sebuah dokumen web. Struktur ini terdiri dari:
- `<!DOCTYPE html>`: Memberitahu browser bahwa ini adalah dokumen HTML5.
- `<html>`: Wadah utama untuk seluruh konten web.
- `<head>`: Tempat menyimpan informasi "di balik layar" seperti judul tab (`<title>`) dan link ke file CSS.
- `<body>`: Tempat semua konten yang terlihat oleh pengunjung (teks, gambar, tombol).

## 2. Menu Navigasi

Dalam HTML, kita biasanya menggunakan elemen <nav> untuk membungkus daftar link navigasi. Kita akan menggunakan kombinasi tag <ul> (daftar tidak berurutan) dan <li> (item daftar) agar strukturnya rapi.

tambahkan kode berikut di dalam bagian <body>:
```
<nav>
    <ul>
        <li><a href="#">Beranda</a></li>
        <li><a href="#">Tentang Saya</a></li>
        <li><a href="#">Kontak</a></li>
    </ul>
</nav>
```

