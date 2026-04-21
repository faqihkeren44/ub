```
/UB
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └──style.css
│   └── js/
│       └── script.js
├── ...
└── README.md
```

# `index.html`

## 1. Struktur `index.html`

```
<!DOCTYPE html>
<html lang = "id">
<html>
    <head>
        <meta ...>
        <link rel="stylesheet" ...>
    </head>

    <body>
        <header>
            ...
        </header>

        <main>
            <section> ... </section>
        </main>

        <footer>
            ...
        </footer>
    </body>

    <script src="..."></script>
</html>
```

## 2. `<meta>`

### `<meta charset="UTF-8">`

Fungsinya untuk memberitahu browser untuk menggunakan standar karakter internasional. Tanpa ini, simbol seperti mata uang (Rp, $), emoji, atau karakter khusus lainnya mungkin akan muncul sebagai kotak-kotak aneh atau tanda tanya.

### `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

Fungsi untuk Mengatur skala website agar sesuai dengan lebar layar perangkat (HP/Tablet). Inilah yang membuat website kita menjadi "Mobile-Friendly". Tanpa tag ini, website kamu di HP akan terlihat sangat kecil (seperti tampilan desktop yang dipaksa masuk ke layar kecil).

### `<meta name="description" content="UB Mandiri Sejahtera ...">`

Tag ini tidak wajib agar web berjalan, tapi wajib jika kamu ingin website UB Mandiri Sejahtera terlihat profesional di hasil pencarian. Fungsinya untuk Menampilkan cuplikan teks di bawah judul website saat muncul di Google.

### `<meta property="og:title" content="UB Mandiri Sejahtera">`

Pernahkah kamu membagikan link di WhatsApp atau Facebook dan muncul gambar beserta judulnya? Itu karena tag ini:

- `<meta property="og:title" content="UB Mandiri Sejahtera">`
- `<meta property="og:image" content="assets/img/preview-koperasi.jpg">`

## 3. `<header>`

`<header>` adalah elemen yang digunakan untuk membungkus konten pembuka atau sekumpulan link navigasi dalam website.

