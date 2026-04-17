from flask import Blueprint, request, jsonify
import os

medical_bp = Blueprint('medical', __name__)

@medical_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_type = request.form['type']
    
    save_path = os.path.join('storage/', file.filename)
    file.save(save_path)
    
    return jsonify({"message": "File uploaded successfully"})
