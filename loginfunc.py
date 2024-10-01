import pandas as pd

# Data dari tabel disimpan sebagai list of dictionaries
def load_users_from_excel(file_path):
    df = pd.read_excel(file_path)
    users = df.to_dict(orient='records')
    return users

file_path = 'data/admin.xlsx'
users = load_users_from_excel(file_path)

# Function login 
def login_function(username_input, password_input):
    for user in users:
        if user['username'] == username_input and user['password'] == password_input:
            return {"success": True, "message": f"Selamat datang, {user['position']}"}
    return {"success": False, "message": "Username atau password salah."}
