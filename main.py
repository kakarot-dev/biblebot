from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch
import json
import os
import time

synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7308]["xvector"]).unsqueeze(0)


def generate_audio(text: str, filename: str):
    speech = synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding})

    sf.write(filename, speech["audio"], samplerate=speech["sampling_rate"])

# Define the path to the 'bible' directory
bible_dir = 'bible'

val = True
# Iterate over the books in the 'bible' directory
for book in os.listdir(bible_dir):
    # Generate the path to the book directory
    book_dir = os.path.join(bible_dir, book)

    # Iterate over the chapters in the book directory
    for chapter in os.listdir(book_dir):
        # Generate the path to the chapter directory
        chapter_dir = os.path.join(book_dir, chapter)

        # Iterate over the verses in the chapter directory
        for verse_file in os.listdir(chapter_dir):
            # Check if the file is a text file
            if not verse_file.endswith('.txt'):
                continue
            # Generate the path to the verse text file
            verse_file_path = os.path.join(chapter_dir, verse_file)
            print("Generating audio for:", verse_file_path)

            # Check if the wav file already exists
            if os.path.exists(verse_file_path.replace('.txt', '.wav')):
                continue
            # Read the verse text from the text file
            with open(verse_file_path, 'r') as f:
                verse_text = f.read()
            audio_filename = f"{verse_file_path.replace('.txt', '.wav')}"
            
            generate_audio(verse_text, audio_filename)
            time.sleep(5)