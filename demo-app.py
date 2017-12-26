#!/usr/bin/env python

'''
My lightweight J.A.R.V.I.S desktop experiment.

Prints a lot of debug info to STDOUT.

See README for requirements to run.


Docs:

https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst
https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py

https://docs.python.org/3/library/webbrowser.html


TTS Google
Google is very limited (max 200 characters per call and 50 calls per day)

TTS Wit.ai
https://wit.ai/getting-started

STT Google
Google is limited to 100 characters per call.

Run info:
1. Install requirements as described in the README.
2. Set the settings.
3. Run the app.

'''

import speech_recognition as sr
import os
import platform
import webbrowser
import sys
import time

from settings import env_vars

''' Default to silence for TTS output. '''
TTS_PROVIDER = 'Silence'


''' Check, that the Speech-to-text provider has been set and is known one. '''
if env_vars['STT_PROVIDER'] is not None:
    STT_PROVIDER = env_vars['STT_PROVIDER']

    if STT_PROVIDER not in ['Google', 'Wit.ai']:
        print(f'Unknown STT provider {STT_PROVIDER}, so terminating.')
        sys.exit()
else:
    print('Could not find STT_PROVIDER in settings, so terminating.')
    sys.exit()

if STT_PROVIDER == 'Wit.ai':
    if env_vars['WITAI_APIKEY'] is not None:
        WITAI_APIKEY = env_vars['WITAI_APIKEY']
    else:
        print('Could not find API KEY for STT provider Wit.ai, so terminating.')
        sys.exit()

''' Check, that the text-to-speach provider has been set and is known one. '''
if env_vars['TTS_PROVIDER'] is not None:
    TTS_PROVIDER = env_vars['TTS_PROVIDER']

    if TTS_PROVIDER not in ['Google', 'Say', 'Silence']:
        print(f'Unknown TTS provider {TTS_PROVIDER}, so terminating.')
        sys.exit()
else:
    print('Could not find TTS_PROVIDER in settings, so terminating.')
    sys.exit()

''' Import the gTTS only, if it's needed. '''
if TTS_PROVIDER == 'Google' or STT_PROVIDER == 'Google':
        from gtts import gTTS


def speak(audio):
    ''' speaks audio passed as argument '''
    print(f'(speak) Speaking: {audio}')

    ''' Say command works on macOS. '''
    if TTS_PROVIDER == 'Say' and platform.system() == 'Darwin':
        os.system(f'say {audio}')
    elif TTS_PROVIDER == 'Google':
        tts = gTTS(text=audio, lang='en')
        tts.save('audio.mp3')
        os.system('afplay audio.mp3')


def listen_and_interpret():
    ''' listens for commands, and sends them to STT. Returns text to process. '''

    r = sr.Recognizer()

    command = None

    with sr.Microphone() as source:
        print('(listen_and_interpret) Ready for next command, listening...')
        ''' The following setting seem to work with my MBP Pro and Blue Yeti microphone.
            Mic gain is quite high, same as input level on System Settings. '''
        # r.dynamic_energy_threshold = True
        r.energy_threshold = 4000
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        print('catched audio')

    try:
        print(f"Sending audio to {STT_PROVIDER} for TTS...")

        if STT_PROVIDER == 'Google':
            command = r.recognize_google(audio, language="en")
        elif STT_PROVIDER == 'Wit.ai':
            command = r.recognize_wit(audio, key=WITAI_APIKEY)

        print(f'(listen_and_interpret) You said: {command}')
    except sr.UnknownValueError:
        print('(listen_and_interpret) Could not understand the command.')
        command_palette(listen_and_interpret())
    except sr.RequestError as e:
        print(f"Could not request TTS results from {STT_PROVIDER}: {e}")
        command_palette(listen_and_interpret())

    return command


def command_palette(command):
    ''' Command palette. The things, J.A.R.V.I.S. Lite knows how to do. Not too much :) '''
    if command is None:
        return

    if 'hello there' in command:
        print(f'(command_palette) Hello command: {command}')
        speak('Hello there!')
    elif 'send message to' in command:
        print(f'(command_palette) Send message command: {command}')
        speak('Sending message to someone.')
    elif 'send email to' in command:
        print(f'(command_palette) Send email command: {command}')
        speak('Sending email to someone.')
    elif 'open my blog' in command:
        url = 'https://janikarhunen.fi'
        # webbrowser.get('safari').open(url)
        # 'google-chrome' is not working
        # 'macosx' returns the default browser
        webbrowser.get('macosx').open(url)
        speak('Your blog is now open in the browser.')
    elif 'exit' in command:
        print(f'Bye bye... {command}')
        speak('Shutting down now. Bye bye.')
        sys.exit()
    else:
        print(f'(command_palette) Command not recognized: {command}')


if __name__ == '__main__':
    speak('Ready for commands.')
    ''' Loop and wait for commands forever. '''
    while True:
        command_palette(listen_and_interpret())
        print('Sleeping 2 secs...')
        time.sleep(2)
