import os
from binascii import a2b_base64

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
from sqlalchemy.sql.expression import func

import settings
import gpt4_service
import dalle_service
from database import db, Koan

openai.api_key = settings.openai_api_key
app = Flask(__name__, static_folder=settings.static_folder, static_url_path='/')
CORS(app)  # Enable CORS for all routes


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///koans.db'
db.init_app(app)

with app.app_context():
    db.create_all()  # Creates SQLite database file and schema on startup


@app.route('/', defaults={'path': ''})
@app.route("/<string:path>")
@app.route('/<path:path>/<int:id>')
def serve(path, id=None):
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/generate-koan', methods=['POST'])
def generate_koan():
    prompt = request.json.get('prompt')
    koan_text = gpt4_service.generate_koan(prompt)
    koan = Koan(koan_text=koan_text)
    db.session.add(koan)
    db.session.commit()
    return jsonify({'koan_id': koan.id, 'koan': koan_text})


@app.route('/api/koan/<int:id>', methods=['GET'])
def get_koan(id):
    koan = Koan.query.get(id)
    if koan is None:
        return jsonify({'error': 'Koan not found'}), 404
    return jsonify({
        'koan': koan.koan_text,
        'image_url': koan.image_url,
        'image_alt_text': koan.image_description,
    })


# TODO make this like a paginated thing with random option
@app.route('/api/koans', methods=['GET'])
def get_koans():
    random_koans = Koan.query.order_by(func.random()).limit(10).all()
    koan_list = [{
        'koan_id': koan.id, 
        'koan_text': koan.koan_text, 
        'image_url': koan.image_url,
        'image_alt_text': koan.image_description,
    } for koan in random_koans]
    return jsonify({'koans': koan_list})


@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    koan_id = request.json.get('koan_id')
    koan = Koan.query.get(koan_id)
    if koan is None:
        return jsonify({'error': 'Koan not found'}), 404

    description, image_data = dalle_service.generate_image(koan.koan_text)
    binary_data = a2b_base64(image_data)
    with open(os.path.join(settings.static_folder, "static", "koans", f'{koan_id}.png'), 'wb') as fd:
        fd.write(binary_data)
        fd.close()

    koan.image_url = f"/static/koans/{koan_id}.png"
    koan.image_description = description
    db.session.commit()
    return jsonify({'image_url': koan.image_url, "image_alt_text": koan.image_description})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
