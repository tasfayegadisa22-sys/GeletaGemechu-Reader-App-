import os
from flask import Flask, request, send_file, render_template, make_response
from gtts import gTTS
import PyPDF2
import docx
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read_text():
    text = request.form.get('text', '')
    file = request.files.get('file')
    page_count = 0

    if file:
        filename = file.filename.lower()
        try:
            if filename.endswith('.txt'):
                text = file.read().decode('utf-8')
            elif filename.endswith('.pdf'):
                reader = PyPDF2.PdfReader(file)
                page_count = len(reader.pages)
                text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
            elif filename.endswith('.docx'):
                doc = docx.Document(file)
                text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"ፋይሉን ማንበብ አልተቻለም: {str(e)}", 500
    
    if not text.strip():
        return "ምንም ጽሁፍ አልተገኘም", 400

    word_count = len(text.split())
    audio_minutes = max(1, round(word_count / 130))
    
    try:
        # ጽሁፉ በጣም ረጅም ከሆነ በትንሽ በትንሹ ከፋፍሎ እንዲያነብ (slow=False መሆኑን እናረጋግጣለን)
        tts = gTTS(text=text, lang='am', slow=False)
        tts.save("speech.mp3")
        
        response = make_response(send_file("speech.mp3", mimetype="audio/mpeg"))
        response.headers['X-Word-Count'] = str(word_count)
        response.headers['X-Audio-Minutes'] = str(audio_minutes)
        response.headers['X-Page-Count'] = str(page_count)
        return response
    except Exception as e:
        if "429" in str(e):
            return "ጉግል በአጭር ጊዜ ውስጥ ብዙ ጥያቄ ስለቀረበለት አግዶናል። እባክዎ 10 ደቂቃ ቆይተው ይሞክሩ።", 429
        return f"የድምጽ ስህተት: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
