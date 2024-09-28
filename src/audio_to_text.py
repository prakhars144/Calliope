from flask import Flask, request, jsonify, send_from_directory
import io
import os
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment
from visual_novel_assistant import VisualNovelAssistant

UPLOAD_FOLDER = '../recorded_wav_files'
WEB_STATIC_FILES = '../static'

class AudioProcessor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(self.upload_folder, exist_ok=True)  # Ensure upload folder exists
        self.recognizer = sr.Recognizer()

    def save_audio(self, audio_file):
        """Save the uploaded audio file with a timestamped filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_filename = f"{timestamp}.wav"
        file_path = os.path.join(self.upload_folder, wav_filename)
        audio_file.save(file_path)
        return file_path

    def convert_audio_to_text(self, file_path):
        """Convert audio file to text using Google Speech Recognition."""
        try:
            print("Loading audio segment")
            audio_segment = AudioSegment.from_file(file_path)  # Load the audio file
            
            wav_io = io.BytesIO()
            print("Exporting as wav")
            audio_segment.export(wav_io, format="wav")  # Export as WAV
            wav_io.seek(0)  # Reset buffer position
            
            print("Recognizing audio")
            with sr.AudioFile(wav_io) as audio_source:
                print("Recording Audio")
                audio_data = self.recognizer.record(audio_source)
                print("Trying to get text")
                text = self.recognizer.recognize_google(audio_data)
                print("Text: ", text)
                return text
        except Exception as e:
            print(f"Error processing audio: {str(e)}")  # Log error for debugging
            return f"Error processing audio: {str(e)}"

class AudioApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.audio_processor = AudioProcessor(upload_folder=UPLOAD_FOLDER)
        self.visual_novel_assistant = VisualNovelAssistant()
        
        # Set static folder for serving HTML files
        self.app.static_folder = WEB_STATIC_FILES
        
        # Define routes
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/upload', 'upload_audio', self.upload_audio, methods=['POST'])

    def index(self):
        """Serve the index HTML page."""
        return send_from_directory(self.app.static_folder, 'index.html')

    def upload_audio(self):
        """Handle the uploaded audio file and return its transcription."""
        if 'audio' not in request.files:
            return "No audio part", 400

        # Get the audio file from the request
        audio_file = request.files['audio']
        
        # Save the audio file and convert it to text
        file_path = self.audio_processor.save_audio(audio_file)
        text_output = self.audio_processor.convert_audio_to_text(file_path)

        # Now use this text as a query to the visual novel assistant
        world_desc = "The world is composed of a normal human society where all people live in peace."
        difficulty = "medium"  # You can modify this based on user input or other logic
        
        llm_output = self.visual_novel_assistant.get_structured_response(world_desc, difficulty, text_output)
        json_llm_output = llm_output.model_dump()

        return {"transcription": text_output, "llm_output": json_llm_output}, 200

if __name__ == '__main__':
    app_instance = AudioApp()
    app_instance.app.run(host='0.0.0.0', debug=True)