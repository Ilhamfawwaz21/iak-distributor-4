from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import pandas as pd
from create_resi import add_resi, generate_resi_code
from purchases import process_purchases
from database import db
import firebase_admin
from firebase_admin import credentials, firestore
from loginfunc import login_function

app = Flask(__name__)

##Inisiasi firebase dari database.py##
if not firebase_admin._apps:  
    cred = credentials.Certificate("data/iak-distributor-4-firebase-adminsdk-1dhwp-d6d2c24fb7.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
orders_ref = db.collection('order')
history_ref = db.collection('history')
request_ref = db.collection('request_harga')
##firebase end##

##Fungsi Fungsi Start##
# Fungsi untuk mengambil data dari collection 'order'
def get_order_data():
    docs = orders_ref.stream() 

    orders = []
    for doc in docs:
        order_data = {
            'id_log': doc.get('id_log'),       
            'id_pembelian': doc.get('id_pembelian'), 
            'berat': doc.get('berat'),               
            'status': doc.get('status'),           
            'kota_asal': doc.get('kota_asal'), 
            'kota_tujuan': doc.get('kota_tujuan'),
            'resi': doc.get('resi')       
        }
        orders.append(order_data) 

    return orders 

# Fungsi history
def get_history_data():

    
    # Dapatkan semua dokumen dari koleksi 'history'
    docs = history_ref.stream()

    # Simpan hasil dalam list
    history_results = []

    # Iterasi melalui dokumen untuk mengumpulkan data
    for doc in docs:
        # Mengonversi dokumen Firestore ke dictionary
        data = doc.to_dict()

        # Simpan data ke list
        history_results.append({
            'id_log': data.get('id_log'),
            'id_pembelian': data.get('id_pembelian'),
            'berat': data.get('berat'),
            'status': data.get('status'),
            'kota_asal': data.get('kota_asal'),
            'kota_tujuan': data.get('kota_tujuan'),
            'resi': data.get('resi')
        })

    return history_results
##Fungsi Fungsi End##


## App Route Start##
# Route for the login page 
@app.route('/')
def landing():
    return render_template('landing_page.html')

# Route for the landing page
@app.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')


@app.route('/loginbro', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':  # Check if the request method is POST
        username = request.form.get('username')  # Use .get() to avoid errors
        password = request.form.get('password')

        # Ensure username and password are not empty
        if username and password:
            # Call login function
            login_result = login_function(username, password)

            if login_result['success']:  # If login is successful
                # Redirect to /home_order with a welcome message
                return redirect(url_for('home_order', message=login_result['message'], success=True))

            # If login fails, return to login page with an error message
            return render_template('loginbro.html', message=login_result['message'])
    
    # If the method is not POST, return the login form
    return render_template('loginbro.html')

# Route homeorder
@app.route('/home_order')
def home_order():
    # Call function to get order data from Firestore
    orders = get_order_data()
    history_orders = get_history_data()

    results = []
    for order in orders:
        data = {
            'id_log': order['id_log'],
            'id_pembelian': order['id_pembelian'],
            'berat': order['berat'],
            'status': order['status'],
            'kota_asal': order['kota_asal'],
            'kota_tujuan': order['kota_tujuan'],
            'resi': order['resi'],
            'update_url': url_for('update_order', resi=order['resi']),
            'delete_url': url_for('delete_order', resi=order['resi'])
        }
        results.append(data)

    history_results = []
    for order in history_orders:
        data = {
            'id_log': order['id_log'],
            'id_pembelian': order['id_pembelian'],
            'berat': order['berat'],
            'status': order['status'],
            'kota_asal': order['kota_asal'],
            'kota_tujuan': order['kota_tujuan'],
            'resi': order['resi']
        }
        history_results.append(data)

    # Retrieve message and success status from query parameters
    message = request.args.get('message')
    success = request.args.get('success')

    # Render the home_order template with the data and message
    return render_template('home_order.html', results=results, history_results=history_results, message=message, success=success)


# Route for checking resi
@app.route('/check_resi', methods=['GET', 'POST'])
def check_resi():
    if request.method == 'POST':
        resi = request.form.get('resi_code').strip()

        if not resi:
            return render_template('check_resi.html', message="Masukkan nomor resi.")

        # Query Firestore untuk order dengan resi yang ditentukan
        order_query = orders_ref.where('resi', '==', resi).limit(1).stream()
        order_data = None

        # Loop untuk mengecek apakah resi ditemukan
        for order in order_query:
            order_data = order.to_dict()

        # Jika tidak ditemukan di order, cari di history
        finished_statuses = []
        if not order_data:
            history_query = history_ref.where('resi', '==', resi).where('status', '==', 'Finished').stream()
            finished_statuses = [history.to_dict() for history in history_query]

        # Tentukan data yang akan ditampilkan
        if order_data:
            data_to_display = [order_data]  # Ambil data dari order
            order_status_message = (
                f"Tracking Number: {order_data['resi']}, Status: {order_data['status']}, "
                f"From: {order_data['kota_asal']}, To: {order_data['kota_tujuan']}"
            )
        elif finished_statuses:
            data_to_display = finished_statuses  # Ambil data dari history
            order_status_message = (
                f"Tracking Number: {resi}, Status: Finished"
            )
        else:
            return render_template('check_resi.html', message="Resi tidak ditemukan.")

        # Tampilkan halaman status dengan informasi order atau history
        return render_template('status.html', order_status=order_status_message, data_to_display=data_to_display)

    return render_template('check_resi.html')

# Route /status untuk mengambil data dengan status "Finished" dari koleksi 'history'
@app.route('/status')
def status():
    resi = request.args.get('resi_code')

    # Validasi jika resi tidak ditemukan
    if not resi:
        return redirect(url_for('check_resi', message="Nomor resi tidak ditemukan."))

    # Query ke koleksi 'order' untuk mengecek apakah resi ada
    order_query = orders_ref.where('resi', '==', resi).limit(1).stream()
    order_data = None

    for order in order_query:
        order_data = order.to_dict()  # Mengambil data order jika resi ditemukan

    # Jika resi tidak ditemukan di koleksi 'order', arahkan kembali ke halaman check_resi
    if not order_data:
        return redirect(url_for('check_resi', message="Resi tidak ditemukan di database order."))

    # Query untuk mengambil data history dengan status 'Finished'
    history_query = db.collection('history').where('resi', '==', resi).where('status', '==', 'Finished').stream()

    # Ambil data history jika ditemukan
    history_data = [history.to_dict() for history in history_query]

    # Jika data history tidak ditemukan, tampilkan pesan
    if not history_data:
        return redirect(url_for('check_resi', message="Data dengan status 'Finished' tidak ditemukan."))

    # Render halaman status dengan data order dan history
    return render_template('status.html', order_data=order_data, history_data=history_data)
##App Route End##


##Public API Route Start##
#Route GET status pengiriman
@app.route('/cekstatus', methods=['GET'])
def get_status():
    no_resi = request.args.get('no_resi')

    if not no_resi:
        return jsonify({'status': 'error', 'message': 'no_resi parameter is required'}), 400

    query = orders_ref.where('resi', '==', no_resi).get()

    if query:
        doc = query[0]
        data_status = doc.to_dict()
        status_data = {
            'id_log': data_status.get('id_log'),
            'kota_asal':data_status.get('kota_asal'),
            'kota_tujuan': data_status.get('kota_tujuan'),
            'resi': data_status.get('resi'),
            'status': data_status.get('status', 'on progress'),
        }
        return jsonify(status_data), 200
    else:
        return jsonify({'status': 'error', 'message': 'No resi found'}), 404


# Route untuk proses pembelian dan menghitung rute
@app.route('/request_harga', methods=['POST'])
def process_purchases_route():
    df_graph = pd.read_csv('data/data graph.csv')

    if request.is_json:
        try:
            purchase_data = request.get_json()
            if 'purchases' not in purchase_data:
                return jsonify({'status': 'error', 'message': 'Missing "purchases" key in JSON data'}), 400
            
            df_purchases = pd.DataFrame(purchase_data['purchases'])
            results = process_purchases(df_graph, df_purchases)

            for _, row in results.iterrows():
                if pd.isna(row['total_biaya']) or pd.isna(row['total_waktu']):
                    continue
                request_ref.add({
                    'id_log': row['id_log'],
                    'id_pembelian': row['id_pembelian'],
                    'kota_asal': row['kota_asal'],
                    'kota_tujuan': row['kota_tujuan'],
                    'berat': row['berat'],
                    'total_biaya': row['total_biaya'],
                    'total_waktu': row['total_waktu']
                })

            return jsonify(results.to_dict(orient='records')), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    else:
        return jsonify({'status': 'error', 'message': 'Invalid JSON format'}), 400

# Route create resi for supplier
@app.route('/create_resi', methods=['POST'])
def update_resi():
    # Ambil data dari request
    data = request.get_json()
    id_log = data.get('id_log')

    if not id_log:
        return jsonify({'message': 'id_log tidak ditemukan dalam request'}), 400

    result = add_resi(id_log)
    return jsonify(result)

##Public API Route End##


##CRUD Route Start##
#Route Create
@app.route('/add_orders', methods=['POST'])
def add_order():
    # Ambil data dari form
    id_log = request.form.get('id_log')
    id_pembelian = request.form.get('id_pembelian')
    berat = request.form.get('berat')
    kota_asal = request.form.get('kota_asal')
    kota_tujuan = request.form.get('kota_tujuan')

    # Set status default ke 'On Progress'
    status = "On Progress"

    # Validasi input
    if not all([id_log, id_pembelian, kota_asal, kota_tujuan]):
        return redirect(url_for('home_order', message='Semua field harus diisi!', success=False))

    # Generate nomor resi secara otomatis
    resi = generate_resi_code() 

    # Tambahkan order baru ke Firestore
    new_order = {
        'id_log': id_log,
        'id_pembelian': id_pembelian,
        'berat': berat,
        'status': status,
        'kota_asal': kota_asal,
        'kota_tujuan': kota_tujuan,
        'resi': resi,

    }

    try:
        # Simpan ke Firestore
        orders_ref.add(new_order)
        message = 'Order berhasil ditambahkan!'
        success = True
    except Exception as e:
        message = f'Gagal menambahkan order: {e}'
        success = False

    # Redirect ke home_order dengan pesan di query string
    return redirect(url_for('home_order', message=message, success=success))


# Route update
@app.route('/update/<resi>', methods=['POST'])
def update_order(resi):
    id_log = request.form.get('id_log')
    id_pembelian = request.form.get('id_pembelian')
    status = request.form.get('status')
    kota_asal = request.form.get('kota_asal')
    kota_tujuan = request.form.get('kota_tujuan')
    berat = request.form.get('berat')

    # Validasi input
    if not all([id_log, id_pembelian, resi, status, kota_asal, kota_tujuan, berat]):
        return redirect(url_for('home_order', message='Semua field harus diisi!', success=False))

    # Cari dokumen dengan resi tertentu di koleksi 'orders'
    query = orders_ref.where('resi', '==', resi).stream()
    updated = False

    try:
        for doc in query:
            existing_data = doc.to_dict()
            total_biaya = existing_data.get('total_biaya')
            order_data = {
                'id_log': id_log,
                'id_pembelian': id_pembelian,
                'resi': resi,
                'status': status,
                'kota_asal': kota_asal,
                'kota_tujuan': kota_tujuan,
                'total_biaya': total_biaya,
                'berat': berat,

            }

            # Jika status diubah menjadi "Finished", pindahkan ke 'history'
            if status == 'Finished':
                # Pindahkan data ke koleksi 'history'
                history_ref.add(order_data)
                doc.reference.delete()
            else:
                # Jika status bukan "Finished", cukup update status di 'orders'
                doc.reference.update(order_data)

            updated = True

        # Membuat message berdasarkan hasil update
        message = 'Order berhasil diperbarui!' if updated else 'Order tidak ditemukan.'
        return redirect(url_for('home_order', message=message, success=updated))
    
    except Exception as e:
        return redirect(url_for('home_order', message=f'Gagal memperbarui order: {e}', success=False))

#Route delete
@app.route('/delete/<resi>', methods=['POST'])
def delete_order(resi):
    # Cari dokumen dengan order_id tertentu
    query = orders_ref.where('resi', '==', resi).stream()
    deleted = False
    try:
        for doc in query:
            doc.reference.delete()
            deleted = True
        
        if deleted:
            return redirect(url_for('home_order', message='Order berhasil dihapus!', success=True))
        else:
            return redirect(url_for('home_order', message='Order tidak ditemukan.', success=False))
    except Exception as e:
        return redirect(url_for('home_order', message=f'Gagal menghapus order: {e}', success=False))

##CRUD Route End##

# Main entry point
if __name__ == '__main__':
    app.run(debug=True)
