import flask
from flask import Flask, render_template, request
import pandas as pd
from purchases import process_purchases
from login import load_users_from_excel, login
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

file_path = '.../iak-distributor-4/data/admin.xlsx'
users = load_users_from_excel(file_path)

##Database start##
cred = credentials.Certificate(".../iak-distributor-4/data/iak-distributor-4-78b8c3de8089.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
##Database End##

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_route():
    username = request.form['username']
    password = request.form['password']
    
    # Panggil fungsi login
    message = login(username, password)
    
    return render_template('login.html', message=message)

# Route untuk memproses pembelian dan menghitung rute
@app.route('/process_purchases', methods=['POST'])
def process_purchases_route():
    # Baca file 'data graph.csv' sebagai grafik yang sudah ada
    df_graph = pd.read_csv('.../iak-distributor-4/data/data_graph.csv')

    # Periksa apakah request JSON ada
    if request.is_json:
        try:
            # Ambil data JSON dari request
            purchase_data = request.get_json()

            # Konversi data JSON ke DataFrame pandas
            df_purchases = pd.DataFrame(purchase_data)

            # Proses pembelian dengan algoritma
            results = process_purchases(df_graph, df_purchases)

            # Simpan hasil ke Firebase
            for result in results:
                db.collection('request_harga').add(result)

            # Kembalikan hasil
            return jsonify(results), 200

        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    else:
        return jsonify({'status': 'error', 'message': 'Invalid JSON format'}), 400

@app.route('/update_resi', methods=['POST'])
def update_resi():
    # Ambil data dari request
    data = request.get_json()
    id_log = data.get('id_log')

    if not id_log:
        return jsonify({'message': 'id_log tidak ditemukan dalam request'}), 400

    # Panggil fungsi untuk update resi
    result = add_resi(id_log)

    # Kembalikan hasil sebagai response JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
