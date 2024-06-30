import streamlit as st
import pyaudio
import wave
import os
import requests
import time

from retry_requests import retry
from requests import Session

from vulavula import VulavulaClient
from vulavula.common.error_handler import VulavulaError
from vulavula import VulavulaClient
from vulavula.common.error_handler import VulavulaError



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
    ######################################################################################
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjcwNjAyM2NkNmQyMzQzOGRiOWU4ZWQwMjYyMGFjOTM5IiwiY2xpZW50X2lkIjozMSwicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.T9tbypdARqIXLRI6a2kRrNpfwnmg-lc0D-Hj0rh0q5g'
VULAVULA_TOKEN = api_key
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
# WEBHOOK_URL="https://webhook.site/793085d1-aedb-4aba-9151-a931a7efba54"
WEBHOOK_URL="https://webhook.site/637a5a5f-c8a1-4869-87d5-85431d23fdc9"

client = VulavulaClient(VULAVULA_TOKEN)
# audio_file = 'C:\Users\bmmah\OneDrive\Documents\vulavula\VulaNami\output.wav'
audio_file ='output.wav'

  ## Translate IsiZulu Text to English
def translate_zul_text(zul_txt):
  translation_data = {
    # "input_text": "Iyiphi ingxenye yomzimba oyisebenzisa uma uhamba?",
    "input_text": f"{zul_txt}",
    "source_lang": "zul_Latn",
    "target_lang": "eng_Latn"
  }

  translation_result = client.translate(translation_data)
  print("Translation Result:", translation_result)
  trns = translation_result.get('translation')
  trns = trns[0].get('translation_text')
  cleaned_translation_text = trns.strip("()").split(",")[0].strip("' ")
  print(f'#### Translation done')
  return cleaned_translation_text


###############################################################

# VULAVULA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM2ZGQ4NTgyNDRkNDQ4NmI5MzM3MTBiOGU0OGMwMTIyIiwiY2xpZW50X2lkIjo3MCwicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.JKe-hoIrlDX5FH4b2eJPdLyi_OLVhDXLqXVYAUmz0Ro"
# client = VulavulaClient(VULAVULA_TOKEN)

# WEBHOOK_URL="https://webhook.site/e1a0628c-614e-4f0b-af4e-51f1d353e3d6"
# # Name of the file you are transcribing
# FILE_TO_TRANSCRIBE = "output.wav"

# try:
#     upload_id, transcription_result = client.transcribe(FILE_TO_TRANSCRIBE, webhook=WEBHOOK_URL)
#     print("Acknowledgement:", transcription_result) #A success message, data is sent to webhook
# except VulavulaError as e:
#     print("An error occurred:", e.message)
#     if 'details' in e.error_data:
#         print("Error Details:", e.error_data['details'])
#     else:
#         print("No additional error details are available.")
# except Exception as e:
#     print("An unexpected error occurred:", str(e))

# while client.get_transcribed_text(upload_id)['message'] == "Item has not been processed.":
#     time.sleep(5)
#     print("Waiting for transcribe to complete...")
# client.get_transcribed_text(upload_id)

    # Vulavula API endpoint and API key (replace with your actual endpoint and API key)
#   API_ENDPOINT = 'https://vulavula-services.lelapa.ai/#/transcribe'
#   API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNmNTRkMWE3YzFiYzQzN2I5YzQzNTZiN2NjNDc4OTBjIiwiY2xpZW50X2lkIjo2NywicmVxdWVzdHNfcGVyX21pbnV0ZSI6MCwibGFzdF9yZXF1ZXN0X3RpbWUiOm51bGx9.n-mGUs7LyPtqUkg2Lv8pteGeCxfkdV7EQ9pGlzmi4EE'  # Replace with your actual API key

# Function to transcribe audio using Vulavula API
# def transcribe_audio(audio_file):
#     files = {'file': output.wav}
#     headers = {'Authorization': f'Bearer {API_KEY}'}

#     # try:
#         response = requests.post(API_ENDPOINT, files=files, headers=headers)
#         if response.status_code == 200:
#             return response.json()['transcript']
#         else:
#             st.error(f"Error: {response.status_code} - {response.json()['error']}")
#     except requests.exceptions.RequestException as e:
#         st.error(f"Request error: {e}")

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

#   while client.get_transcribed_text(upload_id)['message'] == "Item has not been processed.":
#       time.sleep(5)
#       print("Waiting for transcribe to complete...")
#   transcribed = client.get_transcribed_text(upload_id)
#   # print(transcribed)
#   tr = transcribed.get('text')
    # print(f'transcribed text: {tr}')
  return "" 

# Main Streamlit app
def main():
    st.title('Vula Nami')

    if st.button('Record'):
        record_audio('output.wav')  # Change filename as needed

    # Option to download the recorded file
    if os.path.exists('output.wav'):
        st.audio('output.wav', format='audio/wav', start_time=0)

    ######################Transcribing


    uploaded_file = st.file_uploader("Upload an audio file (WAV)")
    # print(uploaded_file)
    audio_file_path = "output.wav"
    if uploaded_file is not None:
        print("rdtfyguhijop", )
        if st.button('Transcribe'):
            transcript = transcribe_speech(uploaded_file.name)
            print(transcript)
            # if transcript:
            #     st.write('Transcription:')
            #     st.write(transcript)
 

if __name__ == '__main__':
    main()