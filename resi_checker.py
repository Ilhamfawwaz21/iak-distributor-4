import random
import string
from datetime import datetime

def generate_resi_code():
    now = datetime.now()
    date_part = now.strftime("%d%m%y")
    time_part = now.strftime("%H%M%S")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    resi_code = f"{date_part}{time_part}{random_part}"
    return resi_code

# Fungsi untuk mengecek apakah resi valid (contoh sederhana)
def check_resi_code(resi, valid_resis):
    if resi in valid_resis:
        return "Resi valid."
    else:
        return "Resi tidak ditemukan."