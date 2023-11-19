from flask import Flask, render_template, request, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import firebase_admin
from firebase_admin import credentials, firestore
from credentials import firebase_credentials
import string
import random

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

# Functions
def returnValidLink(link):
    print(link)

    if link.startswith("https://") or link.startswith("http://"):
        return link

    if link.startswith("https:/") or link.startswith("http:/"):
        return f"/{link}"

    return f"https://{link}"

def returnValidShortened():
    validLink = None
    while validLink == None:
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(6))

        doc_ref = db.collection('urls').document(short_code)
        doc = doc_ref.get()
        if not doc.exists:
            validLink = short_code

    return validLink

# Routes
@app.route('/')
@limiter.limit("15000 per day", override_defaults=True)
def index():
    return render_template('index.html')

@app.route('/api/shorten', methods=['GET'])
def shorten():
    original_url = request.args.get('original_url')
    original_url = returnValidLink(original_url)
    short_code = returnValidShortened()

    if not original_url:
        return "Missing original_url in request", 400

    doc_ref = db.collection('urls').document(short_code)
    doc_ref.set({
        'original_url': original_url
    })

    shortened_url = request.url_root + short_code

    return shortened_url

@app.route('/<short_code>')
@limiter.limit("15000 per day", override_defaults=True)
def redirect_to_original(short_code):
    doc_ref = db.collection('urls').document(short_code)
    doc = doc_ref.get()

    if doc.exists:
        original_url = doc.to_dict()['original_url']
        return redirect(original_url)
    else:
        return "Short URL not found", 404

if __name__ == "__main__":
    app.run()