J.A.R.V.I.S. Lite
=================

My lightweight J.A.R.V.I.S desktop experiment.

Built mainly for learning purposes, how to implement lightweight *speech-to-text* and *text-to-speech* to a Python app. Could be more in the future.

Requires Python 3.6, tested on *macOS Sierra* and *Raspberry Pi 3*.

## The code

A simple demo app to test the tech is in `demo-app.py`.

## Install prerequisites

To capture the speech and change that to text, we are going to need a couple of things. We are going to work with **Python 3.6** and within **a virtualenv**, so create one.

Because the installation process is a bit tricky, this time we are going to install the Python requirements one by one, instead of `pip install -r requirements.txt`.

### PyAudio

Install PyAudio (and the required portaudio). [Read more](http://people.csail.mit.edu/hubert/pyaudio/).

#### macOS

Given, that we have *Homebrew installed*, run `brew install portaudio`.

Run `pip install pyaudio`.

#### Raspberry Pi 3

See the Debian/Ubuntu section on [the PyAudio installation guide](http://people.csail.mit.edu/hubert/pyaudio/).

### Google API Client Library for Python

This is needed, if Google is used in STT and/or TTS. Install **Google API Client Library for Python**, [read more](https://developers.google.com/api-client-library/python/).

Run `pip install google-api-python-client` and follow the instructions on the previous link how to authenticate.

### SpeechRecognition

For STT (speech-to-text) we are using [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/). [Read more](https://github.com/Uberi/speech_recognition), [and](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst).

Run `pip install SpeechRecognition`.

### Setup Wit.ai for STT

If [Wit.ai](https://wit.ai/) is used for STT, we need to *create an app* to Wit.ai. Create one *entity* within the app, does not matter what it is.

Get the API KEY (Server Access Token) in the app settings.

### Text to Speech

Install [gTTS](https://github.com/pndurette/gTTS), or we can use the *say* command on macOS, or e.g. *espeak* on Linux.

Run `pip install gTTS`.

## Settings

Copy the sample settings file `dot.env.sample` to `.env` and enter the correct values.

If we are using Wit.ai for STT, get the API KEY as described above.

## Run the app

Run with `python demo-app.py`, and try the commands out.

## Next steps

It might be a good idea to teach a couple of new commands suitable to *your use case*.

## TODO

*Couple of ideas to make things better.*

Add AWS Polly as text-to-speech. Better voices and longer texts. Google is limited to 100 characters per call.

Store (TTS) texts in DB and audio outputs to disk to enable caching (no need to call TTS service for known texts).

## License

MIT. See LICENSE for more.
