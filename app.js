// FAD v2.0 - Improved JavaScript Application

class FADApp {
    constructor() {
        this.videoElement = document.getElementById('videoElement');
        this.canvasElement = document.getElementById('canvasElement');
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        
        this.stream = null;
        this.isAnalyzing = false;
        this.analysisInterval = null;
        this.lastFacialData = null;
        this.lastTextData = null;
        
        this.API_BASE = window.location.origin;
        
        console.log('🛡️ FAD System initializing...');
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        console.log('✅ FAD System ready');
    }
    
    setupEventListeners() {
        // Permission button
        document.getElementById('grantPermissionBtn').addEventListener('click', () => {
            this.requestPermissions();
        });
        
        // Camera controls
        document.getElementById('toggleCameraBtn').addEventListener('click', () => {
            this.toggleCamera();
        });
        
        document.getElementById('captureBtn').addEventListener('click', () => {
            this.captureAndAnalyze();
        });
        
        document.getElementById('autoAnalyzeBtn').addEventListener('click', () => {
            this.toggleAutoAnalysis();
        });
        
        // Chat controls
        document.getElementById('sendBtn').addEventListener('click', () => {
            this.sendMessage();
        });
        
        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        document.getElementById('voiceBtn').addEventListener('click', () => {
            this.startVoiceInput();
        });
    }
    
    async requestPermissions() {
        try {
            console.log('📹 Requesting camera and microphone permissions...');
            
            // Request permissions
            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { 
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }, 
                audio: true 
            });
            
            console.log('✅ Permissions granted!');
            
            // Stop the stream - we just needed permission
            stream.getTracks().forEach(track => {
                console.log(`Stopping ${track.kind} track`);
                track.stop();
            });
            
            // Hide modal and show main app
            document.getElementById('permissionModal').classList.add('hidden');
            document.getElementById('mainContainer').style.display = 'block';
            
            // Show success message
            this.showAlert('✅ Permissions granted! You can now use all features.', 'success');
            
        } catch (error) {
            console.error('❌ Permission error:', error);
            
            let errorMessage = '❌ Permission denied. ';
            if (error.name === 'NotAllowedError') {
                errorMessage += 'Please click "Allow" when your browser asks for camera and microphone access.';
            } else if (error.name === 'NotFoundError') {
                errorMessage += 'No camera or microphone found. Please connect your devices.';
            } else if (error.name === 'NotReadableError') {
                errorMessage += 'Camera or microphone is already in use by another application.';
            } else {
                errorMessage += error.message;
            }
            
            alert(errorMessage);
        }
    }
    
    async toggleCamera() {
        const btn = document.getElementById('toggleCameraBtn');
        const captureBtn = document.getElementById('captureBtn');
        const autoBtn = document.getElementById('autoAnalyzeBtn');
        const videoPlaceholder = document.getElementById('videoPlaceholder');
        
        if (this.stream) {
            // Stop camera
            console.log('📹 Stopping camera...');
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
            this.videoElement.srcObject = null;
            this.videoElement.style.display = 'none';
            videoPlaceholder.style.display = 'flex';
            btn.innerHTML = '<i class="fas fa-video"></i> Start Camera';
            captureBtn.disabled = true;
            autoBtn.disabled = true;
            this.updateStatus('Camera Off');
            
            // Hide emotion overlay
            document.getElementById('emotionOverlay').style.display = 'none';
        } else {
            // Start camera
            try {
                console.log('📹 Starting camera...');
                this.stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { 
                        width: { ideal: 1280 },
                        height: { ideal: 720 }
                    } 
                });
                
                this.videoElement.srcObject = this.stream;
                this.videoElement.style.display = 'block';
                videoPlaceholder.style.display = 'none';
                btn.innerHTML = '<i class="fas fa-video-slash"></i> Stop Camera';
                captureBtn.disabled = false;
                autoBtn.disabled = false;
                this.updateStatus('Camera Active');
                console.log('✅ Camera started');
            } catch (error) {
                console.error('❌ Camera error:', error);
                this.showAlert('❌ Failed to access camera: ' + error.message, 'danger');
            }
        }
    }
    
    captureAndAnalyze() {
        if (!this.stream) {
            this.showAlert('⚠️ Please start the camera first', 'danger');
            return;
        }
        
        console.log('📸 Capturing frame...');
        
        const canvas = this.canvasElement;
        const context = canvas.getContext('2d');
        
        canvas.width = this.videoElement.videoWidth;
        canvas.height = this.videoElement.videoHeight;
        
        context.drawImage(this.videoElement, 0, 0, canvas.width, canvas.height);
        
        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        this.analyzeFacialExpression(imageData);
    }
    
    async analyzeFacialExpression(imageData) {
        this.showLoading(true);
        
        try {
            console.log('🔍 Analyzing facial expression...');
            
            const response = await fetch(`${this.API_BASE}/analyze/facial`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image: imageData })
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Facial analysis complete:', result.dominant_emotion);
                this.lastFacialData = result;
                this.updateFacialMetrics(result);
                this.displayEmotion(result.emotions, result.dominant_emotion);
                
                // Generate comprehensive report if we have text data
                if (this.lastTextData) {
                    this.generateComprehensiveReport();
                }
            } else {
                console.error('❌ Facial analysis failed:', result.message);
                this.showAlert('⚠️ ' + (result.message || 'Failed to analyze face'), 'danger');
            }
        } catch (error) {
            console.error('❌ Facial analysis error:', error);
            this.showAlert('❌ Error analyzing facial expression', 'danger');
        } finally {
            this.showLoading(false);
        }
    }
    
    updateFacialMetrics(data) {
        // Mental Health Score
        const mentalScore = Math.round(data.mental_health_score);
        document.getElementById('mentalHealthValue').textContent = mentalScore + '%';
        document.getElementById('mentalHealthBar').style.width = mentalScore + '%';
        
        // Stress Level
        const stressPercent = Math.round(data.stress_level * 100);
        document.getElementById('stressValue').textContent = stressPercent + '%';
        document.getElementById('stressBar').style.width = stressPercent + '%';
        
        // Deception Risk
        const deceptionPercent = Math.round(data.deception_risk * 100);
        document.getElementById('deceptionValue').textContent = deceptionPercent + '%';
        document.getElementById('deceptionBar').style.width = deceptionPercent + '%';
    }
    
    displayEmotion(emotions, dominant) {
        const emotionIcons = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'fear': '😨',
            'surprise': '😲',
            'disgust': '🤢',
            'neutral': '😐'
        };
        
        const icon = emotionIcons[dominant] || '😐';
        const percentage = Math.round(emotions[dominant]);
        
        document.getElementById('emotionIcon').textContent = icon;
        document.getElementById('emotionText').textContent = dominant.charAt(0).toUpperCase() + dominant.slice(1);
        document.getElementById('emotionPercent').textContent = percentage + '%';
        document.getElementById('emotionOverlay').style.display = 'block';
    }
    
    toggleAutoAnalysis() {
        const btn = document.getElementById('autoAnalyzeBtn');
        
        if (this.isAnalyzing) {
            clearInterval(this.analysisInterval);
            this.isAnalyzing = false;
            btn.innerHTML = '<i class="fas fa-play"></i> Auto';
            this.updateStatus('Camera Active');
            console.log('⏸️ Auto-analysis stopped');
        } else {
            this.isAnalyzing = true;
            btn.innerHTML = '<i class="fas fa-pause"></i> Stop';
            this.updateStatus('Analyzing...');
            console.log('▶️ Auto-analysis started');
            
            // Analyze every 3 seconds
            this.analysisInterval = setInterval(() => {
                this.captureAndAnalyze();
            }, 3000);
            
            // First analysis immediately
            this.captureAndAnalyze();
        }
    }
    
    async sendMessage() {
        const text = this.chatInput.value.trim();
        if (!text) return;
        
        console.log('💬 Sending message:', text);
        
        // Display user message
        this.addMessage(text, 'user');
        this.chatInput.value = '';
        
        // Analyze text
        await this.analyzeText(text);
    }
    
    async analyzeText(text) {
        this.showLoading(true);
        
        try {
            console.log('🔍 Analyzing text...');
            
            const response = await fetch(`${this.API_BASE}/analyze/text`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text })
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Text analysis complete:', result.sentiment_category);
                this.lastTextData = result;
                
                // Generate bot response
                let botResponse = this.generateBotResponse(result);
                this.addMessage(botResponse, 'bot');
                
                // Check for high fraud risk
                if (result.is_suspicious) {
                    this.showAlert('⚠️ Suspicious activity detected in message!', 'danger');
                }
                
                // Generate comprehensive report if we have facial data
                if (this.lastFacialData) {
                    this.generateComprehensiveReport();
                }
            }
        } catch (error) {
            console.error('❌ Text analysis error:', error);
            this.showAlert('❌ Error analyzing text', 'danger');
        } finally {
            this.showLoading(false);
        }
    }
    
    generateBotResponse(textData) {
        const sentiment = textData.sentiment_category;
        const riskScore = Math.round(textData.fraud_risk_score * 100);
        
        let response = `I've analyzed your message. `;
        
        if (sentiment === 'positive') {
            response += 'Your sentiment appears positive. ';
        } else if (sentiment === 'negative') {
            response += 'I detect some negative sentiment. ';
        } else {
            response += 'Your sentiment appears neutral. ';
        }
        
        if (riskScore > 60) {
            response += `However, I've detected a ${riskScore}% fraud risk score. `;
            if (textData.fraud_keywords_found.length > 0) {
                response += `Keywords of concern: ${textData.fraud_keywords_found.slice(0, 3).join(', ')}. `;
            }
            response += 'Please be cautious with this type of communication.';
        } else if (riskScore > 30) {
            response += `There's a moderate fraud risk score of ${riskScore}%. Please verify any sensitive information.`;
        } else {
            response += `The fraud risk score is low (${riskScore}%). This appears to be normal communication.`;
        }
        
        return response;
    }
    
    async generateComprehensiveReport() {
        try {
            console.log('📊 Generating comprehensive report...');
            
            const response = await fetch(`${this.API_BASE}/analyze/comprehensive`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    facial_data: this.lastFacialData,
                    text_data: this.lastTextData
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Comprehensive report generated:', result.risk_level);
                
                // Update overall fraud risk
                const overallRisk = Math.round(result.overall_risk_score * 100);
                document.getElementById('fraudValue').textContent = overallRisk + '%';
                document.getElementById('fraudBar').style.width = overallRisk + '%';
                
                // Show alert for high risk
                if (result.risk_level === 'HIGH') {
                    this.showAlert('🚨 HIGH FRAUD RISK DETECTED!', 'danger');
                }
            }
        } catch (error) {
            console.error('❌ Comprehensive report error:', error);
        }
    }
    
    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        messageDiv.textContent = text;
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    async startVoiceInput() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showAlert('⚠️ Voice input not supported in this browser', 'danger');
            return;
        }
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.lang = 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.innerHTML = '<i class="fas fa-circle" style="color: red; animation: pulse 1s infinite;"></i>';
        
        console.log('🎤 Listening...');
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('🎤 Transcribed:', transcript);
            this.chatInput.value = transcript;
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        };
        
        recognition.onerror = (event) => {
            console.error('🎤 Voice recognition error:', event.error);
            this.showAlert('❌ Voice recognition error: ' + event.error, 'danger');
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        };
        
        recognition.onend = () => {
            voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        };
        
        recognition.start();
    }
    
    updateStatus(text) {
        document.getElementById('statusText').textContent = text;
    }
    
    showAlert(message, type = 'success') {
        const alert = document.getElementById('alert');
        alert.textContent = message;
        alert.className = 'alert show';
        if (type === 'danger') {
            alert.classList.add('danger');
        }
        
        setTimeout(() => {
            alert.classList.remove('show');
        }, 5000);
    }
    
    showLoading(show) {
        const loading = document.getElementById('loading');
        if (show) {
            loading.classList.add('show');
        } else {
            loading.classList.remove('show');
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.fadApp = new FADApp();
    console.log('🚀 FAD Application loaded');
});
