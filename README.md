# Venus


### How to run it on your own machine

1. Create env
- python install virtualenv
- python -m virtualenv env-vulanami


1. Activate Env
.\env-vulanami\Scripts\activate

2. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

### save packages to the requirements

pip freeze > requirements.txt

### normal commit and push to github



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
