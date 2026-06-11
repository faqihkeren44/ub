# 0. Struktur File

## Penjelasan

Menggunakan satu file raksasa akan menjadi mimpi buruk dalam menggunakan Vanilla CSS. Pendekatan paling umum yang digunakan adalah pola 7-1 architecture (versi sederhana). Berikut contoh struktur folder:

```
static/
└── css/
    └── base/
    │   ├── reset.css       # Reset margin/padding bawaan browser
    │   ├── typography.css  # Aturan font, ukuran heading, link
    │   └── variables.css   # Variabel warna, sapcing, shadow (:root)
    ├── componnets/
    │   ├── buttons.css     # Semua jenis tombol
    │   ├── cards.css       # Kartu produk (product grid)
    │   ├── forms.css       # Input, checkbox, login form
    │   └── navbar.css      # Desain navigasi utama
    ├── layouts/
    │   ├── footer.css
    │   ├── grid.css        # Sistem layout (Flexbox/Grid)
    │   └── section.css     # Aturan padding antar seksi
    ├── pages/
    │   ├── home.css
    │   ├── products.css
    │   └── cart.css
    └── main.css
```

## Penamaan Class (BEM)

BEM adalah singkatan dari Block, Element, Modifier. Ini merupakan metodologi penamaan class pada CSS. Berikut penjelasan detailnya:
- Block: Komponen mandiri yang bermakna secara fungsional (misalnya `nav`, `button`, `card`).
- Element: Bagian dari blok yang tidak mmeiliki arti sendiri, dan terikat pada bloknya secara semantik (misalnya `item`, `title`, `image`). Penulisannya dihubungkan dengan dua garis bawah (`__`).
- Modifier: Flag pada blok atau elemen yang digunakan untuk mengubah tampilan atau prilaku (misalnya `large`, `red`, `disable`). Penulisannya dihubungkan dengan dua garis tengah (`--`).

Contoh:
```
/* Block */
.product-card {...}

/* Element */
.product-card__title {...}
.product-card__price {...}

/* Modifier */
.product-card--featured {...}
```

# 1. `reset.css `

Tujuan utama `reset.css` adalah menghapus default styling yang diberikan browser. Jika tidak direset, tampilan akan terlihat berbeda-beda atau berantakan di setiap perangkat.

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
| `Rockwell, Arial` | Font cadangan yang sangat umum dan pasti ada di hampir semua komputer. |
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

## `text-decoration: none; color: inherit;`

Ketika membuat link (`<a>`), secara default browser memberikan warna biru terang dan garis bawah. Saat di klik, warnanya berubah menjadi ungu.

Elemen formulir seperti `button`, `input`, dan `select` umumnya tidak mengikuti jenis font atau warna teks yang diatur di `body`. Itulah alasannya menggunakan `inherit`. Fungsinya memaksa elemen tersebut menggunakan warna teks yang sama dengan lingkungannya.

# 2. `.container`

Dalam desain web, class ini adalah sebuah pembatas agar tidak berantakan dan mudah dibaca di layar yang lebar. Berikut penjelasan detailnya:
- `max-width: 1100px;`: Menjaga agar tidak melebar tanpa batas. Di monitor yang sangat besar (misal monitor 27 inci), jika teks memanjang dari ujung kiri ke ujung kanan, mata pembaca akan cepat lelah. Angka 1100px adalah standar kenyamanan untuk pandangan manusia agar tetap fokus.
- `margin: 0 auto;`: Ini adalah teknik paling populer untuk membuat kotak berada tepat di tengah layar.
    `0`: memberi jarak 0 (nol) untuk bagian atas dan bawah kotak.
    `auto`: Memerintahkan browser untuk menghitung sisa ruang kosong di kiri dan kanan layar secara otomatis, lalu membaginya sama rata.
    Hasilnya, Kotak kontainer akan selalu berada di tengah, tidak peduli seberapa lebar layar monitor.
- `padding: 0 20px;`: Saat website dibuka di ponsel (layar kecil), lebar layar mungkin hanya 360px. Tanpa padding ini, teks kamu akan menempel ke pinggir casing HP. Memberikan jarak aman sebesar 20px di sisi kiri dan kanan ini membuat website terlihat rapi dan profesional di perangkat mobile.

# 3. `buttons.css`

## `.btn`

Class untuk tombol:
- `display: inline-block;`: Secara default, tag link (`<a>`) bersifat inline (tidak bisa mengubah lebar/tinggi). Dengan mengubahnya menjadi inline-block, tombol bisa memiliki padding dan margin dan tetap bisa duduk berdampingan dengan elemen lain.
- `text-decoration: none;`: Link secara otomatis memiliki garis bawah (underline). Baris ini menghapus underline tersebut.
- `padding: 10px 20px;`: Memberikan ruang di dalam tombol (10px untuk atas-bawah, dan 20px untuk kiri-kanan).
- `border-radius: 50px;`: Membuat tampilan pill-shaped (berbentuk kapsul). Angka yang besar (50px) memastikan ujung tombol benar-benar melingkar sempurna.
- `font-weight: 600;`: Membuat teks sedikit tebal (semi-bold) agar terlihat lebih tegas dan menonjol.
- `font-size: 15px;`: Ukuran teks yang ideal—tidak terlalu besar sehingga merusak layout, tapi cukup jelas untuk dibaca.
- `transition: all 0.2s ease;`: Artinya semua perubahan (seperti warna latar atau bayangan (`all`)) akan dianimasikan. Durasinya 0,2 detik (`0.2s`), dengan gerakan animasi yang halus (mulai perlahan, cepat di tengah, melambat di akhir) (`ease`). Tanpa ini, saat ada efek hover (misalnya warna berubah saat kursor menyentuh tombol), perubahannya akan terasa kaku dan tiba-tiba.

## `btn-dark`

Class ini digunakan untuk tombol utama. Warna tombol diambil dari variabel `stripe-dark`, dan tulisannya berwarna `text-light`. Saat kursor di tombol, warnanya berubah dan naik ke atas 1 pixel (`transform: translateY(-1px);`).

## `btn-light`

Tombol dengan class ini digunakan untuk tombol sekunder. Dengan opacity 20% (`rgba(255, 255, 255, 0.2)`), tombol terlihat menyatu dengan latar belakang. Agar tidak menempel jika diletakkan tepat di sebelah tombol utama (`.btn-dark`), diberi jarak 10 pixel.

# 3. Header / Navigasi

- `position`: absolute;: Ini menarik header keluar dari aliran dokumen normal. Header tidak lagi mengambil ruang fisik di atas elemen lain, melainkan menumpuk di atasnya.
- `top: 0;`: Memastikan header menempel tepat di batas paling atas halaman.
- `width: 100%;`: Karena absolute membuat elemen menciut sesuai isinya, kita perlu menegaskan agar lebarnya memenuhi layar dari kiri ke kanan.
- `height: 80px;`: Menentukan tinggi header secara tetap agar kita punya ruang yang konsisten untuk logo dan menu.
- `display: flex;`: Mengaktifkan mode Flexbox. Semua elemen di dalam header (logo, nav) sekarang bisa diatur posisinya dengan mudah.
- `align-items: center;`: Ini adalah cara instan untuk membuat semua isi header berada tepat di tengah secara vertikal (atas-bawah). Jadi, logo dan teks menu kamu tidak akan menempel ke langit-langit header.
- `z-index: 10;`: Bayangkan ini sebagai urutan lapisan tumpukan. Semakin tinggi angkanya, semakin "depan" posisinya di mata pengguna. Karena kamu punya background gradient atau elemen miring di bawahnya, z-index memastikan navigasi kamu tidak "tenggelam" atau tertutup oleh dekorasi tersebut.

### `.nav-wrapper`

`.nav-wrapper` digunakan senagai dirigen tata letak utama di header. Di dalamnya ada:
- `justify-content: space-between;`: Elemen pertama (logo) akan dipaksa ke ujung kiri, dan elemen terakhir (menu navigasi) dipaksa ke ujung kanan. 
- `align-items: center;`: Menjaga agar logo dan teks menu tetap sejajar di tengah secara vertikal.
- `width: 100%;`: Memastikan `.nav-wrapper` mengambil seluruh lebar yang tersedia. Ini krusial agar `space-between` punya ruang yang cukup untuk mendorong logo dan menu ke ujung-ujung layar.

# `main.css`

