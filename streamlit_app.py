import streamlit as st

#create an audio button and be able to record 
import pyaudio
import wave 
import os

#use the lelapa API to transcribe. Implement a retry to try again the model when is sleeping 
from retry_requests import retry
from requests import Sessioz
import IPython

#create an audio button and be able to record 
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5  # Adjust recording duration as needed

# Function to record audio
def record_audio(filename):
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    st.write(f"Recording for {RECORD_SECONDS} seconds...")

    # Record for the specified number of seconds
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio to a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    st.write(f"Finished recording to {filename}")

# Main Streamlit app
def main():
    st.title('Vula Nami')

    if st.button('Record'):
        record_audio('output.wav')  # Change filename as needed

    # Option to download the recorded file
    if os.path.exists('output.wav'):
        st.audio('output.wav', format='audio/wav', start_time=0)

if __name__ == '__main__':
    main()




#use the lelapa API to transcribe
#get your vulavula token 
VULAVULA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImZlZDFiM2ExMjFkZjQ5MGM5MmRkOTdkN2U0Yjg0NjgxIiwiY2xpZW50X2lkIjo0MywicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.lQDbGTfd1sUzK_LoawGri1Jx4XRt6SXHx1brsmhGp9s"

# Our headers for authentication
headers={
    "X-CLIENT-TOKEN": VULAVULA_TOKEN,
}

# The transport API to upload your file
TRANSPORT_URL = "https://vulavula-services.lelapa.ai/api/v1/transport/file-upload"

# The transcribe API URL to kick off your transcription job.
TRANSCRIBE_URL = "https://vulavula-services.lelapa.ai/api/v1/transcribe/process/"

# When transcription is complete, our system calls a webhook that you provide.
# Here, we’re using a demo webhook from webhook.site for testing.
WEBHOOK_URL="https://webhook.site/3594b17d-a879-41b8-bb28-e59d08e16be6"

# Name of the file you are transcribing
FILE_TO_TRANSCRIBE = "output.wav"

IPython.display.Audio(FILE_TO_TRANSCRIBE)

# Get file size
file_size = os.path.getsize(FILE_TO_TRANSCRIBE)

# Open file in binary mode
with open(FILE_TO_TRANSCRIBE, 'rb') as file:
    # Read file
    file_content = file.read()

# Encode file content
encoded_content = base64.b64encode(file_content)

# Decode bytes to string
encoded_string = encoded_content.decode()

transport_request_body = {
    "file_name": FILE_TO_TRANSCRIBE,
    "audio_blob": encoded_string,
    "file_size": file_size,
}

resp = requests.post(
    TRANSPORT_URL,
    json=transport_request_body,
    headers=headers,
)




