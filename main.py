import os
from flask import Flask, request, send_file, render_template
from gtts import gTTS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read_text():
    text = request.form.get('text', '')
    file = request.files.get('file')

    # ፋይል ከገባ ፋይሉን ማንበብ
    if file and file.filename.endswith('.txt'):
        text = file.read().decode('utf-8')
    
    # ባዶ ከሆነ መልስ መስጠት
    if not text.strip():
        return "ምንም ጽሁፍ አልተገኘም", 400
    
    try:
        # ጽሁፉን ወደ ድምጽ መቀየር
        tts = gTTS(text=text, lang='am')
        tts.save("speech.mp3")
        return send_file("speech.mp3", mimetype="audio/mpeg")
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
