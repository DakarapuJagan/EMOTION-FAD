"""
EmotionFAD - Emotion Analysis Module
Handles real-time facial expression and emotion detection
"""

import cv2
import numpy as np
from fer import FER
from PIL import Image
import io
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('emotion_analysis')

class EmotionAnalyzer:
    def __init__(self):
        """Initialize the emotion detector and face detector."""
        try:
            # Initialize FER (Facial Emotion Recognition) detector
            self.detector = FER(mtcnn=True)  # Using MTCNN for better face detection
            logger.info("Emotion detector initialized successfully")
            
            # Initialize OpenCV's face detector
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            logger.info("Face detector initialized successfully")
            
            # Define emotion labels
            self.EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
            
        except Exception as e:
            logger.error(f"Error initializing emotion analyzer: {str(e)}")
            raise

    def detect_face(self, image):
        """Detect faces in the image using OpenCV."""
        try:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            return faces
            
        except Exception as e:
            logger.error(f"Error in face detection: {str(e)}")
            return []

    def analyze_emotions(self, image):
        """Analyze emotions in the given image."""
        try:
            # Convert image to RGB (FER expects RGB)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect emotions
            results = self.detector.detect_emotions(rgb_image)
            
            if not results:
                return {"status": "no_faces", "message": "No faces detected"}
            
            # Process results
            emotions = []
            for face in results:
                # Get face coordinates
                x, y, w, h = face['box']
                
                # Get emotion scores
                emotion_scores = face['emotions']
                
                # Get dominant emotion
                dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
                
                emotions.append({
                    "box": {"x": int(x), "y": int(y), "w": int(w), "h": int(h)},
                    "emotions": emotion_scores,
                    "dominant_emotion": dominant_emotion[0],
                    "confidence": float(dominant_emotion[1])
                })
            
            return {
                "status": "success",
                "faces_detected": len(emotions),
                "analysis": emotions
            }
            
        except Exception as e:
            logger.error(f"Error in emotion analysis: {str(e)}")
            return {"status": "error", "message": str(e)}

    def process_frame(self, frame_data):
        """Process a single frame of video data (base64 encoded)."""
        try:
            # Convert base64 to image
            if ',' in frame_data:
                frame_data = frame_data.split(',')[1]
            
            img_data = base64.b64decode(frame_data)
            nparr = np.frombuffer(img_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {"status": "error", "message": "Failed to decode image"}
            
            # Analyze emotions
            result = self.analyze_emotions(image)
            
            # Add visualization if faces were detected
            if result["status"] == "success" and result["faces_detected"] > 0:
                result["frame_with_boxes"] = self.draw_boxes(image, result["analysis"])
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def draw_boxes(self, image, analysis_results):
        """Draw bounding boxes and emotion labels on the image."""
        try:
            img = image.copy()
            
            for face in analysis_results:
                box = face["box"]
                emotion = face["dominant_emotion"]
                confidence = face["confidence"]
                
                # Draw rectangle around face
                cv2.rectangle(
                    img,
                    (box["x"], box["y"]),
                    (box["x"] + box["w"], box["y"] + box["h"]),
                    (0, 255, 0),
                    2
                )
                
                # Draw emotion label
                label = f"{emotion}: {confidence:.2f}"
                cv2.putText(
                    img,
                    label,
                    (box["x"], box["y"] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )
            
            # Convert back to base64
            _, buffer = cv2.imencode('.jpg', img)
            img_str = base64.b64encode(buffer).decode('utf-8')
            
            return f"data:image/jpeg;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"Error drawing boxes: {str(e)}")
            return ""

# Example usage
if __name__ == "__main__":
    try:
        # Initialize analyzer
        analyzer = EmotionAnalyzer()
        
        # Test with a sample image
        test_image_path = "test_face.jpg"  # Replace with path to a test image
        
        if os.path.exists(test_image_path):
            # Read test image
            image = cv2.imread(test_image_path)
            
            if image is not None:
                # Analyze emotions
                result = analyzer.analyze_emotions(image)
                print("Emotion Analysis Result:")
                print(json.dumps(result, indent=2))
                
                # Show image with boxes
                if result["status"] == "success" and result["faces_detected"] > 0:
                    img_with_boxes = analyzer.draw_boxes(image, result["analysis"])
                    if img_with_boxes:
                        # Display the image (for testing)
                        img_data = base64.b64decode(img_with_boxes.split(',')[1])
                        nparr = np.frombuffer(img_data, np.uint8)
                        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        cv2.imshow("Emotion Detection", img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
            else:
                print(f"Failed to load test image: {test_image_path}")
        else:
            print(f"Test image not found: {test_image_path}")
            print("Please provide a path to a test image.")
            
    except Exception as e:
        print(f"Error in example usage: {str(e)}")
