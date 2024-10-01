import random
import string
from datetime import datetime
from database import db

# Generate nomor resi
def generate_resi_code():
    now = datetime.now()
    date_part = now.strftime("%d%m%y")
    time_part = now.strftime("%H%M%S")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    resi_code = f"{date_part}{time_part}{random_part}"
    return resi_code

def add_resi(id_log):
    request_harga_ref = db.collection('request_harga')
    query = request_harga_ref.where('id_log', '==', id_log).get()
    if query:
        doc = query[0]  # Ambil dokumen pertama

        # Ambil data dari dokumen yang ditemukan di 'request_harga'
        purchase_data = doc.to_dict()

        # Generate nomor resi baru
        resi_code = generate_resi_code()

        order_data = {
            'id_log': purchase_data['id_log'],
            'kota_asal': purchase_data['kota_asal'],
            'kota_tujuan': purchase_data['kota_tujuan'],
            'berat': purchase_data['berat'],
            'total_biaya': purchase_data['total_biaya'],
            'resi': resi_code, 
            'status': 'on progress', 
        }

        try:
            order_ref = db.collection('order')
            order_ref.add(order_data)

            # Hapus dokumen dari 'request_harga' hanya jika penyimpanan berhasil
            for doc in query:
                doc.reference.delete()

            # Kembalikan hasil jika proses berhasil
            return {
                'id_log': purchase_data['id_log'],
                'resi': resi_code,
            }
        
        except Exception as e:
            return {
                'id_log': id_log,
                'message': f'Gagal menyimpan data ke order: {str(e)}'
            }

    else:
        return {
            'id_log': id_log,
            'message': 'Data dengan id_log tidak ditemukan'
        }
   