import firebase_admin
from firebase_admin import credentials, firestore

# Inisialisasi Firebase dengan kunci pribadi
cred = credentials.Certificate("data/cred.json")
firebase_admin.initialize_app(cred)

# Inisialisasi Firestore
try:
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firestore: {e}")
