from flask import Flask, render_template, request, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import firebase_admin
from firebase_admin import credentials, firestore
from credentials import firebase_credentials

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

app = Flask(__name__)
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get/<short_code>', methods=['GET'])
def returnLink(short_code):
    doc_ref = db.collection('urls').document(short_code)
    doc = doc_ref.get()

    if doc.exists:
        original_url = doc.to_dict()['original_url']
        return original_url
    else:
        return "Short URL not found", 404

if __name__ == "__main__":
    app.run()