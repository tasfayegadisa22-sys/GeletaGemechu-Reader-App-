import os
from flask import Flask, request, send_file, render_template
from gtts import gTTS
import PyPDF2
import docx

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/read', methods=['POST'])
def read_text():
    text = request.form.get('text', '')
    file = request.files.get('file')

    # ፋይል ከገባ አይነቱን ለይቶ ማንበብ
    if file:
        filename = file.filename.lower()
        try:
            if filename.endswith('.txt'):
                text = file.read().decode('utf-8')
                
            elif filename.endswith('.pdf'):
                reader = PyPDF2.PdfReader(file)
                extracted_text = []
                for page in reader.pages:
                    extracted_text.append(page.extract_text())
                text = " ".join(extracted_text)
                
            elif filename.endswith('.docx'):
                doc = docx.Document(file)
                text = "\n".join([para.text for para in doc.paragraphs])
                
            else:
                return "ይህ የፋይል አይነት አይደገፍም።", 400
                
        except Exception as e:
            return f"ፋይሉን ማንበብ አልተቻለም: {str(e)}", 500
    
    if not text.strip():
        return "ምንም ጽሁፍ አልተገኘም", 400
    
    try:
        # የተገኘውን ጽሁፍ ወደ ድምጽ መቀየር
        tts = gTTS(text=text, lang='am')
        tts.save("speech.mp3")
        return send_file("speech.mp3", mimetype="audio/mpeg")
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
