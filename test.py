from utils.audio_processor import process_input
from core.transcriber import transcribe_all_chunks

source = "https://youtu.be/YGgNBcIgI4s"

chunksiii = process_input(source)

print(transcribe_all_chunks(chunksiii))