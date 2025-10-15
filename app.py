"""
EmotionFAD - Fraud Activity Detection System
AI-powered fraud detection using emotion analysis and sentiment detection
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import numpy as np
import base64
from deepface import DeepFace
import io
from PIL import Image
import json
from datetime import datetime
import os
from textblob import TextBlob
import re
import threading
import webbrowser

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
app.config['SECRET_KEY'] = 'fad-fraud-detection-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Fraud detection keywords and patterns
FRAUD_KEYWORDS = [
    'steal', 'hack', 'fraud', 'scam', 'cheat', 'lie', 'deceive', 'manipulate',
    'fake', 'forge', 'embezzle', 'launder', 'bribe', 'extort', 'blackmail',
    'phishing', 'identity theft', 'credit card', 'bank account', 'password',
    'social security', 'illegal', 'crime', 'criminal', 'money transfer',
    'wire transfer', 'western union', 'gift card', 'bitcoin', 'cryptocurrency'
]

SUSPICIOUS_PATTERNS = [
    r'\b(give|send|transfer)\s+(me|us)\s+(money|cash|bitcoin|crypto)',
    r'\b(bank|credit\s+card|account)\s+(details|number|info)',
    r'\b(urgent|emergency|immediately|right\s+now)\b.*\b(money|payment)',
    r'\b(secret|don\'t\s+tell|keep\s+quiet|confidential)\b',
    r'\b(guaranteed|100%|risk-free)\s+(profit|return|money)',
    r'\b(act\s+now|limited\s+time|expires\s+soon)\b',
]

class FraudDetectionSystem:
    def __init__(self):
        self.session_data = {}
        self.fraud_threshold = 0.6
        print("✅ Fraud Detection System initialized")
        
    def analyze_facial_expression(self, image_data):
        """Analyze facial expressions and detect emotions"""
        try:
            # Decode base64 image
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            img_bytes = base64.b64decode(image_data)
            img = Image.open(io.BytesIO(img_bytes))
            img_array = np.array(img)
            
            # Convert RGB to BGR for OpenCV
            if len(img_array.shape) == 3 and img_array.shape[2] == 3:
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                img_bgr = img_array
            
            # Analyze emotions using DeepFace
            print("🔍 Analyzing facial expression...")
            analysis = DeepFace.analyze(img_bgr, actions=['emotion'], enforce_detection=False, silent=True)
            
            if isinstance(analysis, list):
                analysis = analysis[0]
            
            emotions = analysis['emotion']
            dominant_emotion = analysis['dominant_emotion']
            
            # Calculate stress and deception indicators
            stress_level = self._calculate_stress_level(emotions)
            deception_risk = self._calculate_deception_risk(emotions)
            mental_health_score = self._calculate_mental_health_score(emotions)
            
            print(f"✅ Analysis complete: {dominant_emotion} ({emotions[dominant_emotion]:.1f}%)")
            
            return {
                'success': True,
                'emotions': emotions,
                'dominant_emotion': dominant_emotion,
                'stress_level': stress_level,
                'deception_risk': deception_risk,
                'mental_health_score': mental_health_score,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Facial analysis error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Could not detect face. Please ensure your face is clearly visible with good lighting.'
            }
    
    def _calculate_stress_level(self, emotions):
        """Calculate stress level based on emotions"""
        stress_indicators = {
            'angry': 0.8,
            'fear': 0.9,
            'sad': 0.6,
            'disgust': 0.7,
            'surprise': 0.3,
            'neutral': 0.1,
            'happy': 0.0
        }
        
        stress = sum(emotions.get(emotion, 0) * weight 
                    for emotion, weight in stress_indicators.items())
        return min(stress / 100, 1.0)
    
    def _calculate_deception_risk(self, emotions):
        """Calculate deception risk based on emotional patterns"""
        fear = emotions.get('fear', 0)
        happy = emotions.get('happy', 0)
        surprise = emotions.get('surprise', 0)
        angry = emotions.get('angry', 0)
        
        deception_score = (fear * 0.4 + surprise * 0.2 + angry * 0.3 - happy * 0.1) / 100
        return max(0, min(deception_score, 1.0))
    
    def _calculate_mental_health_score(self, emotions):
        """Calculate mental health score (0-100, higher is better)"""
        positive_emotions = emotions.get('happy', 0) + emotions.get('neutral', 0) * 0.5
        negative_emotions = (emotions.get('sad', 0) + emotions.get('angry', 0) + 
                           emotions.get('fear', 0) + emotions.get('disgust', 0))
        
        score = (positive_emotions - negative_emotions * 0.5) 
        return max(0, min(score, 100))
    
    def analyze_text_sentiment(self, text):
        """Analyze text for sentiment and fraud indicators"""
        try:
            print(f"🔍 Analyzing text: {text[:50]}...")
            
            # Sentiment analysis
            blob = TextBlob(text)
            sentiment_polarity = blob.sentiment.polarity
            sentiment_subjectivity = blob.sentiment.subjectivity
            
            # Fraud keyword detection
            text_lower = text.lower()
            fraud_keywords_found = [kw for kw in FRAUD_KEYWORDS if kw in text_lower]
            
            # Pattern matching for suspicious phrases
            suspicious_patterns_found = []
            for pattern in SUSPICIOUS_PATTERNS:
                if re.search(pattern, text_lower):
                    suspicious_patterns_found.append(pattern)
            
            # Calculate fraud risk score
            fraud_risk = self._calculate_fraud_risk(
                sentiment_polarity,
                len(fraud_keywords_found),
                len(suspicious_patterns_found),
                sentiment_subjectivity
            )
            
            # Determine sentiment category
            if sentiment_polarity > 0.3:
                sentiment_category = 'positive'
            elif sentiment_polarity < -0.3:
                sentiment_category = 'negative'
            else:
                sentiment_category = 'neutral'
            
            print(f"✅ Text analysis complete: {sentiment_category}, risk: {fraud_risk:.2f}")
            
            return {
                'success': True,
                'text': text,
                'sentiment_polarity': sentiment_polarity,
                'sentiment_subjectivity': sentiment_subjectivity,
                'sentiment_category': sentiment_category,
                'fraud_keywords_found': fraud_keywords_found,
                'suspicious_patterns_count': len(suspicious_patterns_found),
                'fraud_risk_score': fraud_risk,
                'is_suspicious': fraud_risk > self.fraud_threshold,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Text analysis error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_fraud_risk(self, sentiment, keyword_count, pattern_count, subjectivity):
        """Calculate overall fraud risk score"""
        keyword_score = min(keyword_count * 0.2, 0.5)
        pattern_score = min(pattern_count * 0.25, 0.4)
        sentiment_score = max(0, -sentiment * 0.3)
        subjectivity_score = subjectivity * 0.1
        
        total_risk = keyword_score + pattern_score + sentiment_score + subjectivity_score
        return min(total_risk, 1.0)
    
    def generate_comprehensive_report(self, facial_data, text_data):
        """Generate comprehensive fraud detection report"""
        try:
            overall_risk = 0
            risk_factors = []
            
            # Analyze facial data
            if facial_data and facial_data.get('success'):
                facial_risk = (facial_data['deception_risk'] * 0.4 + 
                             facial_data['stress_level'] * 0.3)
                overall_risk += facial_risk * 0.5
                
                if facial_data['deception_risk'] > 0.6:
                    risk_factors.append('High deception indicators in facial expression')
                if facial_data['stress_level'] > 0.7:
                    risk_factors.append('Elevated stress levels detected')
                if facial_data['mental_health_score'] < 40:
                    risk_factors.append('Poor mental health indicators')
            
            # Analyze text data
            if text_data and text_data.get('success'):
                overall_risk += text_data['fraud_risk_score'] * 0.5
                
                if text_data['fraud_keywords_found']:
                    risk_factors.append(f"Fraud-related keywords detected: {', '.join(text_data['fraud_keywords_found'][:3])}")
                if text_data['suspicious_patterns_count'] > 0:
                    risk_factors.append('Suspicious communication patterns detected')
                if text_data['sentiment_polarity'] < -0.5:
                    risk_factors.append('Highly negative sentiment detected')
            
            # Determine risk level
            if overall_risk > 0.7:
                risk_level = 'HIGH'
                recommendation = '🚨 ALERT: High fraud risk detected. Immediate investigation recommended.'
            elif overall_risk > 0.4:
                risk_level = 'MEDIUM'
                recommendation = '⚠️ WARNING: Moderate fraud risk. Monitor closely and verify information.'
            else:
                risk_level = 'LOW'
                recommendation = '✅ Low fraud risk. Continue normal interaction.'
            
            print(f"📊 Comprehensive report: {risk_level} risk ({overall_risk:.2f})")
            
            return {
                'success': True,
                'overall_risk_score': overall_risk,
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendation': recommendation,
                'facial_analysis': facial_data,
                'text_analysis': text_data,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Report generation error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

# Initialize fraud detection system
fds = FraudDetectionSystem()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/analyze/facial', methods=['POST'])
def analyze_facial():
    """Endpoint for facial expression analysis"""
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'error': 'No image data provided'}), 400
        
        result = fds.analyze_facial_expression(image_data)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Facial endpoint error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Endpoint for text sentiment and fraud analysis"""
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        result = fds.analyze_text_sentiment(text)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Text endpoint error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/analyze/comprehensive', methods=['POST'])
def analyze_comprehensive():
    """Endpoint for comprehensive analysis"""
    try:
        data = request.json
        facial_data = data.get('facial_data')
        text_data = data.get('text_data')
        
        result = fds.generate_comprehensive_report(facial_data, text_data)
        return jsonify(result)
    except Exception as e:
        print(f"❌ Comprehensive endpoint error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'EmotionFAD - Fraud Activity Detection',
        'version': '2.0',
        'timestamp': datetime.now().isoformat()
    })

def open_browser():
    """Open browser automatically"""
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*60)
    print("🛡️  EmotionFAD - Fraud Activity Detection System")
    print("="*60)
    print("\n🚀 Starting server...")
    print("📍 Local URL: http://localhost:5000")
    print("📍 Network URL: http://0.0.0.0:5000")
    print("\n💡 For public access, use ngrok:")
    print("   ngrok http 5000")
    print("   URL will be: https://EmotionFAD.ngrok.io")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser after a short delay
    threading.Timer(1.5, open_browser).start()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
