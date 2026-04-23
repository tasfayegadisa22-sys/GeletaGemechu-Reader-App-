import os
from flask import Flask, request, send_file, render_template
from gtts import gTTS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read_text():
    text = request.form.get('text')
    if not text:
        return "No text", 400
    
    # gTTS በመጠቀም አማርኛውን ወደ ድምጽ መቀየር
    tts = gTTS(text=text, lang='am')
    tts.save("speech.mp3")
    return send_file("speech.mp3", mimetype="audio/mpeg")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
