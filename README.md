# 🛡️ EmotionFAD - Fraud Activity Detection System

![Python](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/flask-3.0-green)
![AI](https://img.shields.io/badge/AI-DeepFace-orange)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

AI-powered fraud detection system using facial expression analysis, text sentiment analysis, and behavioral pattern recognition.

**Live Demo:** [Coming Soon]

---

## 🌟 Features

### 🎭 Facial Expression Analysis
- Detects 7 emotions: Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral
- Real-time mental health scoring (0-100%)
- Stress level monitoring
- Deception risk assessment
- Auto-analysis mode (continuous monitoring)

### 💬 Text Sentiment Analysis
- Sentiment detection (positive/negative/neutral)
- 30+ fraud keyword detection
- Suspicious pattern recognition
- Real-time fraud risk scoring (0-100%)

### 🎤 Voice Input
- Speech-to-text conversion
- Voice sentiment analysis
- Multi-language support

### 📊 Comprehensive Reporting
- Overall risk assessment (LOW/MEDIUM/HIGH)
- Detailed risk factor identification
- Actionable recommendations
- Real-time dashboard with live metrics

### 📱 Progressive Web App
- Installable on any device
- Works offline (limited functionality)
- Native app experience
- Searchable as "EmotionFAD"

---

## 🚀 Quick Start

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
# Option 1: Double-click
START_EmotionFAD.bat

# Option 2: Command line
python app.py
```

### Step 3: Access the Application
- Open browser to: **http://localhost:5000**
- Click "Grant Permissions" for camera and microphone
- Start analyzing!

---

## 🌐 Create Public URL

### Using ngrok (Easiest):

**Step 1:** Download ngrok from https://ngrok.com/download

**Step 2:** Sign up and get auth token from https://dashboard.ngrok.com/signup

**Step 3:** Configure ngrok
```bash
ngrok config add-authtoken YOUR_TOKEN
```

**Step 4:** Create public URL
```bash
# Option 1: Automated
create_public_url.bat

# Option 2: Manual
# Terminal 1
python app.py

# Terminal 2
ngrok http 5000
```

**Step 5:** Share the URL (e.g., `https://EmotionFAD.ngrok.io`)

---

## ✨ Features

### 🎭 Facial Expression Analysis
- 7 emotions detected: Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral
- Mental health score (0-100%)
- Stress level monitoring
- Deception risk assessment
- Auto-analysis mode

### 💬 Text Sentiment Analysis
- Sentiment detection (positive/negative/neutral)
- 30+ fraud keyword detection
- Suspicious pattern recognition
- Real-time fraud risk scoring

### 🎤 Voice Input
- Speech-to-text conversion
- Voice sentiment analysis
- Multi-language support

### 📊 Comprehensive Reporting
- Overall risk assessment (LOW/MEDIUM/HIGH)
- Risk factor identification
- Actionable recommendations
- Real-time dashboard

### 📱 Progressive Web App
- Installable on any device
- Works offline (limited)
- Native app experience
- Searchable as "EmotionFAD"

---

## 📁 Project Structure

```
EmotionFAD/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Web interface
├── static/
│   ├── app.js                 # JavaScript logic
│   ├── styles.css             # Styling
│   ├── manifest.json          # PWA configuration
│   └── sw.js                  # Service worker
├── START_EmotionFAD.bat       # Windows startup script
├── create_public_url.bat      # Public URL creator
└── setup_ngrok.py             # Automated ngrok setup
```

---

## 🎯 Usage

### Facial Analysis
1. Click "Start Camera"
2. Click "Analyze" for single scan
3. Click "Auto" for continuous monitoring (every 3 seconds)

### Text Analysis
1. Type a message in the chat box
2. Press Enter or click send
3. View sentiment and fraud risk assessment

### Voice Input
1. Click the microphone icon
2. Speak your message
3. System converts to text and analyzes

---

## 🔧 Troubleshooting

### Camera Not Working
- Close other apps using camera (Zoom, Teams, Skype)
- Check browser permissions: Settings → Privacy → Camera
- Try different browser (Chrome recommended)

### Port Already in Use
```bash
# Find and kill process
netstat -ano | findstr :5000
taskkill /PID [PID] /F
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### ngrok Not Working
- Make sure both app.py and ngrok are running
- Check if auth token is configured
- Verify ngrok shows "Forwarding" message

For more help, see **FIX_ERRORS.md**

---

## 📚 Documentation

- **README.md** (this file) - Quick start guide
- **HOW_TO_ACCESS.md** - All ways to access the application
- **SETUP_PUBLIC_URL.md** - Detailed public URL setup
- **FIX_ERRORS.md** - Common errors and solutions

---

## 🌍 Deployment Options

### Local (Development)
```bash
python app.py
# Access at: http://localhost:5000
```

### Public (ngrok)
```bash
ngrok http 5000
# Access at: https://[random].ngrok.io
```

### Cloud (Production)
- **Render.com** - Free, permanent URL
- **Heroku** - Free tier available
- **AWS/Azure** - Enterprise solutions

See **SETUP_PUBLIC_URL.md** for detailed instructions.

---

## 🔒 Security & Privacy

- ✅ Local processing - no cloud data storage
- ✅ Session-based analysis only
- ✅ No permanent data storage
- ✅ Permission-based access
- ✅ HTTPS ready (via ngrok or cloud)

---

## 📊 Technical Stack

- **Backend:** Flask 3.0, Python 3.12
- **AI/ML:** DeepFace, TensorFlow, OpenCV
- **NLP:** TextBlob, Scikit-learn
- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **PWA:** Service Workers, Web Manifest

---

## ✅ System Requirements

- Python 3.8 or higher
- Webcam (for facial analysis)
- Microphone (for voice input)
- Modern browser (Chrome recommended)
- Internet connection (for first run - downloads AI models)

---

## 🎓 Use Cases

- Security screening
- Customer service monitoring
- Interview analysis
- Mental health assessment
- Fraud prevention
- Behavioral research

---

## 📞 Support

### Quick Commands
```bash
# Check setup
python check_setup.py

# Start application
python app.py

# Create public URL
create_public_url.bat
```

### Documentation
- Complete guide: **HOW_TO_ACCESS.md**
- Public URL setup: **SETUP_PUBLIC_URL.md**
- Error solutions: **FIX_ERRORS.md**

---

## 🎉 Ready to Use!

**To start EmotionFAD:**
```bash
# Just double-click:
START_EmotionFAD.bat

# Or run:
python app.py
```

**To create public URL:**
```bash
# Just double-click:
create_public_url.bat
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [DeepFace](https://github.com/serengil/deepface) for facial analysis
- [TensorFlow](https://www.tensorflow.org/) for deep learning
- [Flask](https://flask.palletsprojects.com/) for web framework
- [TextBlob](https://textblob.readthedocs.io/) for NLP
- [ngrok](https://ngrok.com/) for public URLs

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**EmotionFAD - Protecting against fraud with AI-powered analysis! 🛡️**

**Version:** 2.0  
**Status:** Production Ready ✅  
**Last Updated:** October 2025
