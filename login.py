import pandas as pd

# Fungsi untuk memuat data user dari file Excel
def load_users_from_excel(file_path):
    df = pd.read_excel(file_path)
    users = df.to_dict(orient='records')
    return users

# Fungsi login untuk memeriksa username dan password
def login(users, username_input, password_input):
    for user in users:
        if user['username'] == username_input and user['password'] == password_input:
            return f"Login berhasil! Selamat datang, {user['position']}."
    return "Login gagal! Username atau password salah."
