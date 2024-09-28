import io
import os
import speech_recognition as sr
from datetime import datetime
from pydub import AudioSegment


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
            audio_segment = AudioSegment.from_file(file_path)  # Load the audio file

            wav_io = io.BytesIO()
            audio_segment.export(wav_io, format="wav")  # Export as WAV
            wav_io.seek(0)  # Reset buffer position

            print("Recognizing audio")
            with sr.AudioFile(wav_io) as audio_source:
                audio_data = self.recognizer.record(audio_source)
                text = self.recognizer.recognize_google(audio_data)
                print("Audio to text: ", text)
                return text
        except Exception as e:
            print(f"Error processing audio: {str(e)}")  # Log error for debugging
            return f"Error processing audio: {str(e)}"
