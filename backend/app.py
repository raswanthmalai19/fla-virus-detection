"""
Flask API Server for Virus Detection System
Provides RESTful endpoints for file scanning and log retrieval
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.detector import VirusDetector
from backend.logger import DetectionLogger

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'exe', 'dll', 'bat', 'vbs', 'js', 'ps1', 'sh', 'bin', 'dat', 'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize detector and logger
detector = VirusDetector()
logger = DetectionLogger()

def ensure_upload_directory():
    """Create upload directory if it doesn't exist"""
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the frontend dashboard"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/scan', methods=['POST'])
def scan_file():
    """
    Scan uploaded file for virus signatures.
    Returns detection results and logs the scan.
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Get algorithms to use (optional parameter)
        algorithms = request.form.get('algorithms', None)
        if algorithms:
            algorithms = algorithms.split(',')
        
        # Save file temporarily
        ensure_upload_directory()
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Scan the file
        scan_results = detector.scan_file(file_path, algorithms)
        
        # Log the scan
        log_data = {
            'filename': filename,
            'file_size': scan_results.get('file_size', 0),
            'threats_found': scan_results.get('threats_found', []),
            'risk_level': scan_results.get('risk_level', 'UNKNOWN'),
            'algorithm_detections': scan_results.get('algorithm_detections', {}),
            'scan_summary': scan_results.get('scan_summary', {})
        }
        timestamp = logger.log_scan(log_data)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        # Prepare response
        response = {
            'success': True,
            'timestamp': timestamp,
            'filename': filename,
            'file_size': scan_results.get('file_size', 0),
            'risk_level': scan_results.get('risk_level', 'UNKNOWN'),
            'threats_found': scan_results.get('threats_found', []),
            'threat_count': len(scan_results.get('threats_found', [])),
            'algorithm_detections': scan_results.get('algorithm_detections', {}),
            'scan_summary': scan_results.get('scan_summary', {}),
            'is_infected': len(scan_results.get('threats_found', [])) > 0
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """
    Get recent scan logs.
    Query parameter: limit (default: 10)
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        logs = logger.get_recent_logs(limit)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """
    Get overall detection statistics.
    """
    try:
        stats = logger.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/signatures', methods=['GET'])
def get_signatures():
    """
    Get information about virus signatures in the database.
    """
    try:
        signatures = detector.get_signature_info()
        
        return jsonify({
            'success': True,
            'signatures': signatures,
            'count': len(signatures)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'signatures_loaded': len(detector.signatures),
        'algorithms_available': list(detector.algorithms.keys())
    }), 200

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 10MB.'
    }), 413

if __name__ == '__main__':
    ensure_upload_directory()
    print("\n" + "="*60)
    print("🛡️  Virus Signature Detection System")
    print("="*60)
    print(f"✓ Loaded {len(detector.signatures)} virus signatures")
    print(f"✓ {len(detector.algorithms)} detection algorithms ready")
    print("\n📊 Algorithms:")
    print("   • KMP (Knuth-Morris-Pratt)")
    print("   • Aho-Corasick (Multi-Pattern)")
    print("   • DFA (Finite State Automaton)")
    print("\n🌐 Server starting at http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
