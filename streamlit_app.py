import streamlit as st
import pyaudio
from retry_requests import retry
# from requests import Session

import time


def install_package(package_name):
    subprocess.run(["pip","install","-U", package_name])

from vulavula import VulavulaClient
from vulavula.common.error_handler import VulavulaError

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


VULAVULA_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImY0YzZlZjBkMGMxOTQ0NjI4M2RhMGI5NWU1NmI3ZjQ2IiwiY2xpZW50X2lkIjo0MywicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.i-oHmnJrpc627G4eH9FQ6FBSjCkBmwqmDksmgRJ06Rw'
# Our headers for authentication
headers={
    "X-CLIENT-TOKEN": VULAVULA_TOKEN,
}

# The transport API to upload your file
TRANSPORT_URL = "https://vulavula-services.lelapa.ai/api/v1/transport/file-upload"


# The transcribe API URL to kick off your transcription job.
TRANSCRIBE_URL = "https://vulavula-services.lelapa.ai/api/v1/transcribe/process/"

client = VulavulaClient(VULAVULA_TOKEN)

## Transcribe isiZulu speech to text
def transcribe_speech(audio_file):
  try:
      upload_id, transcription_result = client.transcribe(audio_file, webhook=WEBHOOK_URL)
      print("Acknowledgement:", transcription_result) #A success message, data is sent to webhook
  except VulavulaError as e:
      print("An error occurred:", e.message)
      if 'details' in e.error_data:
          print("Error Details:", e.error_data['details'])
      else:
          print("No additional error details are available.")
  except Exception as e:
      print("An unexpected error occurred:", str(e))

  while client.get_transcribed_text(upload_id)['message'] == "Item has not been processed.":
      time.sleep(5)
      print("Waiting for transcribe to complete...")
  transcribed = client.get_transcribed_text(upload_id)
  # print(transcribed)
  tr = transcribed.get('text')

  return tr, print(f'transcribed text: {tr}')

# Main Streamlit app
def main():
    st.title('Vula Nami')
    if st.button("Install vulavula"):
        install_package("vula")
        print("success, package installed successfully!")

    if st.button('Record'):
        record_audio('output.wav')  # Change filename as needed

    # Option to download the recorded file
    if os.path.exists('output.wav'):
        st.audio('output.wav', format='audio/wav', start_time=0)

if __name__ == '__main__':
    main()