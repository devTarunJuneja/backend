from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files or 'image_id' not in request.form:
        return jsonify({'error': 'Missing image or image_id'}), 400

    image = request.files['image']
    image_id = request.form['image_id']

    filename = secure_filename(f"{image_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}")
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(save_path)

    return jsonify({
        'url': f"/uploads/{filename}"
    }), 200

@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Use environment PORT if Railway provides it
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
