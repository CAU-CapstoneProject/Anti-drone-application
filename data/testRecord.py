import pyaudio
import sys
import time
import wave
import RPi.GPIO as GPIO

# Get time
now = time.gmtime(time.time())

# Global parameter
CHUNK = 1023
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = int(sys.argv[1])
WAVE_OUTPUT_FILENAME = "Desktop/data/" + str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) + ".wav"
PIN = 4

# Open recorder
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
# Print for debugging
print("Start to record the audio.")
GPIO.output(PIN, False)

frames = []

# Start recording
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

# Print for dubgging
print("Recording is finished.")
GPIO.output(PIN, True)

# Stop recording
stream.stop_stream()
stream.close()
p.terminate()

# Write as file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
