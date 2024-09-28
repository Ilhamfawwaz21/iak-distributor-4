from flask import Flask, render_template, request
import pandas as pd
from purchases import process_purchases
from resi_checker import check_resi_code, generate_resi_code

app = Flask(__name__)

# Data dari tabel disimpan sebagai list of dictionaries
def load_users_from_excel(file_path):
    df = pd.read_excel(file_path)
    users = df.to_dict(orient='records')
    return users

file_path = 'D:/Kuliah/IAK UTS/UTS/iak-distributor-4/data/admin.xlsx'
users = load_users_from_excel(file_path)

# Function login 
def login(username_input, password_input):
    for user in users:
        if user['username'] == username_input and user['password'] == password_input:
            return f"Login berhasil! Selamat datang, {user['position']}."
    return "Login gagal! Username atau password salah."

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
    df_graph = pd.read_csv('data graph.csv')
    df_purchases = pd.read_excel('cobacobaaja.xlsx')

    results = process_purchases(df_graph, df_purchases)

    return render_template('results.html', results=results)

# Route untuk mengecek kode resi
@app.route('/check_resi', methods=['GET', 'POST'])
def check_resi_route():
    if request.method == 'POST':
        resi_code = request.form['resi_code']
        valid_resis = ['100923145601ABCD', '210923101233WXYZ']  # Daftar kode resi valid
        message = check_resi_code(resi_code, valid_resis)
        return render_template('check_resi.html', message=message)

    return render_template('check_resi.html')

if __name__ == '__main__':
    app.run(debug=True)
