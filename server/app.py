from flask import Flask, request, jsonify
from flask_cors import CORS
import gpt4_service
import dalle_service
from database import db, Koan
import openai
import settings

openai.api_key = settings.openai_api_key
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///koans.db'
db.init_app(app)

with app.app_context():
    db.create_all()  # Creates SQLite database file and schema on startup


@app.route('/generate-koan', methods=['POST'])
def generate_koan():
    prompt = request.json.get('prompt')
    koan_text = gpt4_service.generate_koan(prompt)
    koan = Koan(koan_text=koan_text)
    db.session.add(koan)
    db.session.commit()
    return jsonify({'koan_id': koan.id, 'koan': koan_text})

@app.route('/koan/<int:id>', methods=['GET'])
def get_koan(id):
    koan = Koan.query.get(id)
    if koan is None:
        return jsonify({'error': 'Koan not found'}), 404
    return jsonify({'koan': koan.koan_text, 'image_url': koan.image_url})

@app.route('/generate-image', methods=['POST'])
def generate_image():
    koan_id = request.json.get('koan_id')
    koan = Koan.query.get(koan_id)
    if koan is None:
        return jsonify({'error': 'Koan not found'}), 404
    image_url = dalle_service.generate_image(koan.koan_text)
    koan.image_url = image_url
    db.session.commit()
    return jsonify({'image_url': image_url})

if __name__ == '__main__':
    app.run(debug=True)
