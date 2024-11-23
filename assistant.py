import os
import numpy as np
import tempfile
from groq import Groq
from google.cloud import texttospeech_v1

class Ai_assistant:
    def __init__(self,system_prompt_file=None):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                # Read system prompt from file if provided, otherwise use default
        if system_prompt_file and os.path.exists(system_prompt_file):
            with open(system_prompt_file, 'r') as f:
                system_prompt = f.read().strip()
        else:
            system_prompt = "Respond like Jarvis from Iron Man—concise, highly intelligent, and formal. Use advanced language, technical precision, and maintain a respectful tone, keeping responses under 50 characters."
        self.full_transcript = [{"role": "system", "content": system_prompt}]
        self.sample_rate = 16000
        self.silence_threshold = 0.05
        self.silence_duration = 1.0
        self.chunk_duration = 0.2
        self.google_tts_client = texttospeech_v1.TextToSpeechClient()
        
    def is_silence(self, audio_chunk):
        max_volume = np.max(np.abs(audio_chunk))
        print(f"max_volume: {max_volume}")
        return max_volume < self.silence_threshold

    def transcribe_audio(self, audio_file):
        with open(audio_file, 'rb') as wav_file:
            transcription_response = self.groq_client.audio.transcriptions.create(
                file=(audio_file, wav_file),
                model="whisper-large-v3",
                language="en"
            )
        return transcription_response.text if hasattr(transcription_response, 'text') else ""

    def generate_ai_response(self, transcript_text):
        self.full_transcript.append({"role": "user", "content": transcript_text})
        chat_completion = self.groq_client.chat.completions.create(
            messages=self.full_transcript, model="llama3-8b-8192"
        )
        ai_response = chat_completion.choices[0].message.content
        self.full_transcript.append({"role": "assistant", "content": ai_response})
        return ai_response
    def generate_speech(self, text):
        synthesis_input = texttospeech_v1.SynthesisInput(text=text)

        voice = texttospeech_v1.VoiceSelectionParams(
            language_code="en-US", 
            name = "en-US-Standard-D",
            ssml_gender=texttospeech_v1.SsmlVoiceGender.MALE
        )

        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3,
            pitch=-3.3,
            speaking_rate = 1.1
        )

        response = self.google_tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            temp_audio.write(response.audio_content)
            temp_audio_path = temp_audio.name
            print(f"Audio file saved at: {temp_audio_path}")

        return temp_audio_path