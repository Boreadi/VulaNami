import streamlit as st
import pyaudio
import wave
import os
import requests



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10  # Adjust recording duration as needed

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