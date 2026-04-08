                    from flask import Flask, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route                            ('/')
def home():
    return "<h1>የድምጽ ማቀነባበሪያ ሞተር</h1><p>ጊትሃብ ላይ በትክክል እየሰራ ነው!</p>"

@app.route('/read', methods=['POST'])
def read_text():
    text = request.form.get('text')
    if not text:
        return "እባክህ ጽሁፍ አስገባ", 400
    
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")
return send_file("speech.mp3")  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
