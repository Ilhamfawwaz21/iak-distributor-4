import firebase_admin
from firebase_admin import credentials, firestore

# Inisialisasi Firebase dengan kunci pribadi
cred = credentials.Certificate('path/to/your-firebase-credentials.json')
firebase_admin.initialize_app(cred)

# Inisialisasi Firestore
db = firestore.client()