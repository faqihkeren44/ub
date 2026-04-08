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

Atau seperi inilah jika dianalogikan:
- Ketika ada user yang datang ingin mendaftar (masuk endpoint `/register`), terjadilah prosedur `register_user`.
- Saat itu juga datanglah `schemas` membawa selembar formulir pendaftaran (`UserCreate`) untuk diisi oleh user. Di dalam lembaran itu sudah ada ketentuan apa saja yang harus diisi, yaitu `email`, `password`, dan `full_name`. Dalam pengisian form tersebut, ada aturan yang wajib dipenuhi user agar formulir nya tidak ditolak.
- Jika user selesai mengisi form, `schemas` otomatis mengecek form tersebut menggunakan `pydantic`. Kalau formulir sesuai aturan, pintu `Session` terbuka, lalu menyerahkan lembaran formulir itu ke manajer (`main`). Tapi, kalau isi formulir itu ada yang tidak sesuai aturan tadi, otomatis lembaran form itu langsung ditolak di tempat.
- `main` menyuruh divisi `models` untuk melihat excel `database`, dan mengecek apakah `email` di form tadi ada yang sama dengan yang di database atau nggak. Kalau ada, kasih pesan error. Kalo nggak, divisi `utils` ngubah `password` jadi sandi baru yang gak gampang dimengerti biar lebih aman.
- Balik lagi ke divisi `models`. Setelah dapet password baru dari `utils`, `models` bikin baris baru di excel `database`, terus ngetik ulang form ke database (dibuat `new_user`).
- Kalau mau, di sini bisa dilakukan pengecekan lagi sebelum disimpan di `database`. Kalau yakin, baru manajer memerintahkan `add`, `commit` untuk menyimpan di `database`. 
- Kalo nanti `schemas` minta jawaban form tadi, bagian `models` bisa ngasih sesuai yang diminta `schemas` (misal minta gak pake `password`). `schemas` bisa datang lagi ke user buat ngasih tau kalo pendaftarannya udah selesai, dan dapet nomor id sekian.

# Day 5 - 

## 1. Model Database Produk

Kita membutuhkan tabel untuk menyimpan detail setiap produk. Oleh karena itu, kita harus mendefinisikannya di `app/models.py`:
```
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
```

## 2. Skema Pydantic

Selanjutnya, definisikan bagaimana data produk dikirim dan diterima melalui API di file `app/schemas.py`:
```
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
```

### Bedah Kode:
- `from decimal import Decimal`: Karena di `models.py` menggunakan `Numeric`, di sini menggunakan `Decimal`. Ini jauh lebih aman untuk perhitungan uang daripada `float`.
- `ProductBase`: Fondasi yang berisi semua informasi umum produk
- `ProductCreate`: 
- `pass`: Turunan dari `ProductBase`. Jadi mengikuti semua field dari `ProductBase` tanpa tambahan apapun.
- `ProductOut`: Digunakan untuk mengirim data dari server ke aplikasi user.

## 3. Endpoint `/products`

Untuk menampilkan produk, tambahkan fungsionalitas:
```
@app.get("/products", response_model=list[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products
```

Untuk menambah produk, tambahkan:
```
@app.post("/products", response_model=schemas.ProductOut)
def input_product(product_data:schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
```

### Bedah Kode `**product.dict()`

Pada `product_data.dict()`, data dalam schema Pydantic diubah menjadi dictionary: `{"name": "Laptop", "price": 5000, ...}.

Simbol `**` disebut Dictionary Unpacking, fungsinya untuk membongkar isi dictionary tersebut menjadi argumen untuk model SQLAlchemy: `name="Laptop", price=500, ...`.

Ini jauh lebih ringkas daripada menulis satu-satu: 
```
new_product = models.Product(
    name=product_data.name, 
    price=product_data.price, 
    ...
)
```