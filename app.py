import numpy as np
import os
import tempfile
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from assistant import Ai_assistant 

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

app = Flask(__name__)
CORS(app)

assistant = Ai_assistant(system_prompt_file=r"PATH: GIVE A TEXT FILE OF PROMPTS")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        audio_file.save(temp_wav.name)
        transcription = assistant.transcribe_audio(temp_wav.name)
    os.remove(temp_wav.name)
    return jsonify({"transcription": transcription})

@app.route('/check-silence', methods=['POST'])
def check_silence():
    audio_chunk = request.json.get('audio_chunk')
    if audio_chunk is None:
        return jsonify({"error": "No audio chunk provided"}), 400
    
    audio_data = np.array(audio_chunk, dtype=np.float32)
    is_silent = assistant.is_silence(audio_data)
    return jsonify({"is_silent": "true" if is_silent else "false"})

@app.route('/generate-response', methods=['POST'])
def generate_response():
    transcript_text = request.json.get('transcription')
    if transcript_text.strip().lower() == "thank you.":
        return jsonify({"response": "", "audio_file": ""})
    ai_response = assistant.generate_ai_response(transcript_text)
    audio_file = assistant.generate_speech(ai_response)
    return jsonify({"response": ai_response, "audio_file": f"/audio/{os.path.basename(audio_file)}"})

@app.route('/audio/<filename>')
def serve_audio(filename):
    temp_dir = tempfile.gettempdir()
    return send_from_directory(temp_dir, filename)
if __name__ == '__main__':
    app.run(debug=True)