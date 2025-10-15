"""
EmotionFAD - Main Application with Emotion Analysis
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from emotion_analysis import EmotionAnalyzer
import base64
import os
import logging
import json
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('emotion_fad')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'emotion-fad-secret-2025')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Get port from environment variable or use default
port = int(os.environ.get('PORT', 5000))

# Initialize SocketIO with appropriate settings for production
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='eventlet',
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=1e8  # 100MB max for file uploads
)

# Initialize emotion analyzer (lazy loading)
analyzer = None

def get_analyzer():
    global analyzer
    if analyzer is None:
        try:
            analyzer = EmotionAnalyzer()
            logger.info("Emotion analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize emotion analyzer: {str(e)}")
            return None
    return analyzer

# Routes
@app.route('/')
def index():
    """Render the main application page."""
    return render_template('emotion_analysis.html')

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connection."""
    logger.info(f'Client connected: {request.sid}')
    emit('connection_response', {'status': 'connected', 'analyzer_ready': analyzer is not None})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection."""
    logger.info(f'Client disconnected: {request.sid}')

@socketio.on('start_analysis')
def handle_start_analysis():
    """Handle request to start emotion analysis."""
    try:
        if analyzer is None:
            emit('analysis_error', {'error': 'Emotion analyzer not initialized'})
            return
        
        emit('analysis_started', {'status': 'success'})
        logger.info('Emotion analysis started')
        
    except Exception as e:
        error_msg = f'Error starting analysis: {str(e)}'
        logger.error(error_msg)
        emit('analysis_error', {'error': error_msg})

@socketio.on('video_frame')
def handle_video_frame(data):
    """Process video frame for emotion analysis."""
    try:
        if analyzer is None:
            emit('analysis_error', {'error': 'Emotion analyzer not initialized'})
            return
        
        # Process the frame
        result = analyzer.process_frame(data['frame'])
        
        # Add timestamp
        result['timestamp'] = datetime.now().isoformat()
        
        # Send the result back to the client
        emit('analysis_result', result)
        
    except Exception as e:
        error_msg = f'Error processing video frame: {str(e)}'
        logger.error(error_msg)
        emit('analysis_error', {'error': error_msg})

# API endpoint for single image analysis
@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """API endpoint for analyzing a single image."""
    try:
        if 'image' not in request.files and 'image' not in request.json:
            return jsonify({'error': 'No image provided'}), 400
            
        if 'image' in request.files:
            # Handle file upload
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
                
            # Read image file
            image_data = file.read()
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
        else:
            # Handle base64 encoded image
            image_data = request.json['image']
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            img_data = base64.b64decode(image_data)
            nparr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'error': 'Failed to decode image'}), 400
        
        # Analyze emotions
        result = analyzer.analyze_emotions(image)
        
        # Add visualization if faces were detected
        if result["status"] == "success" and result["faces_detected"] > 0:
            result["frame_with_boxes"] = analyzer.draw_boxes(image, result["analysis"])
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'Error in analyze_image: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    
    # Print startup message
    print("\n" + "="*60)
    print("EmotionFAD - Emotion and Fraud Analysis Detection")
    print("="*60)
    print("\nStarting server...")
    print(f"Local URL: http://localhost:5000")
    
    # Run the application
    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False,
            allow_unsafe_werkzeug=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        print("\nError:", str(e))
        print("\nTroubleshooting:")
        print("1. Make sure port 5000 is not in use by another application")
        print("2. Try running as administrator")
        print("3. Check your firewall settings")
        input("\nPress Enter to exit...")
