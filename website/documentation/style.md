# 1. CSS Reset & Dasar

## `:root {...}`

Sederhananya, `:root` tempat menyimpan variabel yang bisa diakses oleh seluruh bagian kode CSS (terbatas hanya untuk file css). Ini sangat berguna ketika ingin mengubah warna tema seluruh website. Cukup mengubahnya di sini, dan semua elemen yang menggunakan variabel tersebut otomatis ikut berubah.

Cara menggunakannya, semua nama variabel diawali dengan dua tanda minus (`--`). Contoh:

- `--stripe-purple: #635bff;`: Membuat variabel bernama `stripe-purple` dan memberi nilai warna ungu.
- `--font-main: ...;`: Menyimpan jenis huruf (font family) agar konsisten di semua halaman.

Jika ingin menerapkan warna `--stripe-purple` tersebut, gunakan fungsi `var()` untuk memanggil nama variabel dalam `:root`. Contoh: `background-color: var(--stripe-purple);`.

## `--font-main: ...`

Kode ini disebut sebagai Font Stack. Fungsinya adalah memberikan daftar cadangan (fallback) jenis huruf kepada browser. Jika huruf pertama tidak tersedia di komputer pengunjung, browser akan mencoba huruf kedua, dan seterusnya.

Hal ini bepengaruh pada kecepatan (performance). Website langsung menggunakan font yang sudah ada di perangkat user tanpa perlu mendownlod font dari internet.

Website juga terasa seperti aplikasi bawaan HP atau komputer, karena jenis hurufnya sama dengan bawaan sistem mereka.

Berikut rincian daftar font nya:

| Nama Font | Penjelasan |
| :--- | :--- |
| `-apple-system` | Menggunakan font standar sistem di perangkat Apple (macOS/iOS). |
| `BlinkMacSystemFont` | Versi khusus untuk browser Chrome di perangkat Mac lama. |
| `"Segoe UI"` | Font standar yang sangat bersih milik Windows 10/11. |
| `Roboto` | Font standar untuk perangkat Android. |
| `Helvetica, Arial` | Font cadangan yang sangat umum dan pasti ada di hampir semua komputer. |
| `sans-serif` | Instruksi terakhir: "Gunakan font apa saja yang tidak punya 'ekor' (serif)." |

## `* {margin: 0; padding: 0;}`

Setiap browser (seperti Chrome, Safari, atau Firefox) memiliki selera masing-masing dalam memberikan jarak bawaan pada elemen HTML. Jika tidak menghapus jarak bawaan ini, tampilan website bisa terlihat berbeda-beda di setiap browser, atau muncul ruang kosong aneh di pinggir layar yang sulit dihilangkan.

Dengan menuliskan * { margin: 0; padding: 0; }, sama seperti melakukan CSS Reset dengan berkata kepada semua browser: *"Hapus semua jarak bawaan, biarkan saya yang menentukan jaraknya sendiri secara manual."*

## `box-sizing: border-box`

Ada dua jenis cara browser menghitung lebar (`width`) dan tinggi (`height`) sebuah elemen:

1. `content-box` (Default):
    Jika mengatur lebar kotak 200px, lalu menambah padding 20px dan border 5px, maka lebar total kotak di layar akan menjadi 250px ($200 + 20 + 20 + 5 + 5$). Ini sering membuat tata letak berantakan karena kotak jadi lebih besar dari yang kita kira.
2. `border-box`:
    Jika mengatur lebar kotak 200px, maka 200px itulah hasil akhirnya. Jika menambah padding atau border, browser akan "menciutkan" ruang konten di dalamnya agar total lebarnya tetap 200px.

## `overflow-x: hidden`

Dalam desain modern, seringkali ada elemen yang ukurannya melebihi lebar layar. Daripada memunculkan scroll bar di bagian bawah, `hidden` memerintahkan browser untuk menyembunyikan bagian elemen yang keluar dari batas lebar layar.

Bayangkan jika ada sebuah gambar yang lebarnya 1500px, padahal layar HP pengunjung hanya 400px. Akan muncul batang geser (scroll bar) di bagian bawah layar yang biasanya merusak estetika desain profesional, dan pengunjung bisa menggeser halaman ke arah kanan secara tidak sengaja. Pengunjung akan melihat ruang kosong putih di sebelah kanan konten utama, karena browser mencoba mengakomodasi gambar 1500px tersebut meskipun layarnya sempit.

# 2. Komponen Umum

# 3. Header / Navigasi

## `position: absolute;`

