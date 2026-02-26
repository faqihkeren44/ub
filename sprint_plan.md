# 🚀 Sprint Plan 30 Hari – MVP E-Commerce UMKM

Stack utama: **FastAPI** + **PostgreSQL**
Target: Live URL + end-to-end order + payment tercatat

Durasi: 2–3 jam/hari, 6 hari/minggu

---

# 🗓️ GAMBARAN 4 SPRINT

| Sprint | Fokus            | Hasil Utama               |
| ------ | ---------------- | ------------------------- |
| 1      | Fondasi Backend  | Auth + Produk CRUD        |
| 2      | Core E-commerce  | Cart → Order → Stock aman |
| 3      | Frontend Web     | Bisa dipakai UMKM         |
| 4      | Payment & Deploy | Live Production           |

---

# 🧱 SPRINT 1 — Fondasi Backend (Hari 1–7)

🎯 Target: API stabil + JWT auth jalan

## Hari 1 — Setup Project

* Buat virtualenv
* Install FastAPI, Uvicorn
* Struktur folder awal
* Endpoint `GET /health`

✅ Output: server jalan

---

## Hari 2 — Database Setup

* Install PostgreSQL
* Setup SQLAlchemy
* Config `.env`
* Migration (Alembic)

✅ Output: bisa create tabel

---

## Hari 3 — User Model

* Table `users`
* Hash password (bcrypt)
* Endpoint register

✅ Output: user bisa daftar

---

## Hari 4 — Login JWT

* Login endpoint
* JWT token
* Protected route

✅ Output: auth working

---

## Hari 5 — Product Model

* Table `products`
* CRUD produk
* Upload gambar sederhana (local dulu)

✅ Output: admin bisa tambah produk

---

## Hari 6 — Refactor & Testing

* Pisahkan routers
* Error handling
* Validasi Pydantic

---

## Hari 7 — Review Sprint 1

🎯 Harus sudah:

* Register/login aman
* Produk CRUD jalan
* DB stabil

Kalau belum stabil → STOP. Jangan lanjut.

---

# 🛒 SPRINT 2 — Core E-commerce (Hari 8–14)

🎯 Target: Checkout jalan + stok aman

---

## Hari 8 — Cart

* Table `carts`
* Table `cart_items`
* Add/update/remove item

---

## Hari 9 — Order

* Table `orders`
* Table `order_items`
* Create order endpoint

---

## Hari 10 — Stock Transaction (KRUSIAL 🔥)

* Kurangi stok saat order
* Gunakan DB transaction
* Lock row (`SELECT FOR UPDATE`)
* Handle race condition

Ini bagian paling bernilai untuk recruiter backend.

---

## Hari 11 — Order Status

Enum:

* pending
* paid
* processing
* completed
* cancelled

---

## Hari 12 — Admin Order View

* List orders
* Update status

---

## Hari 13 — Basic Reporting

* Total sales harian
* Jumlah order
* Total revenue

---

## Hari 14 — Hard Testing

🎯 Harus sudah:

* Checkout aman
* Stok tidak minus
* Order konsisten

Kalau belum solid → tahan.

---

# 🌐 SPRINT 3 — Frontend Web (Hari 15–21)

🎯 Target: Bisa dipakai UMKM

Pilihan cepat:

* HTML + Tailwind (paling realistis)
* React (kalau waktu cukup)

---

## Hari 15 — Setup Frontend

* Base layout
* Responsive

---

## Hari 16 — Product List

* List produk
* Mobile friendly

---

## Hari 17 — Cart Page

* Add/update qty
* Hitung total

---

## Hari 18 — Checkout Page

* Form alamat
* Ringkasan order

---

## Hari 19 — Admin Dashboard

* CRUD produk
* List order

---

## Hari 20 — POS Kasir 🔥

* Pilih produk
* Input qty
* Total otomatis
* Submit cepat

Ini nilai jual besar untuk UMKM offline.

---

## Hari 21 — UI Polish

🎯 Harus sudah:

* Bisa order dari HP
* Admin bisa proses
* Flow end-to-end

---

# 💳 SPRINT 4 — Payment & Deploy (Hari 22–30)

🎯 Target: Live Production

---

## Hari 22 — Payment Integration

Pilih:

* **Midtrans**
* **Xendit**
* atau transfer manual dulu

---

## Hari 23 — Webhook Handler 🔥

* Endpoint webhook
* Verify signature
* Update status → paid

Banyak pemula gagal di sini.

---

## Hari 24 — Dockerize

* Dockerfile
* docker-compose
* ENV config

---

## Hari 25 — Production DB

* PostgreSQL production
* Migration run

---

## Hari 26 — Deploy

* VPS/cloud
* Nginx
* Domain
* HTTPS (Let's Encrypt)

---

## Hari 27 — Bug Fixing Besar

---

## Hari 28 — End-to-End Testing

---

## Hari 29 — Hardening

* Input validation
* Logging
* Basic security
* CORS config

---

## Hari 30 — 🚀 GO LIVE

🎯 Definition of Done:

✅ User bisa order
✅ Payment tercatat
✅ Stok aman
✅ Admin bisa proses
✅ Live URL
✅ Mobile usable

---

# 🧠 Rule Emas (Wajib Patuhi)

* Jangan Flutter dulu
* Jangan microservices
* Jangan over-design
* Jangan perfeksionis UI
* Wajib deploy

---

# 🎯 Realistisnya Setelah 30 Hari

Kalau konsisten:

* Backend transactional logic kuat
* Paham payment gateway
* Paham deployment
* Portfolio production-ready
* Siap scaling / lanjut SaaS UMKM