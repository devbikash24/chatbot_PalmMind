import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from src.utilities.load_configuration import LoadConfiguration
from src.utilities.create_vectordb import PrepareFAISSVectorDB

# Initialize configuration and blueprint
app_config = LoadConfiguration()
ALLOWED_EXTENSIONS = app_config.allowed_extension
upload_bp = Blueprint('upload', __name__)

def allowed_file(filename):
    """
    Checks if the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clear_upload_folder(upload_folder):
    """
    Clears all files in the specified upload folder.
    """
    try:
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    except Exception as e:
        return f"Failed to delete files: {str(e)}"
    return None

@upload_bp.route('/upload-document', methods=['POST'])
def upload_file():
    """
    Handles document upload, validates file type, clears the folder before saving,
    and processes the document for FAISS vectorization.
    """
    upload_folder = app_config.directories_for_doc

    # Ensure the upload folder exists
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Clear the upload folder
    error = clear_upload_folder(upload_folder)
    if error:
        return jsonify({'success': False, 'message': error})

    # Validate if the 'document' key is in the request files
    if 'document' not in request.files:
        return jsonify({'success': False, 'message': 'No file part in the request.'}), 400

    file = request.files['document']

    # Validate the file name and format
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Invalid or no file selected.'}), 400

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({'success': False, 'message': f'File could not be saved: {str(e)}'}), 500

    # Process the uploaded file with FAISS
    try:
        db_instance = PrepareFAISSVectorDB(app_config)
        db_instance.prepare_and_save_vectordb()  # Implement logic for preparing FAISS
        db_instance.load_vectordb()  # Implement logic for loading FAISS
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error during vectorization: {str(e)}'}), 500

    return jsonify({'success': True, 'message': 'File successfully uploaded and vectorized.'}), 200
