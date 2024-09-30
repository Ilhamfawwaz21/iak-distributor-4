# Dokumentasi API Distributor Kelompok 4

## Daftar Isi

- [Ringkasan](#ringkasan)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Konfigurasi](#konfigurasi)
  - [Firebase](#konfigurasi-firebase)
  - [Swagger](#konfigurasi-swagger)
- [Endpoint API](#endpoint-api)
  - [Login](#1-login-post)
  - [Proses Pembelian](#2-process-purchase-post)
  - [Update Resi](#3-update-resi-post)
  - [Cek Status](#4-cek-status-get)
  - [Manajemen Data Pesanan](#5-data-pesanan-get)
  - [Tambah Data Pesanan](#6-tambah-pesanan-post)
  - [Update Resi](#7-update-resi-post)
  - [Hapus Pesanan](#8-hapus-pesanan-post)
- [Dokumentasi Swagger](#dokumentasi-swagger)

## Ringkasan

API Distributor adalah layanan yang dirancang untuk mengelola pesanan pembelian dan pengiriman barang untuk perusahaan distributor. API ini mencakup berbagai operasi seperti login, memproses pembelian, menghasilkan dan memperbarui nomor resi pengiriman, serta mengambil status pesanan. Sistem ini terintegrasi dengan Firebase untuk operasi basis data secara real-time dan Swagger untuk dokumentasi API.

## Instalasi

1. **Instalasi dependensi:**

   ```bash
   pip install -r requirements.txt

3. **Jalankan aplikasi Flask:**

   ```bash
   python app.py

## Penggunaan

1. Jalankan server lokal dengan `python app.py`

2. Akses halaman Swagger di `/api/docs` untuk dokumentasi dan mencoba endpoint API. 

## Konfigurasi

### Konfigurasi Firebase

Aplikasi ini menggunakan Firebase untuk menyimpan data pesanan dan pembelian. Kredensial Firebase harus disimpan dalam file `data/iak-distributor-4-78b8c3de8089.json`

## Konfigurasi Swagger

Swagger UI tersedia di endpoint `/api/docs`. Untuk mengakses dokumentasi API yang lebih interaktif, buka URL: [http://localhost:5000/api/docs](http://localhost:5000/api/docs).

## Endpoint API

| HTTP Method | Endpoint             | Deskripsi                                                                            |
|-------------|----------------------|--------------------------------------------------------------------------------------|
| GET         | `/`                  | Menampilkan halaman login.                                                           |
| POST        | `/loginbro`          | Proses login pengguna berdasarkan username dan password.                             |
| GET         | `/landing_page`      | Menampilkan halaman landing page.                                                    |
| POST        | `/process_purchases` | Memproses data pembelian jasa distributor dan menyimpan hasilnya ke Firebase.        |
| POST        | `/update_resi`       | Mengupdate resi berdasarkan `id_log`.                                                |
| GET         | `/status`            | Mendapatkan status pesanan berdasarkan nomor resi.                                   |
| GET         | `/orders`            | Mengambil semua data pesanan dari database.                                          |
| POST        | `/add_orders`        | Menambahkan pesanan baru ke dalam database.                                          |
| POST        | `/update/<resi>`     | Mengupdate data pesanan berdasarkan nomor resi.                                      |
| POST        | `/delete/<resi>`     | Menghapus data pesanan berdasarkan nomor resi.                                       |

## Detail Endpoint

### 1. Login (POST)

- **Deskripsi**: Endpoint untuk login pengguna menggunakan username dan password.
- **Endpoint**: `\loginbro`
- **Input**:
  - `username`: (string) Username pengguna.
  - `password`: (string) Password pengguna.
- **Respon**:
  - Sukses: Menampilkan halaman home jika login berhasil.
  - Gagal: Menampilkan pesan kesalahan jika login gagal.

### 2. Process purchase (POST)

- **Deskripsi**: Endpoint untuk memproses data pembelian dan menghitung rute pengiriman.
- **Endpoint**: `/process_purchases`
- **Input**:
  - Data JSON dengan detail pembelian.
- **Respon**:
  - Sukses: Mengembalikan hasil pemrosesan pembelian.
  - Gagal: Mengembalikan pesan kesalahan jika format JSON tidak valid.

### 3. Update Resi (POST)

- **Deskripsi**: Endpoint untuk memperbarui resi berdasarkan `id_log`.
- **Endpoint**: `/update_resi`
- **Input**:
  - `id_log`: (string) ID log pesanan.
- **Respon**:
  - Sukses: Mengembalikan hasil update resi.
  - Gagal: Mengembalikan pesan kesalahan jika `id_log` tidak ditemukan.

### 4. Cek Status (GET)

- **Deskripsi**: Endpoint untuk mendapatkan status pesanan berdasarkan nomor resi.
- **Endpoint**: `/status`
- **Input**:
  - `no_resi`: (string) Nomor resi pesanan.
- **Respon**:
  - Sukses: Mengembalikan status pesanan.
  - Gagal: Mengembalikan pesan kesalahan jika nomor resi tidak ditemukan.

### 5. Data Pesanan (GET)

- **Deskripsi**: Endpoint untuk mendapatkan semua data pesanan dari database.
- **Endpoint**: `/orders`
- **Respon**:
  - Sukses: Mengembalikan daftar pesanan yang ada di database.
  - Gagal: Mengembalikan pesan kesalahan jika data pesanan tidak ditemukan.

### 6. Tambah Pesanan (POST)

- **Deskripsi**: Endpoint untuk menambahkan pesanan baru ke dalam database.
- **Endpoint**: `/add_orders`
- **Input**:
  - `id_log`: (string) ID log pesanan.
  - `id_pembelian`: (string) ID pembelian.
  - `status`: (string) Status pesanan.
  - `kota_asal`: (string) Kota asal pesanan.
  - `kota_tujuan`: (string) Kota tujuan pesanan.
- **Respon**:
  - Sukses: Mengembalikan pesan sukses setelah pesanan ditambahkan.
  - Gagal: Mengembalikan pesan kesalahan jika terjadi masalah saat menambahkan pesanan.

### 7. Update Resi (POST)

- **Deskripsi**: Endpoint untuk memperbarui pesanan berdasarkan nomor resi.
- **Endpoint**: `/update/<resi>`
- **Input**:
  - `id_log`: (string) ID log pesanan.
  - `id_pembelian`: (string) ID pembelian.
  - `resi`: (string) Nomor resi pesanan.
  - `status`: (string) Status pesanan.
  - `kota_asal`: (string) Kota asal pesanan.
  - `kota_tujuan`: (string) Kota tujuan pesanan.
- **Respon**:
  - Sukses: Mengembalikan pesan sukses setelah pesanan diperbarui.
  - Gagal: Mengembalikan pesan kesalahan jika terjadi masalah saat memperbarui pesanan.

### 8. Hapus Pesanan (POST)

- **Deskripsi**: Endpoint untuk menghapus pesanan berdasarkan nomor resi.
- **Endpoint**: `/delete/<resi>`
- **Input**:
  - `resi`: (string) Nomor resi pesanan.
- **Respon**:
  - Sukses: Mengembalikan pesan sukses setelah pesanan dihapus.
  - Gagal: Mengembalikan pesan kesalahan jika pesanan tidak ditemukan atau terjadi masalah saat menghapus pesanan.
