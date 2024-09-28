from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

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

if __name__ == '__main__':
    app.run(debug=True)
