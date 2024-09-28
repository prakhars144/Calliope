from flask import Flask, request, send_from_directory
from visual_novel_assistant import VisualNovelAssistant
from audio_processor import AudioProcessor

UPLOAD_FOLDER = "../recorded_wav_files"
WEB_STATIC_FILES = "../static"


class WebServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.audio_processor = AudioProcessor(upload_folder=UPLOAD_FOLDER)
        self.visual_novel_assistant = VisualNovelAssistant()

        # Set static folder for serving HTML files
        self.app.static_folder = WEB_STATIC_FILES

        # Define routes
        self.app.add_url_rule("/", "index", self.index)
        self.app.add_url_rule(
            "/upload", "upload_audio", self.upload_audio, methods=["POST"]
        )

    def index(self):
        """Serve the index HTML page."""
        return send_from_directory(self.app.static_folder, "index.html")

    def upload_audio(self):
        """Handle the uploaded audio file and return its transcription."""
        if "audio" not in request.files:
            return "No audio part", 400

        # Get the audio file from the request
        audio_file = request.files["audio"]

        # Save the audio file and convert it to text
        file_path = self.audio_processor.save_audio(audio_file)
        text_output = self.audio_processor.convert_audio_to_text(file_path)

        # Now use this text as a query to the visual novel assistant
        difficulty = "medium"  # You can modify this based on user input or other logic
        llm_output = None
        if text_output.lower() in ["start over", "reset", "new game"]:
            self.visual_novel_assistant.clear_memory()
            print("Memory cleared. Starting a new game.")
        else:
            # Process normal input
            llm_output = self.visual_novel_assistant.get_structured_response(
                difficulty, text_output
            )

        if llm_output is None:
            # Handle the case where no output was generated
            print("No output generated. Please provide valid input.")
            return {}, 400

        json_llm_output = llm_output.model_dump()

        return {"transcription": text_output, "llm_output": json_llm_output}, 200
