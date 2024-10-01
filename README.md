# Dokumentasi API Distributor Kelompok 4

## Daftar Isi

- [Ringkasan](#ringkasan)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
  - [Firebase](#konfigurasi-firebase)
- [Endpoint API Public](#endpoint-api-public)
  - [Cek Status](#1-cek-status)
  - [Cek Harga](#2-cek-harga)

## Ringkasan

API Distributor adalah layanan yang dirancang untuk mengelola pesanan pembelian dan pengiriman barang untuk perusahaan distributor. API ini mencakup berbagai operasi seperti login, memproses pembelian, menghasilkan dan memperbarui nomor resi pengiriman, serta mengambil status pesanan. Sistem ini terintegrasi dengan Firebase untuk operasi basis data secara real-time dan Swagger untuk dokumentasi API.

## Instalasi

1. **Instalasi dependensi:**

   ```bash
   pip install -r requirements.txt

3. **Jalankan aplikasi Flask:**

   ```bash
   python app.py

## Konfigurasi

### Konfigurasi Firebase

Aplikasi ini menggunakan Firebase untuk menyimpan data pesanan dan pembelian. Kredensial Firebase harus disimpan dalam file `data/iak-distributor-4-firebase-adminsdk-1dhwp-d6d2c24fb7.json`

## Endpoint API Public

### 1. Cek Status

- **Deskripsi**: API untuk mengecek status pengiriman berdasarkan input nomor resi
- **Endpoint:**: `GET /cekstatus`
- **Input**:
  - `no_resi`: Nomor resi dari pengiriman yang ingin dicek
- **Respon**:
  - **200 OK (Sukses):**
    ```json
    {
        "id_log": "string",
        "kota_asal": "string",
        "kota_tujuan": "string",
        "resi": "string",
        "status": "string"
    }
    ```
  - **400 Bad Request:**
    ```json
    {
        "status": "error",
        "message": "no_resi parameter is required"
    }
    ```
  - **404 Not Found:**
    ```json
    {
        "status": "error",
        "message": "No resi found"
    }
    ```

---

### 2. Cek Harga
- **Deskripsi**: API untuk mengecek harga pengiriman berdasarkan berat, kota asal, dan kota tujuan pengiriman.
- **Endpoint**: `POST /request_harga`
- **Input (JSON):**
  ```json
  {
      "purchases": [
          {
              "id_log": "string",
              "id_pembelian": "string",
              "berat": "float",
              "kota_asal": "string",
              "kota_tujuan": "string"
          }
      ]
  }
